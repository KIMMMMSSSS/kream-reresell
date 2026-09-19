from kream_bot.pricing import BidAction, decide_bid


def test_new_bid_uses_minimum_1000_won_step():
    d = decide_bid(
        instant_sell_price=119_000,
        general_delivery_price=135_000,
        fast_delivery_price=134_000,
    )
    assert d.qualifies is True
    assert d.action == BidAction.CREATE
    assert d.target_bid_price == 120_000


def test_existing_top_bid_does_not_raise_against_itself():
    d = decide_bid(
        instant_sell_price=120_000,
        general_delivery_price=135_000,
        fast_delivery_price=134_000,
        existing_bid_price=120_000,
    )
    assert d.action == BidAction.KEEP
    assert d.target_bid_price == 120_000


def test_existing_bid_is_updated_when_outbid():
    d = decide_bid(
        instant_sell_price=121_000,
        general_delivery_price=136_000,
        fast_delivery_price=135_000,
        existing_bid_price=120_000,
    )
    assert d.qualifies is True
    assert d.action == BidAction.UPDATE
    assert d.target_bid_price == 122_000


def test_skip_when_one_delivery_type_is_missing():
    d = decide_bid(
        instant_sell_price=119_000,
        general_delivery_price=135_000,
        fast_delivery_price=None,
    )
    assert d.action == BidAction.SKIP


def test_skip_when_spread_is_too_small():
    d = decide_bid(
        instant_sell_price=123_000,
        general_delivery_price=135_000,
        fast_delivery_price=134_000,
    )
    assert d.qualifies is False
    assert d.action == BidAction.SKIP
