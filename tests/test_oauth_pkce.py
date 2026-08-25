import base64
import hashlib

import pytest

from src.auth.oauth import (
    CODE_CHALLENGE_METHOD_PLAIN,
    CODE_CHALLENGE_METHOD_S256,
    AuthorizationServer,
    InvalidClientError,
    InvalidGrantError,
    InvalidRedirectUriError,
    OAuthClient,
    PKCEVerificationError,
    create_code_challenge,
    generate_code_verifier,
)

# RFC 7636 Appendix B test vector.
RFC_VERIFIER = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
RFC_CHALLENGE = "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM"


class TestPKCEHelpers:
    def test_s256_challenge_matches_rfc_vector(self):
        assert (
            create_code_challenge(RFC_VERIFIER, CODE_CHALLENGE_METHOD_S256)
            == RFC_CHALLENGE
        )

    def test_s256_is_base64url_sha256_without_padding(self):
        verifier = "some-verifier-value"
        expected = (
            base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("ascii")).digest())
            .rstrip(b"=")
            .decode("ascii")
        )
        assert create_code_challenge(verifier, CODE_CHALLENGE_METHOD_S256) == expected

    def test_plain_method_returns_verifier_unchanged(self):
        assert (
            create_code_challenge(RFC_VERIFIER, CODE_CHALLENGE_METHOD_PLAIN)
            == RFC_VERIFIER
        )

    def test_unknown_method_raises(self):
        with pytest.raises(ValueError):
            create_code_challenge(RFC_VERIFIER, "bogus")

    def test_generated_verifiers_are_unique(self):
        verifiers = {generate_code_verifier() for _ in range(50)}
        assert len(verifiers) == 50

    def test_generated_verifier_is_url_safe(self):
        verifier = generate_code_verifier()
        assert verifier.isascii()
        for char in verifier:
            assert char.isalnum() or char in "-._~"


@pytest.fixture
def server():
    srv = AuthorizationServer()
    srv.register_client("client-1", redirect_uris=["https://app.example/cb"])
    return srv


@pytest.fixture
def pkce_pair():
    verifier = generate_code_verifier()
    challenge = create_code_challenge(verifier, CODE_CHALLENGE_METHOD_S256)
    return verifier, challenge


class TestAuthorizationServerCodeExchange:
    def test_exchange_code_issues_and_stores_tokens(self, server, pkce_pair):
        verifier, challenge = pkce_pair
        code = server.create_authorization_code(
            "client-1",
            "https://app.example/cb",
            challenge,
            CODE_CHALLENGE_METHOD_S256,
            scope="read",
        )
        token_set = server.exchange_code(
            code, "https://app.example/cb", verifier, "client-1"
        )

        assert token_set.access_token
        assert token_set.refresh_token
        assert token_set.access_token != token_set.refresh_token
        assert token_set.scope == "read"
        assert server.token_store.is_valid_access_token(token_set.access_token) is True

    def test_exchange_code_with_wrong_verifier_fails(self, server, pkce_pair):
        _, challenge = pkce_pair
        code = server.create_authorization_code(
            "client-1", "https://app.example/cb", challenge, CODE_CHALLENGE_METHOD_S256
        )
        with pytest.raises(PKCEVerificationError):
            server.exchange_code(
                code, "https://app.example/cb", "wrong-verifier", "client-1"
            )

    def test_exchange_code_consumed_code_cannot_be_reused(self, server, pkce_pair):
        verifier, challenge = pkce_pair
        code = server.create_authorization_code(
            "client-1", "https://app.example/cb", challenge, CODE_CHALLENGE_METHOD_S256
        )
        server.exchange_code(code, "https://app.example/cb", verifier, "client-1")
        with pytest.raises(InvalidGrantError):
            server.exchange_code(code, "https://app.example/cb", verifier, "client-1")

    def test_exchange_unknown_code_fails(self, server, pkce_pair):
        verifier, _ = pkce_pair
        with pytest.raises(InvalidGrantError):
            server.exchange_code("nope", "https://app.example/cb", verifier, "client-1")

    def test_exchange_redirect_uri_mismatch_fails(self, server, pkce_pair):
        verifier, challenge = pkce_pair
        code = server.create_authorization_code(
            "client-1", "https://app.example/cb", challenge, CODE_CHALLENGE_METHOD_S256
        )
        with pytest.raises(InvalidGrantError):
            server.exchange_code(code, "https://other.example/cb", verifier, "client-1")

    def test_exchange_client_mismatch_fails(self, server, pkce_pair):
        verifier, challenge = pkce_pair
        code = server.create_authorization_code(
            "client-1", "https://app.example/cb", challenge, CODE_CHALLENGE_METHOD_S256
        )
        with pytest.raises(InvalidGrantError):
            server.exchange_code(code, "https://app.example/cb", verifier, "client-2")

    def test_create_code_for_unregistered_client_fails(self, server, pkce_pair):
        _, challenge = pkce_pair
        with pytest.raises(InvalidClientError):
            server.create_authorization_code(
                "ghost", "https://app.example/cb", challenge, CODE_CHALLENGE_METHOD_S256
            )

    def test_create_code_unregistered_redirect_uri_fails(self, server, pkce_pair):
        _, challenge = pkce_pair
        with pytest.raises(InvalidRedirectUriError):
            server.create_authorization_code(
                "client-1",
                "https://evil.example/cb",
                challenge,
                CODE_CHALLENGE_METHOD_S256,
            )


class TestAuthorizationServerRefreshGrant:
    def test_refresh_issues_new_tokens_and_rotates(self, server, pkce_pair):
        verifier, challenge = pkce_pair
        code = server.create_authorization_code(
            "client-1", "https://app.example/cb", challenge, CODE_CHALLENGE_METHOD_S256
        )
        original = server.exchange_code(
            code, "https://app.example/cb", verifier, "client-1"
        )

        refreshed = server.refresh(original.refresh_token)

        assert refreshed.access_token != original.access_token
        assert refreshed.refresh_token != original.refresh_token
        assert server.token_store.is_valid_access_token(refreshed.access_token) is True
        assert server.token_store.is_valid_access_token(original.access_token) is False

    def test_refresh_unknown_token_fails(self, server):
        with pytest.raises(InvalidGrantError):
            server.refresh("does-not-exist")

    def test_refresh_reuse_of_retired_token_fails(self, server, pkce_pair):
        verifier, challenge = pkce_pair
        code = server.create_authorization_code(
            "client-1", "https://app.example/cb", challenge, CODE_CHALLENGE_METHOD_S256
        )
        original = server.exchange_code(
            code, "https://app.example/cb", verifier, "client-1"
        )

        server.refresh(original.refresh_token)

        with pytest.raises(InvalidGrantError):
            server.refresh(original.refresh_token)

    def test_revoke_invalidates_token(self, server, pkce_pair):
        verifier, challenge = pkce_pair
        code = server.create_authorization_code(
            "client-1", "https://app.example/cb", challenge, CODE_CHALLENGE_METHOD_S256
        )
        token_set = server.exchange_code(
            code, "https://app.example/cb", verifier, "client-1"
        )

        server.revoke(token_set.refresh_token)

        assert server.token_store.is_valid_access_token(token_set.access_token) is False
        with pytest.raises(InvalidGrantError):
            server.refresh(token_set.refresh_token)


class TestOAuthClient:
    def test_build_authorization_url_contains_required_params(self, server):
        client = OAuthClient(
            "client-1", "https://app.example/cb", server, scope="read write"
        )
        url = client.build_authorization_url(
            "https://auth.example/authorize",
            code_challenge="challenge-value",
            code_challenge_method=CODE_CHALLENGE_METHOD_S256,
            state="state-123",
        )
        assert url.startswith("https://auth.example/authorize?")
        assert "client_id=client-1" in url
        assert "redirect_uri=" in url
        assert "response_type=code" in url
        assert "code_challenge=challenge-value" in url
        assert "code_challenge_method=S256" in url
        assert "state=state-123" in url
        assert "scope=" in url

    def test_start_pkce_flow_returns_matching_verifier_and_challenge(self, server):
        client = OAuthClient("client-1", "https://app.example/cb", server)
        request = client.start_pkce_flow()
        expected = create_code_challenge(
            request.code_verifier, request.code_challenge_method
        )
        assert request.code_challenge == expected
        assert request.state
        assert "code_challenge=" in request.authorization_url

    def test_client_full_exchange_and_refresh(self, server):
        client = OAuthClient("client-1", "https://app.example/cb", server, scope="read")
        request = client.start_pkce_flow()

        # Simulate the resource owner granting access via the AS.
        code = server.create_authorization_code(
            "client-1",
            "https://app.example/cb",
            request.code_challenge,
            request.code_challenge_method,
            scope="read",
        )

        token_set = client.exchange_code(code, request.code_verifier)
        assert token_set.scope == "read"

        refreshed = client.refresh(token_set.refresh_token)
        assert refreshed.access_token != token_set.access_token
