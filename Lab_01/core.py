from copy import deepcopy
from typing import Callable, Dict, Iterable, List, Optional, Tuple, TypeVar, TypedDict

class Product(TypedDict, total=False):
    id: int
    name: str
    category: str
    stock: int
    min_stock: int
    unit_price: float
    reorder_qty: int
    total_cost: float
    timestamp: float

class InventoryResult(TypedDict):
    count: int
    total_cost: float
    products: List[Product]

ReorderCheckFn = Callable[[Product], bool]
DiscountFn = Callable[[float], float]
CostFn = Callable[[float], float]
NowFn = Callable[[], float]

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

def calculate_reorder_qty(product: Product) -> int:
    deficit = product["min_stock"] - product["stock"]
    return max(0, deficit)

def base_reorder_cost(product: Product, qty: int) -> float:
    return qty * product["unit_price"]

def with_reorder_info(
    product: Product,
    reorder_qty: int,
    total_cost: float,
    timestamp: Optional[float] = None,
) -> Product:
    new_product: Product = deepcopy(product)
    new_product["reorder_qty"] = reorder_qty
    new_product["total_cost"] = total_cost
    if timestamp is not None:
        new_product["timestamp"] = timestamp
    return new_product

def compose(f: Callable[[B], C], g: Callable[[A], B]) -> Callable[[A], C]:
    return lambda x: f(g(x))

def make_multiplier(k: float) -> Callable[[float], float]:
    return lambda x: x * k

def stamp_cost(cost: float, now: NowFn) -> Tuple[float, float]:
    return cost, now()

def process_inventory_pure(
    products: Iterable[Product],
    *,
    discount_rate: float,
    tax_rate: float,
) -> InventoryResult:
    reorder_items: List[Product] = []
    total_reorder_cost: float = 0.0

    for p in products:
        if p["stock"] >= p["min_stock"]:
            continue

        qty = calculate_reorder_qty(p)
        subtotal = base_reorder_cost(p, qty)
        cost = subtotal * (1.0 - discount_rate) * (1.0 + tax_rate)

        new_p = with_reorder_info(p, qty, cost)
        reorder_items.append(new_p)
        total_reorder_cost += cost

    return {
        "count": len(reorder_items),
        "total_cost": total_reorder_cost,
        "products": reorder_items,
    }

def make_processor(
    *,
    should_reorder: ReorderCheckFn,
    apply_discount: DiscountFn,
    apply_tax: CostFn,
    now: Optional[NowFn] = None,
) -> Callable[[Iterable[Product]], InventoryResult]:
    def process(products: Iterable[Product]) -> InventoryResult:
        reorder_items: List[Product] = []
        total_reorder_cost: float = 0.0

        for p in products:
            if not should_reorder(p):
                continue

            qty = calculate_reorder_qty(p)
            subtotal = base_reorder_cost(p, qty)
            discounted = apply_discount(subtotal)
            final_cost = apply_tax(discounted)

            ts = now() if now is not None else None
            new_p = with_reorder_info(p, qty, final_cost, timestamp=ts)

            reorder_items.append(new_p)
            total_reorder_cost += final_cost

        return {
            "count": len(reorder_items),
            "total_cost": total_reorder_cost,
            "products": reorder_items,
        }

    return process