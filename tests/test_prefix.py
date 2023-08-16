import pytest

from bolt11.decode import decode
from bolt11.exceptions import (
    Bolt11AmountInvalidException,
    Bolt11HrpInvalidException,
    Bolt11PrefixInvalidException,
)
from bolt11.utils import verify_hrp


class TestInvalidPrefix:
    @pytest.mark.parametrize(
        "prefix",
        ["nl", "lln", "10ln"],
    )
    def test_invalid_prefix(self, prefix):
        # Invalid Prefix, bolt11 should start with `ln`.
        with pytest.raises(Bolt11PrefixInvalidException):
            decode(prefix)


class TestVerifyHrp:
    @pytest.mark.parametrize(
        ("hrp", "currency", "amount"),
        [
            ("lntbs10u", "tbs", 1000000),
            ("lntb10u", "tb", 1000000),
            ("lnbc10u", "bc", 1000000),
            ("lnbcrt10u", "bcrt", 1000000),
        ],
    )
    def test_verify_hrp(self, hrp, currency, amount):
        cur, amt = verify_hrp(hrp)
        assert currency == cur
        assert amount == amt

    @pytest.mark.parametrize(
        "hrp",
        [
            "lntbss10u",
            "lnbcg10u",
            "lnbcrttt10u",
        ],
    )
    def test_verify_invalid_amount(self, hrp):
        with pytest.raises(Bolt11AmountInvalidException):
            verify_hrp(hrp)

    @pytest.mark.parametrize(
        "hrp",
        [
            "lnog10u",
            "ln6610u",
            "ln12312310u",
            "olnbc10u",
        ],
    )
    def test_verify_invalid_hrp(self, hrp):
        with pytest.raises(Bolt11HrpInvalidException):
            verify_hrp(hrp)
