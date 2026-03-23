#!/usr/bin/env python3
import argparse
import json
from datetime import datetime


def normalize_item(item: dict) -> dict:
    content = item.get("content", {}) if isinstance(item, dict) else {}
    canonical = content.get("canonicalUrl", {}) if isinstance(content, dict) else {}
    provider = item.get("provider") if isinstance(item, dict) else None
    return {
        "title": content.get("title") or item.get("title"),
        "summary": content.get("summary") or item.get("summary"),
        "publisher": provider.get("displayName") if isinstance(provider, dict) else item.get("publisher"),
        "published_at": content.get("pubDate") or item.get("providerPublishTime"),
        "url": canonical.get("url") or item.get("link"),
        "type": content.get("contentType"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch ticker-linked news via yfinance.")
    parser.add_argument("--symbol", required=True, help="Ticker symbol, for example NVDA")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of news items")
    args = parser.parse_args()

    try:
        import yfinance as yf
    except ImportError as exc:
        raise SystemExit('yfinance is not installed in the selected Python environment.') from exc

    ticker = yf.Ticker(args.symbol)
    raw_news = ticker.news or []
    news = [normalize_item(item) for item in raw_news[: args.limit]]

    result = {
        "symbol": args.symbol.upper(),
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "count": len(news),
        "news": news,
    }
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()

