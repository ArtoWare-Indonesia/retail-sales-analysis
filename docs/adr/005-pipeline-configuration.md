# ADR-005 — Pipeline Configuration & Execution Boundary

- **Status:** Proposed
- **Date:** 2026-09-23
- **Baseline:** `main @ 76cbcc12f117e4be225c8c3a197577f429132fd6`
- **Decision Scope:** Configuration-driven dataset selection, schema mapping, output paths, and pipeline orchestration

## Context

ADR-004 established a controlled dataset-reusability boundary through an explicit canonical schema and source-column mapping.

The current implementation, however, exposes that boundary primarily as a Python API. The application entry point still contains dataset- and output-specific decisions:

- `main.py` loads the Superstore dataset through `DATASET_FILE`.
- `main.py` hard-codes the cleaned output path `data/processed/superstore_clean.csv`.
- `main.py` hard-codes static visualization output to `images`.
- `main.py` hard-codes the interactive dashboard output to `output/interactive`.
- `main.py` calls `normalize_dataset(df)` without a configurable source-column mapping.
- `config.py` defines some application and dataset settings, but not the complete execution configuration.
- Using an alternate schema currently requires code-level invocation of `normalize_dataset(..., column_mapping)` rather than selecting a dataset configuration at the application boundary.

This creates a gap between **architectural reusability** and **operational reusability**.

The project can now reuse the downstream analysis pipeline after explicit mapping, but the top-level execution path remains tied to the reference Superstore setup.

## Audit Finding

The remaining coupling is primarily at the application orchestration boundary rather than inside the analysis modules.

A dedicated decision is justified if the project is expected to demonstrate that the reusable pipeline can be operated through configuration without modifying application code for each compatible dataset.

The intended target is a **small, explicit configuration boundary**, not a general workflow engine or plugin framework.

## Decision Candidate

Introduce a centralized pipeline configuration boundary that defines:

1. Input dataset path.
2. Optional source-column → canonical-column mapping.
3. Cleaned dataset output path.
4. Static visualization output directory.
5. Interactive dashboard output directory.
6. Other execution-level settings required by the pipeline.

The architecture would become:

```text
Pipeline Configuration
        ↓
Dataset Loader
        ↓
Schema Normalization
        ↓
Data Cleaning
        ↓
Business Metrics
        ↓
Business Insights
        ↓
Visualization
        ↓
Interactive Visualization
        ↓
Configured Outputs
```

The existing analysis modules should continue to operate on the canonical DataFrame and should not become responsible for configuration parsing or application-level path selection.

## In Scope

- Centralize currently hard-coded execution paths and dataset selection.
- Provide an explicit configuration representation for schema mappings.
- Make the Superstore configuration the reference/default configuration.
- Allow a compatible alternate dataset to be selected without changing analysis modules.
- Keep configuration validation separate from business-analysis logic.
- Add tests for configuration loading/validation and configured pipeline boundaries.
- Preserve existing Superstore results and output behavior.
- Update documentation to explain how a compatible dataset is configured.

## Out of Scope

- Automatic semantic column inference.
- Automatic dataset discovery.
- A plugin architecture.
- A workflow/orchestration framework.
- Database configuration or database ingestion.
- New business KPIs or analysis semantics.
- New visualization types.
- CLI redesign beyond what is minimally required to select configuration.
- Deployment configuration.
- Environment-specific infrastructure management.
- Changing the canonical schema defined by ADR-004.

## Guardrails

- Start from post-ADR-004 baseline.
- No business logic changes solely to support configuration.
- Superstore remains the reference configuration and regression baseline.
- Existing public analysis APIs remain stable unless a separate decision requires otherwise.
- Configuration must be explicit and deterministic.
- Invalid configuration must fail clearly before analysis begins.
- Do not introduce a dependency or framework disproportionate to the portfolio project's size.
- Alternate-schema support must remain explicit; configuration must not infer business meaning.
- Existing tests must remain green.

## Validation Contract

ADR-005 implementation will be considered successful only if:

1. The reference Superstore pipeline can run from the centralized configuration.
2. Dataset input and output paths are no longer hard-coded in `main.py`.
3. Schema mapping can be supplied through configuration rather than source-code changes.
4. An alternate compatible dataset can be selected through configuration and reach the same downstream analysis pipeline.
5. Invalid configuration is rejected with clear validation errors.
6. Existing Superstore analytical results remain unchanged.
7. Existing test behavior remains green and new configuration behavior is covered by tests.
8. CI remains green.
9. No unrelated business logic changes are introduced.

## Risks

- Configuration can become a second programming language if its scope grows without discipline.
- Too much configurability can make the small project harder to understand.
- Incorrect mappings may produce structurally valid but semantically incorrect analysis.
- Configuration files may become tightly coupled to implementation details.

## Alternatives Considered

### 1. Keep configuration inside `main.py`

This is simplest for the current reference dataset, but preserves the operational coupling identified by the audit.

### 2. Pass configuration through every analysis module

This would spread application concerns into reusable business-analysis components and weaken the existing separation.

### 3. Build a full workflow/configuration framework

This could support many future scenarios but would be disproportionate to the project's current scope.

### 4. Automatic schema inference

This would reduce manual configuration but would introduce ambiguous semantic decisions and conflict with the explicit-mapping boundary established by ADR-004.

## Expected Outcome

The project should have two distinct reusable boundaries:

```text
Dataset-specific source
        ↓
Explicit configuration
        ↓
Schema normalization
        ↓
Canonical retail DataFrame
        ↓
Reusable analysis pipeline
        ↓
Configured outputs
```

ADR-004 establishes **what data shape the analysis pipeline accepts**.

ADR-005 would establish **how the application selects and executes that pipeline without source-code changes**.

## Relationship to Previous ADRs

- **ADR-001:** Preserves the internal BusinessInsights refactoring boundary.
- **ADR-002:** Preserves the existing CI contract.
- **ADR-003:** Preserves documentation/version consistency.
- **ADR-004:** Builds on the canonical schema and explicit mapping boundary.
- **ADR-005:** Addresses the remaining application-level configuration and execution boundary.

## Acceptance Criteria

Before implementation begins, this ADR must be explicitly accepted. Implementation should then proceed in a separate branch and remain limited to the scope and guardrails above.