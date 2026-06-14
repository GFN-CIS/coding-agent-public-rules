# Test Organization & Documentation Rules (Language-Agnostic)

This document defines organization-wide, **language-agnostic** rules for:

- organizing unit/integration tests,
- writing tests that validate behavior (not existence),
- documenting tests and test suites in a consistent, project-approved format.

## Goals

- Tests must fail when behavior breaks (not only when names/types change).
- Tests must be deterministic, isolated, parallel-safe, and easy to maintain.
- Test documentation must clearly state what is validated and why it matters.

## Golden rule (behavior over shape)

Ask:

**“If I fake the implementation with a dumb object that only has the right attributes, will the test still pass?”**

- If **yes** → the test likely checks *shape/existence* and is low-value.
- If **no** → the test likely checks *behavior* and is valuable.

## Core principle: test behavior, not existence

Avoid tests that only check:

- a field/attribute exists,
- a function returns the correct type,
- an internal cache/private variable changes,
- names/strings/paths that can be refactored without changing behavior.

Test languages:
 - For the programming language-specific projects (e.g. python, js, java, php, etc) - prefer using language-specific testing framework.
 - For the non-programming projects (pipes, contracts, terraform, ansible) prefer either using specific framework that best suit needs or using python testing framework.
 - The shell-script based tests should be used only as a last resort.
 - The data tests should avoid using "grep" for testing unless it is really fits best. Avoid using grep-like tests for the structured data. 

Prefer tests that verify at least one of:

- output values,
- state transitions (persisted or observable state),
- emitted events/messages,
- observable side effects,
- error handling behavior.

## Anti-patterns to avoid

1) **Attribute/type checks without behavioral assertion**
   - Acceptable only as a minor setup sanity check (and the real behavioral assertion must follow).

2) **Testing internal implementation**
   - Avoid asserting private/internal fields, cache structures, intermediate steps, or exact call sequences unless the call sequence *is* the contract.

3) **Over-mocking**
   - If you mock the system under test into a no-op, you are not testing behavior.
   - Prefer fakes/stubs at boundaries and keep the core logic real.

4) **Brittle assertions**
   - Avoid depending on exact error messages, formatting, or ordering unless that ordering is part of the contract.

## Test types and boundaries

- **Unit tests**: validate one unit (function/class/module) with minimal dependencies; run fast.
- **Integration tests**: validate interaction of multiple units; keep them deterministic and scoped.
- **End-to-end tests**: validate user-visible flows; fewer in number; highest setup cost.

Always choose the lowest-cost test type that reliably validates the behavior.

## Test placement (where tests live)

- **Unit tests** should live *next to the code they test* : inside/near the module/package in folder like 'tests' or another best-practice language or framework-specific folder.
  - Goal: local ownership, easy navigation, and small, cohesive test suites.
- **End-to-end (E2E) tests** should be placed based on scope:
  - **Module-level** E2E tests: when the scenario touches only one module/component and does not require project-wide wiring.
  - **Project-level** E2E tests: when the scenario spans multiple modules/components or requires end-to-end wiring across the project.
- Prefer **auto-discoverable** test locations/naming conventions for the given language/platform/framework so CI/CD can pick up new tests without manual configuration.
  - This avoids manual CI changes per test and prevents a single project-global test folder from growing into an unstructured dump.

## Structure: Arrange / Act / Assert

Use a consistent structure in test bodies (names vary by project; keep consistency):

- **Arrange (Given)**: create state/inputs.
- **Act (When)**: call the behavior.
- **Assert (Then)**: verify outcomes.

Keep each test focused on one scenario.

## Determinism and isolation

- Tests must not depend on current time, randomness, locale, network, or external services unless explicitly designed to.
- Control nondeterminism: freeze time, seed randomness, stub external calls, isolate filesystem.
- Avoid shared mutable global state.
- Every test must be runnable in parallel with others.

## Naming and intent

- Test names must describe **behavior** and the condition under which it holds.
  - Good pattern: `test_<behavior>_<condition>_<expected>` (adapt to project conventions).
- Prefer many small, readable tests over one large test that hides multiple behaviors.

## Test documentation rules

- All test docstrings/comments must be in **English**.
- Test documentation and inline comments must be understandable to both humans and automated agents.
  - Do not duplicate the same content as separate “for humans” and “for agents” versions.
- Avoid emojis in test logs, comments, and documentation.
- Use the docstring format adopted by the repository (be consistent within the project).
- Documentation should explain **why** this behavior matters (risk/impact), not only what the code does.
- Avoid duplication by using a layered approach and links:
  - **Test docstrings**: scenario-specific intent, assertion, and methodology.
  - **Test module docstring**: suite scope/coverage and pointers to key tests.
  - **Suite-level docs (folder README)**: shared conventions, helpers, datasets, and “how to run”, linking to the module docs/tests for details.
- Documentation location conventions:
  - **Per-test documentation**: docstrings on the test case/function/method.
  - **Per-test-module documentation**: a module/file-level docstring describing scope, coverage, and how to run.
  - **Suite-level documentation** (shared conventions, datasets, helpers, how-to-run): place it in the folder that contains the test suite (e.g., a README in that test directory).

### Standard test docstring template

Use a short, structured docstring (adapt fields to project conventions):

```
"""[One line: behavior being validated]

Validates: [What contract/behavior is being validated]
Code: [production code location(s) being validated]

Assertion: [What MUST be true]

Method:
1. Arrange: [key setup]
2. Act: [the operation]
3. Assert: [key checks and why]

Related:
- [links to related tests or docs]
"""
```

### Regression test docstring template

```
"""[One line: bug being prevented]

Regression: [What the bug was, impact, and how it was triggered]
Reference: [issue/PR/ticket if available]

Code: [production code location(s) that were fixed]
Assertion: [What MUST NOT happen anymore]
"""
```

### Test suite (file/class/module) documentation

Each test suite should have a short header (module docstring or README-style section) that states:

- what component/behavior group it covers,
- what it intentionally does not cover,
- how to run it (if not obvious),
- and any important test data/fixtures conventions.

## Cross-referencing production code

When referencing production code, use a stable, readable format accepted by the project.
Example format:

```
path/to/file.ext::SymbolName (optional line range)
```

Keep references up to date when code moves.

## Tags / categories (if used in the project)

Tests must use markers (e.g., `unit`, `integration`, `slow`, `critical`, `regression`, `migration`):

- use them consistently,
- document what each tag means,
- keep “slow” tests opt-in where possible,
- avoid inflating “critical” labels.

## Review checklist

- [ ] The test validates behavior (not mere existence).
- [ ] It would fail if business logic breaks.
- [ ] It uses a stable public API/contract where possible.
- [ ] It is deterministic and parallel-safe.
- [ ] It has clear intent (name + Arrange/Act/Assert).
- [ ] Any deviation from project conventions is documented (what/why).
