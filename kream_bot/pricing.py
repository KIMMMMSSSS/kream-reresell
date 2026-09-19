from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class BidAction(str, Enum):
    SKIP = "skip"
    CREATE = "create"
    KEEP = "keep"
    UPDATE = "update"


@dataclass(frozen=True)
class PriceDecision:
    reference_price: int
    instant_sell_price: int
    spread: int
    minimum_spread: int | None
    qualifies: bool
    action: BidAction
    target_bid_price: int | None
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
    existing_bid_price: int | None = None,
) -> PriceDecision:
    # User rule: both normal delivery types must exist.
    if general_delivery_price is None or fast_delivery_price is None:
        return PriceDecision(
            reference_price=0,
            instant_sell_price=instant_sell_price,
            spread=0,
            minimum_spread=None,
            qualifies=False,
            action=BidAction.SKIP,
            target_bid_price=None,
            reason="일반배송/빠른배송 중 한 종류라도 없어서 스킵",
        )

    reference = min(general_delivery_price, fast_delivery_price)
    threshold = minimum_spread(reference)
    spread = reference - instant_sell_price

    if threshold is None:
        return PriceDecision(
            reference_price=reference,
            instant_sell_price=instant_sell_price,
            spread=spread,
            minimum_spread=None,
            qualifies=False,
            action=BidAction.SKIP,
            target_bid_price=None,
            reason="기준가격이 5만~45만원 범위를 벗어나 스킵",
        )

    qualifies = spread >= threshold

    if not qualifies:
        return PriceDecision(
            reference_price=reference,
            instant_sell_price=instant_sell_price,
            spread=spread,
            minimum_spread=threshold,
            qualifies=False,
            action=BidAction.KEEP if existing_bid_price is not None else BidAction.SKIP,
            target_bid_price=existing_bid_price,
            reason="현재 신규 조건은 미충족. 기존 입찰이 있으면 임의 취소하지 않음",
        )

    # KREAM instant-sell price represents the current best purchase bid.
    # +1,000 won is the smallest step needed to become the new best bid.
    desired_price = instant_sell_price + 1_000

    if existing_bid_price is None:
        return PriceDecision(
            reference_price=reference,
            instant_sell_price=instant_sell_price,
            spread=spread,
            minimum_spread=threshold,
            qualifies=True,
            action=BidAction.CREATE,
            target_bid_price=desired_price,
            reason="조건 충족: 현재 최우선 구매입찰보다 1,000원 높게 신규 입찰",
        )

    # If my existing bid is already at least the displayed best bid,
    # do not keep raising against myself.
    if existing_bid_price >= instant_sell_price:
        return PriceDecision(
            reference_price=reference,
            instant_sell_price=instant_sell_price,
            spread=spread,
            minimum_spread=threshold,
            qualifies=True,
            action=BidAction.KEEP,
            target_bid_price=existing_bid_price,
            reason="기존 입찰이 이미 최우선권을 유지하므로 가격 유지",
        )

    return PriceDecision(
        reference_price=reference,
        instant_sell_price=instant_sell_price,
        spread=spread,
        minimum_spread=threshold,
        qualifies=True,
        action=BidAction.UPDATE,
        target_bid_price=desired_price,
        reason="기존 입찰이 밀렸으므로 현재 최우선 구매입찰보다 1,000원 높게 변경",
    )
