from copy import deepcopy
import pytest
from core import (
    Product,
    compose,
    make_multiplier,
    make_processor,
    process_inventory_pure,
    stamp_cost,
    with_reorder_info,
)

@pytest.fixture
def sample_products() -> list[Product]:
    return [
        {"id": 1, "name": "Клавіатура", "category": "Периферія", "stock": 3, "min_stock": 10, "unit_price": 50.0},
        {"id": 2, "name": "Монітор", "category": "Дисплеї", "stock": 10, "min_stock": 5, "unit_price": 200.0},
        {"id": 3, "name": "Мишка", "category": "Периферія", "stock": 0, "min_stock": 5, "unit_price": 20.0},
    ]

def test_referential_transparency(sample_products: list[Product]) -> None:
    args = {"discount_rate": 0.1, "tax_rate": 0.2}
    r1 = process_inventory_pure(sample_products, **args)
    r2 = process_inventory_pure(sample_products, **args)
    assert r1 == r2

def test_no_mutation(sample_products: list[Product]) -> None:
    original = deepcopy(sample_products)
    process_inventory_pure(sample_products, discount_rate=0.0, tax_rate=0.0)
    assert sample_products == original

def test_callable_policies(sample_products: list[Product]) -> None:
    should_reorder = lambda p: p["stock"] < p["min_stock"]
    apply_discount = lambda cost: cost * 0.9
    apply_tax = lambda cost: cost * 1.2

    processor = make_processor(
        should_reorder=should_reorder,
        apply_discount=apply_discount,
        apply_tax=apply_tax,
    )
    result = processor(sample_products)

    assert result["count"] == 2
    assert pytest.approx(result["total_cost"], 0.01) == 486.0
    assert len(result["products"]) == 2

def test_compose_and_multiplier() -> None:
    discount1 = make_multiplier(0.9)
    discount2 = make_multiplier(0.95)
    combined = compose(discount2, discount1)

    assert combined(100.0) == 85.5

def test_stamp_cost_dependency_injection() -> None:
    fake_now = lambda: 1700000000.0
    cost, ts = stamp_cost(250.0, fake_now)

    assert cost == 250.0
    assert ts == 1700000000.0

def test_with_reorder_info_purity() -> None:
    product: Product = {"id": 1, "name": "Test", "category": "Cat", "stock": 1, "min_stock": 5, "unit_price": 10.0}
    new_product = with_reorder_info(product, 4, 40.0)

    assert "reorder_qty" not in product
    assert "total_cost" not in product
    assert new_product["reorder_qty"] == 4
    assert new_product["total_cost"] == 40.0
    assert new_product is not product