"""Token storage layer with refresh-token rotation and reuse detection.

This module is intentionally framework-free: it knows how to store, look up,
rotate and revoke OAuth2 token sets, but it does not issue tokens itself.
Token issuance lives in :mod:`src.auth.oauth`.
"""

from __future__ import annotations

import time
from collections.abc import Callable

DEFAULT_ACCESS_TOKEN_TTL = 3600
DEFAULT_REFRESH_TOKEN_TTL = 60 * 60 * 24 * 30

Clock = Callable[[], int]


class TokenError(Exception):
    """Base class for token storage errors."""


class InvalidTokenError(TokenError):
    """Raised when a token (access or refresh) is unknown or already removed."""


class InvalidAccessTokenError(InvalidTokenError):
    """Raised when an access token is unknown or already removed."""


class InvalidRefreshTokenError(InvalidTokenError):
    """Raised when a refresh token is unknown or already removed."""


class RefreshTokenReuseError(TokenError):
    """Raised when a previously rotated/revoked refresh token is reused.

    Refresh-token rotation is only effective if reuse of a retired token is
    detectable: presenting a rotated-out refresh token signals theft and the
    active token family should be revoked. This error lets callers escalate.
    """


class ExpiredTokenError(TokenError):
    """Raised when a stored access token has passed its expiry."""


class TokenSet:
    """An issued OAuth2 token bundle: an access token plus its refresh token.

    ``expires_at`` is derived from ``issued_at + expires_in`` by default. When
    an explicit ``expires_at`` is supplied (e.g. extended lifetime, clock-skew
    correction) it is authoritative and survives a ``to_dict``/``from_dict``
    round-trip; ``expires_in`` is preserved unchanged as the value advertised
    to the OAuth client at issuance.
    """

    def __init__(
        self,
        access_token: str,
        refresh_token: str,
        expires_in: int = DEFAULT_ACCESS_TOKEN_TTL,
        token_type: str = "Bearer",
        scope: str = "",
        issued_at: int | None = None,
        client_id: str | None = None,
        expires_at: int | None = None,
    ) -> None:
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in
        self.token_type = token_type
        self.scope = scope
        self.issued_at = issued_at if issued_at is not None else int(time.time())
        self.client_id = client_id
        self.expires_at = (
            expires_at if expires_at is not None else self.issued_at + self.expires_in
        )

    def is_expired(self, now: int | None = None) -> bool:
        check_at = now if now is not None else int(time.time())
        return check_at >= self.expires_at

    def to_dict(self) -> dict:
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_in": self.expires_in,
            "token_type": self.token_type,
            "scope": self.scope,
            "issued_at": self.issued_at,
            "client_id": self.client_id,
            "expires_at": self.expires_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> TokenSet:
        return cls(
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
            expires_in=data["expires_in"],
            token_type=data.get("token_type", "Bearer"),
            scope=data.get("scope", ""),
            issued_at=data.get("issued_at"),
            client_id=data.get("client_id"),
            expires_at=data.get("expires_at"),
        )


class TokenStore:
    """In-memory token storage with refresh-token rotation.

    Tokens are indexed both by access token (for request validation) and by
    refresh token (for rotation). Retired refresh tokens are remembered in a
    revoked set so that reuse can be detected and reported.
    """

    def __init__(self, clock: Clock | None = None) -> None:
        self._by_access: dict[str, TokenSet] = {}
        self._by_refresh: dict[str, TokenSet] = {}
        self._revoked_refresh: set[str] = set()
        self._clock: Clock = clock or (lambda: int(time.time()))

    def store(self, token_set: TokenSet) -> None:
        self._by_access[token_set.access_token] = token_set
        self._by_refresh[token_set.refresh_token] = token_set

    def get_by_access_token(self, access_token: str) -> TokenSet:
        token_set = self._by_access.get(access_token)
        if token_set is None:
            raise InvalidAccessTokenError(access_token)
        if token_set.is_expired(now=self._clock()):
            raise ExpiredTokenError(access_token)
        return token_set

    def get_by_refresh_token(self, refresh_token: str) -> TokenSet:
        token_set = self._by_refresh.get(refresh_token)
        if token_set is None:
            raise InvalidRefreshTokenError(refresh_token)
        return token_set

    def is_valid_access_token(self, access_token: str) -> bool:
        token_set = self._by_access.get(access_token)
        if token_set is None:
            return False
        return not token_set.is_expired(now=self._clock())

    def rotate(self, refresh_token: str, new_token_set: TokenSet) -> TokenSet:
        """Retire ``refresh_token`` and store ``new_token_set`` in its place.

        Raises :class:`RefreshTokenReuseError` if the refresh token has already
        been rotated or revoked — a strong indicator of token theft.
        """
        if refresh_token in self._revoked_refresh:
            raise RefreshTokenReuseError(refresh_token)

        existing = self._by_refresh.pop(refresh_token, None)
        if existing is None:
            raise InvalidRefreshTokenError(refresh_token)

        self._by_access.pop(existing.access_token, None)
        self._revoked_refresh.add(refresh_token)
        self.store(new_token_set)
        return new_token_set

    def revoke(self, refresh_token: str) -> None:
        token_set = self._by_refresh.pop(refresh_token, None)
        if token_set is not None:
            self._by_access.pop(token_set.access_token, None)
        self._revoked_refresh.add(refresh_token)

    def is_revoked(self, refresh_token: str) -> bool:
        return refresh_token in self._revoked_refresh
