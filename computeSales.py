import json
import sys


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python computeSales.py priceCatalogue.json salesRecord.json")
        return

    catalogue_path = sys.argv[1]
    sales_path = sys.argv[2]

    with open(catalogue_path, "r", encoding="utf-8") as f:
        catalogue = json.load(f)

    with open(sales_path, "r", encoding="utf-8") as f:
        sales = json.load(f)

    prices = {item["product"]: float(item["price"]) for item in catalogue}

    total = 0.0
    for row in sales:
        total += prices[row["product"]] * float(row["quantity"])

    print(f"TOTAL COST: {total:.2f}")


if __name__ == "__main__":
    main()
