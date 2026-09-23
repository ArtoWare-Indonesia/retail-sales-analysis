# ADR-004 — Dataset Reusability / Generic Schema Abstraction

- **Status:** Proposed
- **Date:** 2026-09-23
- **Baseline:** `main @ ad295bdec602fce70e0671ced2f24f826a86415c`
- **Decision Scope:** Dataset schema abstraction and reusable pipeline boundaries

## Context

The v0.6.0 pipeline is structurally healthy, but its reusable boundary is narrower than the repository positioning suggests.

The current implementation is tightly coupled to the Kaggle Superstore schema:

- `DataCleaner.REQUIRED_COLUMNS` hard-codes 13 Superstore column names.
- `DataCleaner.NUMERIC_COLUMNS` and `DATE_COLUMNS` hard-code Superstore fields.
- `BusinessMetrics` directly consumes `Sales`, `Profit`, and Superstore identifier fields.
- `BusinessInsights` directly groups by `Category`, `Region`, `Customer Name`, `Product Name`, and `Order Date`.
- `Visualizer` directly consumes Superstore dimensions and measures across multiple chart methods.
- `InteractiveVisualizer` directly consumes the same schema.
- `main.py` hard-codes the Superstore input and cleaned-output filenames.
- Existing tests primarily use Superstore-shaped fixtures and do not establish a reusable schema contract.

This means the current project is reusable as an analysis implementation for Superstore-shaped retail data, but it is not yet a dataset-agnostic retail analysis framework.

## Audit Finding

The coupling is significant enough to justify a dedicated architectural decision.

The intended target is **controlled reusability**, not arbitrary CSV compatibility.

A future dataset should be able to use the same analysis pipeline when it can be mapped to a documented canonical schema. The project should not attempt to infer arbitrary business semantics from unknown columns.

## Decision Candidate

Introduce a **canonical internal schema with an explicit dataset-to-canonical mapping boundary**.

The proposed architecture is:

```text
External Dataset
      ↓
Dataset Schema / Mapping
      ↓
Canonical Analysis DataFrame
      ↓
Cleaning / Metrics / Insights / Visualization
```

The canonical schema should represent the business concepts required by the existing analysis pipeline, while source-specific column names remain outside the analysis modules.

The abstraction should support:

1. Explicit source-column → canonical-column mapping.
2. Validation of required canonical fields before analysis.
3. Preservation of the existing v0.6.0 public analysis behavior for the Superstore dataset.
4. A clear extension point for another compatible retail dataset.
5. Tests proving that at least one alternate column naming scheme can pass through the same analysis pipeline after mapping.

## In Scope

- Canonical analysis schema definition.
- Dataset schema/mapping configuration or equivalent explicit boundary.
- Refactoring direct source-schema assumptions out of reusable analysis layers where required.
- Validation of canonical required fields.
- Updating fixtures/tests to establish the reusable schema contract.
- Preserving existing Superstore outputs and behavior.
- Documentation of supported dataset compatibility.

## Out of Scope

- Automatic semantic column inference.
- Machine-learning-based schema detection.
- Support for arbitrary non-retail datasets.
- Rewriting business metrics or insight semantics.
- New business KPIs or analysis features.
- New visualization types.
- Database ingestion.
- ETL orchestration beyond the schema boundary.
- Performance optimization unrelated to schema abstraction.
- Deployment or packaging changes.
- Changing the v0.6.0 analytical results.

## Guardrails

- Start from post-ADR-003 baseline.
- No implementation before this ADR is accepted.
- Prefer the smallest abstraction that establishes a real reusable boundary.
- Do not introduce a generic framework solely for theoretical future use.
- Superstore must remain the reference dataset and regression baseline.
- Existing tests must remain green.
- Existing analysis result keys and semantics must remain stable unless a separate ADR explicitly changes them.
- Alternate-dataset support must be demonstrated by tests, not only by documentation.

## Validation Contract

ADR-004 implementation will be considered successful only if:

1. Superstore continues to produce the existing expected results.
2. The analysis modules no longer require source-specific names outside the mapping/normalization boundary.
3. A documented canonical schema exists.
4. At least one alternate column naming scheme is mapped explicitly to the canonical schema in tests.
5. The same downstream analysis pipeline can consume the mapped data.
6. CI remains green.
7. No unrelated business logic changes are introduced.

## Risks

- Over-abstraction could make a small portfolio project unnecessarily complex.
- A canonical schema may hide dataset-specific semantic differences if mapping rules are too permissive.
- Visualization requirements may expose fields that are optional for some datasets.
- Backward compatibility may require careful handling of existing Superstore fixtures and outputs.

## Alternatives Considered

### 1. Keep the current Superstore-specific architecture

This preserves simplicity but does not materially improve dataset reusability.

### 2. Make every module accept arbitrary column names

This would spread schema configuration throughout the codebase and increase coupling rather than establish a single boundary.

### 3. Automatic column-name inference

This could make onboarding datasets appear easier, but introduces ambiguous semantic mapping and is outside the project's current scope.

### 4. Full generic analytics framework

This would provide broader reuse but is disproportionate to the current project and portfolio objective.

## Expected Outcome

The project remains a focused retail BI application while gaining a deliberate, testable reuse boundary:

```text
Dataset-specific schema
        ↓
Explicit mapping
        ↓
Canonical retail schema
        ↓
Reusable analysis pipeline
```

The ADR does **not** authorize implementation until the decision is explicitly accepted.
