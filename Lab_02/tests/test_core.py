from copy import deepcopy

import pytest

from core import (
    Record,
    boost_tariff,
    build_pipeline,
    compose,
    normalize_names,
    only_active,
    pipe,
    reduce_stats,
    sort_by_total_desc,
    take,
    with_total,
)


@pytest.fixture
def sample_subscribers() -> list[Record]:
    return [
        {"id": 1, "name": "  олена коваль ", "tariff": "Premium", "payments": [200.0, 250.0]},
        {"id": 2, "name": "іван петренко", "tariff": "Basic", "payments": [100.0, 150.0]},
        {"id": 3, "name": "марія сидоренко", "tariff": "Premium", "payments": []},
        {"id": 4, "name": "дмитро бондар", "tariff": "Standard", "payments": [300.0, 240.0]},
    ]


def test_no_mutation(sample_subscribers: list[Record]) -> None:
    original = deepcopy(sample_subscribers)
    pipeline = build_pipeline(top_n=3, tariff="Premium", factor=1.2)
    _ = pipeline(sample_subscribers)
    assert sample_subscribers == original


def test_pipeline_top_n_and_tie_breaker(sample_subscribers: list[Record]) -> None:
    pipeline = build_pipeline(top_n=2, tariff="Premium", factor=1.2)
    result = pipeline(sample_subscribers)

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[0]["name"] == "Олена Коваль"
    assert pytest.approx(result[0]["total"], 0.01) == 540.0

    assert result[1]["id"] == 4
    assert result[1]["name"] == "Дмитро Бондар"
    assert pytest.approx(result[1]["total"], 0.01) == 540.0


def test_only_active_filters_zero_payments(sample_subscribers: list[Record]) -> None:
    step = compose(list, only_active(0.01), with_total())
    active = step(sample_subscribers)
    ids = [r["id"] for r in active]
    assert 3 not in ids
    assert ids == [1, 2, 4]


def test_reduce_stats(sample_subscribers: list[Record]) -> None:
    pipeline = build_pipeline(top_n=2, tariff="Premium", factor=1.2)
    top_records = pipeline(sample_subscribers)
    stats = reduce_stats(top_records)

    assert stats["count"] == 2
    assert pytest.approx(stats["payments_sum"], 0.01) == 1080.0
    assert pytest.approx(stats["avg_payment"], 0.01) == 540.0


def test_reduce_stats_empty() -> None:
    stats = reduce_stats([])
    assert stats == {"count": 0, "payments_sum": 0.0, "avg_payment": 0.0}


def test_compose_and_pipe_equivalence(sample_subscribers: list[Record]) -> None:
    c = compose(
        take(2),
        sort_by_total_desc(),
        only_active(),
        boost_tariff("Premium", 1.2),
        with_total(),
        normalize_names(),
    )
    p = pipe(
        normalize_names(),
        with_total(),
        boost_tariff("Premium", 1.2),
        only_active(),
        sort_by_total_desc(),
        take(2),
    )
    assert c(sample_subscribers) == p(sample_subscribers)
