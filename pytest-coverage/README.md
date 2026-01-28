## 0. What this document is (and is not)

This document is a review-first handout, not a tutorial.

It is meant to be read:

- after you have learned pytest
- when you want to refresh concepts
- when you want to remember why certain patterns exist
- when designing or reviewing a test suite

It follows the same order we learned things, from core pytest mechanics → advanced pytest features → coverage → ML/MLOps usage.

It intentionally:

- does not explain what testing is
- does not explain how to install pytest
- does not explain basic Python syntax

---
## 1. Pytest's core mental model

Pytest is built around three ideas:

    1. Test discovery by convention
    2. Plain assert statements
    3. Dependency injection via fixtures

Almost everything in pytest is a refinement of these three.

---

## 2. Test discovery (why names matter)

Pytest finds tests based on naming rules, not registration.

Defaults:

- test files: `test_*.py` or `*_test.py`
- test functions: `test_*`
- test classes: `Test*` (no `__init__`)

If pytest says "collected 0 items", the first suspects are:

- wrong file name
- wrong function name
- wrong project root

This convention-based discovery is what enables pytest to stay lightweight.

---

## 3. Imports and the src/ layout (critical)

Correct structure:


```markdown
project/
├── src/
│   └── your_package/
│       ├── __init__.py
│       └── module.py
├── tests/
│   └── test_module.py
```

Key rules:

- `src/` is not a package
- `your_package/` is the package
- tests import only from `your_package`, never from the project root

Why this matters:

- prevents accidental imports
- works identically in IDE, CI, Docker
- avoids "it works on my machine" bugs

---

## 4. pytest.ini is not optional

A serious project always has `pytest.ini`.

Responsibilities:

- define Python path (`pythonpath = src`)
- configure coverage
- standardize behavior across environments

If pytest only works in your IDE but not in terminal or CI, configuration is incomplete.

---

## 5. Assertions and assertion introspection

Pytest rewrites assert statements at runtime.

This gives:

- rich failure output
- values, expressions, and call results
- zero boilerplate

You should:

- use plain `assert`
- never use unittest-style assertion helpers
- rely on pytest's introspection for debugging

This is especially valuable for:

- numerical code
- tensors
- arrays
- shapes and types

---

## 6. Fixtures: the most important concept

Fixtures are dependency providers, not helpers.

Mental model:

A fixture is a named resource that pytest injects into tests by argument name.

Key rule:

Fixture name == test function argument

Fixtures solve:

- setup duplication
- global state
- manual initialization
- brittle test scaffolding

---

## 7. Fixture lifetime and scope

Fixture scope controls lifetime, not visibility.

Scopes:

- function (default): new instance per test
- module: shared within one test file
- session: shared across entire test run

Rules of thumb:

- default to function
- widen scope only when necessary
- never widen scope silently

In ML:

- session scope is tempting
- session scope is dangerous
- only safe for immutable, read-only objects

---

## 8. Yield fixtures (setup + teardown)

Yield fixtures define two phases:


```python
@pytest.fixture
def resource():
    setup()
    yield value
    teardown()
```

Rules:

- everything before `yield` is setup
- everything after `yield` is teardown
- teardown always runs, even on failure

Use yield fixtures for:

- files
- directories
- models
- external resources

Never rely on manual cleanup inside tests.

---

## 9. tmp_path: filesystem isolation done right

`tmp_path` is a built-in fixture that provides:

- a unique directory per test
- automatic cleanup
- `pathlib.Path` interface

Rules:

- prefer `tmp_path` over `tempfile`
- never write outside `tmp_path`
- never share temp directories across tests

In CI, this prevents:

- race conditions
- leftover artifacts
- cross-test interference

---

## 10. Parametrization

Parametrization lets one test cover many inputs.

Use it when:

- logic is identical
- inputs vary
- edge cases matter

Avoid:

- copy-pasted test functions
- deeply nested parametrization grids

Best practice:

- use `id=` for readability in CI output
- keep parameter sets small and meaningful

---

## 11. Exception testing

Always test exception type, not just failure.

Correct pattern:


```python
with pytest.raises(ValueError):
    ...
```

Why:

- exception type defines behavior
- messages change
- types are stable contracts

Only match messages when validating user-facing error text.

---

## 12. Floating-point correctness

Never compare floats with `==`.

Use:

- `pytest.approx`
- `torch.allclose`
- tolerances appropriate to the domain

Floating-point instability is normal.
Flaky tests are not.

---

## 13. conftest.py: fixture visibility

`conftest.py` is a pytest-specific mechanism for sharing fixtures.

Properties:

- automatically discovered
- no imports required
- scoped by directory hierarchy

Important distinction:

`conftest.py` controls where fixtures are visible, not how long they live.

This enables layered test architectures without global state.

---

## 14. autouse fixtures (use with caution)

Autouse fixtures run implicitly.

Valid uses:

- enforcing invariants
- seeding randomness
- disabling network access
- cleanup guards

Invalid uses:

- loading datasets
- creating models
- allocating heavy resources

Rule:

If a fixture allocates or mutates a resource, it must be explicit.

---

## 15. monkeypatch: isolating side effects

`monkeypatch` safely modifies:

- environment variables
- module attributes
- paths
- time
- randomness

Guarantees:

- automatic rollback
- no state leakage
- deterministic tests

Never patch globals manually.

---

## 16. Capturing output and logs

Use:

- `capsys` for stdout/stderr
- `caplog` for logging

Prefer logs over prints.

Assert on:

- key signals
- important events

Avoid asserting full log content.

---

## 17. Coverage: what it really means

Coverage answers one question only:

Which lines and branches were executed?

Coverage does not guarantee:

- correctness
- test quality
- bug absence

Treat coverage as a diagnostic tool, not a score.

---

## 18. Branch coverage vs line coverage

Branch coverage matters when:

- logic has conditionals
- preprocessing paths differ
- configuration flags exist

Line coverage alone can be misleading.

In ML code, branch coverage is often more meaningful.

---

## 19. What to exclude from coverage

Usually exclude:

- experiments
- notebooks
- plotting
- CLI glue
- training loops

Focus coverage on:

- validation
- preprocessing
- configuration logic
- invariants and contracts

---

## 20. ML-specific testing mindset

ML unit tests should emphasize:

- behavior over values
- shapes over numbers
- determinism over realism
- isolation over performance

Training, accuracy, and convergence belong in:

- integration tests
- evaluation pipelines
- offline experiments

---

## 21. Final consolidated rules

- Fixtures are dependencies, not helpers
- Default scope is safest
- Cleanup must be automatic
- Temporary files must be isolated
- Session scope requires immutability
- Coverage is a guardrail
- CI must be fast and deterministic