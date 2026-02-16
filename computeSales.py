import json
import sys
from pathlib import Path


RESULTS_FILE = Path("SalesResults.txt")


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python computeSales.py priceCatalogue.json salesRecord.json")
        return 2

    catalogue_path = sys.argv[1]
    sales_path = sys.argv[2]

    with open(catalogue_path, "r", encoding="utf-8") as f:
        catalogue = json.load(f)

    with open(sales_path, "r", encoding="utf-8") as f:
        sales = json.load(f)

    prices = {item["title"]: float(item["price"]) for item in catalogue}

    total = 0.0
    warnings = []
    errors = []

    for row in sales:
        product = row.get("Product")
        quantity = row.get("Quantity")

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

    report_lines = [
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
    ]
    report = "\n".join(report_lines)

    print(report)
    RESULTS_FILE.write_text(report, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
