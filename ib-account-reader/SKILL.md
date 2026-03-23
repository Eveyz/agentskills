---
name: ib-account-reader
description: Read live Interactive Brokers account data through a local IB Gateway or TWS session using ib_insync and a preconfigured conda environment. Use when Codex needs current portfolio holdings, account summary values, net liquidation, cash balances, open orders, or a machine-readable account snapshot from the user's IB account without placing trades.
---

# IB Account Reader

Read live IB account data in a safe, read-only way and prefer the bundled scripts over ad hoc Python snippets.

## Required Runtime

- Local IB Gateway or TWS must already be running and accepting API connections.
- `conda` must be available.
- The `finance` conda environment must contain `ib_insync`.

## Required Script

Run [scripts/run_ib_account_query.ps1](scripts/run_ib_account_query.ps1) for all account reads.

The wrapper calls [scripts/ib_account_query.py](scripts/ib_account_query.py) inside `conda run -n finance`, which keeps the environment and JSON output consistent across skills.

## Default Connection Assumptions

- Host: `127.0.0.1`
- Port: `4001` for live IB Gateway
- Client ID: `101`

Override these with flags when needed. If the user mentions paper trading, switch the port to `4002` unless they specify otherwise.

## Primary Commands

### Full Snapshot

Use this when another skill needs the whole account state:

```powershell
powershell -ExecutionPolicy Bypass -File .\ib-account-reader\scripts\run_ib_account_query.ps1 snapshot
```

This returns JSON with:

- `account_summary`
- `portfolio`
- `open_orders`
- `connection`
- `generated_at`

### Positions Only

Use this when only holdings are needed:

```powershell
powershell -ExecutionPolicy Bypass -File .\ib-account-reader\scripts\run_ib_account_query.ps1 positions
```

### Account Summary Only

Use this when only balances or margin data are needed:

```powershell
powershell -ExecutionPolicy Bypass -File .\ib-account-reader\scripts\run_ib_account_query.ps1 account-summary
```

### Open Orders Only

Use this when checking pending activity:

```powershell
powershell -ExecutionPolicy Bypass -File .\ib-account-reader\scripts\run_ib_account_query.ps1 open-orders
```

## Operating Rules

- Keep usage read-only. Do not place, modify, or cancel orders from this skill.
- Prefer `snapshot` unless the caller clearly needs a narrower payload.
- Return the script JSON directly when another skill needs structured input.
- If you summarize the output for the user, preserve the key figures exactly and label any inference as an inference.
- If the connection fails, report the exact host, port, and client ID used and suggest checking API settings or choosing a different client ID.

## Common Flags

- `--host 127.0.0.1`
- `--port 4001`
- `--client-id 101`
- `--account U1234567`
- `--pretty`

Example:

```powershell
powershell -ExecutionPolicy Bypass -File .\ib-account-reader\scripts\run_ib_account_query.ps1 snapshot --account U1234567 --pretty
```

## How Other Skills Should Use This Skill

1. Call the wrapper script and capture its JSON output.
2. Reuse the returned `portfolio` and `account_summary` fields instead of re-querying unless a fresher read is required.
3. Keep the original raw JSON available when downstream calculations depend on exact numeric fields.

## Failure Handling

- If `conda` is unavailable, stop and say the runtime is missing.
- If `ib_insync` is missing in `finance`, stop and say the environment needs that package.
- If IB rejects the connection, stop and report the connection parameters used.
- If the payload is empty, do not guess; return the empty result and say no data was returned.
