# CI (Phase 5)

GitHub Actions workflow: `.github/workflows/ci.yml`

## What runs

On push and pull request to `master` / `main`:

1. Checkout  
2. Set up Python 3.10  
3. `pip install -r requirements-dev.txt`  
4. `ruff check app tests`  
5. `pytest`

## Security

- `permissions: contents: read` only  
- No secrets required for CI  
- Action versions pinned to tagged releases (`@v4`)

## Local mirror

```bash
pip install -r requirements-dev.txt
ruff check app tests
pytest
```
