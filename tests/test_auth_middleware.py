import pytest

from src.auth.tokens import ExpiredTokenError, TokenSet
from src.middleware.auth import (
    AuthMiddleware,
    Middleware,
    MiddlewareChain,
    RequireAuthMiddleware,
)


def make_request(headers=None, **extra):
    request = {"headers": headers or {}}
    request.update(extra)
    return request


class MarkerMiddleware(Middleware):
    """Records execution order for testing the chain."""

    def __init__(self, marker, order_list):
        super().__init__()
        self._marker = marker
        self._order_list = order_list

    def handle(self, request):
        self._order_list.append(self._marker)
        return super().handle(request)


class TestAuthMiddleware:
    def test_valid_bearer_token_authenticates_request(self, token_store):
        token_store.store(TokenSet("good-token", "r", scope="read"))
        middleware = AuthMiddleware(token_store)

        request = make_request(headers={"Authorization": "Bearer good-token"})
        middleware.handle(request)

        assert request["authenticated"] is True
        assert request["auth"]["access_token"] == "good-token"
        assert request["auth"]["scope"] == "read"

    def test_expired_token_is_not_authenticated(self):
        from src.auth.tokens import TokenStore

        store = TokenStore(clock=lambda: 5000)
        store.store(TokenSet("expired", "r", expires_in=10, issued_at=1000))
        middleware = AuthMiddleware(store)

        request = make_request(headers={"Authorization": "Bearer expired"})
        middleware.handle(request)

        assert request["authenticated"] is False

    def test_unknown_token_is_not_authenticated(self, token_store):
        middleware = AuthMiddleware(token_store)
        request = make_request(headers={"Authorization": "Bearer nope"})
        middleware.handle(request)
        assert request["authenticated"] is False

    def test_missing_authorization_header_is_not_authenticated(self, token_store):
        middleware = AuthMiddleware(token_store)
        request = make_request()
        middleware.handle(request)
        assert request["authenticated"] is False

    def test_non_bearer_scheme_is_not_authenticated(self, token_store):
        token_store.store(TokenSet("good-token", "r"))
        middleware = AuthMiddleware(token_store)
        request = make_request(headers={"Authorization": "Basic good-token"})
        middleware.handle(request)
        assert request["authenticated"] is False

    def test_lowercase_authorization_header_is_accepted(self, token_store):
        token_store.store(TokenSet("good-token", "r"))
        middleware = AuthMiddleware(token_store)
        request = make_request(headers={"authorization": "Bearer good-token"})
        middleware.handle(request)
        assert request["authenticated"] is True


class TestMiddlewareChain:
    def test_chain_runs_middleware_in_order(self):
        order = []
        chain = MiddlewareChain()
        chain.add(MarkerMiddleware("first", order))
        chain.add(MarkerMiddleware("second", order))
        chain.add(MarkerMiddleware("third", order))

        chain.handle(make_request())

        assert order == ["first", "second", "third"]

    def test_empty_chain_returns_request_unchanged(self):
        chain = MiddlewareChain()
        request = make_request()
        assert chain.handle(request) is request

    def test_require_auth_short_circuits_when_unauthenticated(self, token_store):
        order = []
        chain = MiddlewareChain()
        chain.add(AuthMiddleware(token_store))
        chain.add(RequireAuthMiddleware())
        chain.add(MarkerMiddleware("reached", order))

        response = chain.handle(make_request(headers={"Authorization": "Bearer bad"}))

        assert response["status"] == 401
        assert order == []

    def test_require_auth_passes_through_when_authenticated(self, token_store):
        token_store.store(TokenSet("good-token", "r", scope="read"))
        order = []
        chain = MiddlewareChain()
        chain.add(AuthMiddleware(token_store))
        chain.add(RequireAuthMiddleware())
        chain.add(MarkerMiddleware("reached", order))

        chain.handle(make_request(headers={"Authorization": "Bearer good-token"}))

        assert order == ["reached"]


@pytest.fixture
def token_store():
    from src.auth.tokens import TokenStore

    return TokenStore()


def test_authmiddleware_attaches_scope_for_downstream(token_store):
    token_store.store(TokenSet("tok", "r", scope="read write"))
    captured = {}

    class CaptureMiddleware(Middleware):
        def handle(self, request):
            captured.update(request)
            return super().handle(request)

    chain = MiddlewareChain()
    chain.add(AuthMiddleware(token_store))
    chain.add(CaptureMiddleware())

    chain.handle(make_request(headers={"Authorization": "Bearer tok"}))

    assert captured["auth"]["scope"] == "read write"
    assert captured["authenticated"] is True


def test_expired_token_error_is_token_error():
    from src.auth.tokens import TokenError

    assert issubclass(ExpiredTokenError, TokenError)
