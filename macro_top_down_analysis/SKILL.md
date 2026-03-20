---
name: macro_top_down_analysis
description: Use this skill when the user wants a current top-down macro view, regime classification, historical analog analysis, or actionable cross-asset allocation implications grounded in recent macro data.
---

# Macro Top Down Analysis

Use this skill when the user wants a current top-down macro view, regime classification, historical analog analysis, or actionable cross-asset allocation implications grounded in recent macro data.

## Purpose

Analyze the current global macro environment and derive actionable asset allocation insights using recent macro data and historical analogs. The output must be evidence-based, citation-backed, and returned as strict JSON matching the provided schema.

## When To Use

Use this skill when the request involves any of the following:

- Global macro regime analysis
- Asset allocation from inflation, rates, growth, and labor data
- Cross-asset implications for equities, bonds, commodities, and USD
- Historical analog matching based on macro conditions
- Sector overweights and avoids derived from a macro regime

Do not use this skill for:

- Single-company fundamental research
- Pure technical analysis
- Intraday trading signals
- Portfolio optimization requiring proprietary holdings, constraints, or risk models not provided by the user

## Required Tooling

- `tavily_search`

If `tavily_search` is unavailable, say so briefly and stop rather than inventing facts.

## Non-Negotiable Rules

- Use at least 3 distinct sources.
- Prefer primary or near-primary sources when available: central banks, statistical agencies, major data publishers, and high-quality financial press summarizing official releases.
- No hallucination. Every non-obvious factual claim must be supported by a retrieved source.
- If data cannot be verified, set the field to `"unknown"` rather than inferring it.
- Separate verified facts from interpretation.
- Include source URLs in the `sources` array.
- Return only valid JSON in the final answer when the user asks for the analysis output itself.

## Output Schema

Return JSON matching this shape exactly:

```json
{
  "macro_state": {
    "inflation_trend": "rising|falling|stable|unknown",
    "rate_trend": "hiking|cutting|on_hold|mixed|unknown",
    "liquidity_condition": "tightening|stable|easing|mixed|unknown",
    "growth_regime": "accelerating|slowing|stagnant|contracting|mixed|unknown",
    "inflation_summary": "string",
    "rates_summary": "string",
    "growth_summary": "string",
    "employment_summary": "string"
  },
  "historical_analogs": [
    {
      "period": "string",
      "match_rationale": "string",
      "asset_performance_summary": {
        "equities_growth": "string",
        "equities_value": "string",
        "bonds": "string",
        "commodities": "string",
        "usd": "string"
      },
      "confidence": 0
    }
  ],
  "regime": "string",
  "asset_performance_map": {
    "equities": {
      "growth": "string",
      "value": "string"
    },
    "bonds": "string",
    "commodities": "string",
    "usd": "string"
  },
  "trade_implications": [
    {
      "type": "overweight|avoid",
      "asset_or_sector": "string",
      "rationale": "string"
    }
  ],
  "confidence_score": 0,
  "sources": [
    {
      "title": "string",
      "url": "string",
      "publisher": "string",
      "date": "YYYY-MM-DD|unknown"
    }
  ]
}
```

## Execution Workflow

### 1. Gather The Current Macro Data

Use `tavily_search` to retrieve the latest available evidence for:

- Inflation: CPI and PCE, prioritizing US data and adding major international context where relevant
- Interest rates: Fed, ECB, and other major central banks if they materially affect the global regime
- Growth: GDP growth or equivalent high-signal activity indicators when GDP is stale
- Employment: payrolls, unemployment, wage growth, or labor-market tightness indicators

Suggested search batches:

- `"latest US CPI PCE inflation release site:bls.gov OR site:bea.gov"`
- `"latest Federal Reserve rate decision site:federalreserve.gov"`
- `"latest ECB interest rate decision site:ecb.europa.eu"`
- `"latest US GDP growth release site:bea.gov"`
- `"latest US employment situation release site:bls.gov"`
- `"latest global central bank policy rate decision inflation growth outlook"`

If multiple regions conflict, summarize as `mixed` where the global picture is genuinely mixed.

### 2. Extract Structured Indicators

Map the retrieved evidence into:

- `inflation_trend`
- `rate_trend`
- `liquidity_condition`
- `growth_regime`

Use these rules:

- `inflation_trend`
  - `rising`: recent headline/core inflation re-accelerating
  - `falling`: disinflation clearly ongoing
  - `stable`: little meaningful change over recent releases
  - `unknown`: insufficient evidence
- `rate_trend`
  - `hiking`: current policy path still tightening
  - `cutting`: policy rates actively being reduced
  - `on_hold`: central bank paused with no active move
  - `mixed`: major central banks diverge
  - `unknown`: insufficient evidence
- `liquidity_condition`
  - `tightening`: policy, balance sheet, or financing conditions still restrictive
  - `easing`: cuts, balance-sheet support, or loosening financial conditions dominate
  - `stable`: little net change
  - `mixed`: cross-region or cross-indicator conflict
  - `unknown`: insufficient evidence
- `growth_regime`
  - `accelerating`: growth broadening or surprising positively
  - `slowing`: still positive but decelerating
  - `stagnant`: near flat
  - `contracting`: recessionary or negative prints
  - `mixed`: major economies diverge
  - `unknown`: insufficient evidence

### 3. Identify Historical Analogs

Select exactly 3 historical analog periods that best match the current combination of:

- Inflation behavior
- Policy-rate direction or stance
- Growth regime

Good analog examples may include:

- Late-cycle tightening with sticky inflation
- Early disinflation after a hiking cycle
- Reflation after growth troughs

For each analog:

- Name a concrete period, for example `"1994-1995"`, `"2004-2006"`, `"2022-2023"`
- Explain why it matches
- Summarize directional asset performance only if verifiable from reputable historical summaries
- If exact style-box or asset performance cannot be verified, use `"unknown"`

Do not pretend precision that the sources do not provide.

### 4. Classify The Current Regime

Classify the environment into one concise macro label such as:

- `"late-cycle tightening"`
- `"disinflation with restrictive policy"`
- `"reflation"`
- `"soft-landing disinflation"`
- `"stagflation risk"`
- `"mixed global easing"`

The label must follow from the data gathered, not from a canned prior.

### 5. Map Regime To Asset Performance

Provide directional expectations for:

- Equities: growth and value
- Bonds
- Commodities
- USD

Keep this section interpretive but evidence-constrained:

- Tie each conclusion to the identified regime and analogs
- Avoid absolute forecasts
- Use phrasing like `"historically supportive"`, `"typically challenged"`, or `"mixed"`

### 6. Generate Trade Implications

Produce a short list of actionable implications:

- Top sectors to overweight
- Sectors to avoid

Rules:

- Keep implications regime-driven, for example defensives in late-cycle slowdown, cyclicals in reflation, duration if disinflation plus easing, energy/materials if inflation re-accelerates
- If evidence is mixed, say so in the rationale
- Do not invent price targets, timing precision, or risk budgets

## Confidence Scoring

Set `confidence_score` from 0 to 1 based on:

- Breadth and quality of sources
- Freshness of data
- Consistency across inflation, rates, growth, and labor signals
- Degree of disagreement across major economies

Rule of thumb:

- `0.8-1.0`: fresh, consistent, and well-sourced
- `0.5-0.79`: adequate evidence with some mixed signals
- `0.0-0.49`: sparse, stale, or conflicting evidence

Historical analog entries should also include an individual `confidence` from 0 to 1.

## Quality Checklist

Before finalizing, verify:

- At least 3 sources are included
- All major required data categories were attempted
- Missing facts are marked `"unknown"`
- Regime classification matches the extracted macro state
- Trade implications follow from the regime and analogs
- Final output is valid JSON with no markdown wrapper

## Default Operating Prompt

Use this prompt structure when executing the skill:

1. Retrieve the latest available inflation, rates, growth, and employment data with `tavily_search`.
2. Extract structured macro indicators exactly as required.
3. Identify 3 historical analog periods and summarize verified asset behavior.
4. Classify the current macro regime.
5. Map the regime to likely performance for growth/value equities, bonds, commodities, and USD.
6. Generate actionable sector overweights and avoids.
7. Return strict JSON only. Use `"unknown"` for any unverifiable field.

