# ADR-001 — Internal Deduplication Refactor for `BusinessInsights`

- **Status:** Accepted
- **Date:** 2026-09-23
- **Decision scope:** Internal implementation only
- **Baseline:** `main @ 41a9d213450a5064139c252dd77f3ee2c33c4f50` (v0.6.0)

## Context

`BusinessInsights` currently repeats the same dimension-level aggregation pattern in multiple analysis methods:

1. Group by a business dimension.
2. Aggregate `Sales` and `Profit`.
3. Derive `Profit Margin` from aggregated profit and sales.

This pattern appears across category, region, contribution, and profitability analysis. The duplication increases maintenance cost and creates unnecessary opportunities for the same calculation to diverge between methods.

A historical Phase A refactor exists at commit `15386f5`, but it is **experimental/history only** and is not the project baseline. ADR-001 therefore defines the intended refactor independently rather than treating that branch/commit as authoritative.

## Decision

Introduce **one private/internal helper** inside `BusinessInsights` for the shared dimension-level aggregation and margin calculation.

The helper will:

- accept the dataframe and the grouping dimension;
- aggregate `Sales` and `Profit` using the existing semantics;
- calculate `Profit Margin` from the aggregated values;
- return the same pandas DataFrame structure currently produced by the affected methods.

Existing public analysis methods will remain responsible for their own domain-specific outputs and additional calculations. The helper is an implementation detail, not a new public API.

## Scope

### In scope

- Deduplicate the repeated **Sales + Profit aggregation** logic.
- Deduplicate the repeated **Profit Margin** calculation that follows that aggregation.
- Reuse the helper from the affected existing methods where the semantics are identical.
- Add or update focused tests for the helper and affected methods.
- Verify regression behavior against the v0.6.0 baseline.

### Out of scope

ADR-001 does **not** change:

- public method names or signatures;
- `BusinessInsights.run()` result keys or result shape;
- narrative text generation;
- implication generation;
- contribution calculations beyond replacing their shared aggregation/margin internals;
- customer/product-specific analysis;
- pandas as the implementation dependency;
- tie-breaking behavior;
- empty-data behavior;
- zero-sales division behavior;
- NaN robustness;
- class decomposition or extraction into new modules.

These robustness concerns are intentionally deferred.

## Behavioral Contract

The refactor must preserve observable behavior for the supported v0.6.0 input domain:

- identical grouping dimensions;
- identical aggregated `Sales` and `Profit` values;
- identical `Profit Margin` values;
- identical index and column semantics for affected summary DataFrames;
- identical `idxmax()` / `idxmin()` behavior;
- identical downstream result structure;
- no changes to narrative or implication content caused solely by the refactor.

The goal is **structural deduplication, not behavioral redesign**.

## Implementation Guardrails

1. Start from the official baseline, not from `15386f5`.
2. Keep the helper private (underscore-prefixed).
3. Keep the helper narrowly scoped to the duplicated aggregation + margin pattern.
4. Do not introduce a generalized framework or decompose `BusinessInsights` into additional classes/modules.
5. Make the smallest viable change.
6. Validate with focused tests first, then the full test suite/CI.
7. Treat any output or test difference as a regression requiring investigation, not as an opportunity to expand scope.

## Consequences

### Positive

- One source of truth for repeated aggregation/margin logic.
- Lower maintenance and duplication inside `BusinessInsights`.
- Easier future changes to the shared calculation.
- Smaller and more auditable implementation than a broad refactor.

### Negative / Trade-offs

- Adds one internal abstraction that must remain narrow.
- Existing methods still contain their domain-specific analysis logic.
- Some duplicated-looking code may intentionally remain where semantics differ.

## Validation Strategy

Success requires:

1. Focused tests cover the helper's aggregation and margin behavior.
2. Existing `BusinessInsights` tests remain green.
3. Full regression suite remains green.
4. No public API/result-schema changes are observed.
5. The resulting diff is limited to the ADR/refactor/test scope defined here.

## Follow-up

Implementation and review proceed separately from this decision record:

**ADR-001 → one helper → focused tests → AI-C review → regression/CI → merge decision.**

Robustness improvements explicitly excluded above may be considered in a future ADR/change set.
