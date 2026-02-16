#!/usr/bin/env python3
"""Compute total sales cost from a product catalogue and a sales record."""

# pylint: disable=invalid-name

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


RESULTS_FILE = Path("SalesResults.txt")


def eprint(msg: str) -> None:
    """Print a message to stderr."""
    print(msg, file=sys.stderr)


def load_json(path: Path) -> Optional[Any]:
    """Load JSON from a file path."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        eprint(f"[ERROR] Cannot load JSON from {path}: {exc}")
        return None


def build_price_map(catalogue: Any) -> Dict[str, float]:
    """Build a mapping of product title -> price from catalogue JSON."""
    prices: Dict[str, float] = {}

    if not isinstance(catalogue, list):
        eprint("[ERROR] Catalogue JSON must be a list.")
        return prices

    for idx, item in enumerate(catalogue):
        if not isinstance(item, dict):
            eprint(f"[ERROR] Catalogue item #{idx} is not an object. Skipping.")
            continue

        title = item.get("title")
        price = item.get("price")

        if not isinstance(title, str) or not title.strip():
            eprint(f"[ERROR] Catalogue item #{idx} has invalid title. Skipping.")
            continue

        try:
            price_value = float(price)
        except (TypeError, ValueError):
            eprint(
                f"[ERROR] Catalogue item #{idx} has invalid price for '{title}'. "
                "Skipping."
            )
            continue

        if price_value < 0:
            eprint(
                f"[ERROR] Catalogue item #{idx} has negative price for '{title}'. "
                "Skipping."
            )
            continue

        prices[title] = price_value

    return prices


def compute_total(
    prices: Dict[str, float],
    sales: Any,
) -> Tuple[float, List[str], List[str]]:
    """Compute total cost (negative quantities are included)."""
    total = 0.0
    warnings: List[str] = []
    errors: List[str] = []

    if not isinstance(sales, list):
        errors.append("[ERROR] Sales JSON must be a list.")
        return total, warnings, errors

    for idx, row in enumerate(sales):
        if not isinstance(row, dict):
            errors.append(f"[ERROR] Sales row #{idx} is not an object. Skipping.")
            continue

        product = row.get("Product")
        quantity = row.get("Quantity")

        if not isinstance(product, str) or not product.strip():
            errors.append(
                f"[ERROR] Sales row #{idx} missing/invalid Product. Skipping."
            )
            continue

        try:
            qty = float(quantity)
        except (TypeError, ValueError):
            errors.append(f"[ERROR] Invalid Quantity for '{product}'. Skipping.")
            continue

        if product not in prices:
            warnings.append(
                f"[WARN] Product not found in catalogue: '{product}'. Skipping."
            )
            continue

        total += prices[product] * qty

    return total, warnings, errors


def build_report(
    catalogue_path: Path,
    sales_path: Path,
    total: float,
    warnings: List[str],
    errors: List[str],
    stats: Dict[str, float],
) -> str:
    """Build a human-readable report for console and output file."""
    elapsed = stats.get("elapsed_seconds", 0.0)

    lines: List[str] = [
        "=== Sales Computation Results ===",
        f"Catalogue: {catalogue_path}",
        f"Sales:     {sales_path}",
        "",
        f"TOTAL COST: {total:,.2f}",
        "",
        "Errors (skipped):",
    ]

    if errors:
        lines.extend(f"- {msg}" for msg in errors)
    else:
        lines.append("- None")

    lines.extend(["", "Warnings (skipped):"])

    if warnings:
        lines.extend(f"- {msg}" for msg in warnings)
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            f"Elapsed time (s): {elapsed:.6f}",
            "===============================",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: List[str]) -> int:
    """Run the program."""
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

    elapsed_seconds = time.perf_counter() - start
    stats = {"elapsed_seconds": elapsed_seconds}

    report = build_report(
        catalogue_path=catalogue_path,
        sales_path=sales_path,
        total=total,
        warnings=warnings,
        errors=errors,
        stats=stats,
    )

    print(report)
    try:
        RESULTS_FILE.write_text(report, encoding="utf-8")
    except OSError as exc:
        eprint(f"[ERROR] Could not write {RESULTS_FILE}: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
