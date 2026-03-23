#!/usr/bin/env python3
import argparse
import json
from datetime import datetime


def frame_to_rows(frame, limit: int) -> list:
    if frame is None or frame.empty:
        return []
    rows = []
    for _, row in frame.head(limit).iterrows():
        rows.append(
            {
                "contractSymbol": row.get("contractSymbol"),
                "strike": None if row.get("strike") is None else float(row.get("strike")),
                "lastPrice": None if row.get("lastPrice") is None else float(row.get("lastPrice")),
                "bid": None if row.get("bid") is None else float(row.get("bid")),
                "ask": None if row.get("ask") is None else float(row.get("ask")),
                "change": None if row.get("change") is None else float(row.get("change")),
                "percentChange": None if row.get("percentChange") is None else float(row.get("percentChange")),
                "volume": None if row.get("volume") is None else float(row.get("volume")),
                "openInterest": None if row.get("openInterest") is None else float(row.get("openInterest")),
                "impliedVolatility": None if row.get("impliedVolatility") is None else float(row.get("impliedVolatility")),
                "inTheMoney": bool(row.get("inTheMoney")),
                "expiration": str(row.get("expiration")),
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch options chain data via yfinance.")
    parser.add_argument("--symbol", required=True, help="Ticker symbol, for example TSLA")
    parser.add_argument("--expiration", help="Expiration date in YYYY-MM-DD format")
    parser.add_argument("--limit", type=int, default=10, help="Maximum calls and puts rows to return")
    args = parser.parse_args()

    try:
        import yfinance as yf
    except ImportError as exc:
        raise SystemExit('yfinance is not installed in the selected Python environment.') from exc

    ticker = yf.Ticker(args.symbol)
    expirations = list(ticker.options or [])
    expiration = args.expiration or (expirations[0] if expirations else None)

    chain = ticker.option_chain(expiration) if expiration else None

    result = {
        "symbol": args.symbol.upper(),
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "available_expirations": expirations,
        "selected_expiration": expiration,
        "calls": frame_to_rows(chain.calls if chain else None, args.limit),
        "puts": frame_to_rows(chain.puts if chain else None, args.limit),
    }
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()

