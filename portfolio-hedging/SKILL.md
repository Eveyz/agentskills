---
name: portfolio-hedging
description: Design portfolio hedging strategies for equity or multi-asset exposures using current market context, sector concentration, and macro risk. Use when the user wants hedge ideas for portfolio exposure, downside protection plans, inverse ETF or options overlays, hedge ratios, expected hedge cost, or event-driven hedge triggers tied to sectors or macro risks.
---

# Portfolio Hedging

Design practical hedging plans for a portfolio and return them as strict JSON.

By default, return both a readable Markdown hedge memo and a machine-readable JSON payload. Return JSON only when the user explicitly asks for JSON only.

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

- Always fetch the latest option-chain, volatility, and exposure data at run time, including the current VIX level when VIX is part of the hedge context.
- Do not rely on cached option premiums, stale implied volatility, stale VIX levels, or prior hedge costs.
- Re-check the hedge inputs every time before sizing protection.

## Data Source Priority

- Tier 1: `IBKR` or `CBOE` for options, and `VIX` for volatility context
- Tier 2: `yfinance-market-data` and `alphavantage-api` only as supporting or fallback market context
- Prefer exchange or broker option data over commentary or summaries.

## Output Contract

Return strict JSON matching [templates/output_schema.json](templates/output_schema.json).

## Inputs

Expect `portfolio_exposure` as the primary input.

Treat it as the user's best available description of holdings, weights, sector tilts, factor tilts, beta, or concentration. If the input is incomplete, make conservative assumptions, state them inside the `trigger` or `cost` wording when needed, and avoid false precision.

## Core Workflow

### 1. Identify The Main Risk

Parse the portfolio into the most decision-useful risk buckets:

- Sector concentration such as technology, financials, energy, biotech, semiconductors, or consumer cyclicals
- Market beta and broad equity drawdown risk
- Macro sensitivity such as rates, inflation, growth slowdown, credit stress, oil shock, or USD strength

If the portfolio contains only partial exposure detail, infer the simplest credible risk summary rather than reconstructing a full risk model.

### 2. Select Hedge Instruments

Prefer simple, liquid instruments that match the exposure:

- Broad index puts for general downside protection
- Sector ETF puts for concentrated sector risk
- Inverse ETFs for users who want straightforward implementation without options
- Volatility-sensitive hedges only when the portfolio is explicitly crash-sensitive and the hedge can be justified

Instrument selection rules:

- Use `SPY`, `QQQ`, `IWM`, or similar broad hedges for diversified long-equity beta
- Use sector ETFs such as `XLK`, `XLF`, `XLE`, `SMH`, `XBI`, or comparable funds for concentrated sector books
- Use inverse ETFs such as `SH`, `PSQ`, `SDS`, `SQQQ`, or sector inverses when options are unsuitable
- Avoid exotic or illiquid instruments unless the user explicitly asks for them

### 3. Estimate Hedge Ratio

Estimate a practical hedge ratio rather than an academic optimum.

Use this hierarchy:

1. Match notional exposure directly when the portfolio description includes size or weights
2. Adjust for beta when a sector or index hedge is materially more or less volatile than the underlying exposure
3. Use partial hedges by default, usually targeting roughly 25% to 75% of exposed notional, unless the user explicitly asks for a full hedge

Guidelines:

- Broad market uncertainty with no strong view: prefer partial hedges
- Near-term event risk: tighter, short-dated hedges can justify higher coverage
- Highly concentrated single-theme exposure: size the hedge to the concentrated sleeve, not the whole portfolio

Express `hedge_ratio` as a concise string such as `"0.5x of tech exposure"` or `"30% portfolio notional"`.

### 4. Estimate Cost

Estimate cost using the best available public data:

- For options, use recent premium levels or reasonable quoted ranges from current market data if available
- For inverse ETFs, estimate cost mainly from expense ratio, tracking drag, and expected holding-period burden

Rules:

- If live option chain detail is unavailable, provide a bounded estimate such as `"approximately 1.5% to 2.5% of hedged notional for 3-month puts"`
- Distinguish one-time premium from ongoing carry cost
- Do not imply exact execution pricing unless directly verified

Express `cost` as a short string tied to the assumed horizon.

### 5. Define Trigger Conditions

Each hedge idea must include a concrete trigger so the plan is actionable.

Good trigger types:

- Macro events such as CPI, Fed decisions, payrolls, earnings season, or recession-risk deterioration
- Technical or price triggers such as a break below a major index level
- Position-specific triggers such as sector outperformance leading to excessive concentration
- Volatility regime changes

Make triggers observable and public. Avoid vague language like `"if sentiment worsens"`.

## Source Requirements

- Use at least 2 sources when possible
- Prefer recent market data, ETF issuer pages, exchange or broker education pages for product mechanics, and high-quality financial coverage for macro context
- Include URLs in the top-level `sources` array
- Prefer current sources because hedge costs and macro conditions change quickly

## Quality Rules

- Keep recommendations implementable with liquid listed instruments
- Align each hedge to a clearly identified risk
- Prefer partial hedges unless the request clearly asks for maximum protection
- Mark uncertain estimates clearly in `cost` rather than pretending precision
- If exposure detail is missing, hedge only the risks that can be credibly inferred
- Never claim a hedge is perfect; basis risk and timing risk always exist

## Markdown Report Contract

When the user does not explicitly request JSON only, also return a Markdown report following [templates/report_template.md](templates/report_template.md).

The Markdown report should include these sections:

- Hedge Summary
- Risks Being Hedged
- Recommended Instruments
- Cost And Carry
- Trigger Conditions
- Residual Risks

Keep the Markdown concise and implementation-focused.

## Default Operating Prompt

1. Read `portfolio_exposure` and identify sector concentration, broad beta risk, and macro sensitivity.
2. Use current market context to select practical hedges with options or inverse ETFs.
3. Estimate a reasonable hedge ratio for each idea.
4. Estimate the cost using current public information, clearly labeling assumptions.
5. Add a concrete trigger for when each hedge should be used.
6. Return a Markdown hedge memo plus the matching structured JSON payload.