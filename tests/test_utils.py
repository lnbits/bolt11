from decimal import Decimal

import pytest

from bolt11.compat import shorten_amount, unshorten_amount
from bolt11.utils import amount_to_btc, amount_to_sat, btc_to_amount, sat_to_amount


class TestAmounts:
    @pytest.mark.parametrize(
        "btc, amount",
        [
            (Decimal(10) / 10**12, "10p"),
            (Decimal(1000) / 10**12, "1n"),
            (Decimal(1200) / 10**12, "1200p"),
            (Decimal(123) / 10**6, "123u"),
            (Decimal(123) / 1000, "123m"),
            (3, "3"),
        ],
    )
    def test_amount_to_btc(self, btc, amount):
        assert amount_to_btc(amount) == btc
        assert btc_to_amount(btc) == amount
        # compat test
        assert shorten_amount(btc) == amount
        assert unshorten_amount(amount) == btc

    @pytest.mark.parametrize(
        "sat, amount",
        [
            (1, "10n"),
            (10, "100n"),
            (100, "1u"),
            (100000, "1m"),
            (100000000, "1"),
            (123456789, "1234567890n"),
            (123450000, "1234500u"),
            (123400000, "1234m"),
        ],
    )
    def test_amount_to_sat(self, sat, amount):
        assert amount_to_sat(amount) == sat
        assert sat_to_amount(sat) == amount

    @pytest.mark.parametrize("sat", [100.5, 27.03])
    def test_sat_to_amount(self, sat):
        with pytest.raises(ValueError):
            sat_to_amount(sat)

    @pytest.mark.parametrize("amount", ["123x", "1f0"])
    def test_invalid_amount(self, amount):
        with pytest.raises(ValueError):
            amount_to_btc(amount)
