from bolt11 import Signature

ex = {
    "private_key": "e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734",
    "public_key": "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
}


class TestBolt11Signature:
    def test_signature(self):
        signature = Signature.from_private_key(
            hrp="lnbc1",
            private_key=ex["private_key"],
            signing_data=b"1234567890",
        )
        assert signature.recover_public_key() == ex["public_key"]

        signature = Signature.from_signature_data(
            hrp="lnbc1",
            signing_data=b"1234567890",
            signature_data=signature.signature_data,
        )
        assert signature.verify(ex["public_key"])
