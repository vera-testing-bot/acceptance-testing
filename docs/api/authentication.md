# Authentication API

This module implements an OAuth2 Authorization Code flow with PKCE
([RFC 7636](https://datatracker.ietf.org/doc/html/rfc7636)) together with a
token storage layer that supports refresh-token rotation and an
authentication middleware chain.

The authorization server is implemented in-process so the full grant
lifecycle can be exercised end-to-end (including in the test suite) without
a network dependency. Token persistence and rotation are delegated to the
storage layer.

## Components

| Component | Location | Responsibility |
|-----------|----------|----------------|
| `TokenSet`, `TokenStore` | `src/auth/tokens.py` | Token storage, lookup, rotation, revocation |
| PKCE helpers, `AuthorizationServer`, `OAuthClient` | `src/auth/oauth.py` | PKCE challenge derivation, code exchange, token issuance & refresh |
| `AuthMiddleware`, `MiddlewareChain` | `src/middleware/auth.py` | Bearer-token validation in the request pipeline |

## PKCE flow

PKCE (Proof Key for Code Exchange) prevents an intercepted authorization
code from being redeemed by an attacker. The client creates a high-entropy
`code_verifier`, derives a `code_challenge`, and sends only the challenge
in the authorization request. When redeeming the code, the client presents
the verifier; the authorization server confirms it hashes to the stored
challenge.

```python
from src.auth.oauth import (
    AuthorizationServer,
    OAuthClient,
    CODE_CHALLENGE_METHOD_S256,
)

server = AuthorizationServer()
server.register_client("my-client", redirect_uris=["https://app.example/cb"])

client = OAuthClient("my-client", "https://app.example/cb", server, scope="read")

# 1. Client begins the flow.
request = client.start_pkce_flow(
    authorize_endpoint="https://auth.example/authorize",
    code_challenge_method=CODE_CHALLENGE_METHOD_S256,
)
# Redirect the user to request.authorization_url.

# 2. Resource owner grants access; the server issues an authorization code.
code = server.create_authorization_code(
    "my-client",
    "https://app.example/cb",
    request.code_challenge,
    request.code_challenge_method,
    scope="read",
)

# 3. Client redeems the code with the verifier.
token_set = client.exchange_code(code, request.code_verifier)
```

### PKCE helpers

- `generate_code_verifier(length=64)` — returns a cryptographically random,
  URL-safe string of unreserved characters (`[A-Za-z0-9-._~]`), 43–128 chars.
- `create_code_challenge(verifier, method=CODE_CHALLENGE_METHOD_S256)` —
  derives the challenge. `S256` is `base64url(sha256(verifier))` without
  padding; `plain` returns the verifier unchanged.

The `S256` implementation matches the test vector in
[RFC 7636 Appendix B](https://datatracker.ietf.org/doc/html/rfc7636#appendix-B).

## Grant types

### Authorization Code grant (with PKCE)

`AuthorizationServer.exchange_code(code, redirect_uri, code_verifier, client_id)`
validates the authorization code, confirms the redirect URI and client match,
verifies the PKCE `code_verifier` against the stored challenge, then issues a
`TokenSet` (access token + refresh token) and stores it. The issuing
`client_id` is recorded on the `TokenSet` so the refresh grant can enforce
client binding. Authorization codes are single-use; presenting a consumed code
raises `InvalidGrantError`. A mismatched verifier raises `PKCEVerificationError`.

### Refresh Token grant (with rotation)

`AuthorizationServer.refresh(refresh_token, client_id=None)` (or
`OAuthClient.refresh`, which passes its own `client_id`) issues a fresh
`TokenSet` and rotates the refresh token via `TokenStore.rotate`:

- the old refresh token is invalidated and remembered as revoked,
- the old access token is removed,
- the new token set is stored (inheriting the original `client_id`).

Per [RFC 6749 §6](https://datatracker.ietf.org/doc/html/rfc6749#section-6), when
`client_id` is supplied and the stored token set carries one, the authorization
server verifies they match and rejects a mismatch with `InvalidGrantError`
(`OAuthClient.refresh` always supplies its `client_id`, so cross-client
redemption is blocked). Refreshing without a `client_id` skips the binding
check (the caller is implicitly the authorization server itself).

Reusing a retired refresh token raises `RefreshTokenReuseError` (surfaced as
`InvalidGrantError` from the server) — a strong indicator of token theft.

## Token storage layer

`TokenStore` is an in-memory store indexing `TokenSet` records by both access
token (for request validation) and refresh token (for rotation). A clock
callable can be injected for deterministic expiry tests.

| Method | Behavior |
|--------|----------|
| `store(token_set)` | Indexes the token set by access and refresh token. |
| `get_by_access_token(token)` | Returns the set; raises `ExpiredTokenError` if expired, `InvalidAccessTokenError` if unknown. |
| `get_by_refresh_token(token)` | Returns the set; raises `InvalidRefreshTokenError` if unknown. |
| `is_valid_access_token(token)` | `True` only if present and not expired. |
| `rotate(refresh_token, new_set)` | Retires the old token, stores the new one; raises `RefreshTokenReuseError` on reuse. |
| `revoke(refresh_token)` | Removes the token set and marks the refresh token revoked. Idempotent. |

### Error hierarchy

```
TokenError
├── InvalidTokenError            # unknown / removed token (common base)
│   ├── InvalidAccessTokenError  # unknown / removed access token
│   └── InvalidRefreshTokenError # unknown / removed refresh token
├── RefreshTokenReuseError       # retired refresh token reused
└── ExpiredTokenError            # access token past expiry

AuthorizationError
├── InvalidClientError
├── InvalidRedirectUriError
└── InvalidGrantError
    └── PKCEVerificationError
```

`AuthMiddleware` catches the shared `InvalidTokenError` base when validating a
bearer access token, so both unknown-access and unknown-refresh failures are
handled uniformly without callers reasoning backwards through a misleading
type.

## Middleware chain

`src/middleware/auth.py` provides a small middleware pipeline that processes
request-like dicts.

- `Middleware` — base class; `set_next(m)` links handlers, `handle(request)`
  forwards to the next middleware.
- `AuthMiddleware(token_store)` — extracts a `Bearer` access token from the
  `Authorization` header, validates it against the `TokenStore`, and annotates
  the request with `authenticated` (bool) and an `auth` context
  (`{authenticated, access_token, scope}`). Missing, invalid, or expired
  tokens leave `authenticated=False`.
- `RequireAuthMiddleware` — short-circuits the chain with a `401` response
  when the request is not authenticated.
- `MiddlewareChain` — builds an ordered chain via `.add(...)` and runs it
  via `.handle(request)`.

```python
from src.auth.tokens import TokenStore
from src.middleware.auth import AuthMiddleware, MiddlewareChain, RequireAuthMiddleware

token_store = TokenStore()

chain = MiddlewareChain()
chain.add(AuthMiddleware(token_store))
chain.add(RequireAuthMiddleware())

response = chain.handle({"headers": {"Authorization": "Bearer <access-token>"}})
```

A request carrying a valid, non-expired access token passes through to the
end of the chain (`response["authenticated"] is True`). A request with no
token, an expired token, or an unknown token is rejected with
`{"status": 401, "body": {"error": "unauthorized"}}`.
