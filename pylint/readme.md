# Pylint — Static Analysis and Code Quality Handbook

This folder is a **review-first, concept-driven handbook** for using Pylint
correctly in professional Python projects.

It is written to support:
- long-term retention
- large codebases
- ML and MLOps workflows
- CI-enforced quality standards

This is not a tutorial.
This is not a rule dump.
This is a mental model and engineering playbook.

---

## What Pylint is (in one sentence)

Pylint is a **static code analyzer** that enforces correctness, structure,
and long-term maintainability of Python code.

---

## Why Pylint exists alongside other tools

Pylint does NOT replace:
- black (formatting)
- isort (imports)
- pytest (correctness)
- mypy (type checking)

Pylint focuses on:
- structural correctness
- semantic bugs
- maintainability
- design degradation over time

---

## How this folder should be used

### First-time learning
1. Read `docs/pylint_handout.md` top to bottom
2. Open the examples folder
3. Run pylint on each example and inspect messages

### Reviewing later
1. Skim the handout headings
2. Jump to specific sections (config, disabling, ML patterns)
3. Copy config patterns into real projects

### Reusing in real projects
- Copy the **config patterns**, not blindly the rules
- Adapt thresholds to context
- Keep `no-member` and error-level checks enabled

---

## Design philosophy (important)

This handout follows the **exact order Pylint should be learned**:

1. Core mental model
2. Messages and scoring
3. Configuration
4. Disabling rules responsibly
5. Dynamic code and false positives
6. Type hints and Protocols
7. ML/MLOps-specific usage
8. CI and pre-commit integration

This mirrors how engineers actually grow into Pylint —
not how documentation lists features.

---

## Relationship to ML/MLOps

Pylint is especially valuable in ML/MLOps because:
- ML code is long-lived
- pipelines grow organically
- dynamic behavior hides bugs
- CI must fail early and cheaply

Used correctly, Pylint prevents:
- silent design rot
- unreadable training code
- brittle pipelines
- CI surprises

Used incorrectly, it becomes noise.

This handbook teaches the difference.
