#!/usr/bin/env python3
"""Fetch XAU/USD daily history from a non-GitHub public API (XAUS)."""
import json
import math
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

URL = "https://xaus.com/api/v1/history"
OUT = Path("data/gold_prices.json")

def main():
    req = Request(URL, headers={"User-Agent": "gold-price-history/2.0", "Accept": "application/json"})
    with urlopen(req, timeout=40) as response:
        payload = json.load(response)
    if payload.get("symbol") != "XAUUSD" or not isinstance(payload.get("points"), list):
        raise ValueError("Unexpected history response; refusing overwrite")
    prices = {}
    for item in payload["points"]:
        day = str(item["d"])
        date.fromisoformat(day)
        if day > date.today().isoformat():
            continue
        close = float(item["c"])
        if not math.isfinite(close) or close <= 0:
            raise ValueError(f"Invalid close: {day}")
        record = {"close": close}
        for short, full in (("o", "open"), ("h", "high"), ("l", "low")):
            if item.get(short) is not None:
                value = float(item[short])
                if not math.isfinite(value) or value <= 0:
                    raise ValueError(f"Invalid {full}: {day}")
                record[full] = value
        if "high" in record and record["high"] < close:
            raise ValueError(f"Invalid high: {day}")
        if "low" in record and record["low"] > close:
            raise ValueError(f"Invalid low: {day}")
        if day in prices:
            raise ValueError(f"Duplicate date: {day}")
        prices[day] = record
    if len(prices) < 200:
        raise ValueError(f"Insufficient history ({len(prices)} days); refusing overwrite")
    result = {
        "symbol": "XAUUSD", "currency": "USD", "unit": "troy_ounce",
        "frequency": "daily", "source": URL, "license_note": "API data free to use; attribution to xaus.com",
        "first_date": min(prices), "last_date": max(prices), "count": len(prices),
        "prices": dict(sorted(prices.items()))
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
        OUT.write_text(text, encoding="utf-8")
        print(f"Saved {len(prices)} days, {min(prices)} through {max(prices)}")
    else:
        print("No changes")
    if (date.today() - date.fromisoformat(max(prices))).days > 7:
        print("WARNING: history is older than 7 days")

if __name__ == "__main__":
    main()
