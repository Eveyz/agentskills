---
name: yfinance-market-data
description: Use yfinance from the `finance` conda environment to fetch stock quotes, price history, company info, fundamentals, news, and options chains. Use when Codex needs market data from yfinance and should choose a category-specific script for stock, news, or options data instead of loading everything.
---

# YFinance Market Data

Use this skill to retrieve market data with `yfinance` from the prebuilt `finance` conda environment.

Prefer the bundled category-specific scripts over ad hoc snippets. Only run the script for the category you actually need.

## Runtime Assumptions

- `conda` is installed.
- The `finance` conda environment already contains `yfinance`.
- Network access is available when the script is run.

## Category Scripts

Use exactly one of these scripts unless the task genuinely needs multiple categories.

### 1. Stock Data

Run [scripts/yf_stock_data.py](scripts/yf_stock_data.py) when you need:

- latest quote
- OHLCV history
- company info
- valuation fields
- balance-sheet or cash-flow summary fields exposed by yfinance

Typical use cases:

- price context for a ticker
- recent volume and trading-range checks
- valuation or company-profile enrichment
- quick historical price windows

### 2. News Data

Run [scripts/yf_news_data.py](scripts/yf_news_data.py) when you need:

- ticker news headlines
- publisher, publish time, and article link
- a compact raw article feed to compare against Tavily or Alpha Vantage news

Typical use cases:

- recent company headlines
- catalyst validation
- rough sentiment read before deeper narrative verification

### 3. Options Data

Run [scripts/yf_options_data.py](scripts/yf_options_data.py) when you need:

- expiration dates
- calls and puts for one expiration
- open interest and volume snapshots
- quick checks for unusual options activity

Typical use cases:

- squeeze setup validation
- hedge design support
- earnings or event-driven positioning checks

## Data Source Role

When a skill uses the three-source policy, use yfinance for:

- price, volume, history, and trading context
- basic company info and valuation fields
- options-chain data
- ticker-linked headline feeds

Use Alpha Vantage for:

- backup quotes and time series
- fundamental statements or overview fields
- technical indicators
- earnings calendar or news sentiment

Use Tavily for:

- filings, high-quality reporting, and narrative context
- catalyst verification
- cross-checking conflicting facts from structured feeds

If a field is missing from yfinance, do not force it. Fall back to Alpha Vantage or Tavily if appropriate.

## Command Examples

### Bash

Stock:

```bash
conda run -n finance python yfinance-market-data/scripts/yf_stock_data.py --symbol AAPL --period 6mo --include-info
```

News:

```bash
conda run -n finance python yfinance-market-data/scripts/yf_news_data.py --symbol NVDA --limit 10
```

Options:

```bash
conda run -n finance python yfinance-market-data/scripts/yf_options_data.py --symbol TSLA
```

Specific expiration:

```bash
conda run -n finance python yfinance-market-data/scripts/yf_options_data.py --symbol TSLA --expiration 2026-04-17 --limit 15
```

### PowerShell

Stock:

```powershell
conda run -n finance python .\yfinance-market-data\scripts\yf_stock_data.py --symbol AAPL --period 6mo --include-info
```

News:

```powershell
conda run -n finance python .\yfinance-market-data\scripts\yf_news_data.py --symbol NVDA --limit 10
```

Options:

```powershell
conda run -n finance python .\yfinance-market-data\scripts\yf_options_data.py --symbol TSLA
```

Specific expiration:

```powershell
conda run -n finance python .\yfinance-market-data\scripts\yf_options_data.py --symbol TSLA --expiration 2026-04-17 --limit 15
```

## Execution Rules

- Return JSON from the scripts so downstream skills can parse or summarize the result.
- Fetch only the minimum category needed for the task.
- Do not treat missing fields in `info` as a failure if price history or quotes succeeded.
- Do not infer options activity when the chain is empty or unavailable.
- Keep raw article URLs from yfinance news so Tavily can verify the most important headlines.

## Multi-Source Workflow

When a downstream skill needs market data:

1. Try yfinance first for price, volume, options, and ticker-linked news.
2. Try Alpha Vantage for backup time series, company overview, statements, indicators, and news sentiment.
3. Use Tavily to verify catalysts, filings, macro context, or any field that is unclear or missing.
4. If one source is unavailable, continue with the other sources and mark uncertainty instead of guessing.

## Default Operating Prompt

1. Decide whether the task needs stock, news, or options data.
2. Run only the matching yfinance script from the `finance` conda environment.
3. Return the parsed JSON or summarize the fields relevant to the requesting skill.
4. If yfinance is missing a needed field, fall back to Alpha Vantage or Tavily instead of fabricating it.
