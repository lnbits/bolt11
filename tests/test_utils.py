from decimal import Decimal

import pytest
from bitstring import Bits, ReadError

from bolt11.bit_utils import BitReader, int_to_scid, scid_to_int
from bolt11.compat import shorten_amount, unshorten_amount
from bolt11.exceptions import Bolt11AmountInvalidException
from bolt11.utils import amount_to_btc, amount_to_sat, btc_to_amount, sat_to_amount


class TestScid:
    @pytest.mark.parametrize(
        "scid, cid",
        [
            ("589390x3312x1", 648041158511951873),
        ],
    )
    def test_scid(self, scid, cid):
        assert int_to_scid(cid) == scid
        assert scid_to_int(scid) == cid


class TestBitReader:
    def test_zero_length(self):
        reader = BitReader(Bits("0b10110"))
        assert reader.read(0) == Bits()
        assert reader.pos == 0

    def test_consecutive_reads_to_exact_end(self):
        reader = BitReader(Bits("0b10110"))
        assert reader.read(2) == Bits("0b10")
        assert reader.read(3) == Bits("0b110")
        assert reader.pos == len(reader) == 5
        assert reader.read(0) == Bits()

    def test_overrun_leaves_cursor(self):
        reader = BitReader(Bits("0b10110"))
        reader.read(2)
        with pytest.raises(ReadError):
            reader.read(4)
        assert reader.pos == 2

    def test_negative_length_leaves_cursor(self):
        reader = BitReader(Bits("0b10110"))
        reader.read(2)
        with pytest.raises(ValueError):
            reader.read(-1)
        assert reader.pos == 2


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
        with pytest.raises(Bolt11AmountInvalidException):
            amount_to_btc(amount)
