# Alpha Vantage API - Complete Endpoint Reference

## Base URL
```
https://www.alphavantage.co/query
```

## Authentication
```bash
# Query parameter only
?apikey=your_api_key
```

## Stock Time Series

### TIME_SERIES_INTRADAY
Intraday OHLCV data.
```
Params:
  - function: TIME_SERIES_INTRADAY
  - symbol (required)
  - interval: 1min, 5min, 15min, 30min, 60min
  - outputsize: compact (100) | full
  - adjusted: true | false
  - extended_hours: true | false
  - datatype: json | csv
Returns: Meta Data, Time Series (interval)
Free: ✅
```

### TIME_SERIES_DAILY
Daily OHLCV data.
```
Params:
  - function: TIME_SERIES_DAILY
  - symbol
  - outputsize: compact (100 days) | full (20+ years)
  - datatype: json | csv
Returns: Meta Data, Time Series (Daily)
Free: ✅
```

### TIME_SERIES_DAILY_ADJUSTED
Daily with splits/dividends.
```
Params: Same as daily
Returns: Includes adjusted_close, dividend_amount, split_coefficient
Free: ⚠️ Premium feature
```

### TIME_SERIES_WEEKLY
Weekly OHLCV data.
```
Params: function, symbol
Returns: Weekly Time Series
Free: ✅
```

### TIME_SERIES_MONTHLY
Monthly OHLCV data.
```
Params: function, symbol
Returns: Monthly Time Series
Free: ✅
```

### GLOBAL_QUOTE
Real-time quote.
```
Params: function, symbol
Returns:
  01. symbol, 02. open, 03. high, 04. low,
  05. price, 06. volume, 07. latest trading day,
  08. previous close, 09. change, 10. change percent
Free: ✅
```

### SYMBOL_SEARCH
Search for symbols.
```
Params: function, keywords
Returns: bestMatches: [{1. symbol, 2. name, 3. type, 4. region, ...}]
Free: ✅
```

## Fundamental Data

### OVERVIEW
Company overview.
```
Params: function, symbol
Returns: Symbol, Name, Description, Exchange, Currency, Country, Sector, Industry,
         MarketCapitalization, PE, PEG, BookValue, DividendPerShare, DividendYield,
         EPS, RevenuePerShareTTM, ProfitMargin, OperatingMarginTTM, ROA, ROE,
         RevenueTTM, GrossProfitTTM, QuarterlyEarningsGrowthYOY, 52WeekHigh/Low, Beta, etc.
Free: ✅
```

### INCOME_STATEMENT
Income statements.
```
Params: function, symbol
Returns: annualReports[], quarterlyReports[]
Free: ✅
```

### BALANCE_SHEET
Balance sheets.
```
Params: function, symbol
Returns: annualReports[], quarterlyReports[]
Free: ✅
```

### CASH_FLOW
Cash flow statements.
```
Params: function, symbol
Returns: annualReports[], quarterlyReports[]
Free: ✅
```

### EARNINGS
Earnings history.
```
Params: function, symbol
Returns: annualEarnings[], quarterlyEarnings[]
Free: ✅
```

### EARNINGS_CALENDAR
Upcoming earnings.
```
Params: function, horizon (3month|6month|12month), symbol (optional)
Returns: CSV format with symbol, name, reportDate, fiscalDateEnding, estimate, currency
Free: ✅
```

### IPO_CALENDAR
Upcoming IPOs.
```
Params: function
Returns: CSV format
Free: ✅
```

## Forex

### CURRENCY_EXCHANGE_RATE
Real-time exchange rate.
```
Params: function, from_currency, to_currency
Returns: Realtime Currency Exchange Rate {
  1. From Currency Code, 2. From Currency Name,
  3. To Currency Code, 4. To Currency Name,
  5. Exchange Rate, 6. Last Refreshed, 7. Time Zone, 8. Bid Price, 9. Ask Price
}
Free: ✅
```

### FX_INTRADAY
Intraday forex data.
```
Params: function, from_symbol, to_symbol, interval, outputsize
Free: ✅
```

### FX_DAILY
Daily forex data.
```
Params: function, from_symbol, to_symbol, outputsize
Free: ✅
```

### FX_WEEKLY / FX_MONTHLY
Weekly/monthly forex data.
```
Free: ✅
```

## Cryptocurrency

### CURRENCY_EXCHANGE_RATE
Crypto exchange rate (same as forex).
```
Params: from_currency (e.g., BTC), to_currency (e.g., USD)
Free: ✅
```

### DIGITAL_CURRENCY_DAILY
Daily crypto data.
```
Params: function, symbol, market (e.g., USD)
Returns: Time Series with open, high, low, close, volume, market_cap
Free: ✅
```

### DIGITAL_CURRENCY_WEEKLY / MONTHLY
Weekly/monthly crypto data.
```
Free: ✅
```

## Technical Indicators

All indicators accept:
- function: indicator name
- symbol
- interval: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly
- time_period: number of data points
- series_type: close, open, high, low

### Trend Indicators
```
SMA    - Simple Moving Average
EMA    - Exponential Moving Average
WMA    - Weighted Moving Average
DEMA   - Double Exponential Moving Average
TEMA   - Triple Exponential Moving Average
TRIMA  - Triangular Moving Average
KAMA   - Kaufman Adaptive Moving Average
MAMA   - MESA Adaptive Moving Average
T3     - Triple Exponential Moving Average
VWAP   - Volume Weighted Average Price (⚠️ Premium)
```

### Momentum Indicators
```
RSI    - Relative Strength Index
MACD   - Moving Average Convergence/Divergence
        (params: fastperiod, slowperiod, signalperiod)
STOCH  - Stochastic Oscillator
        (params: fastkperiod, slowkperiod, slowdperiod, slowkmatype, slowdmatype)
STOCHRSI - Stochastic RSI
WILLR  - Williams %R
ADX    - Average Directional Index
ADXR   - ADX Rating
APO    - Absolute Price Oscillator
PPO    - Percentage Price Oscillator
MOM    - Momentum
BOP    - Balance of Power
CCI    - Commodity Channel Index
CMO    - Chande Momentum Oscillator
ROC    - Rate of Change
ROCR   - Rate of Change Ratio
AROON  - Aroon Indicator
AROONOSC - Aroon Oscillator
MFI    - Money Flow Index
TRIX   - 1-day ROC of Triple Smooth EMA
ULTOSC - Ultimate Oscillator
DX     - Directional Movement Index
MINUS_DI / PLUS_DI - Directional Indicators
MINUS_DM / PLUS_DM - Directional Movement
```

### Volatility Indicators
```
BBANDS - Bollinger Bands
         (params: time_period, nbdevup, nbdevdn, matype)
MIDPOINT - MidPoint over period
MIDPRICE - MidPrice over period
SAR    - Parabolic SAR (params: acceleration, maximum)
TRANGE - True Range
ATR    - Average True Range
NATR   - Normalized ATR
```

### Volume Indicators
```
AD     - Chaikin A/D Line
ADOSC  - Chaikin A/D Oscillator
OBV    - On Balance Volume
```

### Hilbert Transform (Advanced)
```
HT_TRENDLINE - Instantaneous Trendline
HT_SINE      - Sine Wave
HT_TRENDMODE - Trend vs Cycle Mode
HT_DCPERIOD  - Dominant Cycle Period
HT_DCPHASE   - Dominant Cycle Phase
HT_PHASOR    - Phasor Components
```

## Economic Indicators

### REAL_GDP
US Real GDP.
```
Params: function, interval (annual|quarterly)
Free: ✅
```

### REAL_GDP_PER_CAPITA
GDP per capita.
```
Params: function
Free: ✅
```

### TREASURY_YIELD
Treasury yields.
```
Params: function, interval (daily|weekly|monthly), maturity (3month|2year|5year|7year|10year|30year)
Free: ✅
```

### FEDERAL_FUNDS_RATE
Fed funds rate.
```
Params: function, interval
Free: ✅
```

### CPI
Consumer Price Index.
```
Params: function, interval
Free: ✅
```

### INFLATION
Inflation rate.
```
Params: function
Free: ✅
```

### INFLATION_EXPECTATION
Inflation expectations.
```
Free: ✅
```

### CONSUMER_SENTIMENT
Consumer sentiment.
```
Free: ✅
```

### RETAIL_SALES
Retail sales data.
```
Free: ✅
```

### DURABLES
Durable goods orders.
```
Free: ✅
```

### UNEMPLOYMENT
Unemployment rate.
```
Free: ✅
```

### NONFARM_PAYROLL
Nonfarm payroll.
```
Free: ✅
```

## Alpha Intelligence

### NEWS_SENTIMENT
AI-powered news sentiment.
```
Params:
  - function: NEWS_SENTIMENT
  - tickers: comma-separated (optional)
  - topics: blockchain, earnings, etc. (optional)
  - time_from, time_to: YYYYMMDDTHHMM format
  - sort: LATEST | EARLIEST | RELEVANCE
  - limit: 1-1000
Returns: feed[{title, url, time_published, authors, summary, source, topics, overall_sentiment_score/label, ticker_sentiment}]
Free: ✅
```

### TOP_GAINERS_LOSERS
Market movers.
```
Params: function
Returns: top_gainers[], top_losers[], most_actively_traded[]
Free: ✅
```

### INSIDER_TRANSACTIONS
Insider trading data.
```
Params: function, symbol
Free: ⚠️ Premium
```

### ANALYTICS_FIXED_WINDOW
Advanced analytics.
```
Free: ⚠️ Premium
```

## Rate Limits

| Tier | Daily | Per Minute | Price |
|------|-------|------------|-------|
| Free | 25 | 5 | $0 |
| Premium | Unlimited | 75-1,200 | $49.99-$249.99/mo |

## Error Handling

Errors return HTTP 200 with error in body:
```json
{"Note": "Rate limit exceeded..."}
{"Error Message": "Invalid API call..."}
{"Information": "API key info..."}
```

## Data Formats

Most endpoints support `datatype=csv` for CSV output.

## Output Size

- `compact`: Last 100 data points
- `full`: Full-length (20+ years for daily)
