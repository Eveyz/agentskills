---
name: short-squeeze-scanner
description: Identify potential short squeeze candidates in publicly traded stocks using current short interest, days to cover, borrow rate, volume behavior, options activity, and recent catalysts. Use when the user wants a short squeeze watchlist, event-driven long trade ideas, squeeze probability scoring, borrow-cost screens, or structured JSON output for high-short-interest names.
---

# Short Squeeze Scanner

Detect likely short squeeze setups and convert them into a small, evidence-backed candidate list.

## Required Tools

- `yfinance-market-data`
- `alphavantage-api`
- `tavily_search`

Use the three-source policy whenever market, fundamentals, news, or options data is needed:

- Start with `yfinance-market-data` for price history, volume, options chains, and ticker-linked news.
- Query `alphavantage-api` for backup quotes, time series, company overview, statements, indicators, earnings calendars, and news sentiment.
- Use `tavily_search` to verify filings, catalysts, macro context, and narrative claims.

If one source is unavailable or incomplete, continue with the remaining sources and mark uncertainty instead of stopping.

## Output Contract

Return strict JSON matching [templates/output_schema.json](templates/output_schema.json).

Return only the JSON object when the user asks for the scanner output itself.

## Non-Negotiable Rules

- Use current information only. Prefer sources from the last 30 calendar days for short-interest context, borrow-rate context, and catalysts.
- Use exact dates in source notes when timing matters.
- Prefer near-primary or market-structure sources for short data when available, then corroborate with reputable financial coverage.
- Do not report a candidate unless `short_interest` is above `20%`.
- Treat borrow rate as `high` when verified at `10%+`; treat `20%+` as especially squeeze-prone.
- Treat days to cover above `3` as supportive and above `5` as strong.
- If a required field cannot be verified, use `"unknown"` rather than guessing.
- Include source URLs in the top-level `sources` array.

## Primary Workflow

### 1. Gather Candidate Names

Use `tavily_search` to find names with elevated short interest, borrow stress, or active squeeze discussion.

Suggested searches:

- `"highest short interest stocks borrow rate days to cover"`
- `"ticker short interest percent float borrow fee days to cover"`
- `"hard to borrow stock borrow rate catalyst earnings product launch"`
- `"unusual call volume short squeeze candidate"`

Start broad, then run ticker-specific follow-up searches to verify every reported candidate.

### 2. Verify Core Short-Squeeze Inputs

For each ticker, retrieve and normalize:

- `short_interest`: prefer percent of float
- `days_to_cover`
- `borrow_rate`: stock loan fee, cost to borrow, or equivalent hard-to-borrow fee
- current news or event catalyst

Verification rules:

- Prefer two independent confirmations for `short_interest` and `borrow_rate` when possible
- If sources conflict, prefer the most recent timestamped figure and mention the ambiguity in `failure_risk`
- Exclude the ticker if `short_interest` is `20%` or below
- Exclude the ticker if borrow rate cannot be shown to be elevated, unless multiple reliable sources explicitly describe the stock as hard to borrow

### 3. Identify A Real Catalyst

Require at least one plausible public catalyst. Acceptable catalyst types:

- upcoming or freshly reported earnings
- product launch or commercial rollout
- regulatory, legal, financing, or M&A development
- contract win, guidance change, analyst action, or materially positive company news

Do not treat social-media excitement alone as a sufficient catalyst unless it is clearly affecting price, volume, or options flow and is corroborated by reporting.

### 4. Evaluate Squeeze Probability

Use `yfinance-market-data` plus search evidence to assess:

- `liquidity`: avoid names so illiquid that the setup is not realistically tradable
- `volume spike`: compare current or recent volume versus normal volume; `1.5x+` average volume is supportive and `2x+` is strong
- `options activity`: look for unusual call activity, rising implied volatility, or discussion of gamma pressure

Score the setup qualitatively before writing `entry_strategy`:

- Stronger when short interest is above `25%`, borrow rate is above `20%`, days to cover is above `5`, volume is expanding, and the catalyst is near-term
- Moderate when the stock passes the hard filters but one of days to cover, options activity, or volume expansion is only average
- Weaker when liquidity is poor, the catalyst is vague, or the move already looks exhausted

### 5. Define The Trade Setup

Write `entry_strategy` as a concise trade plan containing:

- an `entry zone` based on current price context, such as pullback to support, breakout level, or post-earnings continuation area
- a `trigger condition`, such as reclaim of prior high, volume-backed breakout, earnings gap hold, or unusual call-volume confirmation

Write `failure_risk` as the clearest reason the squeeze thesis could fail, such as:

- dilution risk
- offering or financing overhang
- low liquidity and gap risk
- catalyst disappointment
- borrow easing, short-interest decline, or reversal after a one-day spike

## Source Requirements

- Use at least 2 sources per reported candidate when possible
- Include at least 1 source supporting the short-interest or borrow data and 1 source supporting the catalyst
- Keep the final list small and selective; prefer 1 to 5 names over a padded watchlist

## Confidence Scoring

Set top-level `confidence_score` from `0` to `1` based on:

- freshness of short-interest and borrow-rate evidence
- whether days-to-cover was verified
- clarity and imminence of the catalyst
- whether volume expansion or options activity confirms the setup
- whether the trade setup and failure mode are evidence-backed rather than generic

Rule of thumb:

- `0.8-1.0`: current short data, confirmed borrow stress, clear catalyst, and supportive volume or options evidence
- `0.5-0.79`: passes core filters with mostly current evidence but some uncertainty in options flow, timing, or borrow data
- `0.0-0.49`: partial verification only, stale short data, or weak catalyst confirmation

## Quality Checklist

Before finalizing:

- Confirm every reported ticker has `short_interest` above `20%`
- Confirm borrow rate is elevated or clearly hard-to-borrow
- Confirm at least one real catalyst is present
- Confirm `days_to_cover` is retrieved or set to `"unknown"`
- Confirm `entry_strategy` includes both the zone and trigger
- Confirm `failure_risk` is specific to the candidate
- Confirm the final response is valid JSON with no markdown wrapper

## Default Operating Prompt

1. Search for current high-short-interest stocks with elevated borrow rates and recent catalysts.
2. Verify short interest, days to cover, borrow rate, and catalyst for each candidate.
3. Use `yfinance-market-data` to assess liquidity and recent volume behavior, and use search evidence to evaluate options activity when available.
4. Filter to names with short interest above `20%` and elevated borrow cost.
5. Define a practical entry zone, trigger condition, and failure risk for the best candidates.
6. Return strict JSON only.

