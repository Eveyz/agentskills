---
name: weekly-rebalance-report
description: Produce a weekly rebalance report by summarizing the latest macro, idea, risk, and hedge conclusions into a decision-ready weekly portfolio memo. Use when Codex needs a weekly portfolio report, weekly monitoring priorities, a rebalance checklist, or a bridge between research output and final execution advice.
---

# Weekly Rebalance Report

Run this skill after the top-down, idea, risk, and hedge layers have produced updated views. Turn those outputs into a compact weekly report that can be compared against the current IB portfolio before final execution advice is generated.

## Supporting Skills

Use these underlying skills when available:

- `top-down-alpha-engine`
- `idea-generation-engine`
- `risk-filter-layer`
- `portfolio-hedging`

If one or more modules are missing, continue with the available evidence, list the missing modules, and reduce confidence.

## Freshness And Cache Policy

- Always use the latest available upstream outputs at report time.
- Do not reuse last week's memo, cached JSON, or stale rebalance notes as the current report.
- Re-check the latest source-backed conclusions every time before publishing the report.

## Core Outputs

Always aim to produce:

- `weekly_summary`
- `rebalance_priorities`
- `watchlist_changes`
- `hedge_posture`
- `weekly_risks`
- `monitoring_focus`

## Non-Negotiable Rules

- Treat the report as a decision document, not as a dump of raw research.
- Keep the report aligned with the latest regime view and approved idea list.
- Flag what changed since the last cycle when that information is available.
- Keep uncertainty visible when an upstream layer is missing or conflicted.

## Workflow

### 1. Gather The Latest Upstream Conclusions

Collect the most recent outputs from:

- top-down regime analysis
- idea generation
- risk filtering
- hedging design

Extract the few conclusions that matter most for the next rebalance window.

### 2. Summarize What Changed

Write the weekly summary around:

- regime or risk-posture shifts
- newly approved or newly rejected ideas
- hedge changes
- new concentration or event risks

Prefer deltas over repetition.

### 3. Build The Rebalance Priorities

Turn the latest research into explicit weekly actions such as:

- increase exposure to a sleeve
- reduce or exit a name
- keep exposure unchanged
- add or adjust a hedge

These are report-level priorities, not yet account-specific order suggestions.

### 4. Set Monitoring Focus

State the one to three things that matter most before the next rebalance, such as:

- a macro release
- earnings clusters
- short-interest update
- activist or deal news
- hedge trigger conditions

### 5. Hand Off To Execution

Make the report easy for `portfolio-execution` to compare against current IB holdings.

The handoff should make it obvious:

- what the target book wants to own
- what should be smaller or zero
- how the hedge posture should look over the next week

## Preferred Output Shape

Use this shape when the user wants a structured answer:

```json
{
  "weekly_summary": "string",
  "rebalance_priorities": [
    {
      "action": "increase|reduce|hold|watch|hedge",
      "target": "string",
      "reason": "string"
    }
  ],
  "watchlist_changes": {
    "added": ["string"],
    "removed": ["string"],
    "high_priority": ["string"]
  },
  "hedge_posture": {
    "stance": "string",
    "notes": ["string"]
  },
  "weekly_risks": ["string"],
  "monitoring_focus": ["string"],
  "missing_modules": ["string"]
}
```

## Default Operating Prompt

1. Gather the latest top-down, idea, risk, and hedge conclusions.
2. Write a weekly rebalance report focused on what changed and what matters next.
3. Produce explicit rebalance priorities and monitoring focus for the coming week.
4. Hand the report off in a form that `portfolio-execution` can compare against current IB positions.