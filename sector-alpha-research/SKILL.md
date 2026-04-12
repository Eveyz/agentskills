---
name: sector-alpha-research
description: Research alpha in a user-specified equity sector or industry and review the most important listed names in that group. Use when Codex needs to analyze a sector such as technology, semiconductors, software, banks, energy, or biotech; explain where the alpha is right now; and triage the top 20 stocks in that sector into priority, watch, and deprioritize buckets for the current period.
---

# Sector Alpha Research

Run this skill as a sector-level meta orchestrator. Combine the repo's top-down, idea, and risk layers with a fast constituent review so the user gets both the sector thesis and a practical watchlist of names to care about now.

By default, return both a readable Markdown report and a machine-readable JSON payload. Return JSON only when the user explicitly asks for JSON only.

## Required Inputs

Accept the user's sector or industry, region, time horizon, and top-name count when provided. If omitted, assume:

- one sector or industry group such as `technology`, `software`, `semiconductors`, or `energy`
- US-listed equities
- current period focus, roughly the next 2 to 8 weeks
- top 20 names by market relevance, benchmark weight, or market cap

## Supporting Skills

Prefer these skills and use them in this order:

- `top-down-alpha-engine`
- `idea-generation-engine`
- `risk-filter-layer`
- `yfinance-market-data`

Use these skills conditionally when they materially improve the sector call or the flagged names:

- `hedge-fund-positioning`
- `insider-buying-detector`
- `sentiment-vs-fundamental`
- `short-squeeze-scanner`
- `mna-radar`

If one or more skills are unavailable, continue with the remaining evidence, record the missing modules, and lower confidence.

## Core Objective

Do 2 jobs well:

1. Explain where the alpha is in the chosen sector right now.
2. Check the top 20 names in that sector and identify which stocks deserve attention in this period.

This is not a full initiation report on every constituent. The goal is triage first, then deeper work only on the names that clearly matter.

## Non-Negotiable Rules

- Start with the top-down regime before naming stock ideas.
- Keep the chosen sector anchored to the current regime instead of treating it as an isolated stock basket.
- Build a top 20 universe first, then triage the universe quickly before deep-diving the best names.
- Do not force a bullish idea just because the sector is popular. Surface shorts, avoids, or neutral calls when the evidence points there.
- Promote a name only when there is a clear reason to care now, such as regime fit, fresh catalyst, cross-signal confirmation, valuation reset, smart-money support, or technical stabilization.
- Use `"unknown"` instead of inventing missing constituent, market-cap, or catalyst details.

## Workflow

### 1. Normalize The Sector Request

Turn the user request into one investable universe.

Examples:

- `technology` can stay broad, but note important subgroups such as software, semiconductors, internet, and hardware
- `semiconductors` is already narrow and should stay focused
- `banks` or `biotech` should be treated as industry groups rather than broad sectors

If the user gives a broad sector, keep the report broad but be explicit about which subsectors are currently leading or lagging.

### 2. Build The Top 20 Universe

Construct a current top 20 list for the requested sector or industry using the latest available evidence.

Prefer this order:

1. current benchmark or sector-ETF holdings
2. current index constituent lists
3. current market-cap and liquidity leaders from reliable market data

If an exact top 20 list cannot be fully verified, use the best available approximation of the 20 most relevant listed names and say how the list was built.

For each name, keep:

- `ticker`
- `company_name`
- `subsector`
- `market_relevance_note`

### 3. Run The Top-Down Sector Context

Invoke `top-down-alpha-engine` first and extract:

- `regime`
- `risk_posture`
- `sector_priority`
- `top_down_playbook`

Then translate that output into a sector-specific view:

- why this sector should outperform, lag, or stay mixed
- which subsectors should lead
- which factor exposures matter most
- what would invalidate the sector thesis

### 4. Generate Sector-Specific Ideas

Invoke `idea-generation-engine` with the chosen sector as a constraint.

Prefer ideas that:

- fit the regime
- belong to the chosen sector or its relevant subsectors
- have a real catalyst in the current period
- show confirmation from more than one underlying module when possible

If the sector is narrow, allow the idea set to be smaller rather than padding the list with weak names.

### 5. Triage The Top 20 Names

Review the top 20 quickly before spending time on deep research.

For each name, classify it as one of:

- `priority_now`
- `watch`
- `deprioritize`

Use a fast but evidence-based rubric:

- regime fit
- fresh news or event catalyst
- valuation or sentiment reset
- price and volume context
- smart-money or insider confirmation when available
- obvious balance-sheet, crowding, or thesis-break risk

Do not run every heavy subskill on all 20 names. Use fast screening first, then deepen only the names that stand out.

### 6. Deepen The Flagged Names

Take the best names from the idea layer and the top 20 triage pass, then run `risk-filter-layer` on the promoted set.

Use direct supporting skills only when needed:

- `hedge-fund-positioning` for smart-money confirmation, crowded sector rotation, or notable exits
- `insider-buying-detector` when insider accumulation could explain why a name deserves near-term attention
- `sentiment-vs-fundamental` when the opportunity is a sentiment reset inside the sector
- `short-squeeze-scanner` when a high-short-interest setup is relevant
- `mna-radar` when consolidation is part of the sector thesis

The purpose of this step is to turn a broad watchlist into a smaller list of names that deserve focused attention now.

### 7. Produce The Sector Output

Return one integrated result that makes it obvious:

- whether the sector is attractive now
- where the alpha is coming from
- which subsectors matter most
- which names from the top 20 deserve attention now
- which names are only watchlist items
- which risks could invalidate the call

## Attention Scoring Guidance

Promote a name to `priority_now` when several of these are true:

- fits the current regime and sector playbook
- has a fresh catalyst in the current period
- is supported by more than one idea signal
- survives risk filtering
- has supportive institutional or insider behavior
- shows price stabilization, relative strength, or volume confirmation

Keep a name in `watch` when the setup is plausible but incomplete, early, or mixed.

Move a name to `deprioritize` when:

- there is no visible edge right now
- the thesis conflicts with the regime
- the balance-sheet or crowding risk is too high
- the sector narrative is strong but the stock-specific setup is weak

## Markdown Report Contract

When the user does not explicitly request JSON only, also return a Markdown report following [templates/report_template.md](templates/report_template.md).

The Markdown report should include these sections:

- Sector Snapshot
- Where The Alpha Is
- Top 20 Triage
- Names To Pay Attention To Now
- Risks And Invalidation

Keep the Markdown concise, decision-oriented, and useful for repeated sector reviews.

## JSON Output Shape

Use this shape when the user wants a structured answer:

```json
{
  "sector": "string",
  "region": "string",
  "time_horizon": "string",
  "top_down": {
    "regime": "string",
    "risk_posture": "risk_on|balanced|risk_off|event_driven_mixed|unknown",
    "sector_fit": "favored|mixed|unfavored|unknown",
    "playbook": {
      "prioritize": ["string"],
      "avoid": ["string"],
      "invalidate_if": ["string"]
    }
  },
  "sector_alpha_map": {
    "tailwinds": ["string"],
    "headwinds": ["string"],
    "alpha_vectors": ["string"],
    "subsector_focus": ["string"]
  },
  "top_20_screen": [
    {
      "ticker": "string",
      "company_name": "string",
      "status": "priority_now|watch|deprioritize",
      "why_now": "string",
      "key_signal": "string",
      "key_risk": "string"
    }
  ],
  "priority_names": [
    {
      "ticker": "string",
      "stance": "long|short|event_driven|watch",
      "thesis": "string",
      "catalyst": "string",
      "supporting_modules": ["string"],
      "risk_notes": ["string"]
    }
  ],
  "monitoring_triggers": ["string"],
  "confidence": "low|medium|high|unknown",
  "missing_modules": ["string"],
  "sources": []
}
```

## Quality Checklist

Before finalizing:

- Confirm the chosen top 20 universe is current or clearly labeled as the best available approximation.
- Confirm the sector call starts from the top-down regime, not just bottom-up stock stories.
- Confirm the top 20 screen is a triage pass rather than a padded deep dive.
- Confirm promoted names have a current reason to matter.
- Confirm risks and invalidation conditions are explicit.
- Confirm both Markdown and JSON were produced unless the user explicitly asked for a single format.
- Confirm the JSON is valid when JSON is requested.

## Default Operating Prompt

1. Normalize the user's requested sector or industry and build a current top 20 stock universe.
2. Run `top-down-alpha-engine` to decide how the sector fits the current regime.
3. Run `idea-generation-engine` to surface the best sector-specific long, short, and event-driven ideas.
4. Triage the top 20 names into `priority_now`, `watch`, and `deprioritize`.
5. Run `risk-filter-layer` and any needed supporting skills on the flagged names.
6. Return a concise Markdown sector report plus the matching structured JSON payload.
