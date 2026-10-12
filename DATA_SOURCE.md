# XAU/USD daily gold prices

## Source

Daily historical indicative spot gold data: https://xaus.com/api/v1/history
Documentation: https://xaus.com/api/

Source: XAUS (https://xaus.com/). The publisher describes the API as free to use and appreciates attribution; it is not a government or exchange official benchmark. API history covers **up to five years**, not all historical dates. The publisher's public wording does not expressly grant an irrevocable bulk redistribution licence. Confirm redistribution permission before treating the public repository as a licensed historical-data mirror.

## Format

`data/gold_prices.json`: USD per troy ounce, date-keyed prices, with a required `close` and optional `open`, `high`, `low` when actually supplied by the API. Missing fields are not invented. Non-trading dates are omitted. `source`, `first_date`, `last_date` and `count` document coverage.

## Updates

Workflow runs daily at 03:30 UTC, on manual dispatch and when script/workflow changes. Each run validates the API response and refuses unexpectedly short or malformed data. If the upstream API fails, existing data remains unchanged. A count=0 placeholder is not real historical data.

## Licensing and limitations

This is indicative market data, not LBMA official benchmark or exchange settlement. Attribution: XAUS — https://xaus.com/. Verify provider data provenance and redistribution rights before commercial or bulk publication. The initial API schema and GitHub Actions network reachability must be verified on a successful workflow run.
