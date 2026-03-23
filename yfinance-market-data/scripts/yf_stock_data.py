#!/usr/bin/env python3
import argparse
import json
from datetime import datetime


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch stock quote, price history, and optional info via yfinance.")
    parser.add_argument("--symbol", required=True, help="Ticker symbol, for example AAPL")
    parser.add_argument("--period", default="6mo", help="History period, for example 1mo, 6mo, 1y")
    parser.add_argument("--interval", default="1d", help="History interval, for example 1d, 1wk, 1h")
    parser.add_argument("--include-info", action="store_true", help="Include info and valuation fields")
    parser.add_argument("--history-limit", type=int, default=10, help="Maximum number of historical rows to return")
    args = parser.parse_args()

    try:
        import yfinance as yf
    except ImportError as exc:
        raise SystemExit('yfinance is not installed in the selected Python environment.') from exc

    ticker = yf.Ticker(args.symbol)
    history = ticker.history(period=args.period, interval=args.interval, auto_adjust=False)

    quote = {}
    if not history.empty:
        latest = history.tail(1).reset_index().iloc[0]
        quote = {
            "date": str(latest.iloc[0]),
            "open": None if latest.get("Open") is None else float(latest["Open"]),
            "high": None if latest.get("High") is None else float(latest["High"]),
            "low": None if latest.get("Low") is None else float(latest["Low"]),
            "close": None if latest.get("Close") is None else float(latest["Close"]),
            "volume": None if latest.get("Volume") is None else float(latest["Volume"]),
        }

    history_rows = []
    if not history.empty:
        for _, row in history.tail(args.history_limit).reset_index().iterrows():
            history_rows.append(
                {
                    "date": str(row.iloc[0]),
                    "open": None if row.get("Open") is None else float(row["Open"]),
                    "high": None if row.get("High") is None else float(row["High"]),
                    "low": None if row.get("Low") is None else float(row["Low"]),
                    "close": None if row.get("Close") is None else float(row["Close"]),
                    "adj_close": None if row.get("Adj Close") is None else float(row["Adj Close"]),
                    "volume": None if row.get("Volume") is None else float(row["Volume"]),
                }
            )

    result = {
        "symbol": args.symbol.upper(),
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "period": args.period,
        "interval": args.interval,
        "quote": quote,
        "history": history_rows,
    }

    if args.include_info:
        info = ticker.info or {}
        result["info"] = {
            "shortName": info.get("shortName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "marketCap": info.get("marketCap"),
            "enterpriseValue": info.get("enterpriseValue"),
            "forwardPE": info.get("forwardPE"),
            "trailingPE": info.get("trailingPE"),
            "priceToSalesTrailing12Months": info.get("priceToSalesTrailing12Months"),
            "beta": info.get("beta"),
            "dividendYield": info.get("dividendYield"),
            "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
            "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"),
            "averageVolume": info.get("averageVolume"),
            "sharesOutstanding": info.get("sharesOutstanding"),
            "currency": info.get("currency"),
        }

    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()

