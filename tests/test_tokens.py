import pytest

from src.auth.tokens import (
    DEFAULT_ACCESS_TOKEN_TTL,
    DEFAULT_REFRESH_TOKEN_TTL,
    ExpiredTokenError,
    InvalidAccessTokenError,
    InvalidRefreshTokenError,
    InvalidTokenError,
    RefreshTokenReuseError,
    TokenError,
    TokenSet,
    TokenStore,
)


def make_token_set(access_token="access-1", refresh_token="refresh-1", **kwargs):
    return TokenSet(
        access_token=access_token,
        refresh_token=refresh_token,
        **kwargs,
    )


class TestTokenSet:
    def test_expires_at_is_issued_at_plus_expires_in(self):
        token_set = TokenSet(
            access_token="a",
            refresh_token="r",
            expires_in=120,
            issued_at=1000,
        )
        assert token_set.expires_at == 1120

    def test_is_expired_false_before_expiry(self):
        token_set = TokenSet(
            access_token="a", refresh_token="r", expires_in=100, issued_at=1000
        )
        assert token_set.is_expired(now=1099) is False

    def test_is_expired_true_at_and_after_expiry(self):
        token_set = TokenSet(
            access_token="a", refresh_token="r", expires_in=100, issued_at=1000
        )
        assert token_set.is_expired(now=1100) is True
        assert token_set.is_expired(now=5000) is True

    def test_defaults_are_sensible(self):
        token_set = TokenSet(access_token="a", refresh_token="r")
        assert token_set.token_type == "Bearer"
        assert token_set.expires_in == DEFAULT_ACCESS_TOKEN_TTL
        assert token_set.scope == ""

    def test_to_dict_roundtrips_through_from_dict(self):
        token_set = TokenSet(
            access_token="a",
            refresh_token="r",
            expires_in=90,
            token_type="Bearer",
            scope="read write",
            issued_at=1234,
            client_id="client-1",
        )
        restored = TokenSet.from_dict(token_set.to_dict())
        assert restored.access_token == "a"
        assert restored.refresh_token == "r"
        assert restored.expires_in == 90
        assert restored.scope == "read write"
        assert restored.issued_at == 1234
        assert restored.client_id == "client-1"
        assert restored.expires_at == token_set.expires_at

    def test_to_dict_preserves_non_default_expires_at(self):
        # An explicitly-supplied expires_at (e.g. extended lifetime) must
        # survive a round-trip rather than being silently recomputed.
        token_set = TokenSet(
            access_token="a",
            refresh_token="r",
            expires_in=90,
            issued_at=1000,
            expires_at=5000,
        )
        assert token_set.expires_at == 5000

        restored = TokenSet.from_dict(token_set.to_dict())
        assert restored.expires_at == 5000
        assert restored.issued_at == 1000
        assert restored.expires_in == 90


class TestTokenStoreStorage:
    def test_store_and_get_by_access_token(self):
        store = TokenStore()
        token_set = make_token_set()
        store.store(token_set)
        assert store.get_by_access_token("access-1") is token_set

    def test_store_and_get_by_refresh_token(self):
        store = TokenStore()
        token_set = make_token_set()
        store.store(token_set)
        assert store.get_by_refresh_token("refresh-1") is token_set

    def test_get_unknown_access_token_raises(self):
        store = TokenStore()
        with pytest.raises(InvalidAccessTokenError):
            store.get_by_access_token("nope")

    def test_get_unknown_refresh_token_raises(self):
        store = TokenStore()
        with pytest.raises(InvalidRefreshTokenError):
            store.get_by_refresh_token("nope")

    def test_is_valid_access_token_true_when_stored_and_fresh(self):
        store = TokenStore(clock=lambda: 1000)
        store.store(TokenSet("a", "r", expires_in=100, issued_at=1000))
        assert store.is_valid_access_token("a") is True

    def test_is_valid_access_token_false_when_expired(self):
        store = TokenStore(clock=lambda: 5000)
        store.store(TokenSet("a", "r", expires_in=100, issued_at=1000))
        assert store.is_valid_access_token("a") is False

    def test_is_valid_access_token_false_when_unknown(self):
        store = TokenStore()
        assert store.is_valid_access_token("missing") is False

    def test_get_by_access_token_raises_when_expired(self):
        store = TokenStore(clock=lambda: 5000)
        store.store(TokenSet("a", "r", expires_in=100, issued_at=1000))
        with pytest.raises(ExpiredTokenError):
            store.get_by_access_token("a")


class TestRefreshTokenRotation:
    def test_rotate_invalidates_old_and_stores_new(self):
        store = TokenStore()
        old = make_token_set(access_token="a1", refresh_token="r1")
        new = make_token_set(access_token="a2", refresh_token="r2")
        store.store(old)

        result = store.rotate("r1", new)

        assert result is new
        # Old tokens are gone
        with pytest.raises(InvalidRefreshTokenError):
            store.get_by_refresh_token("r1")
        with pytest.raises(InvalidAccessTokenError):
            store.get_by_access_token("a1")
        # New tokens are retrievable
        assert store.get_by_refresh_token("r2") is new
        assert store.get_by_access_token("a2") is new

    def test_rotate_unknown_refresh_token_raises(self):
        store = TokenStore()
        new = make_token_set(access_token="a2", refresh_token="r2")
        with pytest.raises(InvalidRefreshTokenError):
            store.rotate("unknown", new)

    def test_rotate_detects_reuse_of_revoked_token(self):
        store = TokenStore()
        old = make_token_set(access_token="a1", refresh_token="r1")
        first_new = make_token_set(access_token="a2", refresh_token="r2")
        second_new = make_token_set(access_token="a3", refresh_token="r3")
        store.store(old)

        store.rotate("r1", first_new)

        # Reusing the now-rotated-out refresh token must be flagged as reuse.
        with pytest.raises(RefreshTokenReuseError):
            store.rotate("r1", second_new)

    def test_rotate_detects_reuse_of_explicitly_revoked_token(self):
        store = TokenStore()
        token_set = make_token_set(access_token="a1", refresh_token="r1")
        store.store(token_set)

        store.revoke("r1")

        with pytest.raises(RefreshTokenReuseError):
            store.rotate("r1", make_token_set())

    def test_revoke_removes_tokens(self):
        store = TokenStore()
        token_set = make_token_set()
        store.store(token_set)
        store.revoke("refresh-1")
        with pytest.raises(InvalidRefreshTokenError):
            store.get_by_refresh_token("refresh-1")
        with pytest.raises(InvalidAccessTokenError):
            store.get_by_access_token("access-1")

    def test_revoke_unknown_token_is_idempotent(self):
        store = TokenStore()
        # Should not raise
        store.revoke("never-existed")

    def test_reuse_error_is_subclass_of_token_error(self):
        assert issubclass(RefreshTokenReuseError, TokenError)
        assert issubclass(InvalidRefreshTokenError, TokenError)
        assert issubclass(InvalidAccessTokenError, TokenError)
        assert issubclass(InvalidTokenError, TokenError)
        assert issubclass(ExpiredTokenError, TokenError)
        # Access and refresh token errors share a common base so callers
        # validating either token type can catch InvalidTokenError.
        assert issubclass(InvalidAccessTokenError, InvalidTokenError)
        assert issubclass(InvalidRefreshTokenError, InvalidTokenError)
        # The two leaf types remain distinct: an unknown access token must
        # not be reported as a refresh-token error (and vice versa).
        assert not issubclass(InvalidAccessTokenError, InvalidRefreshTokenError)
        assert not issubclass(InvalidRefreshTokenError, InvalidAccessTokenError)


class TestTokenStoreClock:
    def test_clock_drives_expiry_evaluation(self):
        time_box = {"now": 1000}
        store = TokenStore(clock=lambda: time_box["now"])
        store.store(TokenSet("a", "r", expires_in=100, issued_at=1000))

        assert store.is_valid_access_token("a") is True
        time_box["now"] = 1200
        assert store.is_valid_access_token("a") is False


def test_default_token_ttls_are_distinct_and_positive():
    assert DEFAULT_ACCESS_TOKEN_TTL > 0
    assert DEFAULT_REFRESH_TOKEN_TTL > DEFAULT_ACCESS_TOKEN_TTL
