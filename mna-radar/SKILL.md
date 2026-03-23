---
name: mna-radar
description: Identify publicly traded companies with elevated M&A probability using current financial news, activist investor activity, industry consolidation evidence, strategic-asset logic, and takeover rumors. Use when the user wants event-driven merger-arbitrage idea generation, likely acquisition target screens, buyer-target pairing, takeover premium estimates, or a structured watchlist of companies that may attract bidders.
---

# M&A Radar

Identify likely acquisition targets, connect each target to a plausible buyer, estimate a realistic premium range from comparable deal behavior, and return strict JSON grounded in current sources.

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

- Always fetch the latest filings, company statements, and deal reporting at run time.
- Do not rely on cached rumor lists or stale deal chatter.
- Re-check primary filings every time before calling a target credible.

## Data Source Priority

- Tier 1: company announcements, `8-K`, and other `SEC filings`
- Tier 2: `Reuters`, `Bloomberg`
- Do not treat rumor-only articles as sufficient evidence.

## Output Contract

Return strict JSON matching [templates/output_schema.json](templates/output_schema.json).

Return only the JSON object when the user asks for the radar output itself.

## Non-Negotiable Rules

- Use current-source evidence, not stale takeover lore.
- Prefer target ideas with at least 3 distinct source-backed signals across news, activism, consolidation, asset value, rumor, or strategic fit.
- Separate verified facts from inference. M&A probability is a judgment call, so make the judgment explicit inside `thesis`.
- Prefer named companies over vague sector comments.
- If buyer identity, premium, or regulatory posture cannot be supported, set the field to `"unknown"` rather than guessing.
- Include every cited source URL in the top-level `sources` array.
- Return only valid JSON when the user requests the skill output itself.

## Workflow

### 1. Search For Fresh M&A Signals

Use `tavily_search` to gather recent evidence across three buckets:

- Financial news about strategic reviews, divestitures, breakups, weak valuation, or deal chatter
- Activist investor activity such as board pressure, spin-off demands, sale-process advocacy, or capital allocation campaigns
- Industry consolidation trends that point to likely buyers or sectors with active roll-up behavior

Suggested searches:

- `"takeover rumors activist investor strategic review company sale latest"`
- `"industry consolidation acquisition pipeline sector latest public companies"`
- `"activist investor pushes sale strategic alternatives public company"`
- `"undervalued strategic assets takeover target public company latest"`
- `"potential acquisition target regulatory risk antitrust buyer sector latest"`

Start broad, then run company-specific follow-up searches after likely targets emerge.

### 2. Identify Credible Targets

Prioritize companies showing several of these features:

- Undervalued relative to peers, assets, cash flow, breakup value, or replacement cost
- Strategic assets that matter to a larger buyer, such as spectrum, data, mineral rights, installed base, IP, brands, or distribution
- Public pressure for strategic alternatives from activists, founders, creditors, or boards
- Persistent takeover rumors, media reports, or repeated analyst speculation
- Sector-level consolidation where scale, synergies, or scarce assets make acquisition more plausible

Avoid thin rumor-only ideas unless multiple reputable sources corroborate them.

### 3. Map Each Target To A Plausible Buyer

For each target, identify the most plausible `potential_buyer` by checking:

- Existing strategic overlap or adjacency
- Prior acquisition behavior in the sector
- Geographic or product-fit logic
- Balance-sheet capacity and willingness to transact
- Whether private equity, a strategic acquirer, or a consortium is the cleaner fit

If several buyers are credible, choose the strongest one and explain the broader buyer set inside `thesis`.

### 4. Estimate A Realistic Premium

Set `premium_estimate` using recent comparable transactions, historical premiums in the sector, or prior rumored bid ranges.

Guidance:

- Use a range or concise label such as `"20%-30%"` when exact precision is not justified
- Reference historical acquisition premiums for similar public-company deals in the sector
- Adjust downward for cyclicality, financing strain, or execution risk
- Adjust upward for scarce assets, competitive bidding, or activist pressure

Do not invent a premium if no reasonable comp set is visible. Use `"unknown"` instead.

### 5. Evaluate Regulatory Risk

Classify `regulatory_risk` with concise language such as:

- `"low"`
- `"moderate"`
- `"high"`
- `"unknown"`

Consider:

- Horizontal overlap and market concentration
- Vertical foreclosure concerns
- Foreign ownership or national-security review
- Sector-specific approval regimes such as telecom, energy, defense, banking, or health care
- Political sensitivity and labor or consumer backlash

Briefly explain the main issue inside `thesis` when regulation is a material swing factor.

## Confidence Scoring

Set top-level `confidence_score` from 0 to 1 based on:

- Freshness and credibility of the M&A sources
- Whether activism, consolidation, valuation, and asset-value signals align
- How clearly the buyer-target logic fits
- Whether premium reasoning is anchored in sector history or comps
- Whether rumor and regulatory evidence are corroborated rather than speculative

Rule of thumb:

- `0.8-1.0`: several strong and recent signals with a coherent buyer, premium, and manageable risk assessment
- `0.5-0.79`: plausible target with meaningful evidence, but one or more key elements remain inferential
- `0.0-0.49`: weak, rumor-heavy, stale, or poorly corroborated setup

## Quality Checklist

Before finalizing:

- Confirm the search covered news, activism, and industry consolidation
- Confirm each target has a clear buyer thesis, not just a company name
- Confirm the premium estimate is tied to comps or stated as unknown
- Confirm regulatory risk is assessed explicitly
- Confirm unverifiable claims are marked `"unknown"` rather than implied as fact
- Confirm all cited URLs are included
- Confirm the final output is valid JSON with no markdown wrapper

## Default Operating Prompt

1. Search recent financial news, activist investor developments, and industry consolidation trends for public companies with elevated M&A probability.
2. Identify the strongest likely targets based on undervaluation, strategic assets, and takeover evidence.
3. Assign the most plausible buyer for each target, estimate a realistic premium from sector deal history, and assess regulatory risk.
4. Return strict JSON only.

