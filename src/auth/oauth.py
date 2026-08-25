"""OAuth2 Authorization Code flow with PKCE (RFC 7636).

This module provides:

* PKCE helpers (:func:`generate_code_verifier`, :func:`create_code_challenge`)
* an in-process :class:`AuthorizationServer` that validates PKCE challenges,
  issues token sets, and rotates refresh tokens via :class:`TokenStore`
* an :class:`OAuthClient` that drives the client side of the flow

The authorization server is intentionally in-process so the full PKCE grant
can be exercised end-to-end in tests without a network dependency. Token
persistence and rotation are delegated to :mod:`src.auth.tokens`.
"""

from __future__ import annotations

import base64
import hashlib
import secrets
import urllib.parse
from dataclasses import dataclass
from typing import Optional

from .tokens import (
    InvalidRefreshTokenError,
    RefreshTokenReuseError,
    TokenSet,
    TokenStore,
)

CODE_CHALLENGE_METHOD_S256 = "S256"
CODE_CHALLENGE_METHOD_PLAIN = "plain"

DEFAULT_VERIFIER_LENGTH = 64
DEFAULT_TOKEN_LENGTH = 32
DEFAULT_REFRESH_TOKEN_LENGTH = 48


class AuthorizationError(Exception):
    """Base class for authorization-server errors."""


class InvalidClientError(AuthorizationError):
    """Raised when a client_id is unknown to the authorization server."""


class InvalidRedirectUriError(AuthorizationError):
    """Raised when a redirect_uri is not registered for the client."""


class InvalidGrantError(AuthorizationError):
    """Raised when an authorization code or refresh token is invalid."""


class PKCEVerificationError(InvalidGrantError):
    """Raised when the code_verifier does not match the stored code_challenge."""


def generate_code_verifier(length: int = DEFAULT_VERIFIER_LENGTH) -> str:
    """Return a cryptographically random, URL-safe code verifier.

    Per RFC 7636 the verifier uses the unreserved character set
    ``[A-Z][a-z][0-9]-._~`` and is 43-128 characters long.
    """
    if length < 43 or length > 128:
        raise ValueError("code_verifier length must be between 43 and 128")
    return secrets.token_urlsafe(length)[:length]


def create_code_challenge(verifier: str, method: str = CODE_CHALLENGE_METHOD_S256) -> str:
    """Derive the code challenge from ``verifier`` using ``method``."""
    if method == CODE_CHALLENGE_METHOD_PLAIN:
        return verifier
    if method == CODE_CHALLENGE_METHOD_S256:
        digest = hashlib.sha256(verifier.encode("ascii")).digest()
        return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    raise ValueError(f"unsupported code challenge method: {method!r}")


def generate_token(length: int = DEFAULT_TOKEN_LENGTH) -> str:
    return secrets.token_urlsafe(length)[:length]


@dataclass
class _PendingAuthorization:
    client_id: str
    redirect_uri: str
    code_challenge: str
    code_challenge_method: str
    scope: str
    user_id: str


@dataclass
class PKCERequest:
    """The client-side artifacts needed to complete a PKCE flow."""

    code_verifier: str
    code_challenge: str
    code_challenge_method: str
    state: str
    authorization_url: str


@dataclass
class _ClientRegistration:
    client_id: str
    redirect_uris: set[str]
    client_secret: Optional[str] = None


class AuthorizationServer:
    """An in-process OAuth2 authorization server supporting PKCE."""

    def __init__(self, token_store: Optional[TokenStore] = None) -> None:
        self.token_store = token_store or TokenStore()
        self._clients: dict[str, _ClientRegistration] = {}
        self._codes: dict[str, _PendingAuthorization] = {}

    def register_client(
        self,
        client_id: str,
        redirect_uris,
        client_secret: Optional[str] = None,
    ) -> None:
        self._clients[client_id] = _ClientRegistration(
            client_id=client_id,
            redirect_uris=set(redirect_uris),
            client_secret=client_secret,
        )

    def _get_client(self, client_id: str) -> _ClientRegistration:
        client = self._clients.get(client_id)
        if client is None:
            raise InvalidClientError(client_id)
        return client

    def create_authorization_code(
        self,
        client_id: str,
        redirect_uri: str,
        code_challenge: str,
        code_challenge_method: str,
        scope: str = "",
        user_id: str = "user",
    ) -> str:
        client = self._get_client(client_id)
        if redirect_uri not in client.redirect_uris:
            raise InvalidRedirectUriError(redirect_uri)

        code = generate_token(DEFAULT_TOKEN_LENGTH)
        self._codes[code] = _PendingAuthorization(
            client_id=client_id,
            redirect_uri=redirect_uri,
            code_challenge=code_challenge,
            code_challenge_method=code_challenge_method,
            scope=scope,
            user_id=user_id,
        )
        return code

    def exchange_code(
        self,
        code: str,
        redirect_uri: str,
        code_verifier: str,
        client_id: str,
    ) -> TokenSet:
        pending = self._codes.pop(code, None)
        if pending is None:
            raise InvalidGrantError("invalid authorization code")
        if pending.client_id != client_id:
            raise InvalidGrantError("client_id mismatch")
        if pending.redirect_uri != redirect_uri:
            raise InvalidGrantError("redirect_uri mismatch")

        expected_challenge = create_code_challenge(
            code_verifier, pending.code_challenge_method
        )
        if not secrets.compare_digest(expected_challenge, pending.code_challenge):
            raise PKCEVerificationError("code_verifier does not match code_challenge")

        token_set = TokenSet(
            access_token=generate_token(DEFAULT_TOKEN_LENGTH),
            refresh_token=generate_token(DEFAULT_REFRESH_TOKEN_LENGTH),
            scope=pending.scope,
        )
        self.token_store.store(token_set)
        return token_set

    def refresh(
        self,
        refresh_token: str,
        client_id: Optional[str] = None,
        scope: Optional[str] = None,
    ) -> TokenSet:
        try:
            existing = self.token_store.get_by_refresh_token(refresh_token)
        except InvalidRefreshTokenError as exc:
            raise InvalidGrantError("invalid refresh token") from exc

        new_scope = scope if scope is not None else existing.scope
        new_token_set = TokenSet(
            access_token=generate_token(DEFAULT_TOKEN_LENGTH),
            refresh_token=generate_token(DEFAULT_REFRESH_TOKEN_LENGTH),
            scope=new_scope,
        )
        try:
            self.token_store.rotate(refresh_token, new_token_set)
        except RefreshTokenReuseError as exc:
            raise InvalidGrantError("refresh token reuse detected") from exc
        return new_token_set

    def revoke(self, refresh_token: str) -> None:
        self.token_store.revoke(refresh_token)


class OAuthClient:
    """The client side of the OAuth2 PKCE authorization-code flow."""

    def __init__(
        self,
        client_id: str,
        redirect_uri: str,
        server: AuthorizationServer,
        scope: str = "",
    ) -> None:
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.server = server
        self.scope = scope

    def build_authorization_url(
        self,
        authorize_endpoint: str,
        code_challenge: str,
        code_challenge_method: str,
        state: str,
    ) -> str:
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "code_challenge": code_challenge,
            "code_challenge_method": code_challenge_method,
            "state": state,
        }
        if self.scope:
            params["scope"] = self.scope
        return f"{authorize_endpoint}?{urllib.parse.urlencode(params)}"

    def start_pkce_flow(
        self,
        authorize_endpoint: str = "https://auth.example/authorize",
        code_verifier: Optional[str] = None,
        state: Optional[str] = None,
        code_challenge_method: str = CODE_CHALLENGE_METHOD_S256,
    ) -> PKCERequest:
        verifier = code_verifier or generate_code_verifier()
        challenge = create_code_challenge(verifier, code_challenge_method)
        state_value = state or generate_token(16)
        url = self.build_authorization_url(
            authorize_endpoint, challenge, code_challenge_method, state_value
        )
        return PKCERequest(
            code_verifier=verifier,
            code_challenge=challenge,
            code_challenge_method=code_challenge_method,
            state=state_value,
            authorization_url=url,
        )

    def exchange_code(self, code: str, code_verifier: str) -> TokenSet:
        return self.server.exchange_code(
            code, self.redirect_uri, code_verifier, self.client_id
        )

    def refresh(self, refresh_token: str, scope: Optional[str] = None) -> TokenSet:
        return self.server.refresh(refresh_token, client_id=self.client_id, scope=scope)
