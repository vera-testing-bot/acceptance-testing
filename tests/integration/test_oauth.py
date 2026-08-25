"""Integration tests for the OAuth2 PKCE flow across all auth components.

These tests wire together :class:`OAuthClient`, :class:`AuthorizationServer`,
:class:`TokenStore`, and the authentication middleware chain to exercise the
full grant lifecycle end-to-end for each supported grant type:

* the **authorization code grant with PKCE** (initial token issuance)
* the **refresh token grant** (access-token renewal with rotation)
"""

from __future__ import annotations

import pytest

from src.auth.oauth import (
    CODE_CHALLENGE_METHOD_S256,
    AuthorizationServer,
    OAuthClient,
)
from src.auth.tokens import RefreshTokenReuseError, TokenStore
from src.middleware.auth import AuthMiddleware, MiddlewareChain, RequireAuthMiddleware

CLIENT_ID = "client-int"
REDIRECT_URI = "https://app.example/callback"
AUTHORIZE_ENDPOINT = "https://auth.example/authorize"
SCOPE = "read write"


@pytest.fixture
def system():
    """A fully wired auth system: server, client, store, and middleware chain."""
    token_store = TokenStore()
    server = AuthorizationServer(token_store=token_store)
    server.register_client(CLIENT_ID, redirect_uris=[REDIRECT_URI])
    client = OAuthClient(CLIENT_ID, REDIRECT_URI, server, scope=SCOPE)

    chain = MiddlewareChain()
    chain.add(AuthMiddleware(token_store))
    chain.add(RequireAuthMiddleware())

    return System(token_store, server, client, chain)


@pytest.fixture
def authenticated_system(system):
    """System that has already completed the PKCE code exchange once."""
    token_store, server, client, chain = system.unwrap()
    request = client.start_pkce_flow(authorize_endpoint=AUTHORIZE_ENDPOINT)
    code = server.create_authorization_code(
        CLIENT_ID,
        REDIRECT_URI,
        request.code_challenge,
        request.code_challenge_method,
        scope=SCOPE,
        user_id="user-1",
    )
    token_set = client.exchange_code(code, request.code_verifier)
    return token_set, system


class System:
    """Tiny tuple-like wrapper so a single fixture can expose multiple parts."""

    def __init__(self, token_store, server, client, chain):
        self.token_store = token_store
        self.server = server
        self.client = client
        self.chain = chain

    def unwrap(self):
        return self.token_store, self.server, self.client, self.chain


def _bearer(token):
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# Authorization Code grant with PKCE
# ---------------------------------------------------------------------------


class TestAuthorizationCodeGrantWithPKCE:
    def test_full_pkce_flow_issues_usable_access_token(self, system):
        token_store, server, client, chain = system.unwrap()

        request = client.start_pkce_flow(authorize_endpoint=AUTHORIZE_ENDPOINT)
        code = server.create_authorization_code(
            CLIENT_ID,
            REDIRECT_URI,
            request.code_challenge,
            request.code_challenge_method,
            scope=SCOPE,
            user_id="user-1",
        )
        token_set = client.exchange_code(code, request.code_verifier)

        # The issued access token is accepted by the middleware chain.
        response = chain.handle({"headers": _bearer(token_set.access_token)})
        assert response.get("authenticated") is True
        assert response["auth"]["scope"] == SCOPE

    def test_pkce_flow_with_plain_challenge_method(self, system):
        from src.auth.oauth import CODE_CHALLENGE_METHOD_PLAIN

        token_store, server, client, chain = system.unwrap()
        request = client.start_pkce_flow(
            authorize_endpoint=AUTHORIZE_ENDPOINT,
            code_challenge_method=CODE_CHALLENGE_METHOD_PLAIN,
        )
        code = server.create_authorization_code(
            CLIENT_ID,
            REDIRECT_URI,
            request.code_challenge,
            request.code_challenge_method,
            scope=SCOPE,
        )
        token_set = client.exchange_code(code, request.code_verifier)

        assert server.token_store.is_valid_access_token(token_set.access_token)

    def test_authorization_url_carries_pkce_parameters(self, system):
        _, _, client, _ = system.unwrap()
        request = client.start_pkce_flow(authorize_endpoint=AUTHORIZE_ENDPOINT)
        assert "response_type=code" in request.authorization_url
        assert "code_challenge_method=S256" in request.authorization_url
        assert "code_challenge=" in request.authorization_url
        assert f"client_id={CLIENT_ID}" in request.authorization_url
        assert "state=" in request.authorization_url

    def test_wrong_verifier_blocks_token_issuance(self, system):
        _, server, client, chain = system.unwrap()
        request = client.start_pkce_flow(authorize_endpoint=AUTHORIZE_ENDPOINT)
        code = server.create_authorization_code(
            CLIENT_ID,
            REDIRECT_URI,
            request.code_challenge,
            request.code_challenge_method,
            scope=SCOPE,
        )

        from src.auth.oauth import PKCEVerificationError

        with pytest.raises(PKCEVerificationError):
            client.exchange_code(code, "tampered-verifier")


# ---------------------------------------------------------------------------
# Refresh Token grant (rotation)
# ---------------------------------------------------------------------------


class TestRefreshTokenGrant:
    def test_refresh_grant_rotates_and_keeps_access_working(self, authenticated_system):
        token_set, system = authenticated_system
        _, _, client, chain = system.unwrap()

        refreshed = client.refresh(token_set.refresh_token)

        # New access token is valid; old access token is no longer valid.
        response = chain.handle({"headers": _bearer(refreshed.access_token)})
        assert response.get("authenticated") is True
        assert response["auth"]["scope"] == SCOPE

        old_response = chain.handle({"headers": _bearer(token_set.access_token)})
        assert old_response["status"] == 401

    def test_refresh_grant_can_be_chained_multiple_times(self, authenticated_system):
        token_set, system = authenticated_system
        _, _, client, _ = system.unwrap()

        current = token_set
        for _ in range(3):
            current = client.refresh(current.refresh_token)
            assert current.access_token != token_set.access_token

    def test_reusing_retired_refresh_token_is_detected(self, authenticated_system):
        token_set, system = authenticated_system
        _, server, _, _ = system.unwrap()

        server.refresh(token_set.refresh_token)

        with pytest.raises(RefreshTokenReuseError):
            server.token_store.rotate(
                token_set.refresh_token,
                token_set,
            )

    def test_reuse_at_server_refresh_raises_invalid_grant(self, authenticated_system):
        token_set, system = authenticated_system
        _, server, _, _ = system.unwrap()

        server.refresh(token_set.refresh_token)

        from src.auth.oauth import InvalidGrantError

        with pytest.raises(InvalidGrantError):
            server.refresh(token_set.refresh_token)

    def test_revocation_ends_the_session(self, authenticated_system):
        token_set, system = authenticated_system
        _, server, _, chain = system.unwrap()

        server.revoke(token_set.refresh_token)

        response = chain.handle({"headers": _bearer(token_set.access_token)})
        assert response["status"] == 401


# ---------------------------------------------------------------------------
# Middleware integration
# ---------------------------------------------------------------------------


class TestMiddlewareIntegration:
    def test_protected_route_requires_valid_token(self, system):
        _, _, _, chain = system.unwrap()
        response = chain.handle({"headers": {}})
        assert response["status"] == 401

    def test_protected_route_rejects_tampered_token(self, system):
        _, _, _, chain = system.unwrap()
        response = chain.handle({"headers": _bearer("totally-fake-token")})
        assert response["status"] == 401

    def test_rotated_access_token_passes_middleware(self, authenticated_system):
        token_set, system = authenticated_system
        _, _, client, chain = system.unwrap()

        refreshed = client.refresh(token_set.refresh_token)
        response = chain.handle({"headers": _bearer(refreshed.access_token)})
        assert response.get("authenticated") is True
