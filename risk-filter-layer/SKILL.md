---
name: risk-filter-layer
description: Filter and refine candidate trades by combining dividend-trap detection and hedge-fund positioning analysis. Use when Codex needs to remove low-quality names, follow smart-money evidence, validate or reject trade candidates, and convert raw ideas into a cleaner investable list.
---

# Risk Filter Layer

Run this skill after idea generation and before portfolio construction. Use it to remove fragile names, downgrade low-quality setups, and upgrade candidates supported by smart-money positioning or balance-sheet resilience.

## Supporting Skills

Use these underlying skills when available:

- `dividend-risk`
- `hedge-fund-positioning`

If a module is unavailable, continue with the remaining module, make the limitation explicit, and avoid overstating certainty.

## Core Outputs

Always aim to produce:

- `approved_candidates`
- `rejected_candidates`
- `smart_money_follow_list`
- `risk_flags`

## Filtering Logic

This layer does two jobs:

1. Remove or downgrade structurally weak names.
2. Identify where institutional positioning strengthens the case.

Do not blindly copy hedge funds. Treat 13F support as a confidence input, not a substitute for thesis quality.

## Workflow

### 1. Start From The Candidate Set

Accept a candidate list from the user or from the idea-generation layer.

For each name, keep:

- `ticker`
- `direction`
- `thesis`
- `source_modules`

### 2. Run Dividend-Risk Checks

Invoke `dividend-risk` when a candidate has any of these features:

- high stated yield
- value-trap concerns
- stressed balance sheet
- income-oriented long thesis

Use the result to:

- reject likely dividend traps from long books
- support shorts where the risk of a dividend cut or funding strain is material
- flag weak free-cash-flow coverage or leverage pressure even when yield is not the entire thesis

### 3. Run Hedge-Fund Positioning Checks

Invoke `hedge-fund-positioning` to determine whether the latest 13F cycle shows:

- new smart-money ownership
- repeated increases by major funds
- repeated exits that weaken the case
- sector-level institutional rotation

Use this to:

- raise confidence when multiple respected managers are building the same exposure
- lower confidence when the candidate conflicts with broad smart-money exits
- identify a `smart_money_follow_list` that merits higher research priority

### 4. Make Pass, Watch, Or Reject Decisions

Apply these rules:

- `pass`: thesis survives balance-sheet scrutiny and has neutral-to-positive institutional support
- `watch`: evidence is mixed or incomplete
- `reject`: structural risk is too high or smart-money evidence clearly cuts against the idea

Never keep a name as a clean long if the strongest evidence says it is a dividend trap or deteriorating balance-sheet story.

### 5. Write The Final Filter Notes

For every rejected or downgraded name, say why in one sentence.

Good reasons:

- uncovered dividend and rising debt
- hedge funds exiting the sector while thesis depends on multiple expansion
- crowded ownership with deteriorating cash generation

Avoid vague labels like `bad quality` without evidence.

## Preferred Output Shape

Use this shape when the user wants a structured answer:

```json
{
  "approved_candidates": [
    {
      "ticker": "string",
      "direction": "long|short|event_driven",
      "decision": "pass|watch",
      "smart_money_view": "supportive|mixed|negative|unknown",
      "risk_notes": ["string"]
    }
  ],
  "rejected_candidates": [
    {
      "ticker": "string",
      "reason": "string"
    }
  ],
  "smart_money_follow_list": ["string"],
  "risk_flags": ["string"],
  "missing_modules": ["string"]
}
```

## Default Operating Prompt

1. Take the raw candidate list from the idea layer.
2. Use `dividend-risk` to remove weak balance-sheet or dividend-trap names.
3. Use `hedge-fund-positioning` to identify smart-money confirmation or conflict.
4. Return a cleaner investable list with explicit pass, watch, or reject decisions.
