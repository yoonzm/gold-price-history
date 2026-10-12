#!/usr/bin/env python3
"""Import historical XAUUSD daily OHLC from a public MetaTrader-derived CSV."""
import csv
import io
import json
import math
from datetime import datetime, date
from pathlib import Path
from urllib.request import Request, urlopen

URL = "https://raw.githubusercontent.com/FeziweMelvin/XAUUSD-Gold-Price/main/XAU_1d_data.csv"
OUTPUT = Path("data/gold_prices.json")

def main():
    req = Request(URL, headers={"User-Agent": "gold-price-history/1.1", "Accept": "text/plain"})
    with urlopen(req, timeout=45) as response:
        raw = response.read().decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(raw), delimiter=";")
    if not reader.fieldnames or not {"Date","Open","High","Low","Close"}.issubset(reader.fieldnames):
        raise ValueError("Unexpected upstream schema")
    prices = {}
    for row in reader:
        day = datetime.strptime(row["Date"].strip(), "%Y.%m.%d %H:%M").date()
        if day > date.today():
            continue
        ohlc = {k.lower(): float(row[k]) for k in ("Open","High","Low","Close")}
        if any(not math.isfinite(v) or v <= 0 for v in ohlc.values()):
            raise ValueError(f"Invalid numeric price for {day}")
        if ohlc["high"] < max(ohlc.values()) or ohlc["low"] > min(ohlc.values()):
            raise ValueError(f"Invalid OHLC range for {day}")
        key = day.isoformat()
        if key in prices:
            raise ValueError(f"Duplicate date: {key}")
        prices[key] = ohlc
    if len(prices) < 1000:
        raise ValueError("Incomplete upstream history; refusing overwrite")
    output = {
        "symbol": "XAUUSD", "currency": "USD", "unit": "troy_ounce",
        "frequency": "daily", "source": URL,
        "first_date": min(prices), "last_date": max(prices),
        "count": len(prices), "prices": dict(sorted(prices.items()))
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(output, ensure_ascii=False, indent=2) + "\n"
    if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != rendered:
        OUTPUT.write_text(rendered, encoding="utf-8")
        print(f"Saved {len(prices)} records through {max(prices)}")
    else:
        print("No changes")
    if (date.today() - date.fromisoformat(max(prices))).days > 7:
        print("WARNING: upstream data is stale; this source does not cover current prices.")

if __name__ == "__main__":
    main()
