import json
import sys


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
    for row in sales:
        product = row.get("Product")
        quantity = row.get("Quantity")

        try:
            qty = float(quantity)
        except (TypeError, ValueError):
            print(f"[ERROR] Invalid quantity for '{product}'. Skipping.")
            continue

        if qty < 0:
            print(f"[ERROR] Negative quantity for '{product}' ({qty}). Skipping.")
            continue

        if product not in prices:
            print(f"[WARN] Product not found: '{product}'. Skipping.")
            continue

        total += prices[product] * qty

    print(f"TOTAL COST: {total:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
