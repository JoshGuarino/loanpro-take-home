# Bugs Found

> Discrepancies between the API behavior and the OpenAPI specification.

---

## Bug #1: POST /users returns 500 instead of 409 for duplicate email

- **Endpoint**: `POST /{env}/users`
- **Environment**: both
- **Expected (per spec)**: `409` with `{ "error": "..." }` for duplicate email
- **Actual**: `500` Internal Server Error
- **Test**: `test_create_user.py::TestCreateUser::test_create_duplicate_email_returns_409`
- **Status**: Open

---

## Bug #2: POST /users crashes on invalid email format

- **Endpoint**: `POST /{env}/users`
- **Environment**: both
- **Expected (per spec)**: `400` validation error for invalid email format (e.g., `"not-an-email"`)
- **Actual**: `500` Internal Server Error — API crashes instead of returning a validation error
- **Test**: `test_create_user.py::TestCreateUser::test_create_invalid_email_format_returns_400`
- **Status**: Open

---

## Bug #3: GET /users/{email} returns 500 instead of 404 for nonexistent user

- **Endpoint**: `GET /{env}/users/{email}`
- **Environment**: both
- **Expected (per spec)**: `404` with `{ "error": "..." }` when user not found
- **Actual**: `500` Internal Server Error
- **Test**: `test_get_user.py::TestGetUser::test_get_nonexistent_returns_404`
- **Status**: Open

---

## Bug #4: PUT /users/{email} does not persist changes

- **Endpoint**: `PUT /{env}/users/{email}`
- **Environment**: both
- **Expected (per spec)**: Updated user data is persisted; subsequent GET returns updated values
- **Actual**: PUT returns `200` with updated data, but GET still returns the original values
- **Test**: `test_update_user.py::TestUpdateUser::test_update_persists_changes`
- **Status**: Open

---

## Bug #5: PUT /users/{email} returns 200 instead of 409 for duplicate email

- **Endpoint**: `PUT /{env}/users/{email}`
- **Environment**: both
- **Expected (per spec)**: `409` when updating email to one already in use
- **Actual**: `200` — update succeeds, creating a duplicate
- **Test**: `test_update_user.py::TestUpdateUser::test_update_duplicate_email_returns_409`
- **Status**: Open

---

## Bug #6: DELETE /users/{email} — GET returns 500 after delete instead of 404

- **Endpoint**: `DELETE /{env}/users/{email}` then `GET /{env}/users/{email}`
- **Environment**: both
- **Expected (per spec)**: After deletion, GET should return `404`
- **Actual**: GET returns `500` Internal Server Error
- **Test**: `test_delete_user.py::TestDeleteUser::test_delete_removes_user`
- **Status**: Open

---

## Bug #7: DELETE /users/{email} skips auth in dev environment

- **Endpoint**: `DELETE /{env}/users/{email}`
- **Environment**: dev only (works correctly in prod)
- **Expected (per spec)**: `401` when no `Authentication` header or invalid token is provided
- **Actual**: Returns `204` — deletion proceeds without auth
- **Tests**: `test_delete_user.py::TestDeleteUser::test_delete_no_auth_returns_401` and `test_delete_bad_auth_returns_401`
- **Status**: Open

---

## Summary

| # | Endpoint | Environment | Expected | Actual | Severity |
|---|----------|-------------|----------|--------|----------|
| 1 | POST /users | both | 409 | 500 | High |
| 2 | POST /users | both | 400 | 500 | High |
| 3 | GET /users/{email} | both | 404 | 500 | High |
| 4 | PUT /users/{email} | both | Persisted | Not persisted | High |
| 5 | PUT /users/{email} | both | 409 | 200 | Medium |
| 6 | DELETE → GET | both | 404 | 500 | High |
| 7 | DELETE /users/{email} | dev | 401 | 204 | Critical |
