---
name: portfolio-execution
description: Convert vetted trade ideas into final account-aware execution advice by combining portfolio hedging, weekly rebalance reporting, and live IB portfolio data. Use when Codex needs to turn a filtered idea set into an executable book, weekly rebalance plan, exposure controls, or current-position-aware portfolio instructions.
---

# Portfolio Execution

Run this skill as the final portfolio layer. Take the surviving ideas, the weekly rebalance report, and the current IB portfolio, then produce final execution advice.

By default, return both a readable Markdown report and a machine-readable JSON payload. Return JSON only when the user explicitly asks for JSON only.

## Supporting Skills

Use these underlying skills when available:

- `portfolio-hedging`
- `weekly-rebalance-report`
- `ib-account-reader`

Use `weekly-rebalance-report` before final account-specific execution advice.

Use `ib-account-reader` for the final comparison against live holdings whenever the user wants current-position-aware recommendations. Otherwise work from the provided portfolio description and constraints.

## Core Outputs

Always aim to produce:

- `position_sizing`
- `hedge_overlay`
- `weekly_report_summary`
- `current_vs_target`
- `rebalance_plan`
- `exposure_summary`
- `final_recommendations`

## Non-Negotiable Rules

- Do not size positions before the idea list has passed the risk-filter layer.
- Prefer simple, explainable sizing logic over false precision.
- Run `weekly-rebalance-report` before finalizing account-level actions.
- Use live IB account data only in read-only mode.
- Keep hedge logic tied to the top-down regime and the actual book exposures.
- If live IB data is available, base the final recommendation on the gap between current holdings and the latest weekly target book.

## Workflow

### 1. Build The Weekly Rebalance View

Invoke `weekly-rebalance-report` first and extract:

- weekly summary
- rebalance priorities
- hedge posture
- monitoring focus

Treat this as the research-to-execution bridge.

### 2. Ingest Portfolio Context

Use one of these inputs:

- user-provided cash, holdings, constraints, and target exposures
- live account snapshot from `ib-account-reader`

Normalize:

- gross exposure
- net exposure
- sector concentration
- cash buffer
- max position size

### 3. Size The Positions

Convert approved candidates into target sizes.

Default rules when the user gives no formula:

- highest-conviction names get the largest weights
- event-driven trades get moderate sizing unless catalyst timing is unusually clear
- speculative squeeze trades get smaller initial sizing
- shorts are capped more tightly when borrow, crowding, or squeeze risk is high

Express sizing as percentages or dollar notional, depending on user context.

### 4. Design The Hedge Overlay

Invoke `portfolio-hedging` using the actual or intended book exposure.

Use the hedge module to define:

- hedge instrument
- hedge ratio
- expected cost or carry burden
- trigger conditions

The hedge must respond to the regime from the top-down layer and the weekly report, not exist in isolation.

### 5. Compare Current Versus Target

When live holdings are available from `ib-account-reader`, compare:

- current position
- target weight
- gap to close
- whether the name should be initiated, added, trimmed, held, or exited

If live holdings are not available, state that the plan is target-only rather than account-aware.

### 6. Build The Rebalance Plan

Produce a rebalance or implementation plan that tells the next step clearly:

- initiate
- add
- trim
- hold
- exit

When live holdings are available, compare current versus target and focus on deltas rather than restating the whole portfolio.

### 7. Write The Final Recommendation

End with a concise recommendation layer based on the current IB portfolio:

- what to keep
- what to reduce
- what to add
- what hedge adjustment to make now

This is the last-mile advice layer after the weekly report and live-position comparison.

### 8. Write An Execution Summary

Summarize:

- what the portfolio should own
- what the weekly rebalance report is prioritizing
- what size each sleeve should be
- how the book is hedged
- what should change versus the current IB holdings

## Markdown Report Contract

When the user does not explicitly request JSON only, also return a Markdown report following [templates/report_template.md](templates/report_template.md).

The Markdown report should include these sections:

- Execution Summary
- Target Book
- Current Versus Target
- Rebalance Plan
- Hedge Overlay
- Final Recommendations

Keep the Markdown concise and action-oriented.

## JSON Output Shape

Use this shape when the user wants a structured answer:

```json
{
  "position_sizing": [
    {
      "ticker": "string",
      "direction": "long|short|event_driven",
      "target_weight": "string",
      "sizing_rationale": "string"
    }
  ],
  "hedge_overlay": {
    "instrument": "string",
    "hedge_ratio": "string",
    "cost": "string",
    "trigger": "string"
  },
  "weekly_report_summary": "string",
  "exposure_summary": {
    "gross": "string",
    "net": "string",
    "sector_notes": ["string"]
  },
  "current_vs_target": [
    {
      "ticker": "string",
      "current_weight": "string",
      "target_weight": "string",
      "gap": "string",
      "suggested_action": "initiate|add|trim|hold|exit"
    }
  ],
  "rebalance_plan": [
    {
      "action": "initiate|add|trim|hold|exit",
      "ticker": "string",
      "reason": "string"
    }
  ],
  "final_recommendations": [
    "string"
  ],
  "missing_modules": ["string"]
}
```

## Quality Checklist

Before finalizing:

- Confirm the weekly rebalance report was used before final account-level actions.
- Confirm current IB holdings were compared against the target book when available.
- Confirm both Markdown and JSON were produced unless the user explicitly asked for a single format.
- Confirm the JSON is valid when JSON is requested.

## Default Operating Prompt

1. Run `weekly-rebalance-report` first to summarize the current weekly target book and priorities.
2. Take the approved ideas plus the portfolio constraints or live account snapshot.
3. Size positions based on conviction, catalyst quality, and risk concentration.
4. Use `portfolio-hedging` to add a hedge overlay that matches the book and the current regime.
5. Compare the target book with current IB holdings and return a Markdown report plus the matching structured JSON payload.