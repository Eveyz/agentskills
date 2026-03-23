---
name: idea-generation-engine
description: Orchestrate multi-source equity idea generation by combining insider activity, short-squeeze setups, M&A signals, and sentiment-versus-fundamental divergence. Use when Codex needs long ideas, short ideas, or event-driven trades and should compare competing theses through multi-round debate or independent agent passes before ranking candidates.
---

# Idea Generation Engine

Run this skill as the alpha creation layer after the top-down view is known. Use the underlying event and sentiment skills to surface candidates, then pressure-test them through structured debate before producing ranked long, short, and event-driven ideas.

## Supporting Skills

Use these underlying skills when available:

- `insider-buying-detector`
- `short-squeeze-scanner`
- `mna-radar`
- `sentiment-vs-fundamental`

If a module is missing, continue with the remaining modules, note the gap, and lower conviction.

## Required Outputs

Always aim to produce:

- `long_ideas`
- `short_ideas`
- `event_driven_trades`
- `debate_summary`
- `cross_signal_alignment`

## Debate Framework

Treat every serious candidate as something that should survive argument, not just screening.

If subagents are available, prefer a multi-round debate:

1. Bull case pass
2. Bear case pass
3. Moderator pass to reconcile disagreement

If subagents are unavailable, emulate the same structure sequentially in one thread.

Do not let debate become generic. Every argument must be tied to evidence surfaced by the underlying skills.

## Workflow

### 1. Gather Raw Candidates

Invoke the four idea modules and extract candidate tickers with their initial direction:

- insider buying usually starts as `long`
- short squeeze usually starts as `long` or invalidates a short
- M&A usually starts as `event_driven_long`
- sentiment divergence can become either `long` or `short` depending on whether sentiment is too negative or fundamentals are deteriorating faster than price implies

### 2. Normalize Candidate Records

For each candidate, maintain:

- `ticker`
- `initial_direction`
- `source_modules`
- `core_thesis`
- `near_term_catalyst`
- `key_risk`

Prefer candidates confirmed by more than one module.

### 3. Run Multi-Round Debate

For each high-priority candidate:

- Round 1, Bull: explain why the trade works now
- Round 2, Bear: explain what makes the setup fragile, crowded, late, or fundamentally wrong
- Round 3, Moderator: decide whether the idea should be promoted, demoted, or discarded

Key moderator questions:

- Is the catalyst real and near enough to matter
- Is the market already pricing the thesis
- Does the evidence support a directional trade or only a watchlist item
- Is this truly alpha or just a noisy narrative

### 4. Separate By Trade Type

Place surviving names into:

- `long_ideas`
- `short_ideas`
- `event_driven_trades`

Rules:

- Longs need upside asymmetry plus a defendable catalyst.
- Shorts need clear deterioration, over-optimism, or a risk factor the market may be underpricing.
- Event-driven trades need a concrete event path such as deal speculation, squeeze conditions, financing change, or insider clustering.

### 5. Rank By Cross-Signal Quality

Favor ideas where:

- more than one underlying skill points to the same ticker
- the catalyst is public and timely
- the thesis survives the bear case
- the direction fits the current top-down regime

Demote ideas that rely on rumor only, stale data, or one-dimensional narratives.

## Preferred Output Shape

Use this shape when the user wants a structured answer:

```json
{
  "long_ideas": [
    {
      "ticker": "string",
      "thesis": "string",
      "source_modules": ["string"],
      "catalyst": "string",
      "debate_verdict": "promote|watch|reject"
    }
  ],
  "short_ideas": [],
  "event_driven_trades": [],
  "cross_signal_alignment": [
    {
      "ticker": "string",
      "aligned_modules": ["string"],
      "notes": "string"
    }
  ],
  "debate_summary": [
    {
      "ticker": "string",
      "bull_case": "string",
      "bear_case": "string",
      "moderator_view": "string"
    }
  ],
  "missing_modules": ["string"]
}
```

## Default Operating Prompt

1. Run the insider, squeeze, M&A, and sentiment modules to surface candidates.
2. Normalize the candidate list and identify names supported by multiple modules.
3. Run a bull-versus-bear debate for each serious idea, using subagents when available.
4. Return ranked long ideas, short ideas, and event-driven trades with a concise debate verdict for each.
