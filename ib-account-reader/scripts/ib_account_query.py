#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional

from ib_insync import IB


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read Interactive Brokers account data and emit normalized JSON."
    )
    parser.add_argument(
        "command",
        choices=["snapshot", "positions", "account-summary", "open-orders"],
        help="Data to fetch from IB.",
    )
    parser.add_argument("--host", default="127.0.0.1", help="IB Gateway or TWS host.")
    parser.add_argument(
        "--port", type=int, default=4001, help="IB Gateway or TWS API port."
    )
    parser.add_argument(
        "--client-id",
        type=int,
        default=101,
        help="API client ID. Use a different value if this ID is already connected.",
    )
    parser.add_argument(
        "--account",
        default=None,
        help="Optional IB account code filter such as U1234567.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="Connection timeout in seconds.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON for human inspection.",
    )
    return parser


def to_number(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (int, float, bool)):
        return value
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, str):
        text = value.strip()
        if text == "":
            return ""
        try:
            if "." in text or "e" in text.lower():
                return float(text)
            return int(text)
        except ValueError:
            return value
    return value


def contract_to_dict(contract: Any) -> Dict[str, Any]:
    return {
        "conId": getattr(contract, "conId", None),
        "symbol": getattr(contract, "symbol", None),
        "localSymbol": getattr(contract, "localSymbol", None),
        "secType": getattr(contract, "secType", None),
        "exchange": getattr(contract, "exchange", None),
        "primaryExchange": getattr(contract, "primaryExchange", None),
        "currency": getattr(contract, "currency", None),
        "lastTradeDateOrContractMonth": getattr(
            contract, "lastTradeDateOrContractMonth", None
        ),
        "multiplier": getattr(contract, "multiplier", None),
    }


def summarize_account(rows: List[Any], account_filter: Optional[str]) -> Dict[str, Any]:
    summary: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        account = getattr(row, "account", None)
        if account_filter and account != account_filter:
            continue
        if account not in summary:
            summary[account] = {}
        summary[account][getattr(row, "tag", "")] = {
            "value": to_number(getattr(row, "value", None)),
            "currency": getattr(row, "currency", None),
        }
    return summary


def portfolio_to_dict(items: List[Any], account_filter: Optional[str]) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for item in items:
        if account_filter and getattr(item, "account", None) != account_filter:
            continue
        results.append(
            {
                "account": getattr(item, "account", None),
                "contract": contract_to_dict(getattr(item, "contract", None)),
                "position": to_number(getattr(item, "position", None)),
                "marketPrice": to_number(getattr(item, "marketPrice", None)),
                "marketValue": to_number(getattr(item, "marketValue", None)),
                "averageCost": to_number(getattr(item, "averageCost", None)),
                "unrealizedPNL": to_number(getattr(item, "unrealizedPNL", None)),
                "realizedPNL": to_number(getattr(item, "realizedPNL", None)),
            }
        )
    return results


def open_orders_to_dict(trades: List[Any], account_filter: Optional[str]) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for trade in trades:
        order = getattr(trade, "order", None)
        contract = getattr(trade, "contract", None)
        status = getattr(getattr(trade, "orderStatus", None), "status", None)
        account = getattr(order, "account", None)
        if account_filter and account != account_filter:
            continue
        results.append(
            {
                "account": account,
                "status": status,
                "orderId": getattr(order, "orderId", None),
                "permId": getattr(order, "permId", None),
                "action": getattr(order, "action", None),
                "orderType": getattr(order, "orderType", None),
                "totalQuantity": to_number(getattr(order, "totalQuantity", None)),
                "lmtPrice": to_number(getattr(order, "lmtPrice", None)),
                "auxPrice": to_number(getattr(order, "auxPrice", None)),
                "tif": getattr(order, "tif", None),
                "contract": contract_to_dict(contract),
            }
        )
    return results


def fetch_payload(ib: IB, command: str, account: Optional[str]) -> Dict[str, Any]:
    if command == "account-summary":
        return {
            "account_summary": summarize_account(ib.accountSummary(), account),
        }
    if command == "positions":
        return {
            "portfolio": portfolio_to_dict(ib.portfolio(), account),
        }
    if command == "open-orders":
        return {
            "open_orders": open_orders_to_dict(ib.openTrades(), account),
        }
    return {
        "account_summary": summarize_account(ib.accountSummary(), account),
        "portfolio": portfolio_to_dict(ib.portfolio(), account),
        "open_orders": open_orders_to_dict(ib.openTrades(), account),
    }


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    ib = IB()
    ib.connect(args.host, args.port, clientId=args.client_id, timeout=args.timeout)

    try:
        payload = fetch_payload(ib, args.command, args.account)
        payload["connection"] = {
            "host": args.host,
            "port": args.port,
            "client_id": args.client_id,
            "connected": ib.isConnected(),
        }
        payload["generated_at"] = datetime.now(timezone.utc).isoformat()
        text = json.dumps(payload, indent=2 if args.pretty else None, sort_keys=True)
        print(text)
        return 0
    finally:
        if ib.isConnected():
            ib.disconnect()


if __name__ == "__main__":
    raise SystemExit(main())
