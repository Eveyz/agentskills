---
name: correlation-anomaly
description: Detect abnormal cross-asset correlation behavior using recent market evidence and historical context. Use when the user wants to identify unusual moves such as stocks and gold rising together, bonds and equities falling together, correlation regime breaks, liquidity stress signals, macro regime-shift clues, or mean-reversion and normalization trade ideas grounded in current sources.
---

# Correlation Anomaly

Detect unusual cross-asset correlation patterns, compare them with normal historical behavior, interpret what the break may signal, and return trade ideas as strict JSON.

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

- Always fetch the latest available price data directly from the source at run time. Do not reuse an older price snapshot.
- Do not use cached correlation matrices or reuse prior windows.
- Recompute the correlation every time from fresh price data.

## Data Source Priority

- Tier 1: `IBKR` or `Bloomberg` price data when available
- Tier 2: `yfinance-market-data` or `alphavantage-api` as fallback price sources
- Do not rely on an article claiming that assets are correlated or decoupled.

## Calculation Rule

Compute the relationship directly from the retrieved price series, for example `corr = np.corrcoef(asset1, asset2)`.
## Output Contract

Return strict JSON matching [templates/output_schema.json](templates/output_schema.json).

Return only the JSON object when the user asks for the detector output itself.

## Core Anomalies To Check

Always test at least these two anomaly classes:

- Stocks and gold both rising at the same time
- Bonds and equities both falling at the same time

You may report other correlation breaks if the evidence is strong and relevant, but do not skip the two required checks.

## Non-Negotiable Rules

- Use current-source evidence, not stale priors.
- Use at least 3 distinct sources when possible.
- Prefer primary or near-primary sources: exchange or index providers, central banks, treasury/yield references, major financial data publishers, and high-quality financial press.
- Separate verified observations from interpretation.
- If the move, correlation, or historical comparison cannot be verified, mark it as `"unknown"` rather than guessing.
- Include all cited source URLs in the top-level `sources` array.
- Return only valid JSON when the user requests the skill output itself.

## Suggested Market Proxies

Use liquid, widely recognized proxies unless the user specifies alternatives.

- Equities: S&P 500, SPY, or another broad stock benchmark
- Gold: spot gold, COMEX gold, or GLD
- Bonds: US Treasuries, 10-year Treasury yield, TLT, or another broad duration proxy

If using price proxies for bonds, note that yields move inversely to price. Do not confuse rising yields with rising bond prices.

## Execution Workflow

### 1. Retrieve The Recent Cross-Asset Moves

Use `tavily_search` to gather current evidence on recent performance for:

- Broad equities
- Gold
- Bonds or Treasury yields

Suggested searches:

- `"S&P 500 gold both up today correlation market commentary"`
- `"stocks and gold rising together unusual macro explanation"`
- `"Treasury yields higher stocks lower today bond equity selloff"`
- `"stocks and bonds falling together unusual correlation liquidity stress"`
- `"cross asset correlation regime shift equities gold bonds latest"`

Prefer reports that clearly describe the move over a defined window such as intraday, 1-week, or 1-month. Keep the comparison window consistent within each anomaly.

### 2. Identify Whether An Anomaly Exists

For each required anomaly class, determine:

- Whether the move actually occurred in the chosen recent window
- Why the joint move is unusual relative to normal macro intuition
- Whether the anomaly is isolated noise or part of a broader pattern

Use concise anomaly labels such as:

- `"stocks_gold_rising_together"`
- `"bonds_equities_falling_together"`

Do not force an anomaly if the evidence is weak. If the pattern is not present, report that clearly with low confidence.

### 3. Compare Against Historical Patterns

For every detected anomaly, compare the current move with historically typical relationships:

- Stocks versus gold:
  - Often mixed or negatively correlated in risk-on versus safe-haven framing
  - Can rise together during liquidity expansion, falling real yields, or broad debasement/inflation hedging
- Bonds versus equities:
  - Often negatively correlated in classic risk-off periods
  - Can fall together when inflation shocks, duration repricing, or liquidity stress dominate

Use public historical summaries, reputable market commentary, or research notes discoverable through `tavily_search`.

State the historical baseline in plain language, for example:

- `"This is unusual because gold often outperforms when stocks sell off, not when risk assets rally."`
- `"This resembles periods when inflation repricing or funding stress pushed both stocks and duration lower."`

### 4. Interpret The Signal

Map each anomaly to one or more likely interpretations. Prioritize:

- `liquidity_stress`
- `regime_shift`

Other acceptable interpretations include:

- `inflation_repricing`
- `real_yield_shock`
- `policy_transition`
- `safe_haven_rotation`

Interpretation rules:

- Favor `liquidity_stress` when broad assets sell off together, credit or funding conditions are mentioned, or market commentary emphasizes forced deleveraging
- Favor `regime_shift` when sources indicate a persistent break from prior correlation behavior rather than a one-day event
- Use more than one interpretation if needed, but keep each tied to retrieved evidence
- Frame interpretations as evidence-based inferences, not certainties

### 5. Generate Trade Opportunities

Produce trade ideas only after the anomaly and interpretation are supported.

Use the two required idea buckets:

- `mean_reversion`
- `normalization_trade`

Trade construction guidance:

- Mean reversion:
  - Use when the anomaly appears temporary, positioning-driven, or unsupported by durable macro change
  - Example framing: fade a short-lived stocks/gold co-rally if sources suggest sentiment overshoot
- Normalization trade:
  - Use when a historically normal relationship is likely to reassert itself over time
  - Example framing: position for stocks/bonds diversification to recover after a temporary inflation scare fades

Each trade idea should include:

- The anomaly it responds to
- A concise directional expression
- A rationale tied to the interpretation
- A risk note explaining what would invalidate the trade

Do not invent exact entry prices, leverage, or portfolio sizing unless the user explicitly asks.

## Confidence Scoring

Set confidence from 0 to 1 for each anomaly and for the top-level output.

Raise confidence when:

- Multiple recent sources confirm the same cross-asset behavior
- The comparison window is clear and consistent
- Historical context is supported by reputable commentary or research
- The interpretation is corroborated by macro drivers such as yields, inflation, or liquidity conditions

Lower confidence when:

- Sources describe conflicting windows or contradictory moves
- The anomaly is only a single-session observation with little context
- Historical claims are vague or unsupported
- Trade logic depends on an unverified regime call

Rule of thumb:

- `0.8-1.0`: clearly documented anomaly with strong historical context and coherent macro explanation
- `0.5-0.79`: anomaly likely present but historical comparison or interpretation is somewhat tentative
- `0.0-0.49`: weak, noisy, or conflicting evidence

## Quality Checklist

Before finalizing:

- Confirm both required anomaly classes were checked
- Confirm each anomaly states whether it is present, not just why it might matter
- Confirm historical comparison is described in plain language
- Confirm interpretations are tied to evidence, not asserted as fact
- Confirm trade ideas map to either `mean_reversion` or `normalization_trade`
- Confirm all source URLs are included
- Confirm the final output is valid JSON with no markdown wrapper

## Default Operating Prompt

1. Use `tavily_search` to determine whether stocks and gold are rising together and whether bonds and equities are falling together over a recent consistent window.
2. Compare each observed relationship with normal historical cross-asset behavior.
3. Interpret each confirmed anomaly using evidence-based labels such as `liquidity_stress` or `regime_shift`.
4. Generate cautious `mean_reversion` and `normalization_trade` ideas tied to the detected anomaly.
5. Return strict JSON only, using `"unknown"` for unverifiable fields.

