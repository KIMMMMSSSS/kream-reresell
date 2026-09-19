from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PriceDecision:
    reference_price: int
    instant_sell_price: int
    spread: int
    minimum_spread: int | None
    qualifies: bool
    bid_price: int | None
    reason: str


def minimum_spread(reference_price: int) -> int | None:
    if 50_000 <= reference_price < 100_000:
        return 10_000
    if 100_000 <= reference_price < 150_000:
        return 13_000
    if 150_000 <= reference_price < 250_000:
        return 18_000
    if 250_000 <= reference_price < 350_000:
        return 23_000
    if 350_000 <= reference_price <= 450_000:
        return 28_000
    return None


def decide_bid(
    *,
    instant_sell_price: int,
    general_delivery_price: int | None,
    fast_delivery_price: int | None,
) -> PriceDecision:
    valid = [p for p in (general_delivery_price, fast_delivery_price) if p is not None]
    if not valid:
        return PriceDecision(
            reference_price=0,
            instant_sell_price=instant_sell_price,
            spread=0,
            minimum_spread=None,
            qualifies=False,
            bid_price=None,
            reason="유효한 일반/빠른배송 가격이 없음",
        )

    reference = min(valid)
    threshold = minimum_spread(reference)
    spread = reference - instant_sell_price

    if threshold is None:
        return PriceDecision(
            reference_price=reference,
            instant_sell_price=instant_sell_price,
            spread=spread,
            minimum_spread=None,
            qualifies=False,
            bid_price=None,
            reason="기준가격이 설정된 5만~45만원 범위를 벗어남",
        )

    qualifies = spread >= threshold
    return PriceDecision(
        reference_price=reference,
        instant_sell_price=instant_sell_price,
        spread=spread,
        minimum_spread=threshold,
        qualifies=qualifies,
        bid_price=instant_sell_price + 1_000 if qualifies else None,
        reason="조건 충족" if qualifies else "차액 부족",
    )
