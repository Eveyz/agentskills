---
name: hedge-fund-positioning
description: Analyze recent hedge fund 13F filings to identify new positions, position increases, exits, sector trends, and crowded trades across major managers. Use when the user wants the latest 13F-based hedge fund positioning, smart-money holding changes, consensus longs, or quarter-over-quarter hedge fund portfolio comparisons grounded in current filings and cited sources.
---

# Hedge Fund Positioning

Analyze the latest available 13F reporting cycle across major hedge funds and convert filing changes into a structured positioning summary.

## Required Tools

- `tavily_search`

If `tavily_search` is unavailable, say so briefly and stop rather than fabricating holdings data.

## Output Contract

Return strict JSON matching [templates/output_schema.json](templates/output_schema.json).

Return only the JSON object when the user asks for the positioning output itself.

## Non-Negotiable Rules

- Base the analysis on the latest fully available 13F reporting cycle, not on stale examples.
- State or infer the filing quarter correctly. Remember that Form 13F is filed up to 45 days after quarter end.
- Prefer primary sources first: SEC filing pages, manager filing pages, or reputable 13F aggregators that clearly summarize the filing.
- Compare each manager against the immediately prior 13F quarter when labeling `new`, `increased`, or `exited`.
- Do not treat ordinary market-price moves as position changes if the share count or filing commentary does not support that conclusion.
- If a change cannot be verified, mark the relevant field as `"unknown"` instead of guessing.
- Include source URLs in the top-level `sources` array.

## Workflow

### 1. Identify The Latest Filing Cycle

Use `tavily_search` to determine the most recent quarter with broad 13F availability.

Suggested searches:

- `"latest 13F filings hedge funds quarter"`
- `"most recent 13F filing quarter SEC hedge fund holdings"`
- `"13F filings due date latest quarter hedge funds"`

Anchor the analysis to one explicit reporting period such as `"2025-Q4"` and compare against the prior quarter such as `"2025-Q3"`.

### 2. Select Major Hedge Funds

Identify a manageable set of widely followed hedge funds with public 13F coverage. Prefer large or influential long-only 13F reporters that are frequently tracked by the financial press or filing aggregators.

Typical candidates include managers such as:

- Pershing Square
- Third Point
- Coatue
- Lone Pine
- Viking Global
- Tiger Global
- Baupost
- Appaloosa
- Soros Fund Management
- Scion

Do not force a fixed list. Use the funds with the best current filing coverage for the latest cycle.

### 3. Verify Fund-Level Changes

For each selected fund, gather evidence on:

- `fund_name`
- `reporting_period`
- `comparison_period`
- `new_positions`
- `increased_positions`
- `exited_positions`

Preferred evidence order:

1. SEC or manager filing page
2. Reputable 13F summary page
3. High-quality financial press recap

When source detail is incomplete:

- Use only clearly reported names
- Limit list size to the highest-confidence moves
- Mark uncertain counts or weights as `"unknown"`

### 4. Normalize Position Change Labels

Use these rules consistently:

- `new`: position appears in the latest filing and was absent in the prior quarter
- `increased`: position existed previously and the reported share count increased materially
- `exited`: position appeared in the prior quarter and is absent in the latest filing

Avoid labeling a holding as `increased` based only on market value. Share count evidence is preferred.

### 5. Aggregate Sector Trends

Map each cited holding to a broad sector such as:

- Technology
- Financials
- Health Care
- Consumer
- Energy
- Industrials
- Communication Services
- Materials
- Utilities
- Real Estate

Then summarize cross-fund patterns:

- Sectors with repeated new or increased buying
- Sectors with repeated exits or trims
- Whether the pattern suggests offensive, defensive, cyclical, or quality rotation

Keep the summary evidence-based. If only a few funds are covered, say so.

### 6. Identify Crowded Trades

Flag a trade as potentially crowded when multiple tracked funds report one of the following in the same cycle:

- New positions in the same name
- Increased positions in the same name
- Continued top-holding status across several major funds

For each crowded trade, include:

- `ticker`
- `company_name`
- `sector`
- `funds`
- `crowding_signal`
- `notes`

Use cautious language such as `"emerging crowding"` or `"widely held across tracked funds"` unless the overlap is strong and well verified.

## Source Requirements

- Use at least 3 distinct sources overall when possible.
- Prefer at least 1 filing or filing-derived source for each fund you report.
- Exclude stale sources from old filing cycles unless they are only used to establish the prior-quarter comparison.
- Keep titles and URLs clean enough for another agent or user to trace the claim.

## Quality Checklist

Before finalizing:

- Confirm the reporting quarter is the latest broadly available 13F cycle
- Confirm each fund comparison is quarter-over-quarter
- Confirm `new`, `increased`, and `exited` labels reflect holding presence or share-count change, not just market value
- Confirm sector summaries are aggregated from the reported fund activity
- Confirm crowded trades are supported by multiple tracked funds
- Confirm missing facts are marked `"unknown"` rather than invented
- Confirm the final response is valid JSON with no markdown wrapper

## Default Operating Prompt

1. Determine the latest fully available 13F reporting quarter and the prior comparison quarter.
2. Identify major hedge funds with reliable filing coverage for that cycle.
3. Extract each fund's notable new positions, increased positions, and exited positions.
4. Aggregate the reported moves into sector trends and crowded trades.
5. Return strict JSON only.
