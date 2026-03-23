---
name: daily-alpha-pipeline
description: Orchestrate the full end-to-end portfolio workflow by combining the four upper-layer engines: top-down-alpha-engine, idea-generation-engine, risk-filter-layer, and portfolio-execution. Use when Codex should run the complete daily process from macro regime to idea generation to risk filtering to weekly-and-IB-aware execution advice in one pass.
---

# Daily Alpha Pipeline

Run this skill as the master end-to-end orchestrator. It should not bypass the upper-layer engines unless one is unavailable. The job of this skill is to sequence the four layers, pass context from one layer to the next, and return one integrated daily portfolio output.

Return only valid JSON when the user asks for the pipeline output itself.

## Required Inputs

Accept the user's universe, region, date, liquidity floor, portfolio constraints, and account-awareness preference when provided. If omitted, assume:

- US-listed liquid equities
- holding period of several days to several weeks
- exactly 3 long ideas and 2 short ideas unless the user specifies otherwise
- modest net exposure with an explicit hedge overlay
- live IB comparison is desired when `ib-account-reader` is available

## Supporting Skills

Prefer these upper-layer skills and run them in this order:

- `top-down-alpha-engine`
- `idea-generation-engine`
- `risk-filter-layer`
- `portfolio-execution`

`portfolio-execution` is expected to use:

- `portfolio-hedging`
- `weekly-rebalance-report`
- `ib-account-reader`

If an upper-layer skill is unavailable, do not silently drop the layer. Record the missing module, continue with the remaining layers where possible, and reduce confidence.

## Freshness And Source Aggregation Policy

- Always rerun the four upper-layer engines against the latest available data at run time.
- Do not reuse cached JSON outputs, stale daily notes, or old weekly summaries as the current source of truth.
- Re-check the current source stack every run.
- Preserve each layer's Tier 1 and Tier 2 source discipline rather than replacing it with generic summaries.

## Non-Negotiable Rules

- Run the layers strictly in sequence: top-down, idea generation, risk filter, execution.
- Do not let idea generation override the top-down regime; use the regime as the context for downstream decisions.
- Do not let execution bypass the risk-filter layer.
- Prefer names confirmed by multiple underlying signals and still approved by the filter layer.
- Base the final recommendation on the latest weekly rebalance view and, when available, the current IB portfolio.
- Use `"unknown"` instead of fabricating facts.

## Workflow

### 1. Run The Top-Down Layer

Invoke `top-down-alpha-engine` first and extract:

- `regime`
- `risk_posture`
- `sector_priority`
- `top_down_playbook`

Treat this as the portfolio context for the rest of the run.

### 2. Run The Idea Layer

Invoke `idea-generation-engine` using the latest top-down context.

Extract:

- `long_ideas`
- `short_ideas`
- `event_driven_trades`
- `debate_summary`
- `cross_signal_alignment`

Use the top-down regime to prefer ideas that fit the environment.

### 3. Run The Risk Filter Layer

Invoke `risk-filter-layer` on the idea layer output.

Extract:

- `approved_candidates`
- `rejected_candidates`
- `smart_money_follow_list`
- `risk_flags`

This is the investable gate. Only approved or watch-level names should reach execution.

### 4. Run The Execution Layer

Invoke `portfolio-execution` using:

- the approved candidate set
- the top-down regime context
- the latest hedge posture
- live IB holdings when available

Extract:

- `position_sizing`
- `hedge_overlay`
- `weekly_report_summary`
- `current_vs_target`
- `rebalance_plan`
- `final_recommendations`

### 5. Produce The Daily End-To-End Output

Return one integrated portfolio object that preserves the four-layer structure while remaining concise enough to act on.

The final output should make it obvious:

- what the regime is
- what the best long, short, and event-driven ideas are
- what survived risk filtering
- what the target book is
- how the hedge is structured
- what the current IB portfolio should change today

## Preferred Output Shape

Use this shape when the user wants a structured answer:

```json
{
  "top_down": {
    "regime": "string",
    "risk_posture": "string",
    "sector_priority": {
      "overweight": ["string"],
      "neutral": ["string"],
      "avoid": ["string"]
    },
    "playbook": {
      "prioritize": ["string"],
      "de_emphasize": ["string"],
      "invalidate_if": ["string"]
    }
  },
  "idea_generation": {
    "long_ideas": [],
    "short_ideas": [],
    "event_driven_trades": [],
    "debate_summary": []
  },
  "risk_filter": {
    "approved_candidates": [],
    "rejected_candidates": [],
    "risk_flags": []
  },
  "execution": {
    "weekly_report_summary": "string",
    "position_sizing": [],
    "hedge_overlay": {},
    "current_vs_target": [],
    "rebalance_plan": [],
    "final_recommendations": []
  },
  "confidence": "low|medium|high|unknown",
  "missing_modules": ["string"],
  "sources": []
}
```

## Quality Checklist

Before finalizing:

- Confirm all four upper-layer engines were attempted in order.
- Confirm the idea layer used the top-down layer as context.
- Confirm the risk filter gated what reached execution.
- Confirm execution includes weekly rebalance logic and IB-aware comparison when available.
- Confirm missing layers or unresolved conflicts appear in `missing_modules` or `risk_flags`.
- Confirm the final output is valid JSON when JSON is requested.

## Default Operating Prompt

1. Run `top-down-alpha-engine` to classify the market regime and sector priorities.
2. Run `idea-generation-engine` to produce long, short, and event-driven ideas under that regime.
3. Run `risk-filter-layer` to remove weak names and surface the investable set.
4. Run `portfolio-execution` to turn the filtered set into weekly-and-IB-aware execution advice.
5. Return one integrated end-to-end daily portfolio output.