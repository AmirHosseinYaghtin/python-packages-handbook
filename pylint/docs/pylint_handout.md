# Pylint — Deep Review Handout (Python + ML/MLOps)

This document is a **review-first handout**, not a tutorial.

It is meant to be read:
- after learning Pylint once
- when returning to a codebase months later
- when designing CI rules
- when deciding which warnings to keep or relax

It follows the same order Pylint should be learned and internalized.

---

## 0. What this document is (and is not)

This document:
- explains mental models
- captures engineering trade-offs
- documents best practices
- reflects real-world usage

This document does NOT:
- explain basic Python
- explain how to install Pylint
- aim for a perfect 10/10 score

---

## 1. Core mental model

Pylint is a **static analyzer**, not a formatter and not a test runner.

It:
- parses code into an AST
- builds symbol tables
- reasons about scopes and structure
- applies rule-based checkers

Key consequence:
> Pylint reasons about what *can* be known statically — not what happens at runtime.

---

## 2. Message categories and intent

Pylint messages are grouped by intent:

- E (Error): likely bugs
- W (Warning): risky patterns
- R (Refactor): maintainability pressure
- C (Convention): consistency and readability

Errors should almost never be ignored.
Warnings require justification.
Refactors guide long-term quality.
Conventions are team decisions.

---

## 3. Symbolic names matter

Every message has:
- a numeric code (unstable)
- a symbolic name (stable)

Always reason and configure using **symbolic names**.

Example:

```bash
missing-module-docstring
```

Never rely on numeric IDs.

---

## 4. Score and `fail-under`

The Pylint score:
- is relative
- depends on enabled rules
- is NOT an absolute quality metric

`fail-under` controls:
- CI failure
- exit code
- quality gates

It does NOT affect analysis.

---

## 5. Exit codes (CI relevance)

Pylint always runs the same analysis.
CI reacts only to the **exit code**.

- score >= fail-under → exit code 0
- score < fail-under → non-zero exit

CI should enforce:
- minimum quality
- not perfection

---

## 6. Configuration discovery

Pylint searches configuration in this order:

1. pyproject.toml
2. .pylintrc
3. pylintrc
4. setup.cfg
5. user-level config

Modern best practice:
> Use pyproject.toml as the single source of truth.

---

## 7. Fix vs disable (critical distinction)

There are three valid responses to a warning:

1. Fix the code (preferred)
2. Disable locally with justification
3. Disable globally (last resort)

Disabling globally without discussion destroys Pylint’s value.

---

## 8. Disabling rules responsibly

### Inline (most precise)
```bash
# pylint: disable=some-rule
```

Use when the rule is correct in general but wrong here.

### File-level
```bash
# pylint: disable=some-rule
```

Use when the entire file follows a known pattern.

### Config-level
Use only for team-wide decisions.

Never disable large categories blindly.

---

## 9. Common high-value rules (do not relax casually)

- no-member
- undefined-variable
- unused-import
- dangerous-default-value
- redefined-outer-name

These catch real bugs, especially in refactors.

---

## 10. Dynamic code and false positives

Pylint struggles with:
- registries
- factories
- config-driven behavior
- dynamic attributes

This is common in ML code.

The solution is NOT global disabling.
The solution is **type information**.

---

## 11. Registry / factory pattern (why it exists)

Registries solve:
- code duplication
- tight coupling
- config-driven behavior

They allow:
- selecting implementations by name
- stable pipelines
- experiment-driven workflows

They are fundamental in ML systems.

---

## 12. Why Pylint struggles with registries

Registries:
- store classes in dicts
- create instances dynamically
- depend on runtime strings

Static analyzers cannot infer this without help.

---

## 13. Protocols: the correct fix

Protocols describe **behavior**, not inheritance.

They allow:
- sklearn models
- torch modules
- custom code
to share an interface without coupling.

Protocols make dynamic ML code statically understandable.

---

## 14. Why Protocols beat base classes in ML

- no forced inheritance
- no library coupling
- no refactors
- behavior-based contracts

This matches how ML ecosystems evolve.

---

## 15. Pylint + notebooks

Pylint should NOT be run directly on notebooks.

Recommended patterns:
1. Disposable notebooks → extract to .py
2. Notebook → script conversion
3. Ignore notebooks entirely

Production code must live in .py files.

---

## 16. Project structure that works

Recommended layout:


```markdown
project/
├── notebooks/
├── src/
│   └── your_package/
├── tests/
├── pyproject.toml
```

Run Pylint on src/, not the project root.

---

## 17. ML-friendly configuration principles

Relax:
- naming rules for math variables
- argument limits for training loops
- locals count where justified

Keep:
- error-level checks
- structural warnings
- import correctness

---

## 18. Pylint in pre-commit

Pylint should:
- run on staged files
- fail early
- never surprise CI

Pre-commit integration is essential.

---

## 19. Pylint in CI

CI should:
- run Pylint once
- enforce fail-under
- avoid blocking research unnecessarily

Quality gates should be gradual, not abrupt.

---

## 20. Final consolidated rules

- Static analysis complements tests
- Fix before disabling
- Prefer local disables
- Keep error checks enabled
- Teach Pylint with types
- Never lint notebooks directly
- CI should enforce minimum quality
