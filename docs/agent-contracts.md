# Agent Contracts

## Goal

Each department agent returns structured JSON so the orchestration layer can validate outputs, regenerate specific stages, diff versions, and support direct chat without parsing brittle free-form prose.

## Department Solution Contract

Each department planning agent returns:

```json
{
  "solutions": [
    {
      "name": "string",
      "summary": "string",
      "feasibility_score": 1,
      "dependencies": ["hardware", "design"],
      "assumptions": ["string"],
      "rationale": "string",
      "implementation_steps": ["string"],
      "success_metrics": ["string"]
    }
  ]
}
```

## Research Contract

```json
{
  "customer_segments": ["string"],
  "market_size_view": "string",
  "competitive_landscape": "string",
  "key_risks": ["string"],
  "recommendation": "string"
}
```

## Board Contract

```json
{
  "approved": true,
  "development_difficulty": "string",
  "budget_outlook": "string",
  "funding_cycle": "string",
  "rationale": "string",
  "conditions": ["string"]
}
```

## Chat Contract

```json
{
  "reply": "string",
  "follow_up_questions": ["string"],
  "updated_assumptions": ["string"]
}
```