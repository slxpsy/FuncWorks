import time
from typing import List
from core import (
    Product,
    InventoryResult,
    compose,
    make_multiplier,
    make_processor,
    process_inventory_pure,
)

def render_report(result: InventoryResult) -> None:
    print("=" * 65)
    print("           ЗВІТ СКЛАДСЬКОГО ОБЛІКУ (ДОЗАМОВЛЕННЯ)           ")
    print("=" * 65)
    for p in result["products"]:
        ts_str = f" | time: {p['timestamp']:.2f}" if "timestamp" in p else ""
        print(
            f" ID: {p['id']:<3} | {p['name']:<15} | Qty: {p['reorder_qty']:>3} | Cost: ${p['total_cost']:>8.2f}{ts_str}"
        )
    print("-" * 65)
    print(f" Позицій для дозамовлення : {result['count']}")
    print(f" Загальна вартість       : ${result['total_cost']:.2f}")
    print("=" * 65)

def run() -> None:
    sample_products: List[Product] = [
        {"id": 1, "name": "Клавіатура", "category": "Периферія", "stock": 3, "min_stock": 10, "unit_price": 45.0},
        {"id": 2, "name": "Монітор", "category": "Дисплеї", "stock": 15, "min_stock": 5, "unit_price": 200.0},
        {"id": 3, "name": "Мишка", "category": "Периферія", "stock": 2, "min_stock": 15, "unit_price": 25.0},
        {"id": 4, "name": "Кабель HDMI", "category": "Аксесуари", "stock": 8, "min_stock": 8, "unit_price": 10.0},
    ]

    res1 = process_inventory_pure(sample_products, discount_rate=0.05, tax_rate=0.2)
    render_report(res1)

    bulk_discount = make_multiplier(0.85)
    partner_discount = make_multiplier(0.95)
    combined_discount = compose(partner_discount, bulk_discount)

    tax_policy = make_multiplier(1.20)
    reorder_policy = lambda p: p["stock"] < p["min_stock"]

    processor = make_processor(
        should_reorder=reorder_policy,
        apply_discount=combined_discount,
        apply_tax=tax_policy,
        now=time.time,
    )

    res2 = processor(sample_products)
    render_report(res2)

if __name__ == "__main__":
    run()