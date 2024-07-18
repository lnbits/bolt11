from bitstring import Bits

from bolt11 import Signature

ex = {
    "private_key": "e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734",
    "public_key": "031a7a2db2e0c0fbfcfe62e23b6262b9f2b76bc01b022d17b2f9b49c7bc22310fd",
    "signature": (
        "202bea309bab7aeff223ad2890d42ca00bc5673c88cab47420387100f8939fb26a"
        "dea33c4e1748b3a56f87b3f9b1b001ffdc82169809782a02bd03ae2d1cbdc700"
    ),
}


class TestBolt11Signature:
    def test_recovers_public_key(self):
        signature = Signature.from_private_key(
            ex["private_key"],
            "lnbc",
            Bits(b"1234567890"),
        )
        assert signature.recover_public_key() == ex["public_key"]

    def test_signature_from_private_key(self):
        signature = Signature.from_private_key(
            ex["private_key"],
            "lnbc",
            Bits(b"1234567890"),
        )
        assert signature.signing_data == b"1234567890"
        assert signature.signature_data == bytes.fromhex(ex["signature"])

    def test_signature_verify(self):
        signature = Signature.from_private_key(
            ex["private_key"],
            "lnbc",
            Bits(b"1234567890"),
        )
        assert signature.verify(ex["public_key"])
