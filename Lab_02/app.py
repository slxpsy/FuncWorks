import argparse

from core import Record, StatsResult, build_pipeline, reduce_stats


def render_report(records: list[Record], stats: StatsResult) -> None:
    print("=" * 65)
    print("             РЕЙТИНГ МОБІЛЬНИХ АБОНЕНТІВ (TOP-N)             ")
    print("=" * 65)
    for r in records:
        print(
            f" ID: {r['id']:<3} | {r['name']:<18} "
            f"| Тариф: {r['tariff']:<10} | Сума: {r['total']:>8.2f}"
        )
    print("-" * 65)
    print(f" Активних у рейтингу : {stats['count']}")
    print(f" Сума платежів       : {stats['payments_sum']:.2f}")
    print(f" Середній платіж     : {stats['avg_payment']:.2f}")
    print("=" * 65)


def get_sample_data() -> list[Record]:
    return [
        {"id": 1, "name": "  олена коваль ", "tariff": "Premium", "payments": [200.0, 250.0]},
        {"id": 2, "name": "іван петренко", "tariff": "Basic", "payments": [100.0, 150.0]},
        {"id": 3, "name": "марія сидоренко", "tariff": "Premium", "payments": []},
        {"id": 4, "name": "дмитро бондар", "tariff": "Standard", "payments": [300.0, 240.0]},
        {"id": 5, "name": "анна мельник", "tariff": "Basic", "payments": [0.0]},
    ]


def run(top_n: int = 2, tariff: str = "Premium", factor: float = 1.2) -> None:
    subscribers = get_sample_data()
    pipeline = build_pipeline(top_n=top_n, tariff=tariff, factor=factor)
    top_subscribers = pipeline(subscribers)
    stats = reduce_stats(top_subscribers)
    render_report(top_subscribers, stats)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--top", type=int, default=2)
    parser.add_argument("--tariff", type=str, default="Premium")
    parser.add_argument("--factor", type=float, default=1.2)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(top_n=args.top, tariff=args.tariff, factor=args.factor)
