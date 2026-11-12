from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from functools import reduce
from itertools import islice
from typing import Any, TypedDict


class Record(TypedDict, total=False):
    id: int
    name: str
    tariff: str
    payments: list[float]
    total: float


class StatsResult(TypedDict):
    count: int
    payments_sum: float
    avg_payment: float


class _Acc(TypedDict):
    count: int
    payments_sum: float


def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    def _c(x: Any) -> Any:
        for f in reversed(funcs):
            x = f(x)
        return x

    return _c


def pipe(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    def _p(x: Any) -> Any:
        for f in funcs:
            x = f(x)
        return x

    return _p


def _set_total(r: Record) -> Record:
    return {**r, "total": float(sum(r.get("payments", []) or []))}


def _apply_bonus(r: Record, tariff: str, factor: float) -> Record:
    t = float(r.get("total", 0.0))
    return {**r, "total": (t * factor) if r.get("tariff") == tariff else t}


def _normalize_name(r: Record) -> Record:
    return {**r, "name": str(r.get("name", "")).strip().title()}


def normalize_names() -> Callable[[Iterable[Record]], Iterator[Record]]:
    return lambda recs: map(_normalize_name, recs)


def with_total() -> Callable[[Iterable[Record]], Iterator[Record]]:
    return lambda recs: map(_set_total, recs)


def boost_tariff(tariff: str, factor: float) -> Callable[[Iterable[Record]], Iterator[Record]]:
    return lambda recs: (_apply_bonus(r, tariff, factor) for r in recs)


def only_active(min_payment: float = 0.01) -> Callable[[Iterable[Record]], Iterator[Record]]:
    return lambda recs: filter(lambda r: float(r.get("total", 0.0)) >= min_payment, recs)


def sort_by_total_desc() -> Callable[[Iterable[Record]], list[Record]]:
    return lambda recs: sorted(
        recs,
        key=lambda r: (-float(r.get("total", 0.0)), int(r.get("id", 0))),
    )


def take(n: int) -> Callable[[Iterable[Record]], list[Record]]:
    return lambda recs: list(islice(recs, n))


def reduce_stats(recs: Iterable[Record]) -> StatsResult:
    init: _Acc = {"count": 0, "payments_sum": 0.0}
    acc = reduce(
        lambda a, r: {
            "count": a["count"] + 1,
            "payments_sum": a["payments_sum"] + float(r.get("total", 0.0)),
        },
        recs,
        init,
    )
    avg = acc["payments_sum"] / acc["count"] if acc["count"] > 0 else 0.0
    return {
        "count": acc["count"],
        "payments_sum": acc["payments_sum"],
        "avg_payment": avg,
    }


def build_pipeline(
    top_n: int = 3,
    tariff: str = "Premium",
    factor: float = 1.2,
    min_payment: float = 0.01,
) -> Callable[[Iterable[Record]], list[Record]]:
    return compose(
        take(top_n),
        sort_by_total_desc(),
        only_active(min_payment),
        boost_tariff(tariff, factor),
        with_total(),
        normalize_names(),
    )
