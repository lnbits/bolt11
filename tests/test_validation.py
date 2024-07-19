from hashlib import sha256

import pytest

from bolt11 import Bolt11, Tags, decode, encode
from bolt11.exceptions import (
    Bolt11DescriptionException,
    Bolt11InvalidDescriptionHashException,
    Bolt11NoMinFinalCltvException,
    Bolt11NoPaymentHashException,
    Bolt11NoPaymentSecretException,
    Bolt11SignatureVerifyException,
)

ex = {
    "currency": "bc",
    "amount_msat": 1000,
    "date": 1496314658,
    "payment_hash": "0001020304050607080900010203040506070809000102030405060708090102",
    "payment_secret": (
        "1111111111111111111111111111111111111111111111111111111111111111"
    ),
    "private_key": "e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734",
    "description": "Description",
    "description_hash": sha256("Description".encode()).hexdigest(),
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
            tags=Tags.from_dict(
                {
                    "s": ex["payment_secret"],
                    "d": ex["description"],
                }
            ),
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
            tags=Tags.from_dict(
                {
                    "p": ex["payment_hash"],
                    "d": ex["description"],
                }
            ),
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
            tags=Tags.from_dict(
                {
                    "p": ex["payment_hash"],
                    "s": ex["payment_secret"],
                    "h": ex["description"],
                }
            ),
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
            tags=Tags.from_dict(
                {
                    "p": ex["payment_hash"],
                    "s": ex["payment_secret"],
                }
            ),
        )
        with pytest.raises(Bolt11DescriptionException):
            encode(invoice, ex["private_key"])

        invoice = Bolt11(
            currency=ex["currency"],
            amount_msat=ex["amount_msat"],
            date=ex["date"],
            tags=Tags.from_dict(
                {
                    "p": ex["payment_hash"],
                    "s": ex["payment_secret"],
                    "d": ex["description"],
                    "h": ex["description_hash"],
                }
            ),
        )
        with pytest.raises(Bolt11DescriptionException):
            encode(invoice, ex["private_key"])

        invoice = Bolt11(
            currency=ex["currency"],
            amount_msat=ex["amount_msat"],
            date=ex["date"],
            tags=Tags.from_dict(
                {
                    "p": ex["payment_hash"],
                    "s": ex["payment_secret"],
                    "h": ex["description_hash"],
                }
            ),
        )
        bolt11 = encode(invoice, ex["private_key"])
        assert bolt11.startswith("lnbc"), "should pass without only desc"
        invoice = Bolt11(
            currency=ex["currency"],
            amount_msat=ex["amount_msat"],
            date=ex["date"],
            tags=Tags.from_dict(
                {
                    "p": ex["payment_hash"],
                    "s": ex["payment_secret"],
                    "d": ex["description"],
                }
            ),
        )
        bolt11 = encode(invoice, ex["private_key"])
        assert bolt11.startswith("lnbc"), "should pass only description_hash"

    def test_validate_strict_encoding(self):
        """
        SHOULD include one `c` field (`min_final_cltv_expiry_delta`).
        MUST set `c` to the minimum `cltv_expiry` it will accept for the last
        """
        invoice = Bolt11(
            currency=ex["currency"],
            amount_msat=ex["amount_msat"],
            date=ex["date"],
            tags=Tags.from_dict(
                {
                    "p": ex["payment_hash"],
                    "s": ex["payment_secret"],
                    "h": ex["description_hash"],
                }
            ),
        )
        bolt11 = encode(invoice, ex["private_key"])
        assert bolt11.startswith("lnbc"), "should pass without strict"

        with pytest.raises(Bolt11NoMinFinalCltvException):
            encode(invoice, ex["private_key"], strict=True)

        decoded = decode(bolt11)
        assert decoded.payment_hash == ex["payment_hash"]

        with pytest.raises(Bolt11NoMinFinalCltvException):
            decode(bolt11, strict=True)

    def test_validate_signature_verification(self):
        invoice = Bolt11(
            currency=ex["currency"],
            amount_msat=ex["amount_msat"],
            date=ex["date"],
            tags=Tags.from_dict(
                {
                    "p": ex["payment_hash"],
                    "s": ex["payment_secret"],
                    "h": ex["description_hash"],
                    # invalid pubkey
                    "n": (
                        "03b1c1a3dd064c7b4386b688c1f0950fddb28"
                        "f61f2c3be8bcaf4ef3c78429ffe4e"
                    ),
                }
            ),
        )
        bolt11 = encode(invoice, ex["private_key"], keep_payee=True)
        with pytest.raises(Bolt11SignatureVerifyException):
            decode(bolt11)
