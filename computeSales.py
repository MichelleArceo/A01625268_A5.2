#!/usr/bin/env python3
"""
Compute total sales cost from a product catalogue and a sales record.
Writes a human-readable report to SalesResults.txt.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


RESULTS_FILE = Path("SalesResults.txt")


def eprint(msg: str) -> None:
    print(msg, file=sys.stderr)


def load_json(path: Path) -> Optional[Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        eprint(f"[ERROR] Cannot load JSON from {path}: {exc}")
        return None


def build_price_map(catalogue: Any) -> Dict[str, float]:
    prices: Dict[str, float] = {}
    if not isinstance(catalogue, list):
        eprint("[ERROR] Catalogue JSON must be a list.")
        return prices

    for item in catalogue:
        if not isinstance(item, dict):
            continue
        title = item.get("title")
        price = item.get("price")
        if not isinstance(title, str) or not title.strip():
            continue
        try:
            price_value = float(price)
        except (TypeError, ValueError):
            continue
        if price_value >= 0:
            prices[title] = price_value

    return prices


def compute_total(
    prices: Dict[str, float],
    sales: Any,
) -> Tuple[float, List[str], List[str]]:
    total = 0.0
    warnings: List[str] = []
    errors: List[str] = []

    if not isinstance(sales, list):
        errors.append("[ERROR] Sales JSON must be a list.")
        return total, warnings, errors

    for row in sales:
        if not isinstance(row, dict):
            errors.append("[ERROR] Invalid sales row format. Skipping.")
            continue

        product = row.get("Product")
        quantity = row.get("Quantity")

        if not isinstance(product, str) or not product.strip():
            errors.append("[ERROR] Missing or invalid Product. Skipping.")
            continue

        try:
            qty = float(quantity)
        except (TypeError, ValueError):
            errors.append(f"[ERROR] Invalid quantity for '{product}'. Skipping.")
            continue

        if qty < 0:
            errors.append(f"[ERROR] Negative quantity for '{product}' ({qty}). Skipping.")
            continue

        if product not in prices:
            warnings.append(f"[WARN] Product not found: '{product}'. Skipping.")
            continue

        total += prices[product] * qty

    return total, warnings, errors


def build_report(
    catalogue_path: Path,
    sales_path: Path,
    total: float,
    warnings: List[str],
    errors: List[str],
    elapsed: float,
) -> str:
    lines = [
        "=== Sales Computation Results ===",
        f"Catalogue: {catalogue_path}",
        f"Sales:     {sales_path}",
        "",
        f"TOTAL COST: {total:,.2f}",
        "",
        "Errors (skipped):",
        *([f"- {e}" for e in errors] or ["- None"]),
        "",
        "Warnings (skipped):",
        *([f"- {w}" for w in warnings] or ["- None"]),
        "",
        f"Elapsed time (s): {elapsed:.6f}",
        "===============================",
        "",
    ]
    return "\n".join(lines)


def main(argv: List[str]) -> int:
    if len(argv) != 3:
        eprint("Usage: python computeSales.py priceCatalogue.json salesRecord.json")
        return 2

    catalogue_path = Path(argv[1])
    sales_path = Path(argv[2])

    start = time.perf_counter()

    catalogue = load_json(catalogue_path)
    sales = load_json(sales_path)
    if catalogue is None or sales is None:
        return 1

    prices = build_price_map(catalogue)
    total, warnings, errors = compute_total(prices, sales)

    elapsed = time.perf_counter() - start
    report = build_report(catalogue_path, sales_path, total, warnings, errors, elapsed)

    print(report)
    RESULTS_FILE.write_text(report, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
