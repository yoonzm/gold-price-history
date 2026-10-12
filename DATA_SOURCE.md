# Gold price history

Daily XAU/USD (USD per troy ounce) OHLC data.

## Source
Stooq CSV: https://stooq.com/q/d/l/?s=xauusd&i=d

## Refresh
GitHub Actions runs at 03:30 UTC every day and can also be run manually from Actions > Update daily gold prices > Run workflow. A push of the script or workflow also triggers a run. The first successful run backfills all history available from the provider.

## Format
`data/gold_prices.json` contains `prices`, keyed by ISO date, with `open`, `high`, `low`, `close`. `count`, `first_date`, and `last_date` describe coverage. Non-trading dates are omitted. Dates and closing conventions follow the source provider.

## Important
The initial committed JSON is an EMPTY placeholder (count=0), not historical data. Historical records only appear after the first successful workflow run. This project does not guarantee every calendar day, all-time coverage, exchange-specific official settlement prices, or uninterrupted provider availability. Validate provider licensing and attribution requirements before redistribution or commercial use. If GitHub Actions cannot push, check repository Actions workflow permissions for read/write access.
