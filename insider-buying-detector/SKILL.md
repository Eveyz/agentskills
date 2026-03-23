---
name: insider-buying-detector
description: Detect significant insider buying activity in publicly traded stocks using recent SEC Form 4 filings, OpenInsider-style transaction coverage, and recent financial news. Use when the user wants event-driven equity signals, insider accumulation screens, recent insider purchase analysis, or return-since-purchase calculations for insider buys within the last 30 days.
---

# Insider Buying Detector

Detect recent, significant insider buying and turn it into a structured event-driven signal set.

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

Return only the JSON object when the user asks for the detector output itself.

## Core Filters

Apply these hard filters before treating any transaction as a signal:

- Transaction date within the last 30 calendar days
- Open-market purchase, not award, option exercise, gift, or automatic plan sale
- Aggregate insider buy value above `$100,000` for the signal being reported

Prefer to aggregate multiple qualifying buys for the same issuer within the 30-day window before scoring signal strength.

## Primary Workflow

### 1. Search For Candidate Buys

Use `tavily_search` to gather evidence from:

- OpenInsider transaction pages or summaries
- SEC Form 4 filings or issuer filing pages
- Recent financial news discussing insider accumulation, earnings, capital raises, clinical updates, restructurings, or other catalysts

Suggested searches:

- `"site:openinsider.com insider purchase last 30 days over 100000"`
- `"SEC Form 4 purchase last 30 days insider buy ticker"`
- `"recent insider buying news director ceo cfo purchase"`

Start broad, then run ticker-specific follow-up searches once candidate names appear.

### 2. Verify And Normalize Each Candidate

For each candidate stock, verify:

- Ticker
- Issuer name
- Insider name
- Insider role such as CEO, CFO, Director, Chair, or 10% owner
- Transaction date
- Buy price per share
- Shares purchased
- Total dollar amount

Prefer SEC Form 4 or issuer filings when values conflict with secondary summaries.

If several insiders bought within the window, capture the strongest role in `insider_role` and explain the cluster in `signal_strength`.

### 3. Fetch Current Price And Compute Performance

Use `yfinance-market-data` to fetch the latest regular-market price for each qualifying ticker.

Compute return since purchase as:

`(current_price - buy_price) / buy_price`

Rules:

- If there are multiple qualifying purchases at different prices, use the weighted-average buy price when enough data is available
- If weighted averaging is not possible, use the most material purchase and state that choice in the hypothesis or source notes
- Round displayed prices reasonably, but do not overstate precision

### 4. Score Signal Strength

Classify `signal_strength` using observed evidence, not canned labels alone.

Use:

- `"very strong"` when there is cluster buying by multiple insiders, especially senior executives, or repeated buys after a major drawdown
- `"strong"` when a senior insider such as CEO or CFO makes a large discretionary open-market purchase
- `"moderate"` when a single director or officer makes a meaningful but less decisive buy
- `"weak"` only when the buy passes filters but context is noisy, tiny relative to company size, or contradicted by other facts

Strengthen the signal when:

- More than one insider bought
- CEO/CFO/Chair participated
- Purchases followed sharp price weakness
- Purchases occurred near earnings, financing resolution, regulatory milestones, or other identifiable catalysts

Weaken the signal when:

- The buyer is only a director with no corroboration
- The transaction looks symbolic despite exceeding the dollar threshold
- The company faces imminent dilution, distress, or severe negative news not offset by a clear catalyst

### 5. Form A Hypothesis

Infer a short, evidence-constrained hypothesis for why insiders may be buying.

Acceptable themes include:

- Undervaluation after excessive selloff
- Confidence ahead of earnings or operating inflection
- Balance-sheet repair or financing overhang clearing
- Product, regulatory, legal, or strategic catalyst

Do not claim non-public knowledge as fact. Frame this as a hypothesis tied to public context.

## Source Requirements

- Use at least 2 sources per reported signal when possible
- Prefer SEC or issuer filings plus one independent corroborating source
- Include URLs in the top-level `sources` array
- Exclude stale sources outside the relevant purchase window unless used only for context

## Confidence Scoring

Set top-level `confidence_score` from 0 to 1 based on:

- Freshness and quality of the filings
- Whether buy details were directly verified from Form 4 or issuer disclosures
- Whether current price was retrieved successfully
- Whether the catalyst narrative is supported by recent public news
- Whether multiple insiders corroborate the signal

Rule of thumb:

- `0.8-1.0`: direct filing verification, clear transaction details, current price available, strong contextual support
- `0.5-0.79`: mostly verified but some fields rely on secondary summaries or catalyst context is tentative
- `0.0-0.49`: sparse or conflicting evidence, incomplete pricing, or unclear transaction classification

## Quality Checklist

Before finalizing:

- Confirm every reported buy is within the last 30 days
- Confirm every reported buy exceeds the `$100,000` threshold after aggregation logic
- Confirm the transaction is a purchase, not a sale or derivative conversion
- Confirm `current_price` was fetched or set to `"unknown"`
- Confirm the JSON validates against the schema shape
- Mark unverifiable fields as `"unknown"` rather than inferring them

## Default Operating Prompt

1. Search recent insider buying activity using OpenInsider-style coverage, SEC Form 4 filings, and recent financial news.
2. Filter to open-market insider purchases above `$100,000` from the last 30 days.
3. For each stock, identify the insider role, normalize buy price and amount, fetch the current price with `yfinance-market-data`, and compute return since purchase.
4. Evaluate cluster buying, insider seniority, and timing versus earnings or other catalysts.
5. Infer a cautious public-information hypothesis for the buying.
6. Return strict JSON only.

