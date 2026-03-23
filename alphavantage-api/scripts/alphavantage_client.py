#!/usr/bin/env python3
"""
Alpha Vantage API Client - Production-ready wrapper for Alpha Vantage financial API.

Usage:
    from alphavantage_client import AlphaVantageClient

    client = AlphaVantageClient()  # Uses ALPHAVANTAGE_API_KEY env var
    quote = client.get_quote("AAPL")
    daily = client.get_daily("AAPL")
"""

import os
import time
import requests
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from functools import wraps


def rate_limit(calls_per_minute: int = 5):
    """Decorator to enforce rate limiting (free tier: 5/min, 25/day)."""
    min_interval = 60.0 / calls_per_minute
    last_called = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_called[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator


class AlphaVantageClient:
    """Production-ready Alpha Vantage API client with rate limiting and error handling."""

    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key: Optional[str] = None, calls_per_minute: int = 5):
        """
        Initialize Alpha Vantage client.

        Args:
            api_key: API key. If not provided, reads from ALPHAVANTAGE_API_KEY env var.
            calls_per_minute: Rate limit (free tier = 5/min)
        """
        self.api_key = api_key or os.getenv("ALPHAVANTAGE_API_KEY")
        if not self.api_key:
            raise ValueError("API key required. Set ALPHAVANTAGE_API_KEY or pass api_key parameter.")

        self.session = requests.Session()
        self._daily_calls = 0
        self._daily_limit = 25  # Free tier

    @rate_limit(calls_per_minute=5)
    def _request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make rate-limited API request with error handling."""
        params["apikey"] = self.api_key

        try:
            response = self.session.get(self.BASE_URL, params=params)
            data = response.json()

            # Check for rate limit message
            if "Note" in data:
                print(f"Rate limit warning: {data['Note']}")
                raise Exception("Rate limit exceeded. Wait before retrying.")

            # Check for error message
            if "Error Message" in data:
                raise Exception(f"API error: {data['Error Message']}")

            # Check for information message (often rate limit)
            if "Information" in data:
                print(f"Info: {data['Information']}")
                return {}

            self._daily_calls += 1
            return data

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")

    # ==================== Stock Time Series ====================

    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Get real-time quote for a symbol.

        Returns parsed quote with friendly keys.
        """
        data = self._request({
            "function": "GLOBAL_QUOTE",
            "symbol": symbol
        })

        raw_quote = data.get("Global Quote", {})
        if not raw_quote:
            return {}

        return {
            "symbol": raw_quote.get("01. symbol"),
            "open": float(raw_quote.get("02. open", 0)),
            "high": float(raw_quote.get("03. high", 0)),
            "low": float(raw_quote.get("04. low", 0)),
            "price": float(raw_quote.get("05. price", 0)),
            "volume": int(raw_quote.get("06. volume", 0)),
            "latest_trading_day": raw_quote.get("07. latest trading day"),
            "previous_close": float(raw_quote.get("08. previous close", 0)),
            "change": float(raw_quote.get("09. change", 0)),
            "change_percent": raw_quote.get("10. change percent", "0%").replace("%", "")
        }

    def get_intraday(
        self,
        symbol: str,
        interval: str = "5min",
        outputsize: str = "compact",
        adjusted: bool = True
    ) -> Dict[str, Any]:
        """
        Get intraday time series.

        Args:
            symbol: Stock symbol
            interval: 1min, 5min, 15min, 30min, 60min
            outputsize: compact (100 points) or full
            adjusted: Adjust for splits
        """
        return self._request({
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": interval,
            "outputsize": outputsize,
            "adjusted": str(adjusted).lower()
        })

    def get_daily(
        self,
        symbol: str,
        outputsize: str = "compact"
    ) -> Dict[str, Any]:
        """
        Get daily time series.

        Args:
            symbol: Stock symbol
            outputsize: compact (100 days) or full (20+ years)
        """
        return self._request({
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": outputsize
        })

    def get_daily_adjusted(
        self,
        symbol: str,
        outputsize: str = "compact"
    ) -> Dict[str, Any]:
        """Get daily adjusted time series (premium feature)."""
        return self._request({
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": symbol,
            "outputsize": outputsize
        })

    def get_weekly(self, symbol: str) -> Dict[str, Any]:
        """Get weekly time series."""
        return self._request({
            "function": "TIME_SERIES_WEEKLY",
            "symbol": symbol
        })

    def get_monthly(self, symbol: str) -> Dict[str, Any]:
        """Get monthly time series."""
        return self._request({
            "function": "TIME_SERIES_MONTHLY",
            "symbol": symbol
        })

    def search_symbols(self, keywords: str) -> List[Dict[str, Any]]:
        """Search for stock symbols."""
        data = self._request({
            "function": "SYMBOL_SEARCH",
            "keywords": keywords
        })
        return data.get("bestMatches", [])

    # ==================== Fundamental Data ====================

    def get_overview(self, symbol: str) -> Dict[str, Any]:
        """Get company overview including financials."""
        return self._request({
            "function": "OVERVIEW",
            "symbol": symbol
        })

    def get_income_statement(self, symbol: str) -> Dict[str, Any]:
        """Get income statements (annual and quarterly)."""
        return self._request({
            "function": "INCOME_STATEMENT",
            "symbol": symbol
        })

    def get_balance_sheet(self, symbol: str) -> Dict[str, Any]:
        """Get balance sheets (annual and quarterly)."""
        return self._request({
            "function": "BALANCE_SHEET",
            "symbol": symbol
        })

    def get_cash_flow(self, symbol: str) -> Dict[str, Any]:
        """Get cash flow statements (annual and quarterly)."""
        return self._request({
            "function": "CASH_FLOW",
            "symbol": symbol
        })

    def get_earnings(self, symbol: str) -> Dict[str, Any]:
        """Get earnings history (annual and quarterly)."""
        return self._request({
            "function": "EARNINGS",
            "symbol": symbol
        })

    # ==================== Technical Indicators ====================

    def get_indicator(
        self,
        symbol: str,
        indicator: str,
        interval: str = "daily",
        time_period: int = 14,
        series_type: str = "close",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get technical indicator.

        Args:
            symbol: Stock symbol
            indicator: SMA, EMA, RSI, MACD, BBANDS, etc.
            interval: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly
            time_period: Number of data points
            series_type: close, open, high, low
        """
        params = {
            "function": indicator.upper(),
            "symbol": symbol,
            "interval": interval,
            "time_period": time_period,
            "series_type": series_type,
            **kwargs
        }
        return self._request(params)

    def get_sma(self, symbol: str, time_period: int = 20, **kwargs) -> Dict[str, Any]:
        """Get Simple Moving Average."""
        return self.get_indicator(symbol, "SMA", time_period=time_period, **kwargs)

    def get_ema(self, symbol: str, time_period: int = 20, **kwargs) -> Dict[str, Any]:
        """Get Exponential Moving Average."""
        return self.get_indicator(symbol, "EMA", time_period=time_period, **kwargs)

    def get_rsi(self, symbol: str, time_period: int = 14, **kwargs) -> Dict[str, Any]:
        """Get Relative Strength Index."""
        return self.get_indicator(symbol, "RSI", time_period=time_period, **kwargs)

    def get_macd(self, symbol: str, **kwargs) -> Dict[str, Any]:
        """Get MACD indicator."""
        params = {
            "function": "MACD",
            "symbol": symbol,
            "interval": kwargs.get("interval", "daily"),
            "series_type": kwargs.get("series_type", "close")
        }
        return self._request(params)

    def get_bbands(
        self,
        symbol: str,
        time_period: int = 20,
        nbdevup: int = 2,
        nbdevdn: int = 2,
        **kwargs
    ) -> Dict[str, Any]:
        """Get Bollinger Bands."""
        return self.get_indicator(
            symbol, "BBANDS",
            time_period=time_period,
            nbdevup=nbdevup,
            nbdevdn=nbdevdn,
            **kwargs
        )

    def get_stoch(self, symbol: str, **kwargs) -> Dict[str, Any]:
        """Get Stochastic oscillator."""
        return self.get_indicator(symbol, "STOCH", **kwargs)

    def get_adx(self, symbol: str, time_period: int = 14, **kwargs) -> Dict[str, Any]:
        """Get Average Directional Index."""
        return self.get_indicator(symbol, "ADX", time_period=time_period, **kwargs)

    def get_atr(self, symbol: str, time_period: int = 14, **kwargs) -> Dict[str, Any]:
        """Get Average True Range."""
        return self.get_indicator(symbol, "ATR", time_period=time_period, **kwargs)

    # ==================== Forex ====================

    def get_exchange_rate(self, from_currency: str, to_currency: str) -> Dict[str, Any]:
        """Get real-time exchange rate."""
        data = self._request({
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": from_currency,
            "to_currency": to_currency
        })
        return data.get("Realtime Currency Exchange Rate", {})

    def get_forex_daily(self, from_symbol: str, to_symbol: str) -> Dict[str, Any]:
        """Get daily forex data."""
        return self._request({
            "function": "FX_DAILY",
            "from_symbol": from_symbol,
            "to_symbol": to_symbol
        })

    # ==================== Cryptocurrency ====================

    def get_crypto_rate(self, symbol: str, market: str = "USD") -> Dict[str, Any]:
        """Get cryptocurrency exchange rate."""
        data = self._request({
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": symbol,
            "to_currency": market
        })
        return data.get("Realtime Currency Exchange Rate", {})

    def get_crypto_daily(self, symbol: str, market: str = "USD") -> Dict[str, Any]:
        """Get daily cryptocurrency data."""
        return self._request({
            "function": "DIGITAL_CURRENCY_DAILY",
            "symbol": symbol,
            "market": market
        })

    # ==================== Economic Indicators ====================

    def get_gdp(self, interval: str = "annual") -> Dict[str, Any]:
        """Get US GDP data."""
        return self._request({
            "function": "REAL_GDP",
            "interval": interval
        })

    def get_cpi(self, interval: str = "monthly") -> Dict[str, Any]:
        """Get Consumer Price Index."""
        return self._request({
            "function": "CPI",
            "interval": interval
        })

    def get_inflation(self) -> Dict[str, Any]:
        """Get inflation rate."""
        return self._request({"function": "INFLATION"})

    def get_unemployment(self) -> Dict[str, Any]:
        """Get unemployment rate."""
        return self._request({"function": "UNEMPLOYMENT"})

    def get_fed_funds_rate(self, interval: str = "monthly") -> Dict[str, Any]:
        """Get Federal Funds Rate."""
        return self._request({
            "function": "FEDERAL_FUNDS_RATE",
            "interval": interval
        })

    def get_treasury_yield(
        self,
        interval: str = "monthly",
        maturity: str = "10year"
    ) -> Dict[str, Any]:
        """Get Treasury yield."""
        return self._request({
            "function": "TREASURY_YIELD",
            "interval": interval,
            "maturity": maturity
        })

    # ==================== News & Sentiment ====================

    def get_news_sentiment(
        self,
        tickers: Optional[str] = None,
        topics: Optional[str] = None,
        time_from: Optional[str] = None,
        time_to: Optional[str] = None,
        sort: str = "LATEST",
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Get AI-powered news sentiment.

        Args:
            tickers: Comma-separated tickers (e.g., "AAPL,MSFT")
            topics: Topic filters (e.g., "technology,finance")
            time_from: YYYYMMDDTHHMM format
            time_to: YYYYMMDDTHHMM format
            sort: LATEST, EARLIEST, RELEVANCE
            limit: Max results (1-1000)
        """
        params = {"function": "NEWS_SENTIMENT", "sort": sort, "limit": limit}
        if tickers:
            params["tickers"] = tickers
        if topics:
            params["topics"] = topics
        if time_from:
            params["time_from"] = time_from
        if time_to:
            params["time_to"] = time_to

        return self._request(params)

    def get_top_movers(self) -> Dict[str, Any]:
        """Get top gainers and losers."""
        return self._request({"function": "TOP_GAINERS_LOSERS"})

    # ==================== Utility ====================

    @property
    def daily_calls_used(self) -> int:
        """Get number of API calls used today."""
        return self._daily_calls

    @property
    def daily_calls_remaining(self) -> int:
        """Get estimated remaining API calls today."""
        return max(0, self._daily_limit - self._daily_calls)


# ==================== Quick Test ====================

def test_client():
    """Test the Alpha Vantage client with basic operations."""
    print("Testing Alpha Vantage Client...")
    print("=" * 50)
    print("Note: Free tier is 25 calls/day, 5 calls/minute")
    print("=" * 50)

    try:
        client = AlphaVantageClient()

        # Test quote
        print("\n1. Testing get_quote('AAPL')...")
        quote = client.get_quote("AAPL")
        if quote:
            print(f"   AAPL: ${quote['price']:.2f} ({quote['change_percent']}%)")

        # Test daily time series
        print("\n2. Testing get_daily('AAPL')...")
        daily = client.get_daily("AAPL")
        ts = daily.get("Time Series (Daily)", {})
        if ts:
            latest_date = list(ts.keys())[0]
            latest = ts[latest_date]
            print(f"   Latest ({latest_date}): Close ${latest['4. close']}")
            print(f"   Got {len(ts)} days of data")

        # Test search
        print("\n3. Testing search_symbols('Apple')...")
        results = client.search_symbols("Apple")
        print(f"   Found {len(results)} results")
        if results:
            print(f"   First: {results[0]['1. symbol']} - {results[0]['2. name']}")

        # Test forex
        print("\n4. Testing get_exchange_rate('USD', 'EUR')...")
        rate = client.get_exchange_rate("USD", "EUR")
        if rate:
            print(f"   USD/EUR: {rate.get('5. Exchange Rate', 'N/A')}")

        print(f"\n   Daily calls used: {client.daily_calls_used}")
        print(f"   Daily calls remaining: ~{client.daily_calls_remaining}")

        print("\n" + "=" * 50)
        print("All tests passed!")
        return True

    except Exception as e:
        print(f"\nError: {e}")
        return False


if __name__ == "__main__":
    test_client()
