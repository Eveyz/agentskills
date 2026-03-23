---
name: top-down-alpha-engine
description: Orchestrate top-down market regime analysis by combining macro regime work and cross-asset correlation mapping. Use when Codex needs to turn news, fundamentals, and market data into a regime label, risk-on or risk-off posture, sector priorities, and a top-down playbook before stock selection or portfolio construction.
---

# Top-Down Alpha Engine

Run this skill as the macro orchestration layer. Start with the economic regime, then pressure-test it through cross-asset behavior, and finish with a compact top-down map that downstream idea, risk, and execution skills can consume.

## Supporting Skills

Use these underlying skills when available:

- `macro_top_down_analysis`
- `correlation-anomaly`

If one skill is unavailable, continue with the other, explicitly record the missing module, and reduce confidence.

## Core Outputs

Always produce these outputs in plain language or structured form requested by the user:

- `regime`
- `risk_posture`
- `sector_priority`
- `macro_drivers`
- `cross_asset_signals`
- `top_down_playbook`

Minimum meaning:

- `regime`: concise economic-cycle label
- `risk_posture`: `risk_on`, `balanced`, `risk_off`, or `event_driven_mixed`
- `sector_priority`: sectors or factors to favor, neutralize, or avoid

## Non-Negotiable Rules

- Run `macro_top_down_analysis` first.
- Use `correlation-anomaly` as a validation and refinement layer, not as a substitute for macro analysis.
- Separate verified observations from interpretation.
- If the two modules conflict, keep the disagreement visible and downgrade confidence rather than forcing a false consensus.
- Prefer recent news and market evidence because regime classification can change quickly.

## Workflow

### 1. Build The Macro Base Case

Invoke `macro_top_down_analysis` and extract:

- inflation trend
- rate trend
- liquidity condition
- growth regime
- regime label
- trade implications

Translate that output into a working stance:

- `risk_on`
- `balanced`
- `risk_off`
- `event_driven_mixed`

### 2. Cross-Check With Correlation Behavior

Invoke `correlation-anomaly` to test whether live cross-asset behavior confirms or challenges the macro base case.

Focus on:

- stocks versus gold
- bonds versus equities
- any clear regime-break signal

Use the result to answer:

- Is the market behaving consistently with the macro narrative
- Is liquidity stress rising
- Is inflation repricing overpowering growth signals

### 3. Resolve The Top-Down View

Combine the two modules into one top-down judgment:

- If both agree, raise conviction.
- If macro is benign but cross-asset behavior looks stressed, cap conviction and flag fragility.
- If macro is mixed and correlations are unstable, prefer a cautious or event-driven posture.

### 4. Derive Sector Priorities

Map the regime into sector and factor preferences.

Typical mapping:

- disinflation plus easing or soft landing: favor quality growth and cyclicals with earnings support
- sticky inflation plus restrictive policy: favor defensives, cash-generative value, and selective commodities
- liquidity stress: reduce speculative beta and crowded factor exposure
- reflation: favor cyclicals, industrials, energy, and selected financials

Do not treat this mapping as mechanical when the underlying evidence says otherwise.

### 5. Produce A Downstream Playbook

Return a compact playbook that later layers can use:

- which idea types to prioritize
- which sectors to search first
- which exposures to avoid or underweight
- what could invalidate the current regime call

## Preferred Output Shape

Use this shape when the user wants a structured answer:

```json
{
  "regime": "string",
  "risk_posture": "risk_on|balanced|risk_off|event_driven_mixed|unknown",
  "macro_drivers": [
    "string"
  ],
  "cross_asset_signals": [
    "string"
  ],
  "sector_priority": {
    "overweight": ["string"],
    "neutral": ["string"],
    "avoid": ["string"]
  },
  "top_down_playbook": {
    "prioritize": ["string"],
    "de_emphasize": ["string"],
    "invalidate_if": ["string"]
  },
  "confidence": "low|medium|high",
  "missing_modules": ["string"]
}
```

## Default Operating Prompt

1. Run `macro_top_down_analysis` first and classify the current regime.
2. Run `correlation-anomaly` to confirm or challenge the macro base case using recent cross-asset behavior.
3. Resolve the combined view into a single risk posture and sector-priority map.
4. Return a concise top-down playbook that later alpha, risk, and execution layers can use.
