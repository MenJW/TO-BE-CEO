# Baseline Comparison

This document answers the question the project will always be asked:

Why not just ask a single LLM directly?

## Comparison Setup

Use the same idea brief in two modes:

1. Direct prompt baseline: one request to a single LLM asking for feasibility analysis.
2. Company workflow: research, departments, board decision, scorecard, timeline, revision history, and intervention loop.

## Example Idea

- Idea: AI interview coach for new graduates
- Constraints: launch an MVP in one month, start with Chinese users, validate willingness to pay early
- Success metrics: 7-day retention, paid conversion, completed mock interviews

## Expected Output Difference

| Dimension | Direct prompt | Company workflow |
| --- | --- | --- |
| Structure | Usually one long answer | Typed stages and explicit artifacts |
| Cross-functional coverage | Often uneven | Research, design, software, marketing, finance all present |
| Decision quality | Advice only | Go/Maybe/No-Go plus conditions |
| Traceability | Weak | Timeline, versions, diff, stored interventions |
| Human override | Manual reprompting | Promote a chat turn into a formal intervention |
| Auditability | Low | SQLite-backed state and version history |

## What To Measure

Use the rubric in docs/evaluation-rubric.md and score both modes on:

1. Output completeness
2. Internal consistency
3. Actionability
4. Cross-functional realism
5. Revision transparency

## Why The Workflow Should Win

The company workflow is not trying to beat a direct prompt on raw creativity. It should win on:

- more explicit assumptions,
- better departmental coverage,
- clearer board-level decision output,
- better change tracking after user intervention,
- higher trust because the reasoning surface is inspectable.

## Recommended Demo Format

For README, video, or presentation use this sequence:

1. Show a direct prompt answer for the same idea.
2. Show the company workflow result.
3. Highlight the missing pieces in the direct answer.
4. Trigger an intervention and show a version diff.

That sequence makes the differentiation concrete instead of rhetorical.