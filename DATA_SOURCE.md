# XAU/USD daily gold price history

Gold prices are stored in `data/gold_prices.json` as USD per troy ounce, one record per available trading date (OHLC).

## Data source and coverage

Current import source: https://github.com/FeziweMelvin/XAUUSD-Gold-Price (`XAU_1d_data.csv`, MetaTrader-derived daily bars). At verification on 2026-10-12 the CSV contained dates from 2004-06-11 to 2025-06-06. **This is historical but NOT current data.** The repository upstream README's stated automated refresh was not reflected in the verified file. Do not use it for current quotes, or treat missing days as filled.

The previous Stooq endpoint was removed after a GitHub Actions connection timeout. Data provider licensing/redistribution and broker-specific daily boundaries should be reviewed before commercial use.

## Refresh

GitHub Actions runs at 03:30 UTC daily, on manual dispatch, and when the script/workflow changes. It fetches the upstream file, validates OHLC, and writes JSON only when changed. This does **not** guarantee new prices when the upstream file has not been updated. The script emits a warning if its latest record is older than seven days.

## Schema

`symbol`, `currency`, `unit`, `frequency`, `source`, `first_date`, `last_date`, `count`, and `prices` (date-keyed `open`, `high`, `low`, `close`).

An initial count=0 placeholder is not real data. The first successful action imports full available history.
