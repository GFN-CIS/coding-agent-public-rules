---
name: gfn-python
description: Use when writing or reviewing Python code, `.py` files, `pyproject.toml`, or Python tests. Covers PEP8, Black-style formatting enforced by ruff, ruff with select ALL, mypy --strict, vulture, and pytest with pytest_deduplicate and mutmut.
---
# Rules for python code

- Always use PEP8 styling when creating the code.
- pyproject config :
  - Formatting: Black code style with default settings, enforced by `ruff format --check`.
  - Linting: `ruff` with `select = ["ALL"]`. Project-wide ignores are limited to rules that conflict with the formatter (`COM812`, `ISC001`), one of each mutually exclusive docstring pair (`D203`/`D211`, `D212`/`D213`) and rules that do not apply (e.g. `CPY001`). Tests may additionally ignore `S101` and `PLR2004`. Pylint is not used: ruff implements its rules that need no type inference, and the type checker covers the rest.
  - Typing: `mypy --strict` over sources and tests, with `enable_error_code = ["ignore-without-code"]`. Missing third-party stubs are handled per module (`[[tool.mypy.overrides]]`), never by a global `ignore_missing_imports`.
  - Dead code: vulture (ruff covers unused imports and variables, not unused functions and classes).
  - Tests: pytest with auto-discovery, pytest-cov, mutmut, pytest_deduplicate installed from its upstream repository (https://github.com/xor2003/pytest_deduplicate) pinned to a commit (its PyPI releases are outdated).
- unit tests should be created in test directory close to the module they are testing.
- unit tests should be created in auto-discoverable behaviour for pytest.
- use pytest_deduplicate to find the duplicated tests.
- use mutmut to confirm the tests covers what should be covered.
