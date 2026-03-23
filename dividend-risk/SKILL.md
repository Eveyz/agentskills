---
name: dividend-risk
description: Detect unsustainable dividend yields in public equities by screening for dividend yield above 5%, then analyzing payout ratio, free cash flow coverage, debt trend, and dividend cut risk. Use when the user wants a high-yield dividend risk screen, a dividend sustainability check, a list of likely dividend traps, or safer peer alternatives for income stocks.
---

# Dividend Risk

Detect likely dividend traps among high-yield stocks and return a strict JSON risk report.

## Required Tools

- `yfinance-market-data`
- `alphavantage-api`
- `tavily_search`

Use the three-source policy whenever market, fundamentals, news, or options data is needed:

- Use `yfinance-market-data` first for stock prices, price history, volume, options chains, and ticker-linked news.
- Use `alphavantage-api` second for backup quotes, time series, company overview, statements, indicators, earnings calendars, and news sentiment.
- Use `tavily_search` mainly for news, filings, catalyst verification, macro context, and narrative claims.
- Do not use `tavily_search` as the primary source for stock prices when `yfinance-market-data` or `alphavantage-api` can provide the price directly.
- Only fall back to `tavily_search` for stock-price context when the price cannot be retrieved from the first two sources.

If one source is unavailable or incomplete, continue with the remaining sources and mark uncertainty instead of stopping.

## Freshness And Cache Policy

- Always fetch the latest filings and dividend evidence at run time.
- Do not use cached balance-sheet or cash-flow values.
- Re-check the latest filing set every time before labeling a dividend as safe or risky.

## Data Source Priority

- Tier 1: company filings, especially cash-flow statements, dividend declarations, and 10-K or 10-Q materials
- Tier 2: `Morningstar`
- Use yield alone only as a screen, never as the decision rule.

## Output Contract

Return strict JSON matching [templates/output_schema.json](templates/output_schema.json).

Return only the JSON object when the user asks for the detector output itself.

## Hard Filter

Only include a stock in `risk_stocks` if its indicated dividend yield is greater than `5%`.

If a company is reviewed but does not clear the yield threshold, exclude it from the final list.

## Primary Workflow

### 1. Build A Candidate Set

Use `yfinance-market-data` first to confirm:

- ticker
- current dividend yield
- sector or industry when available

Use `tavily_search` to gather recent evidence on:

- payout ratio
- free cash flow generation or deterioration
- debt growth, refinancing pressure, leverage concerns, or credit downgrades
- dividend coverage commentary
- dividend suspension, cut, or board-review rumors and news

Suggested searches:

- `"ticker dividend payout ratio free cash flow debt trend"`
- `"ticker dividend safety dividend cut risk"`
- `"ticker dividend coverage leverage refinancing"`

Prefer sources from the last 12 months unless older filings are needed to establish a debt trend.

### 2. Evaluate Dividend Sustainability

Assess the following dimensions for every candidate:

- `payout ratio`
- `free cash flow`
- `debt trend`

Use these heuristics:

- Payout ratio is elevated risk when it is persistently above `80%`
- Payout ratio is severe risk when it is above `100%`
- Free cash flow is elevated risk when recent free cash flow is weak, negative, or materially below dividend cash obligations
- Debt trend is elevated risk when total debt is rising, refinancing is expensive, interest burden is increasing, or leverage is worsening

Do not rely on a single weak metric alone if the rest of the evidence is strong. Weigh the combination.

### 3. Assign Cut Probability

Set `cut_probability` using evidence-based labels:

- `"low"` when payout is covered, free cash flow is healthy, and debt trend is stable or improving
- `"medium"` when one major risk factor is present or coverage is borderline
- `"high"` when multiple risk factors are present, especially poor cash coverage plus worsening leverage
- `"very high"` when payout appears uncovered, free cash flow is negative or persistently weak, and debt pressure is obvious

If evidence conflicts, choose the more cautious label and mention the conflict in `risk_factors`.

### 4. Write Risk Factors

Summarize the key issues in `risk_factors` as a concise string. Prefer concrete explanations such as:

- `"Payout ratio above 100%, negative free cash flow, and rising net debt"`
- `"High yield driven by falling share price; debt maturities and weak coverage increase cut risk"`

Avoid generic wording like `"bad fundamentals"` without specifics.

### 5. Suggest A Safer Alternative

For each flagged stock, name one `safer_alternative` from the same sector, industry, or business category when possible.

Choose a safer peer using relative evidence such as:

- lower payout ratio
- stronger or steadier free cash flow
- healthier balance sheet
- more defensible dividend history

Do not claim a peer is risk-free. It is enough that it appears materially safer on public evidence.

### 6. Finalize Sources

Include supporting URLs in the top-level `sources` array.

Prefer:

- company filings, investor relations, earnings releases, or transcripts
- reputable financial news and analysis
- finance data pages used to confirm yield or payout figures

Use at least 2 sources per flagged stock when possible.

## Quality Checklist

Before finalizing:

- confirm every reported stock has yield above `5%`
- confirm each stock has explicit evidence on payout ratio, free cash flow, and debt trend
- confirm `cut_probability` matches the cited evidence
- confirm `safer_alternative` is in a similar business area when possible
- confirm the final response matches the JSON schema exactly
- mark unknown values as `"unknown"` rather than fabricating precision

## Default Operating Prompt

1. Screen for stocks with dividend yield above 5%.
2. Analyze payout ratio, free cash flow, and debt trend using public sources.
3. Flag names with elevated dividend cut risk.
4. Suggest a safer peer for each risky stock.
5. Return strict JSON only.

