# Intelligent Brain Company

Intelligent Brain Company is an AI startup simulator: you submit one idea, an AI company evaluates it through research, departments, and board review, and you get a structured go or no-go plan instead of a single chat reply.

This repository is now usable as a demo product rather than only a concept scaffold. It includes a web console, SQLite-backed project history, plan version diff, direct chat with departments, and a promote-to-intervention loop that turns a conversation turn into a formal change request and triggers recomputation.

Research, board, and department stages can call a real OpenAI-compatible endpoint when configured. Without credentials, the app falls back to deterministic local generation so the full loop still runs end to end.

Hardware, software, design, marketing, and finance outputs are generated against explicit JSON contracts, so the result is closer to a cross-functional planning board than a loose role-play prompt.

## What You See In 30 Seconds

Input:

- One startup or product idea.
- A few constraints such as budget, launch speed, or target market.

Workflow:

1. Research evaluates demand, competition, and risk.
2. Departments propose concrete options with structured artifacts.
3. The board returns a recommendation and conditions.
4. You can chat with any role and promote a message into a formal intervention.

Output:

- A Go, Maybe, or No-Go verdict.
- A five-dimension scorecard: market demand, technical feasibility, execution complexity, time to MVP, monetization potential.
- Department plans with artifacts such as BOM targets, software boundaries, design constraints, channel budget, and capital envelope.
- Timeline, revision history, and markdown diff between plan versions.

## Why This Is Different From A Normal LLM Chat

- It keeps project state instead of producing one-off replies.
- It separates research, departments, and board review into explicit stages.
- It supports human intervention in the middle of the workflow, then recomputes downstream outputs.
- It stores versions, chat turns, and timeline events in SQLite so the demo remains auditable.

## Why This Project

Most multi-agent projects stop at role-playing or software-only collaboration. Your idea is stronger than that: it treats AI agents as a company with explicit departments, governance, review loops, and human intervention at any stage.

The core product thesis is:

1. A user submits an idea.
2. A research team evaluates feasibility, market demand, competition, and risk.
3. Each department generates several viable solution options.
4. Cross-functional roundtables review dependencies and tradeoffs.
5. The best departmental options are merged into one integrated plan.
6. A board-level review decides whether to proceed and under what constraints.
7. The user can intervene at any stage and change the outcome.

## MVP Scope

The current build focuses on the smallest useful end-to-end slice that a new user can understand and try immediately:

- Domain objects for ideas, solutions, reviews, board decisions, and user interventions.
- A company pipeline that simulates the full planning process.
- Department registry for research, hardware, software, design, marketing, and finance.
- Structured JSON contracts for department solution generation.
- A CLI command that turns an idea into a structured draft plan.
- A Flask API for creating projects, generating plans, chatting with roles, and recording interventions.
- A chat API and console panel for direct conversation with research, board, and department agents.
- A verdict scorecard with Go, Maybe, or No-Go output.
- SQLite-backed persistence for project state, task history, versions, and chat records.
- Documentation for execution roadmap and license strategy.

This is intentionally framework-light. The current implementation keeps orchestration logic independent so that you can later plug in AutoGen, CrewAI, LangGraph, Semantic Kernel, or custom model routing without rewriting the business workflow.

## Repository Structure

```text
.
├── docs/
│   ├── architecture.md
│   ├── baseline-comparison.md
│   ├── deployment.md
│   ├── execution-plan.md
│   ├── evaluation-rubric.md
│   ├── github-metadata.md
│   └── license-strategy.md
├── examples/
│   └── demo_cases/
│       ├── ai-interview-coach.md
│       ├── campus-secondhand-marketplace.md
│       ├── crossborder-product-selection.md
│       └── README.md
├── render.yaml
├── src/
│   └── intelligent_brain_company/
│       ├── api/
│       │   ├── planning.py
│       │   └── projects.py
│       ├── agents/
│       │   ├── contracts.py
│       │   ├── registry.py
│       │   └── runtime.py
│       ├── app.py
│       ├── config.py
│       ├── domain/
│       │   ├── models.py
│       │   └── project_state.py
│       ├── interfaces/
│       │   └── cli.py
│       ├── services/
│       │   ├── llm_client.py
│       │   ├── planning.py
│       │   ├── project_store.py
│       │   └── task_store.py
│       ├── wsgi.py
│       ├── workflows/
│       │   └── pipeline.py
│       └── __init__.py
├── tests/
│   ├── test_api.py
│   └── test_pipeline.py
└── pyproject.toml
```

## Quick Start

```bash
python -m pip install -e .
ibc-plan "Build an electric tricycle" --constraint "Target price below 18000 CNY" --constraint "Designed for short-distance cargo delivery"
```

The CLI currently generates a deterministic planning draft. In the next stage, the deterministic steps can be replaced by live agents and model-backed discussion loops.

### API Mode

```bash
python -m pip install -e .[dev]
ibc-api
```

Example flow:

1. POST /api/projects to create a project.
2. POST /api/planning/generate to generate the first plan version.
3. POST /api/planning/interventions to insert user feedback and regenerate.
4. GET /api/projects/<project_id> to inspect the stored state.
5. POST /api/projects/<project_id>/chat to talk to research, board, or a department.
6. POST /api/projects/<project_id>/chat/promote to turn a chat turn into a formal intervention and trigger regeneration.

Open the control surface at http://127.0.0.1:8000 to create projects, view plans, inspect timeline and progress, and submit interventions.

The console also exposes:

- three one-click demo startup ideas for a fast first run,
- a verdict scorecard for immediate Go or No-Go comprehension,
- a conversation panel where you can directly talk to research, board, hardware, software, design, marketing, or finance,
- a one-click path from chat turn to formal intervention and recomputed plan version.

## Demo Ideas

The built-in console presets are designed to make the product legible within a minute:

1. AI interview coach for new graduates.
2. Cross-border ecommerce product selection assistant.
3. Campus second-hand marketplace.

These presets are meant to show the full product loop fast: create project, generate plan, inspect scorecard, question a department, promote a chat turn, and compare versions.

## Docs And Assets

- Deployment: docs/deployment.md
- Baseline comparison: docs/baseline-comparison.md
- Evaluation rubric: docs/evaluation-rubric.md
- Architecture: docs/architecture.md
- GitHub metadata: docs/github-metadata.md
- Demo cases: examples/demo_cases/

If you want live LLM-backed research, board, and department reviews, set these environment variables before starting the API:

```bash
IBC_LLM_API_KEY=your_key
IBC_LLM_BASE_URL=https://your-openai-compatible-endpoint/v1
IBC_LLM_MODEL=your-model-name
```

## Architecture Direction

The architecture is split into four layers:

1. Domain layer: stable business objects and workflow states.
2. Workflow layer: company operating process and handoffs.
3. Service layer: orchestration entry points and future provider adapters.
4. Interface layer: CLI plus HTTP API first, web and chat surfaces later.

That split matters because the long-term moat is not individual prompts. It is the operating model of the AI company: state, review rules, escalation logic, and human-in-the-loop control.

## Recommended Next Milestones

1. Replace deterministic department outputs with live agent adapters.
2. Add persistence for sessions, interventions, and plan revisions.
3. Build a node-based workflow engine with resumable checkpoints.
4. Add a web console for department conversations and board review.
5. Add evaluation datasets for plan quality, consistency, and cost realism.

## License Note

This repository now uses Apache-2.0.

That aligns the codebase with a permissive adoption strategy: easier commercial collaboration, fewer contributor onboarding hurdles, and cleaner integration into enterprise stacks. The rationale and historical tradeoff note remain in docs/license-strategy.md.
