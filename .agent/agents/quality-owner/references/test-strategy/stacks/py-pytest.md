# py-pytest

**Unit/integration:** pytest · **E2E:** pytest + Playwright or httpx client tests

## Layout

```txt
tests/
  unit/
  integration/
  conftest.py
pyproject.toml or pytest.ini
```

## Commands

```bash
pytest
pytest tests/unit -q
pytest --cov=src
```

## US Plan citation

`docs/10_test_strategy.md` — § Runners (`py-pytest`)

## Notes

- Fixtures in `conftest.py` per directory
- Mark slow tests `@pytest.mark.slow` for CI splits
