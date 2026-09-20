# Rules for python code

- Always use PEP8 styling when creating the code.
- pyproject config : 
  - Ensure black formatter with appropriate styling is present
  - Ensure using pytest with tests auto-discovery.
  - Ensure using pylint, pytest-cov, pytest_deduplicate, mutmut.
- unit tests should be created in test directory close to the module they are testing.
- unit tests should be created in auto-discoverable behaviour for pytest.
- use vulture or alternatives to find dead code at linting stage.
- use https://github.com/xor2003/pytest_deduplicate to find the duplicaed tests.
- use mutmut to confirm the tests covers what should be covered.
