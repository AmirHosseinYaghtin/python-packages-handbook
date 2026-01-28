# Pytest for ML / MLOps — Deep Handout

This document is a **conceptual and practical reference** for using `pytest`
correctly in Machine Learning and MLOps contexts.

It focuses on *why* things are done a certain way, not just *how*.

---

## 1. Mental model of testing in ML

Traditional software testing assumes:
- deterministic functions
- stable outputs
- small inputs

ML code violates all three.

Therefore, ML testing must shift focus from:
❌ “Is this output correct?”
to:
✅ “Is this behavior correct?”

---

## 2. What ML unit tests SHOULD verify

Good ML unit tests verify:

- input validation
- output shapes
- data types
- invariants (no gradients, eval mode, etc.)
- error handling
- serialization compatibility
- configuration behavior

They do **not** verify:
- accuracy
- convergence
- training speed
- model quality

Those belong elsewhere.

---

## 3. Project structure rules (`src/` layout)

Always use:
```markdown
src/
src/your_package/
tests/
```


Reasons:
- prevents accidental imports
- forces explicit paths
- works identically in CI and Docker
- avoids IDE-only correctness

Never rely on IDE source roots alone.

---

## 4. pytest.ini is mandatory

`pytest.ini` defines how tests run.

Key responsibilities:
- define Python path
- configure coverage
- enforce consistency

If pytest only works in your IDE, your setup is broken.

---

## 5. Fixtures: dependency injection, not helpers

A fixture is:
- a dependency provider
- injected by name
- managed by pytest

Rule:
> Fixture name == test function argument

Fixtures replace:
- globals
- setup functions
- copy-pasted initialization

---

## 6. Fixture scope rules

Scopes control **lifetime**, not visibility.

- function (default): safest, preferred
- module: limited sharing
- session: dangerous unless immutable

Session scope is only justified when:
- setup is expensive
- object is read-only
- mutation is impossible or copied

---

## 7. Yield fixtures and cleanup

Use `yield` fixtures for:
- files
- directories
- models
- external resources

pytest guarantees teardown even on failure.

Never rely on manual cleanup.

---

## 8. tmp_path: filesystem isolation

Always prefer `tmp_path` over `tempfile`.

Benefits:
- one directory per test
- automatic cleanup
- pathlib API
- CI-safe

Rule:
> No test may write outside its own tmp_path.

---

## 9. Parametrization

Use parametrization when:
- logic is identical
- inputs vary
- edge cases exist

Avoid:
- copy-pasted test functions
- deeply nested parametrization grids

Use `id=` for CI readability.

---

## 10. Exceptions

Test exception **types**, not messages.

Reason:
- messages change
- types define behavior

Only assert messages when validating user-facing contracts.

---

## 11. Floating point correctness

Never compare floats with `==`.

Use:
- `pytest.approx`
- `torch.allclose`

Floating-point instability is normal; flaky tests are not.

---

## 12. Marks: skip vs xfail

- `skip`: test cannot run in this environment
- `xfail`: known broken behavior, documented

Never comment out tests.
Marked tests remain visible and intentional.

---

## 13. conftest.py: fixture visibility

`conftest.py`:
- shares fixture definitions
- requires no imports
- enables layered test design

It does NOT:
- make fixtures global
- change fixture scope

Visibility ≠ lifetime.

---

## 14. autouse fixtures (use sparingly)

Autouse fixtures run implicitly.

Allowed uses:
- enforcing invariants
- seeding randomness
- disabling network access

Forbidden uses:
- loading datasets
- creating models
- allocating GPUs

Rule:
> If it allocates a resource, it must be opt-in.

---

## 15. monkeypatch: side-effect isolation

Use `monkeypatch` for:
- environment variables
- time
- randomness
- paths
- global configuration

Never patch manually.
pytest will always restore state safely.

---

## 16. Logging and output

Prefer logging over print.

Use:
- `caplog` for logs
- `capsys` for stdout/stderr

Assert on:
- signals
- key messages

Not on full log content.

---

## 17. Coverage: correct interpretation

Coverage answers only:
> “Which code paths were executed?”

It does NOT answer:
- correctness
- adequacy
- safety

---

## 18. Branch coverage in ML

Branch coverage matters because:
- preprocessing has conditionals
- error paths are meaningful
- configuration flags change behavior

Line coverage alone is misleading.

---

## 19. What to exclude from coverage

Exclude:
- experiments
- notebooks
- plotting
- CLI glue
- training loops

Focus coverage on:
- logic
- validation
- glue code
- invariants

---

## 20. CI mindset for ML tests

ML CI tests must be:
- fast
- deterministic
- isolated
- readable when failing

CI tests are guardrails, not research blockers.

---

## 21. Final rule set (summary)

- Behavior > values
- Isolation > realism
- Explicit > implicit
- Guardrails > gates
- Confidence > percentages
