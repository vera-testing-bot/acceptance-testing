"""Authentication middleware chain.

The chain processes a request-like dict through a sequence of middleware.
:class:`AuthMiddleware` validates OAuth2 bearer access tokens against a
:class:`~src.auth.tokens.TokenStore` (issued by the PKCE flow) and attaches
an authentication context to the request. :class:`RequireAuthMiddleware`
short-circuits the chain with a 401 response when no valid token was found.
"""

from __future__ import annotations

import copy
from typing import ClassVar

from src.auth.tokens import ExpiredTokenError, InvalidTokenError, TokenStore


class Middleware:
    """Base middleware: calls the next handler in the chain if one is set."""

    def __init__(self) -> None:
        self._next: Middleware | None = None

    def set_next(self, middleware: Middleware) -> Middleware:
        self._next = middleware
        return middleware

    def handle(self, request: dict) -> dict:
        if self._next is not None:
            return self._next.handle(request)
        return request


class AuthMiddleware(Middleware):
    """Extracts and validates a bearer access token from the request.

    On a valid token the request is annotated with ``authenticated=True`` and
    an ``auth`` context carrying the access token and granted scope. Invalid,
    expired, or missing tokens leave ``authenticated=False`` so downstream
    middleware (e.g. :class:`RequireAuthMiddleware`) can decide how to react.
    """

    def __init__(self, token_store: TokenStore) -> None:
        super().__init__()
        self._token_store = token_store

    def handle(self, request: dict) -> dict:
        token = self._extract_bearer(request)
        if token is not None:
            try:
                token_set = self._token_store.get_by_access_token(token)
            except (InvalidTokenError, ExpiredTokenError):
                request["authenticated"] = False
                request["auth"] = {"authenticated": False}
            else:
                request["authenticated"] = True
                request["auth"] = {
                    "authenticated": True,
                    "access_token": token_set.access_token,
                    "scope": token_set.scope,
                }
        else:
            request.setdefault("authenticated", False)
            request.setdefault("auth", {"authenticated": False})
        return super().handle(request)

    @staticmethod
    def _extract_bearer(request: dict) -> str | None:
        headers = request.get("headers") or {}
        header = headers.get("Authorization") or headers.get("authorization")
        if not header or not header.startswith("Bearer "):
            return None
        return header[len("Bearer ") :].strip()


class RequireAuthMiddleware(Middleware):
    """Rejects the request with a 401 response when unauthenticated."""

    UNAUTHORIZED_RESPONSE: ClassVar[dict] = {
        "status": 401,
        "body": {"error": "unauthorized"},
    }

    def handle(self, request: dict) -> dict:
        if not request.get("authenticated"):
            return copy.deepcopy(self.UNAUTHORIZED_RESPONSE)
        return super().handle(request)


class MiddlewareChain:
    """Builds and runs an ordered chain of middleware."""

    def __init__(self) -> None:
        self._head: Middleware | None = None
        self._tail: Middleware | None = None

    def add(self, middleware: Middleware) -> MiddlewareChain:
        if self._head is None:
            self._head = middleware
            self._tail = middleware
        else:
            assert self._tail is not None
            self._tail.set_next(middleware)
            self._tail = middleware
        return self

    def handle(self, request: dict) -> dict:
        if self._head is None:
            return request
        return self._head.handle(request)
