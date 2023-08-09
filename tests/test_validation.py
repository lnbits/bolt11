import pytest

from bolt11.encode import encode
from bolt11.types import (
    Bolt11,
    Bolt11DescriptionException,
    Bolt11NoPaymentHashException,
)

ex = {
    "currency": "bc",
    "amount_msat": 1000,
    "date": 1496314658,
    "payment_hash": "0001020304050607080900010203040506070809000102030405060708090102",
    "private_key": "e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734",
}


class TestBolt11Validation:
    """
    Testing validation from spec
    """

    def test_validate_no_paymenthash(self):
        invoice = Bolt11(
            currency=ex["currency"],
            amount_msat=ex["amount_msat"],
            date=ex["date"],
            tags={
                "d": "description",
            },
        )
        with pytest.raises(Bolt11NoPaymentHashException):
            encode(invoice, ex["private_key"])

    def test_validate_no_desc_or_desc_hash(self):
        """
        A writer MUST include either a `d` or `h` field,
        and MUST NOT include both.
        """
        invoice = Bolt11(
            currency=ex["currency"],
            amount_msat=ex["amount_msat"],
            date=ex["date"],
            tags={
                "p": ex["payment_hash"],
            },
        )
        with pytest.raises(Bolt11DescriptionException):
            encode(invoice, ex["private_key"])

        invoice = Bolt11(
            currency=ex["currency"],
            amount_msat=ex["amount_msat"],
            date=ex["date"],
            tags={
                "p": ex["payment_hash"],
                "d": "description",
                "h": "description",
            },
        )
        with pytest.raises(Bolt11DescriptionException):
            encode(invoice, ex["private_key"])
