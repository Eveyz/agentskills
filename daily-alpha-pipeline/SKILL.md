---
name: daily-alpha-pipeline
description: Orchestrate a daily hedge-fund portfolio workflow that runs macro regime analysis first, dynamically reweights downstream signals by regime, combines insider buying, short squeeze, M&A, sentiment, correlation, dividend, hedge-fund positioning, and hedging modules, cross-validates ideas on the same ticker, filters trades that conflict with the macro backdrop, and returns a strict portfolio report. Use when Codex needs to build a daily long-short book, daily alpha report, hedge overlay, or master investment pipeline from multiple sub-skills.
---

# Daily Alpha Pipeline

Run this skill as the master orchestrator for a hedge fund portfolio manager workflow. Start top-down, merge bottom-up signals, remove ideas that do not survive regime and risk checks, then return one strict JSON object matching [templates/output_schema.json](templates/output_schema.json).

Return only valid JSON when the user asks for the pipeline output itself.

## Required Inputs

Accept the user's universe, region, date, liquidity floor, and risk constraints when provided. If omitted, assume:

- US-listed liquid equities
- Holding period of several days to several weeks
- Exactly 3 long ideas and 2 short ideas
- Modest net exposure with an explicit hedge overlay

## Supporting Skills

Prefer these sub-skills when available:

- `macro_top_down_analysis`
- `insider_buying_detector`
- `short_squeeze_scanner`
- `mna_radar`
- `sentiment_vs_fundamental`
- `correlation_anomaly`
- `dividend_risk`
- `hedge_fund_positioning`
- `portfolio_hedging`

If a sub-skill is unavailable, do not invent its findings. Continue with the available evidence, record the missing module in `risk_flags`, and reduce confidence.

## Non-Negotiable Rules

- Run `macro_top_down_analysis` before any portfolio selection.
- Use the macro regime as a hard gating layer for trade selection and sizing logic.
- Run all four primary signal generators when available: insider, squeeze, M&A, and sentiment.
- Prefer names confirmed by multiple independent signals on the same ticker.
- Remove trades that directly conflict with the macro regime unless a hard idiosyncratic catalyst clearly dominates.
- In risk-off regimes, penalize speculative longs and weak balance sheets.
- In risk-on regimes, allow higher-beta ideas but still screen for crowding, squeeze reversal risk, and catalyst quality.
- Keep the final book to exactly 3 longs and 2 shorts unless the user explicitly requests a different shape.
- Use `"unknown"` instead of fabricating facts.

## Workflow

### 1. Run Macro Analysis

Invoke `macro_top_down_analysis` first and extract:

- Macro regime label
- Risk-on, balanced, risk-off, or event-driven mixed posture
- Growth, liquidity, and policy direction
- High-level sector and factor implications

Translate the macro output into one of these working stances:

- `risk_on`
- `balanced`
- `risk_off`
- `event_driven_mixed`

Set `macro_regime` to the regime label from the macro module, or `"unknown"` if it cannot be verified.

### 2. Apply Regime-Based Weights

Use the working stance to dynamically weight downstream evidence before ranking ideas.

Weighting rules:

- `risk_on`: overweight `sentiment_vs_fundamental` and `short_squeeze_scanner`
- `risk_off`: overweight `dividend_risk` and `portfolio_hedging`
- `balanced`: keep signal families closer to equal weight
- `event_driven_mixed`: emphasize idiosyncratic event signals and reduce broad factor exposure

Use these weights to break ties, prioritize research effort, and explain confidence. Do not let weighting override hard disqualifiers such as severe macro conflict, unmanageable crowding, or obvious event risk.

### 3. Run Signal-Generating Skills

Run these primary idea generators when available:

- `insider_buying_detector`
- `short_squeeze_scanner`
- `mna_radar`
- `sentiment_vs_fundamental`

Use these secondary validators and risk modules where helpful:

- `correlation_anomaly`
- `dividend_risk`
- `hedge_fund_positioning`

Use `portfolio_hedging` during portfolio construction rather than as a primary alpha source.

For each surfaced ticker, maintain a working record with:

- `ticker`
- `direction`
- `signal_types`
- `reason`
- `entry`
- `confidence`
- `macro_fit`
- `risk_notes`

Direction defaults:

- Insider buying usually starts as `long`
- Short squeeze setups usually support a `long` or invalidate a `short`
- M&A target or strategic optionality usually starts as `long`
- Sentiment detached from weakening fundamentals usually starts as `short`
- Dividend risk usually supports a `short` or blocks a `long`

### 4. Cross-Validate Signals

Check whether multiple signals align on the same ticker.

Upgrade conviction when a ticker is supported by at least 2 independent dimensions such as:

- Event flow
- Positioning or crowding
- Sentiment versus fundamentals
- Macro alignment
- Correlation anomaly or relative-value dislocation

Conviction rubric:

- `high`: 3 or more aligned dimensions with no major contradiction
- `medium`: 2 aligned dimensions with manageable risks
- `low`: 1 signal only, conflicting evidence, or missing validation

Prefer names with multi-signal alignment when building the final book.

### 5. Apply Risk Filtering

Remove or downgrade ideas that conflict with the macro regime.

Examples:

- In `risk_off`, reject speculative squeeze-only longs unless there is an additional hard catalyst.
- In `risk_off`, prefer resilient cash flow, defensives, or event-backed longs.
- In `risk_on`, allow cyclical or sentiment-driven longs, but reject crowded shorts exposed to squeeze risk.
- In `event_driven_mixed`, favor idiosyncratic M&A, insider, and dislocation setups over broad beta trades.

Always filter for:

- Severe macro conflict
- Excess crowding
- Near-term dividend or financing risk
- Takeover risk that can blow up a short
- Hedge mismatch at the portfolio level

Record every unresolved issue in `risk_flags`.

### 6. Construct Portfolio

Build:

- `top_longs`: exactly 3 ideas
- `top_shorts`: exactly 2 ideas
- `hedge`: one overlay that offsets the dominant book risk

Rank candidates by:

1. Cross-validation quality
2. Macro fit
3. Catalyst clarity
4. Risk-reward asymmetry
5. Liquidity and implementability

Each selected idea must contain:

- `ticker`
- `reason`
- `entry`
- `confidence`

Use concise but specific rationale. `entry` can be a setup description such as `"accumulate on pullbacks while catalyst remains intact"` when precise price data is unavailable.

### 7. Output Final Report

Return strict JSON matching [templates/output_schema.json](templates/output_schema.json).

Required fields:

- `macro_regime`
- `top_longs`
- `top_shorts`
- `hedge`
- `risk_flags`
- `weekly_focus`
- `sources`

`weekly_focus` should summarize the one portfolio theme or monitoring priority that matters most over the next week.

`sources` should include the supporting URLs, source titles when known, and sub-skill outputs or source references used to justify the report. If exact metadata is unavailable, include the URL or module name and use `"unknown"` for missing fields.

## Output Contract

Use this shape exactly:

```json
{
  "macro_regime": "unknown",
  "top_longs": [
    {
      "ticker": "unknown",
      "reason": "unknown",
      "entry": "unknown",
      "confidence": "low|medium|high|unknown"
    }
  ],
  "top_shorts": [
    {
      "ticker": "unknown",
      "reason": "unknown",
      "entry": "unknown",
      "confidence": "low|medium|high|unknown"
    }
  ],
  "hedge": {
    "type": "unknown",
    "target_exposure": "unknown",
    "rationale": "unknown"
  },
  "risk_flags": [],
  "weekly_focus": "unknown",
  "sources": []
}
```

## Quality Checklist

Before finalizing:

- Confirm `macro_top_down_analysis` ran first or was explicitly unavailable
- Confirm the regime-weighting logic influenced prioritization
- Confirm all four primary signal generators were attempted when available
- Confirm the final book has exactly 3 longs and 2 shorts unless the user changed it
- Confirm every selected name survived cross-validation and risk filtering
- Confirm the hedge offsets the portfolio's dominant beta, sector, or factor risk
- Confirm missing modules and unresolved contradictions appear in `risk_flags`
- Confirm the final answer is valid JSON with no markdown wrapper when output is requested

## Default Operating Prompt

1. Run `macro_top_down_analysis` and classify the regime.
2. Dynamically reweight downstream evidence based on the regime.
3. Run insider, squeeze, M&A, and sentiment modules.
4. Cross-validate overlapping signals on the same ticker.
5. Remove trades that conflict with the macro regime or fail risk checks.
6. Build exactly 3 long ideas, 2 short ideas, and one hedge overlay.
7. Return strict JSON only.
