# ADR-002 — Automated CI Test Workflow

- **Status:** Accepted
- **Date:** 2026-09-23
- **Decision scope:** Repository-level test automation
- **Baseline:** `main @ cae66e5c36e884ddfe00728f59b395ae203079ba` (post ADR-001)

## Context

ADR-001 established a structural refactor workflow that included focused tests and full regression validation. During that work, the project had no GitHub Actions workflow for automated test execution.

Local regression is currently the available validation gate. After ADR-001, the full test suite passed locally with **25 tests passed**. However, without repository-level CI, a pull request can be merged without an automated GitHub-side regression check.

The project now needs a minimal, reproducible automated test gate before future changes are merged.

## Decision

Introduce a **minimal GitHub Actions CI workflow** that automatically runs the project's existing pytest suite for repository changes.

The workflow will:

1. trigger for pull requests targeting `main`;
2. trigger for pushes to `main`;
3. check out the repository;
4. install the project's declared Python dependencies;
5. execute the existing pytest suite;
6. fail the workflow when the test suite fails.

The CI workflow is a validation mechanism only. It does not change application behavior or analysis results.

## Scope

### In scope

- Add `.github/workflows/tests.yml`.
- Use a supported Python version compatible with the current project.
- Install dependencies from the existing dependency definition.
- Run the existing pytest suite.
- Configure CI for pull requests targeting `main`.
- Configure CI for pushes to `main`.
- Verify the workflow executes successfully against the current test suite.

### Out of scope

ADR-002 does **not** change:

- `src/` application logic;
- analysis calculations or output;
- dataset contents;
- test semantics;
- dependency architecture;
- deployment;
- linting or formatting;
- coverage thresholds or coverage reporting;
- release automation;
- README/documentation cleanup unrelated to CI;
- branching or merge-policy redesign.

## CI Behavioral Contract

The workflow must:

- run the existing test suite without requiring manual `PYTHONPATH` setup;
- return a failing status when pytest fails;
- return a passing status when the existing suite passes;
- execute independently of the developer's local shell environment;
- avoid modifying repository source files or generated analysis outputs.

The CI workflow should reproduce the project's intended test command in a clean runner environment.

## Implementation Guardrails

1. Start from the official post-ADR-001 `main` baseline.
2. Keep the workflow minimal and explicit.
3. Reuse the project's existing dependency definition rather than introducing a second dependency system.
4. Do not add unrelated quality gates.
5. Do not modify application code to make CI pass.
6. If CI exposes a pre-existing test-environment issue, investigate it separately rather than silently changing application behavior.
7. Validate the workflow on a pull request before considering ADR-002 complete.

## Consequences

### Positive

- Pull requests receive an automated regression signal.
- Future refactors have a repeatable repository-level validation gate.
- Test execution no longer depends solely on the developer's local environment.
- CI failures become visible in the pull request workflow.

### Negative / Trade-offs

- Adds GitHub Actions configuration that must be maintained.
- CI execution consumes repository automation resources.
- Dependency installation may make CI slower than a purely local test run.

## Validation Strategy

Success requires:

1. The workflow file exists under `.github/workflows/`.
2. Pull requests targeting `main` trigger the workflow.
3. Pushes to `main` trigger the workflow.
4. The existing test suite passes in the GitHub Actions runner.
5. No application behavior or test semantics change as part of the CI implementation.

## Follow-up

Implementation and review proceed separately from this decision record:

**ADR-002 → CI workflow → AI-C review → GitHub Actions regression → merge decision.**

Documentation cleanup and additional quality gates may be considered separately in future changes.
