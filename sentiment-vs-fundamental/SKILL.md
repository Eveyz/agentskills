---
name: sentiment-vs-fundamental
description: Find divergence between market sentiment and company fundamentals by combining recent news tone, public social-media tone, and core financial metrics. Use when the user wants contrarian equity ideas, sentiment-versus-fundamental mismatch detection, negative-news screens with strong underlying business quality, or mean-reversion entry setups for publicly traded stocks.
---

# Sentiment Vs Fundamental

Detect companies where sentiment is materially negative while fundamentals remain comparatively strong, then turn the mismatch into structured idea generation.

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

Return only the JSON object when the user asks for the screener output itself.

## Core Objective

Look for all 3 conditions:

- Clearly negative recent sentiment from news and, when available, public social-media discussion
- Fundamentally solid business performance or valuation support
- A plausible technical or mean-reversion entry setup rather than a falling knife with no trigger

Report only candidates where the mismatch is real enough to explain in one sentence each for:

- `sentiment_issue`
- `fundamental_strength`
- `entry_signal`

## Primary Workflow

### 1. Find Negative Sentiment Candidates

Use `tavily_search` to find companies facing notably bearish tone in the last 7 to 30 days.

Look for:

- Negative earnings-reaction coverage
- Downgrades, lawsuits, regulatory concerns, product delays, macro fears, or other bearish headlines
- Public social-media or retail-discussion evidence from sources surfaced in search results such as X posts quoted in articles, Reddit threads, Stocktwits pages, or market commentary summarizing online tone

Suggested searches:

- `"stocks with negative sentiment but strong fundamentals"`
- `"ticker recent negative news analyst downgrade social media bearish"`
- `"site:reddit.com ticker stock bearish"`
- `"site:stocktwits.com ticker sentiment"`

Prefer fresh sources. If social-media tone is not directly verifiable, keep the sentiment assessment grounded in news and mark any social component as part of the uncertainty rather than inventing it.

### 2. Retrieve And Normalize Fundamentals

Use `yfinance-market-data` to collect or derive:

- Revenue growth
- Profitability or margin quality
- Valuation context such as forward P/E, EV-style multiples if available, price-to-sales, or free-cash-flow framing

Treat fundamentals as strong when evidence supports several of these:

- Positive year-over-year revenue growth
- Stable or improving gross, operating, EBITDA, or net margins
- Positive earnings or free cash flow
- Balance-sheet resilience if relevant
- Valuation that is reasonable relative to growth, sector, or the recent drawdown

If a metric cannot be verified, set the field to `"unknown"` in your reasoning rather than assuming strength.

### 3. Detect The Mismatch

Classify a company as a divergence candidate only if:

- Sentiment is negative or bearish now
- Fundamentals are not deteriorating in a way that fully explains the selloff
- The bearish narrative appears stronger than the fundamental damage

Good mismatch examples:

- Strong revenue growth and healthy margins despite ugly headlines
- Temporary controversy, downgrade, or guidance fear while valuation has compressed sharply
- High-quality business punished for sector-wide panic rather than firm-specific collapse

Reject candidates where:

- Fundamentals are clearly breaking
- The valuation is still expensive despite the negative tone
- The bearish narrative reflects permanent impairment rather than temporary fear

### 4. Define Entry Signals

Use price context from `yfinance-market-data` plus chart-aware reasoning to define an entry setup.

Acceptable entry signals include:

- Reclaim of a recent support or gap level
- Bounce near 52-week support, prior base, or long-term moving-average area when the setup is obvious from available data
- Oversold mean-reversion conditions after an exaggerated drawdown
- Stabilization after earnings or capitulation volume described in reliable market coverage

Do not pretend to have intraday precision. Keep entry logic to simple, explainable technical levels or mean-reversion triggers supported by recent price action.

### 5. Produce Structured Ideas

For each reported idea:

- `ticker`: public ticker symbol
- `sentiment_issue`: short description of the negative narrative
- `fundamental_strength`: short description of the evidence that fundamentals remain solid
- `entry_signal`: short description of the technical or mean-reversion trigger

Keep each field concise and evidence-based.

## Source Requirements

- Use at least 2 sources per reported idea when possible
- Include both sentiment evidence and fundamental evidence
- Prefer reputable financial press, company materials surfaced in search, and finance data from `yfinance-market-data`
- Include URLs in the top-level `sources` array
- Exclude stale sources unless they provide necessary valuation or business context

## Confidence Scoring

Set top-level `confidence_score` from 0 to 1 based on:

- Freshness and quality of the sentiment evidence
- Whether social-media tone was directly observed versus indirectly summarized
- Clarity of the fundamental strength
- Valuation support
- Quality of the entry setup

Rule of thumb:

- `0.8-1.0`: strong multi-source evidence of negative sentiment, fundamentals clearly resilient, and entry setup is well-defined
- `0.5-0.79`: credible mismatch but some uncertainty around social tone, valuation, or technical trigger
- `0.0-0.49`: weak evidence, conflicting fundamentals, or unclear entry timing

## Quality Checklist

Before finalizing:

- Confirm each idea has recent negative sentiment evidence
- Confirm the fundamental case uses real metrics rather than vague quality language
- Confirm the bearish narrative does not simply reflect collapsing fundamentals
- Confirm the entry setup is specific enough to be actionable without false precision
- Confirm the JSON matches the schema shape
- Mark unverifiable facts as `"unknown"` rather than inferring them

## Default Operating Prompt

1. Search for stocks with recent negative news and, when available, bearish public social-media tone using `tavily_search`.
2. Pull revenue growth, margins, and valuation context with `yfinance-market-data`.
3. Identify cases where sentiment is meaningfully worse than the underlying fundamentals.
4. Define a simple technical or mean-reversion entry signal for each valid idea.
5. Return strict JSON only.

