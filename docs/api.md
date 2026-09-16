# Transfers

Teaching stub only: no persistence, real accounts, authentication, or movement of funds.

`POST /transfer` accepts JSON with nonblank `sourceAccount` and `destinationAccount`, a required decimal `amount`, and `currency` (`USD` or `EUR`). Amounts must be at least zero. Zero is a supported no-op and returns the normal receipt. Negative amounts must return HTTP 400.

```json
{"sourceAccount":"acct-100","destinationAccount":"acct-200","amount":12.50,"currency":"USD"}
```

Success: HTTP 201, `{"id":"<generated UUID>","amount":12.50,"currency":"USD","status":"accepted"}`.

Validation errors use HTTP 400 with `code`, `message`, and `errors` (a list of `field` and `message`). A missing amount uses `VALIDATION_ERROR` / `Request validation failed` with the field message `amount is required`. Invalid JSON uses `INVALID_JSON` with an empty errors list.
