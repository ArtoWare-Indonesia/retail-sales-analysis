# ADR-003 — Repository Documentation & Version Consistency

- **Status:** Accepted
- **Date:** 2026-09-23
- **Decision scope:** Repository documentation and version metadata consistency
- **Baseline:** `main` at the current post-ADR-002 state

## Context

The structural audit following ADR-001 and ADR-002 found several documentation and metadata inconsistencies that do not currently affect application execution but reduce repository accuracy and maintainability.

Observed inconsistencies include:

- README test counts are stale and contain multiple historical values.
- README version and roadmap entries do not consistently reflect the current implemented state.
- `config.py`, `main.py`, `interactive_visualization.py`, and `visualization.py` contain inconsistent version references.
- The repository uses `README.MD` while documentation references `README.md`.
- README documentation does not yet describe the current GitHub Actions test workflow introduced by ADR-002.

These are documentation/repository-consistency issues rather than application-logic defects.

## Decision

Establish a single, internally consistent repository documentation state for the current release and development baseline.

The cleanup will:

1. align README version, roadmap, implemented features, and test-status information with the actual repository state;
2. remove stale or contradictory historical test counts from the current-status sections;
3. align version references in source metadata where they are intended to represent the current application version;
4. normalize the README filename to the repository's documented convention;
5. document the current automated test workflow and how developers should run tests locally;
6. preserve historical ADR records and release history rather than rewriting past decisions.

The goal is documentation accuracy and consistency, not application redesign.

## Scope

### In scope

- README current-state documentation.
- README filename casing normalization.
- Current application version metadata consistency.
- Current test count/status documentation.
- Current roadmap/version labeling.
- Documentation of the GitHub Actions test workflow.
- Removal of contradictory or obsolete current-state statements.

### Out of scope

ADR-003 does **not** change:

- analysis calculations;
- dataset contents;
- `src/` architecture or business logic, except version metadata where explicitly required for consistency;
- test semantics;
- dependency architecture;
- CI workflow behavior;
- coverage thresholds;
- linting or formatting;
- release automation;
- dataset reusability or generic schema abstraction;
- historical ADR decisions.

## Documentation Contract

After implementation:

- README must describe the current repository state accurately.
- Current test status must have one authoritative value.
- Current version references must not contradict one another.
- Roadmap entries must distinguish completed work from future work.
- CI documentation must match the actual workflow configuration.
- Historical information may remain where useful, but must be clearly identifiable as historical rather than current state.
- Documentation changes must not silently alter application behavior.

## Implementation Guardrails

1. Start from the official current `main` baseline.
2. Inspect the actual repository state before changing documentation.
3. Do not invent test counts, versions, or implemented features; derive them from repository evidence.
4. Keep historical ADR records unchanged.
5. Avoid bundling unrelated source refactors.
6. If a version inconsistency reveals a genuine release-management problem, record it for a separate decision rather than expanding ADR-003.
7. Validate documentation references after implementation.

## Consequences

### Positive

- Repository documentation becomes trustworthy as a portfolio artifact.
- Developers can understand the current test and CI state without relying on chat history.
- Version references become easier to maintain.
- Historical decisions remain traceable without being confused with current status.

### Negative / Trade-offs

- Documentation must be updated when release state changes.
- Filename normalization may create a case-only rename that requires care across platforms.
- Version metadata consistency may expose a future need for a more formal release/versioning policy.

## Validation Strategy

Success requires:

1. README current-state statements match repository evidence.
2. Test status is represented consistently.
3. Current version references are consistent where they represent the same release state.
4. README naming is normalized without leaving a duplicate case-variant file.
5. CI documentation reflects the actual workflow.
6. ADR-001 and ADR-002 remain unchanged.
7. No analysis behavior or test semantics change.

## Follow-up

Implementation and review proceed separately from this decision record:

**ADR-003 → documentation/version cleanup → AI-C review → regression/consistency audit → merge decision.**

Dataset reusability and generic-schema abstraction remain candidates for a separate future ADR.
