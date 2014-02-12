# Postmaster proxy

Proxy service for Postmaster.

# Authentication

All incoming requests must contain `X-PM-Auth` header. Otherwise 401 will be returned.

# Abilities

## Stamps authenticator

`/stamps_authenticator` will return a JSON object containing two keys: `production` and `testing`, containing production and testing authenticators.

This handler will also automatically validate both authenticators. In case any of them is no longer valid, it will automatically refresh both of them. This is possible every 5 minutes, meaning that in some cases more than 1 request will be necessary to get valid authenticator.

Authenticator will also be forcefully refreshed at 1 AM CST and 6 AM CST.
