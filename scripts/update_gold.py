#!/usr/bin/env python3
"""Fetch and validate daily XAU/USD OHLC prices from Stooq."""
import csv
import io
import json
import math
import os
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

URL = "https://stooq.com/q/d/l/?s=xauusd&i=d"
OUTPUT = Path("data/gold_prices.json")

def main():
    request = Request(URL, headers={"User-Agent": "Mozilla/5.0 gold-price-history/1.0"})
    with urlopen(request, timeout=90) as response:
        content = response.read().decode("utf-8-sig")
    rows = csv.DictReader(io.StringIO(content))
    if not rows.fieldnames or not {"Date", "Open", "High", "Low", "Close"}.issubset(rows.fieldnames):
        raise ValueError("Unexpected CSV schema; refusing to overwrite existing data")
    prices = {}
    today = date.today()
    for row in rows:
        day = date.fromisoformat(row["Date"].strip())
        if day > today:
            continue
        values = {k.lower(): float(row[k]) for k in ("Open", "High", "Low", "Close")}
        if not all(math.isfinite(v) and v > 0 for v in values.values()):
            raise ValueError(f"Invalid price for {day}")
        if values["high"] < max(values.values()) or values["low"] > min(values.values()):
            raise ValueError(f"Invalid OHLC range for {day}")
        key = day.isoformat()
        if key in prices:
            raise ValueError(f"Duplicate date: {key}")
        prices[key] = values
    if len(prices) < 1000:
        raise ValueError(f"Only {len(prices)} rows returned; refusing partial overwrite")
    payload = {
        "symbol": "XAUUSD",
        "currency": "USD",
        "unit": "troy_ounce",
        "frequency": "daily",
        "source": URL,
        "first_date": min(prices),
        "last_date": max(prices),
        "count": len(prices),
        "prices": dict(sorted(prices.items()))
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != rendered:
        OUTPUT.write_text(rendered, encoding="utf-8")
        print(f"Saved {len(prices)} daily records through {max(prices)}")
    else:
        print("No changes")

if __name__ == "__main__":
    main()
