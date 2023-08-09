"""

TODO: multiple f fields not supported yet
    MAY include one or more f fields.
        for Bitcoin payments:
            MUST set an f field to a valid witness version and program,
            OR to 17 followed by a public key hash, OR to 18 followed by a script hash.
"""
import pytest

from bolt11.encode import encode
from bolt11.exceptions import (
    Bolt11DescriptionException,
    Bolt11InvalidDescriptionHashException,
    Bolt11NoMinFinalCltvException,
    Bolt11NoPaymentHashException,
    Bolt11NoPaymentSecretException,
)
from bolt11.types import Bolt11

ex = {
    "currency": "bc",
    "amount_msat": 1000,
    "date": 1496314658,
    "payment_hash": "0001020304050607080900010203040506070809000102030405060708090102",
    "payment_secret": "1111111111111111111111111111111111111111111111111111111111111111",
    "private_key": "e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734",
}


class TestBolt11Validation:
    """
    Testing validation from spec
    https://github.com/lightning/bolts/blob/master/11-payment-encoding.md#requirements-3
    """

    def test_validate_no_paymenthash(self):
        """
        MUST include exactly one p field.
        """
        invoice = Bolt11(
            currency=ex["currency"],
            amount_msat=ex["amount_msat"],
            date=ex["date"],
            tags={
                "s": ex["payment_secret"],
                "d": "description",
            },
        )
        with pytest.raises(Bolt11NoPaymentHashException):
            encode(invoice, ex["private_key"])

    def test_validate_no_payment_secret(self):
        """
        MUST include exactly one s field.
        """
        invoice = Bolt11(
            currency=ex["currency"],
            amount_msat=ex["amount_msat"],
            date=ex["date"],
            tags={
                "p": ex["payment_hash"],
                "d": "description",
            },
        )
        with pytest.raises(Bolt11NoPaymentSecretException):
            encode(invoice, ex["private_key"])

    def test_validate_invalid_desc_hash(self):
        """
        description_hash has the be hex
        """
        invoice = Bolt11(
            currency=ex["currency"],
            amount_msat=ex["amount_msat"],
            date=ex["date"],
            tags={
                "p": ex["payment_hash"],
                "s": ex["payment_secret"],
                "d": "description",
                "h": "description",
            },
        )
        with pytest.raises(Bolt11InvalidDescriptionHashException):
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
                "s": ex["payment_secret"],
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
                "s": ex["payment_secret"],
                "d": "description",
                "h": "6465736372697074696f6e",
            },
        )
        with pytest.raises(Bolt11DescriptionException):
            encode(invoice, ex["private_key"])

    def test_validate_strict_encoding(self):
        """
        SHOULD include one `c` field (`min_final_cltv_expiry_delta`).
        MUST set `c` to the minimum `cltv_expiry` it will accept for the last
        """
        invoice = Bolt11(
            currency=ex["currency"],
            amount_msat=ex["amount_msat"],
            date=ex["date"],
            tags={
                "p": ex["payment_hash"],
                "s": ex["payment_secret"],
                "h": "6465736372697074696f6e",
            },
        )
        bolt11 = encode(invoice, ex["private_key"])
        assert bolt11.startswith("lnbc"), "should pass without strict"
        with pytest.raises(Bolt11NoMinFinalCltvException):
            encode(invoice, ex["private_key"], strict=True)
