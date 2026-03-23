---
name: portfolio-execution
description: Convert vetted trade ideas into position sizing, hedge overlays, and rebalance actions by combining portfolio hedging and reporting or implementation steps. Use when Codex needs to turn a filtered idea set into an executable book, weekly rebalance plan, exposure controls, or portfolio instructions.
---

# Portfolio Execution

Run this skill as the final portfolio layer. Take the surviving ideas, size them, define hedge overlays, and produce an execution-ready rebalance plan.

## Supporting Skills

Use these underlying skills when available:

- `portfolio-hedging`
- `ib-account-reader`

Use `ib-account-reader` only when the user wants live account-aware sizing or exposure checks. Otherwise work from the provided portfolio description and constraints.

## Core Outputs

Always aim to produce:

- `position_sizing`
- `hedge_overlay`
- `rebalance_plan`
- `exposure_summary`

## Non-Negotiable Rules

- Do not size positions before the idea list has passed the risk-filter layer.
- Prefer simple, explainable sizing logic over false precision.
- Use live IB account data only in read-only mode.
- Keep hedge logic tied to the top-down regime and the actual book exposures.

## Workflow

### 1. Ingest Portfolio Context

Use one of these inputs:

- user-provided cash, holdings, constraints, and target exposures
- live account snapshot from `ib-account-reader`

Normalize:

- gross exposure
- net exposure
- sector concentration
- cash buffer
- max position size

### 2. Size The Positions

Convert approved candidates into target sizes.

Default rules when the user gives no formula:

- highest-conviction names get the largest weights
- event-driven trades get moderate sizing unless catalyst timing is unusually clear
- speculative squeeze trades get smaller initial sizing
- shorts are capped more tightly when borrow, crowding, or squeeze risk is high

Express sizing as percentages or dollar notional, depending on user context.

### 3. Design The Hedge Overlay

Invoke `portfolio-hedging` using the actual or intended book exposure.

Use the hedge module to define:

- hedge instrument
- hedge ratio
- expected cost or carry burden
- trigger conditions

The hedge must respond to the regime from the top-down layer, not exist in isolation.

### 4. Build The Rebalance Plan

Produce a rebalance or implementation plan that tells the next step clearly:

- initiate
- add
- trim
- hold
- exit

When live holdings are available, compare current versus target and focus on deltas rather than restating the whole portfolio.

### 5. Write An Execution Summary

Summarize:

- what the portfolio should own
- what size each sleeve should be
- how the book is hedged
- what should change at the next weekly rebalance checkpoint

## Preferred Output Shape

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
  "exposure_summary": {
    "gross": "string",
    "net": "string",
    "sector_notes": ["string"]
  },
  "rebalance_plan": [
    {
      "action": "initiate|add|trim|hold|exit",
      "ticker": "string",
      "reason": "string"
    }
  ],
  "missing_modules": ["string"]
}
```

## Default Operating Prompt

1. Take the approved ideas and the portfolio constraints or live account snapshot.
2. Size positions based on conviction, catalyst quality, and risk concentration.
3. Use `portfolio-hedging` to add a hedge overlay that matches the book and the current regime.
4. Return an execution-ready rebalance plan with weights, hedge, and weekly checkpoint actions.
