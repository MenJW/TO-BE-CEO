# Execution Plan

## Product Goal

Build an AI company operating system that can take a raw idea, simulate specialist departments, support user intervention, and return a board-reviewed execution plan.

## Phase 0: Foundation

Status: completed in this scaffold.

Deliverables:

- Stable domain model for idea intake, solution generation, review, and board decision.
- Minimal workflow pipeline covering the full company loop.
- CLI entry point for local usage.
- Repository structure prepared for future adapters and UI layers.

Exit criteria:

- A developer can run one command and generate a draft plan.
- The workflow stages are explicit and testable.

## Phase 1: Live Agent Adapters

Goal:

Replace deterministic placeholder generation with real model-backed agents.

Deliverables:

- Provider abstraction for model calls.
- Agent prompt contracts for research, department planning, review, and board roles.
- Structured output validation for every stage.

Success metrics:

- Every stage returns schema-valid output.
- Retry and fallback logic handles malformed or incomplete responses.

## Phase 2: Workflow Engine

Goal:

Move from a single in-memory pipeline to a resumable orchestration engine.

Deliverables:

- Persistent workflow state.
- Stage checkpoints and replay.
- Human intervention events that can invalidate and regenerate downstream outputs.

Success metrics:

- A user can change one assumption in the middle of the workflow.
- Only dependent stages are recomputed.

## Phase 3: Collaboration Surface

Goal:

Expose the company to the user through an interactive interface.

Deliverables:

- Web dashboard or chat console.
- Department inboxes and discussion threads.
- Plan diff view between revisions.

Success metrics:

- A user can open any stage, talk to an agent, and trigger a revision.
- Revision history remains auditable.

## Phase 4: Evaluation and Governance

Goal:

Measure whether the company produces plans that are useful, realistic, and internally consistent.

Deliverables:

- Golden test cases for different industries.
- Scoring rubric for feasibility, consistency, speed, and cost awareness.
- Safety and escalation rules for unsupported high-risk domains.

Success metrics:

- Plans score above a defined threshold on internal consistency.
- Regression testing catches workflow quality drops before release.

## Recommended Technical Sequence

1. Add LLM provider adapters behind the current pipeline interface.
2. Add persistent storage for workflow sessions and revisions.
3. Build a simple web API around the orchestrator.
4. Add frontend views for per-department review.
5. Introduce evaluation datasets and automated regression checks.

## Risk Register

- Prompt-only orchestration will become brittle without typed outputs.
- Cross-department discussion can spiral unless the workflow enforces scope.
- Full openness to user intervention requires dependency-aware recomputation.
- AGPL may reduce adoption if the intended product is a hosted SaaS platform.