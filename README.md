# User Management API — E2E Test Suite

End-to-end test suite for the User Management API take-home challenge.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed and running
- Python 3.12+

## Setup

```bash
# Clone the repository
git clone <repository-url>
cd loanpro-take-home

# Install dependencies
pip install -r requirements.txt

# Start the API container
docker run -d -p 3000:3000 ghcr.io/danielsilva-loanpro/sdet-interview-challenge:latest
```

## Running Tests

```bash
# Run tests against dev environment
pytest tests/ --env=dev -v

# Run tests against prod environment
pytest tests/ --env=prod -v

# Generate HTML report
pytest tests/ --env=dev --html=report-dev.html --self-contained-html
```

## Project Structure

```
.
├── .github/workflows/tests.yml    # GitHub Actions CI pipeline
├── tests/
│   ├── conftest.py                # Shared fixtures and CLI options
│   ├── helpers/
│   │   └── api_client.py          # API wrapper class
│   ├── test_list_users.py         # GET /{env}/users
│   ├── test_create_user.py        # POST /{env}/users
│   ├── test_get_user.py           # GET /{env}/users/{email}
│   ├── test_update_user.py        # PUT /{env}/users/{email}
│   ├── test_notes.py              # POST /{env}/users/{email}/notes
│   └── test_delete_user.py        # DELETE /{env}/users/{email}
├── requirements.txt
├── pytest.ini
└── BUGS.md                        # Bug report
```

## Bugs Found

| # | Endpoint | Environment | Expected | Actual | Severity |
|---|----------|-------------|----------|--------|----------|
| 1 | POST /users | both | 409 | 500 | High |
| 2 | POST /users | both | 400 | 500 | High |
| 3 | GET /users/{email} | both | 404 | 500 | High |
| 4 | PUT /users/{email} | both | Persisted | Not persisted | High |
| 5 | PUT /users/{email} | both | 409 | 200 | Medium |
| 6 | DELETE → GET | both | 404 | 500 | High |
| 7 | DELETE /users/{email} | dev | 401 | 204 | Critical |

See [BUGS.md](BUGS.md) for detailed descriptions.

## CI/CD

GitHub Actions runs tests in parallel against both environments:
- **test-dev** — runs against `dev` environment
- **test-prod** — runs against `prod` environment

HTML test reports are uploaded as artifacts after each run.
