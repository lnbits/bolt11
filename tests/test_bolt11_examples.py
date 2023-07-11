from bolt11.decode import decode
from bolt11.encode import encode
from bolt11.models.fallback import Fallback
from bolt11.models.features import Feature, Features, FeatureState
from bolt11.models.routehint import RouteHint
from bolt11.types import Bolt11


class TestBolt11:
    """
    Examples: https://github.com/lightning/bolts/blob/master/11-payment-encoding.md#examples
    """

    def test_example_1(self):
        """
        Please make a donation of any amount using payment_hash
        0001020304050607080900010203040506070809000102030405060708090102
        to me @03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad
        """
        ex = {
            "payment_request": (
                "lnbc1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygspp5qqqsyqcyq5rqwzqfqqq"
                "syqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdpl2pkx2ctnv5sxxmmwwd5kgetjypeh2ursdae8g6twvus8g6rfwvs8q"
                "un0dfjkxaq9qrsgq357wnc5r2ueh7ck6q93dj32dlqnls087fxdwk8qakdyafkq3yap9us6v52vjjsrvywa6rt52c"
                "m9r9zqt8r2t7mlcwspyetp5h2tztugp9lfyql"
            ),
            "currency": "bc",
            "timestamp": 1496314658,
            "payment_hash": "0001020304050607080900010203040506070809000102030405060708090102",
            "payment_secret": "1111111111111111111111111111111111111111111111111111111111111111",
            "amount": None,
            "payee": "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
            "description": "Please consider supporting this project",
            "features": {"var_onion_optin": "required", "payment_secret": "required"},
            "feature_list": {Feature.var_onion_optin: FeatureState.required, Feature.payment_secret: FeatureState.required},
            "signature": (
                "8d3ce9e28357337f62da0162d9454df827f83cfe499aeb1c1db349d4d81127425e434ca29929406c23bba1ae8"
                "ac6ca32880b38d4bf6ff874024cac34ba9625f1"
            ),
            "private_key": "e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734",
        }

        decoded = decode(ex["payment_request"])

        assert decoded.currency == ex["currency"]
        assert decoded.timestamp == ex["timestamp"]
        assert decoded.payment_hash == ex["payment_hash"]
        assert decoded.payment_secret == ex["payment_secret"]
        assert decoded.amount == ex["amount"]
        assert decoded.description == ex["description"]
        assert decoded.payee == ex["payee"]
        assert decoded.features
        assert decoded.features.readable == ex["features"]
        assert decoded.signature
        assert decoded.signature.hex == ex["signature"]

        re_encoded = encode(decoded)
        assert re_encoded == ex["payment_request"]

        invoice = Bolt11(
            currency=ex["currency"],
            amount=ex["amount"],
            timestamp=ex["timestamp"],
            tags={
                "s": ex["payment_secret"],
                "p": ex["payment_hash"],
                "d": ex["description"],
                "n": ex["payee"],
                "9": Features.from_feature_list(ex["feature_list"]),
            },
        )

        encoded = encode(invoice, ex["private_key"])
        assert encoded == ex["payment_request"]

    def test_example_2(self):
        """
        Please send $3 for a cup of coffee to the same peer, within one minute
        """
        ex = {
            "payment_request": (
                "lnbc2500u1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygspp5qqqsyqcyq5rqwzq"
                "fqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdq5xysxxatsyp3k7enxv4jsxqzpu9qrsgquk0rl77nj30yxdy8j9v"
                "dx85fkpmdla2087ne0xh8nhedh8w27kyke0lp53ut353s06fv3qfegext0eh0ymjpf39tuven09sam30g4vgpfna3rh"
            ),
            "currency": "bc",
            "timestamp": 1496314658,
            "expiry": 60,
            "payment_hash": "0001020304050607080900010203040506070809000102030405060708090102",
            "payment_secret": "1111111111111111111111111111111111111111111111111111111111111111",
            "amount": 250_000_000,
            "description": "1 cup coffee",
            "payee": "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
            "features": {"var_onion_optin": "required", "payment_secret": "required"},
            "feature_list": {Feature.var_onion_optin: FeatureState.required, Feature.payment_secret: FeatureState.required},
            "signature": (
                "e59e3ffbd3945e4334879158d31e89b076dff54f3fa7979ae79df2db9dcaf5896cbfe1a478b8d2307e92c8813"
                "9464cb7e6ef26e414c4abe33337961ddc5e8ab1"
            ),
            "private_key": "e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734",
        }

        decoded = decode(ex["payment_request"])
        assert decoded.currency == ex["currency"]
        assert decoded.timestamp == ex["timestamp"]
        assert decoded.expiry == ex["expiry"]
        assert decoded.payment_hash == ex["payment_hash"]
        assert decoded.payment_secret == ex["payment_secret"]
        assert decoded.amount == ex["amount"]
        assert decoded.description == ex["description"]
        assert decoded.payee == ex["payee"]
        assert decoded.features
        assert decoded.features.readable == ex["features"]
        assert decoded.signature
        assert decoded.signature.hex == ex["signature"]

        re_encoded = encode(decoded)
        assert re_encoded == ex["payment_request"]

        invoice = Bolt11(
            currency=ex["currency"],
            amount=ex["amount"],
            timestamp=ex["timestamp"],
            tags={
                "s": ex["payment_secret"],
                "p": ex["payment_hash"],
                "d": ex["description"],
                "x": ex["expiry"],
                "n": ex["payee"],
                "9": Features.from_feature_list(ex["feature_list"]),
            },
        )

        encoded = encode(invoice, ex["private_key"])
        assert encoded == ex["payment_request"]

    def test_example_3(self):
        """
        Please send 0.0025 BTC for a cup of nonsense (ナンセンス 1杯) to the same peer, within one minute
        """
        ex = {
            "payment_request": (
                "lnbc2500u1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygspp5qqqsyqcyq5rqwz"
                "qfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdpquwpc4curk03c9wlrswe78q4eyqc7d8d0xqzpu9qrsgqhtjpa"
                "uu9ur7fw2thcl4y9vfvh4m9wlfyz2gem29g5ghe2aak2pm3ps8fdhtceqsaagty2vph7utlgj48u0ged6a337aewv"
                "raedendscp573dxr"
            ),
            "currency": "bc",
            "timestamp": 1496314658,
            "expiry": 60,
            "payment_hash": "0001020304050607080900010203040506070809000102030405060708090102",
            "payment_secret": "1111111111111111111111111111111111111111111111111111111111111111",
            "amount": 250_000_000,
            "description": "ナンセンス 1杯",
            "payee": "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
            "features": {"var_onion_optin": "required", "payment_secret": "required"},
            "feature_list": {Feature.var_onion_optin: FeatureState.required, Feature.payment_secret: FeatureState.required},
            "signature": (
                "bae41ef385e0fc972977c7ea42b12cbd76577d2412919da8a8a22f9577b6507710c0e96dd78c821dea1645303"
                "7f717f44aa7e3d196ebb18fbb97307dcb7336c3"
            ),
            "private_key": "e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734",
        }

        decoded = decode(ex["payment_request"])
        assert decoded.currency == ex["currency"]
        assert decoded.timestamp == ex["timestamp"]
        assert decoded.expiry == ex["expiry"]
        assert decoded.payment_hash == ex["payment_hash"]
        assert decoded.payment_secret == ex["payment_secret"]
        assert decoded.amount == ex["amount"]
        assert decoded.description == ex["description"]
        assert decoded.payee == ex["payee"]
        assert decoded.features
        assert decoded.features.readable == ex["features"]
        assert decoded.signature
        assert decoded.signature.hex == ex["signature"]

        re_encoded = encode(decoded)
        assert re_encoded == ex["payment_request"]

        invoice = Bolt11(
            currency=ex["currency"],
            amount=ex["amount"],
            timestamp=ex["timestamp"],
            tags={
                "s": ex["payment_secret"],
                "p": ex["payment_hash"],
                "d": ex["description"],
                "x": ex["expiry"],
                "n": ex["payee"],
                "9": Features.from_feature_list(ex["feature_list"]),
            },
        )

        encoded = encode(invoice, ex["private_key"])
        assert encoded == ex["payment_request"]

    def test_example_4(self):
        """
        Now send $24 for an entire list of things (hashed)
        """
        ex = {
            "payment_request": (
                "lnbc20m1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygspp5qqqsyqcyq5rqwzqf"
                "qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqhp58yjmdan79s6qqdhdzgynm4zwqd5d7xmw5fk98klysy043l2ahr"
                "qs9qrsgq7ea976txfraylvgzuxs8kgcw23ezlrszfnh8r6qtfpr6cxga50aj6txm9rxrydzd06dfeawfk6swupvz4"
                "erwnyutnjq7x39ymw6j38gp7ynn44"
            ),
            "currency": "bc",
            "timestamp": 1496314658,
            "payment_hash": "0001020304050607080900010203040506070809000102030405060708090102",
            "payment_secret": "1111111111111111111111111111111111111111111111111111111111111111",
            "amount": 2_000_000_000,
            "description": None,
            "description_hash": "3925b6f67e2c340036ed12093dd44e0368df1b6ea26c53dbe4811f58fd5db8c1",
            "payee": "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
            "features": {"var_onion_optin": "required", "payment_secret": "required"},
            "feature_list": {Feature.var_onion_optin: FeatureState.required, Feature.payment_secret: FeatureState.required},
            "signature": (
                "f67a5f696648fa4fb102e1a07b230e54722f8e024cee71e80b4847ac191da3fb2d2cdb28cc32344d7e9a9cf5c"
                "9b6a0ee0582ae46e9938b9c81e344a4dbb5289d"
            ),
            "private_key": "e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734",
        }

        decoded = decode(ex["payment_request"])
        assert decoded.currency == ex["currency"]
        assert decoded.timestamp == ex["timestamp"]
        assert decoded.payment_hash == ex["payment_hash"]
        assert decoded.payment_secret == ex["payment_secret"]
        assert decoded.amount == ex["amount"]
        assert decoded.description == ex["description"]
        assert decoded.description_hash == ex["description_hash"]
        assert decoded.payee == ex["payee"]
        assert decoded.features
        assert decoded.features.readable == ex["features"]
        assert decoded.signature
        assert decoded.signature.hex == ex["signature"]

        re_encoded = encode(decoded)
        assert re_encoded == ex["payment_request"]

        invoice = Bolt11(
            currency=ex["currency"],
            amount=ex["amount"],
            timestamp=ex["timestamp"],
            tags={
                "s": ex["payment_secret"],
                "p": ex["payment_hash"],
                "h": ex["description_hash"],
                "n": ex["payee"],
                "9": Features.from_feature_list(ex["feature_list"]),
            },
        )

        encoded = encode(invoice, ex["private_key"])
        assert encoded == ex["payment_request"]

    def test_example_5(self):
        """
        The same, on testnet, with a fallback address mk2QpYatsKicvFVuTAQLBryyccRXMUaGHP
        """
        ex = {
            "payment_request": (
                "lntb20m1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygshp58yjmdan79s6qqdhd"
                "zgynm4zwqd5d7xmw5fk98klysy043l2ahrqspp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqy"
                "pqfpp3x9et2e20v6pu37c5d9vax37wxq72un989qrsgqdj545axuxtnfemtpwkc45hx9d2ft7x04mt8q7y6t0k2dg"
                "e9e7h8kpy9p34ytyslj3yu569aalz2xdk8xkd7ltxqld94u8h2esmsmacgpghe9k8"
            ),
            "currency": "tb",
            "timestamp": 1496314658,
            "payment_hash": "0001020304050607080900010203040506070809000102030405060708090102",
            "payment_secret": "1111111111111111111111111111111111111111111111111111111111111111",
            "amount": 2_000_000_000,
            "description": None,
            "description_hash": "3925b6f67e2c340036ed12093dd44e0368df1b6ea26c53dbe4811f58fd5db8c1",
            "payee": "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
            "fallback": "mk2QpYatsKicvFVuTAQLBryyccRXMUaGHP",
            "features": {"var_onion_optin": "required", "payment_secret": "required"},
            "feature_list": {Feature.var_onion_optin: FeatureState.required, Feature.payment_secret: FeatureState.required},
            "signature": (
                "6ca95a74dc32e69ced6175b15a5cc56a92bf19f5dace0f134b7d94d464b9f5cf6090a18d48b243f289394d17b"
                "df89466d8e6b37df5981f696bc3dd5986e1bee1"
            ),
            "private_key": "e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734",
        }

        decoded = decode(ex["payment_request"])
        assert decoded.currency == ex["currency"]
        assert decoded.timestamp == ex["timestamp"]
        assert decoded.payment_hash == ex["payment_hash"]
        assert decoded.payment_secret == ex["payment_secret"]
        assert decoded.fallback
        assert decoded.fallback.address == ex["fallback"]
        assert decoded.amount == ex["amount"]
        assert decoded.description == ex["description"]
        assert decoded.description_hash == ex["description_hash"]
        assert decoded.payee == ex["payee"]
        assert decoded.features
        assert decoded.features.readable == ex["features"]
        assert decoded.signature
        assert decoded.signature.hex == ex["signature"]

        re_encoded = encode(decoded)
        assert re_encoded == ex["payment_request"]

        invoice = Bolt11(
            currency=ex["currency"],
            amount=ex["amount"],
            timestamp=ex["timestamp"],
            tags={
                "s": ex["payment_secret"],
                "h": ex["description_hash"],
                "p": ex["payment_hash"],
                "f": Fallback.from_address(ex["fallback"], ex["currency"]),
                "n": ex["payee"],
                "9": Features.from_feature_list(ex["feature_list"]),
            },
        )

        encoded = encode(invoice, ex["private_key"])
        assert encoded == ex["payment_request"]

    def test_example_6(self):
        """
        On mainnet, with fallback address 1RustyRX2oai4EYYDpQGWvEL62BBGqN9T with extra routing info to go via nodes
        029e03a901b85534ff1e92c43c74431f7ce72046060fcf7a95c37e148f78c77255 then
        039e03a901b85534ff1e92c43c74431f7ce72046060fcf7a95c37e148f78c77255
        """
        ex = {
            "payment_request": (
                "lnbc20m1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygspp5qqqsyqcyq5rqwzqf"
                "qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqhp58yjmdan79s6qqdhdzgynm4zwqd5d7xmw5fk98klysy043l2ahr"
                "qsfpp3qjmp7lwpagxun9pygexvgpjdc4jdj85fr9yq20q82gphp2nflc7jtzrcazrra7wwgzxqc8u7754cdlpfrmc"
                "cae92qgzqvzq2ps8pqqqqqqpqqqqq9qqqvpeuqafqxu92d8lr6fvg0r5gv0heeeqgcrqlnm6jhphu9y00rrhy4grq"
                "szsvpcgpy9qqqqqqgqqqqq7qqzq9qrsgqdfjcdk6w3ak5pca9hwfwfh63zrrz06wwfya0ydlzpgzxkn5xagsqz7x9"
                "j4jwe7yj7vaf2k9lqsdk45kts2fd0fkr28am0u4w95tt2nsq76cqw0"
            ),
            "currency": "bc",
            "timestamp": 1496314658,
            "payment_hash": "0001020304050607080900010203040506070809000102030405060708090102",
            "payment_secret": "1111111111111111111111111111111111111111111111111111111111111111",
            "amount": 2_000_000_000,
            "description": None,
            "description_hash": "3925b6f67e2c340036ed12093dd44e0368df1b6ea26c53dbe4811f58fd5db8c1",
            "payee": "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
            "fallback": "1RustyRX2oai4EYYDpQGWvEL62BBGqN9T",
            "features": {"var_onion_optin": "required", "payment_secret": "required"},
            "feature_list": {Feature.var_onion_optin: FeatureState.required, Feature.payment_secret: FeatureState.required},
            "signature": (
                "6a6586db4e8f6d40e3a5bb92e4df5110c627e9ce493af237e20a046b4e86ea200178c59564ecf892f33a9558b"
                "f041b6ad2cb8292d7a6c351fbb7f2ae2d16b54e"
            ),
            "route_hints": [
                {
                    "public_key": "029e03a901b85534ff1e92c43c74431f7ce72046060fcf7a95c37e148f78c77255",
                    "short_channel_id": "66051x263430x1800",
                    "base_fee": 1,
                    "ppm_fee": 20,
                    "cltv_expiry_delta": 3,
                },
                {
                    "public_key": "039e03a901b85534ff1e92c43c74431f7ce72046060fcf7a95c37e148f78c77255",
                    "short_channel_id": "197637x395016x2314",
                    "base_fee": 2,
                    "ppm_fee": 30,
                    "cltv_expiry_delta": 4,
                },
            ],
            "private_key": "e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734",
        }

        decoded = decode(ex["payment_request"])
        assert decoded.currency == ex["currency"]
        assert decoded.timestamp == ex["timestamp"]
        assert decoded.payment_hash == ex["payment_hash"]
        assert decoded.payment_secret == ex["payment_secret"]
        assert decoded.fallback
        assert decoded.fallback.address == ex["fallback"]
        assert decoded.amount == ex["amount"]
        assert decoded.description == ex["description"]
        assert decoded.description_hash == ex["description_hash"]
        assert decoded.payee == ex["payee"]
        assert decoded.signature
        assert decoded.signature.hex == ex["signature"]
        assert decoded.features
        assert decoded.features.readable == ex["features"]
        assert decoded.route_hints
        assert len(decoded.route_hints.routes) == len(ex["route_hints"])
        for i, route_hint in enumerate(decoded.route_hints.routes):
            ex_route_hint = ex["route_hints"][i]
            assert route_hint.public_key == ex_route_hint["public_key"]
            assert route_hint.short_channel_id == ex_route_hint["short_channel_id"]
            assert route_hint.base_fee == ex_route_hint["base_fee"]
            assert route_hint.ppm_fee == ex_route_hint["ppm_fee"]
            assert route_hint.cltv_expiry_delta == ex_route_hint["cltv_expiry_delta"]

        re_encoded = encode(decoded)
        assert re_encoded == ex["payment_request"]

        invoice = Bolt11(
            currency=ex["currency"],
            amount=ex["amount"],
            timestamp=ex["timestamp"],
            tags={
                "s": ex["payment_secret"],
                "p": ex["payment_hash"],
                "h": ex["description_hash"],
                "f": Fallback.from_address(ex["fallback"], ex["currency"]),
                "r": RouteHint.from_list(ex["route_hints"]),
                "n": ex["payee"],
                "9": Features.from_feature_list(ex["feature_list"]),
            },
        )

        encoded = encode(invoice, ex["private_key"])
        assert encoded == ex["payment_request"]

    def test_example_7(self):
        """
        On mainnet, with fallback (P2SH) address 3EktnHQD7RiAE6uzMj2ZifT9YgRrkSgzQX
        """
        ex = {
            "payment_request": (
                "lnbc20m1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygshp58yjmdan79s6qqdhd"
                "zgynm4zwqd5d7xmw5fk98klysy043l2ahrqspp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqy"
                "pqfppj3a24vwu6r8ejrss3axul8rxldph2q7z99qrsgqz6qsgww34xlatfj6e3sngrwfy3ytkt29d2qttr8qz2mne"
                "dfqysuqypgqex4haa2h8fx3wnypranf3pdwyluftwe680jjcfp438u82xqphf75ym"
            ),
            "currency": "bc",
            "timestamp": 1496314658,
            "payment_hash": "0001020304050607080900010203040506070809000102030405060708090102",
            "payment_secret": "1111111111111111111111111111111111111111111111111111111111111111",
            "amount": 2_000_000_000,
            "description": None,
            "description_hash": "3925b6f67e2c340036ed12093dd44e0368df1b6ea26c53dbe4811f58fd5db8c1",
            "payee": "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
            "fallback": "3EktnHQD7RiAE6uzMj2ZifT9YgRrkSgzQX",
            "features": {"var_onion_optin": "required", "payment_secret": "required"},
            "feature_list": {Feature.var_onion_optin: FeatureState.required, Feature.payment_secret: FeatureState.required},
            "signature": (
                "16810439d1a9bfd5a65acc61340dc92448bb2d456a80b58ce012b73cb5202438020500c9ab7ef5573a4d174c8"
                "11f669885ae27f895bb3a3be52c243589f87518"
            ),
            "private_key": "e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734",
        }

        decoded = decode(ex["payment_request"])
        assert decoded.currency == ex["currency"]
        assert decoded.timestamp == ex["timestamp"]
        assert decoded.payment_hash == ex["payment_hash"]
        assert decoded.payment_secret == ex["payment_secret"]
        assert decoded.amount == ex["amount"]
        assert decoded.description == ex["description"]
        assert decoded.description_hash == ex["description_hash"]
        assert decoded.payee == ex["payee"]
        assert decoded.fallback
        assert decoded.fallback.address == ex["fallback"]
        assert decoded.signature
        assert decoded.signature.hex == ex["signature"]
        assert decoded.features
        assert decoded.features.readable == ex["features"]

        re_encoded = encode(decoded)
        assert re_encoded == ex["payment_request"]

        invoice = Bolt11(
            currency=ex["currency"],
            amount=ex["amount"],
            timestamp=ex["timestamp"],
            tags={
                "s": ex["payment_secret"],
                "h": ex["description_hash"],
                "p": ex["payment_hash"],
                "f": Fallback.from_address(ex["fallback"], ex["currency"]),
                "n": ex["payee"],
                "9": Features.from_feature_list(ex["feature_list"]),
            },
        )

        encoded = encode(invoice, ex["private_key"])
        assert encoded == ex["payment_request"]

    def test_example_8(self):
        """
        On mainnet, with fallback (P2WPKH) address bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4
        """
        ex = {
            "payment_request": (
                "lnbc20m1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygshp58yjmdan79s6qqdhd"
                "zgynm4zwqd5d7xmw5fk98klysy043l2ahrqspp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqy"
                "pqfppqw508d6qejxtdg4y5r3zarvary0c5xw7k9qrsgqt29a0wturnys2hhxpner2e3plp6jyj8qx7548zr2z7ptg"
                "jjc7hljm98xhjym0dg52sdrvqamxdezkmqg4gdrvwwnf0kv2jdfnl4xatsqmrnsse"
            ),
            "currency": "bc",
            "timestamp": 1496314658,
            "payment_hash": "0001020304050607080900010203040506070809000102030405060708090102",
            "payment_secret": "1111111111111111111111111111111111111111111111111111111111111111",
            "amount": 2_000_000_000,
            "description": None,
            "description_hash": "3925b6f67e2c340036ed12093dd44e0368df1b6ea26c53dbe4811f58fd5db8c1",
            "payee": "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
            "fallback": "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4",
            "features": {"var_onion_optin": "required", "payment_secret": "required"},
            "feature_list": {Feature.var_onion_optin: FeatureState.required, Feature.payment_secret: FeatureState.required},
            "signature": (
                "5a8bd7b97c1cc9055ee60cf2356621f8752248e037a953886a1782b44a58f5ff2d94e6bc89b7b514541a3603b"
                "b33722b6c08aa1a3639d34becc549a99fea6eae"
            ),
            "private_key": "e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734",
        }

        decoded = decode(ex["payment_request"])
        assert decoded.currency == ex["currency"]
        assert decoded.timestamp == ex["timestamp"]
        assert decoded.payment_hash == ex["payment_hash"]
        assert decoded.payment_secret == ex["payment_secret"]
        assert decoded.amount == ex["amount"]
        assert decoded.description == ex["description"]
        assert decoded.description_hash == ex["description_hash"]
        assert decoded.payee == ex["payee"]
        assert decoded.fallback
        assert decoded.fallback.address == ex["fallback"]
        assert decoded.signature
        assert decoded.signature.hex == ex["signature"]
        assert decoded.features
        assert decoded.features.readable == ex["features"]

        re_encoded = encode(decoded)
        assert re_encoded == ex["payment_request"]

        invoice = Bolt11(
            currency=ex["currency"],
            amount=ex["amount"],
            timestamp=ex["timestamp"],
            tags={
                "s": ex["payment_secret"],
                "h": ex["description_hash"],
                "p": ex["payment_hash"],
                "f": Fallback.from_address(ex["fallback"], ex["currency"]),
                "n": ex["payee"],
                "9": Features.from_feature_list(ex["feature_list"]),
            },
        )

        encoded = encode(invoice, ex["private_key"])
        assert encoded == ex["payment_request"]

    def test_example_9(self):
        """
        On mainnet, with fallback (P2WSH) address bc1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3qccfmv3
        """
        ex = {
            "payment_request": (
                "lnbc20m1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygshp58yjmdan79s6qqdhd"
                "zgynm4zwqd5d7xmw5fk98klysy043l2ahrqspp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqy"
                "pqfp4qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3q9qrsgq9vlvyj8cqvq6ggvpwd53jncp9"
                "nwc47xlrsnenq2zp70fq83qlgesn4u3uyf4tesfkkwwfg3qs54qe426hp3tz7z6sweqdjg05axsrjqp9yrrwc"
            ),
            "currency": "bc",
            "timestamp": 1496314658,
            "payment_hash": "0001020304050607080900010203040506070809000102030405060708090102",
            "payment_secret": "1111111111111111111111111111111111111111111111111111111111111111",
            "amount": 2_000_000_000,
            "description": None,
            "description_hash": "3925b6f67e2c340036ed12093dd44e0368df1b6ea26c53dbe4811f58fd5db8c1",
            "payee": "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
            "fallback": "bc1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3qccfmv3",
            "features": {"var_onion_optin": "required", "payment_secret": "required"},
            "feature_list": {Feature.var_onion_optin: FeatureState.required, Feature.payment_secret: FeatureState.required},
            "signature": (
                "2b3ec248f80301a421817369194f012cdd8af8df1c279981420f9e901e20fa3309d791e11355e609b59ce4a22"
                "0852a0cd55ab862b1785a83b206c90fa74d01c8"
            ),
            "private_key": "e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734",
        }

        decoded = decode(ex["payment_request"])
        assert decoded.currency == ex["currency"]
        assert decoded.timestamp == ex["timestamp"]
        assert decoded.payment_hash == ex["payment_hash"]
        assert decoded.payment_secret == ex["payment_secret"]
        assert decoded.amount == ex["amount"]
        assert decoded.description == ex["description"]
        assert decoded.description_hash == ex["description_hash"]
        assert decoded.payee == ex["payee"]
        assert decoded.fallback
        assert decoded.fallback.address == ex["fallback"]
        assert decoded.signature
        assert decoded.signature.hex == ex["signature"]
        assert decoded.features
        assert decoded.features.readable == ex["features"]

        re_encoded = encode(decoded)
        assert re_encoded == ex["payment_request"]

        invoice = Bolt11(
            currency=ex["currency"],
            amount=ex["amount"],
            timestamp=ex["timestamp"],
            tags={
                "s": ex["payment_secret"],
                "h": ex["description_hash"],
                "p": ex["payment_hash"],
                "f": Fallback.from_address(ex["fallback"], ex["currency"]),
                "n": ex["payee"],
                "9": Features.from_feature_list(ex["feature_list"]),
            },
        )

        encoded = encode(invoice, ex["private_key"])
        assert encoded == ex["payment_request"]

    def test_example_10(self):
        """
        Please send 0.00967878534 BTC for a list of items within one week, amount in pico-BTC
        """
        ex = {
            "payment_request": (
                "lnbc9678785340p1pwmna7lpp5gc3xfm08u9qy06djf8dfflhugl6p7lgza6dsjxq454gxhj9t7a0sd8dgfkx7cmt"
                "wd68yetpd5s9xar0wfjn5gpc8qhrsdfq24f5ggrxdaezqsnvda3kkum5wfjkzmfqf3jkgem9wgsyuctwdus9xgrcy"
                "qcjcgpzgfskx6eqf9hzqnteypzxz7fzypfhg6trddjhygrcyqezcgpzfysywmm5ypxxjemgw3hxjmn8yptk7untd9"
                "hxwg3q2d6xjcmtv4ezq7pqxgsxzmnyyqcjqmt0wfjjq6t5v4khxsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg"
                "3zyg3zyg3zyg3zygsxqyjw5qcqp2rzjq0gxwkzc8w6323m55m4jyxcjwmy7stt9hwkwe2qxmy8zpsgg7jcuwz87fc"
                "qqeuqqqyqqqqlgqqqqn3qq9q9qrsgqrvgkpnmps664wgkp43l22qsgdw4ve24aca4nymnxddlnp8vh9v2sdxlu5yw"
                "dxefsfvm0fq3sesf08uf6q9a2ke0hc9j6z6wlxg5z5kqpu2v9wz"
            ),
            "currency": "bc",
            "timestamp": 1572468703,
            "payment_hash": "462264ede7e14047e9b249da94fefc47f41f7d02ee9b091815a5506bc8abf75f",
            "payment_secret": "1111111111111111111111111111111111111111111111111111111111111111",
            "amount": 967_878_534,
            "expiry": 604800,
            "min_final_cltv_expiry": 10,
            "description": (
                'Blockstream Store: 88.85 USD for Blockstream Ledger Nano S x 1, "Back In My Day" Sticke'
                'r x 2, "I Got Lightning Working" Sticker x 2 and 1 more items'
            ),
            "payee": "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
            "features": {"var_onion_optin": "required", "payment_secret": "required"},
            "feature_list": {Feature.var_onion_optin: FeatureState.required, Feature.payment_secret: FeatureState.required},
            "signature": (
                "1b1160cf6186b55722c1ac7ea502086baaccaabdc76b326e666b7f309d972b15069bfca11cd365304b36f4823"
                "0cc12f3f13a017aab65f7c165a169df32282a58"
            ),
            "route_hints": [
                {
                    "public_key": "03d06758583bb5154774a6eb221b1276c9e82d65bbaceca806d90e20c108f4b1c7",
                    "short_channel_id": "589390x3312x1",
                    "base_fee": 1000,
                    "ppm_fee": 2500,
                    "cltv_expiry_delta": 40,
                },
            ],
            "private_key": "e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734",
        }

        decoded = decode(ex["payment_request"])
        assert decoded.currency == ex["currency"]
        assert decoded.timestamp == ex["timestamp"]
        assert decoded.expiry == ex["expiry"]
        assert decoded.min_final_cltv_expiry == ex["min_final_cltv_expiry"]
        assert decoded.payment_hash == ex["payment_hash"]
        assert decoded.payment_secret == ex["payment_secret"]
        assert decoded.amount == ex["amount"]
        assert decoded.description == ex["description"]
        assert decoded.payee == ex["payee"]
        assert decoded.signature
        assert decoded.signature.hex == ex["signature"]
        assert decoded.features
        assert decoded.features.readable == ex["features"]

        assert decoded.route_hints
        assert len(decoded.route_hints.routes) == len(ex["route_hints"])
        for i, route_hint in enumerate(decoded.route_hints.routes):
            ex_route_hint = ex["route_hints"][i]
            assert route_hint.public_key == ex_route_hint["public_key"]
            assert route_hint.short_channel_id == ex_route_hint["short_channel_id"]
            assert route_hint.base_fee == ex_route_hint["base_fee"]
            assert route_hint.ppm_fee == ex_route_hint["ppm_fee"]
            assert route_hint.cltv_expiry_delta == ex_route_hint["cltv_expiry_delta"]

        re_encoded = encode(decoded)
        assert re_encoded == ex["payment_request"]

        invoice = Bolt11(
            currency=ex["currency"],
            amount=ex["amount"],
            timestamp=ex["timestamp"],
            tags={
                "p": ex["payment_hash"],
                "d": ex["description"],
                "s": ex["payment_secret"],
                "x": ex["expiry"],
                "c": ex["min_final_cltv_expiry"],
                "r": RouteHint.from_list(ex["route_hints"]),
                "9": Features.from_feature_list(ex["feature_list"]),
                "n": ex["payee"],
            },
        )

        encoded = encode(invoice, ex["private_key"])
        assert encoded == ex["payment_request"]

    def test_example_11(self):
        """
        Please send $30 for coffee beans to the same peer, which supports features 8, 14 and 99,
        using secret 0x1111111111111111111111111111111111111111111111111111111111111111
        """
        ex = {
            "payment_request": (
                "lnbc25m1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdq5vdhkven9v5sxyetp"
                "deessp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygs9q5sqqqqqqqqqqqqqqqqsgq2a25dxl"
                "5hrntdtn6zvydt7d66hyzsyhqs4wdynavys42xgl6sgx9c4g7me86a27t07mdtfry458rtjr0v92cnmswpsjscgt2"
                "vcse3sgpz3uapa"
            ),
            "currency": "bc",
            "timestamp": 1496314658,
            "payment_hash": "0001020304050607080900010203040506070809000102030405060708090102",
            "payment_secret": "1111111111111111111111111111111111111111111111111111111111111111",
            "amount": 2_500_000_000,
            "description": "coffee beans",
            "payee": "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
            "features": {"var_onion_optin": "required", "payment_secret": "required", "extra_31": "supported"},
            "feature_list": {
                Feature.var_onion_optin: FeatureState.required,
                Feature.payment_secret: FeatureState.required,
                Feature.extra_31: FeatureState.supported,
            },
            "signature": (
                "5755469bf4b8e6b6ae7a1308d5f9bad5c82812e0855cd24fac242aa323fa820c5c551ede4faeabcb7fb6d5a46"
                "4ad0e35c86f615589ee0e0c250c216a662198c1"
            ),
            "private_key": "e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734",
        }

        decoded = decode(ex["payment_request"])
        assert decoded.currency == ex["currency"]
        assert decoded.timestamp == ex["timestamp"]
        assert decoded.payment_hash == ex["payment_hash"]
        assert decoded.payment_secret == ex["payment_secret"]
        assert decoded.amount == ex["amount"]
        assert decoded.description == ex["description"]
        assert decoded.payee == ex["payee"]
        assert decoded.signature
        assert decoded.signature.hex == ex["signature"]
        assert decoded.features
        assert decoded.features.readable == ex["features"]

        re_encoded = encode(decoded)
        assert re_encoded == ex["payment_request"]

        invoice = Bolt11(
            currency=ex["currency"],
            amount=ex["amount"],
            timestamp=ex["timestamp"],
            tags={
                "p": ex["payment_hash"],
                "d": ex["description"],
                "s": ex["payment_secret"],
                "9": Features.from_feature_list(ex["feature_list"]),
                "n": ex["payee"],
            },
        )

        encoded = encode(invoice, ex["private_key"])
        assert encoded == ex["payment_request"]

    def test_example_12(self):
        """
        Same, but all upper case.
        """
        ex = {
            "payment_request": (
                "LNBC25M1PVJLUEZPP5QQQSYQCYQ5RQWZQFQQQSYQCYQ5RQWZQFQQQSYQCYQ5RQWZQFQYPQDQ5VDHKVEN9V5SXYETP"
                "DEESSP5ZYG3ZYG3ZYG3ZYG3ZYG3ZYG3ZYG3ZYG3ZYG3ZYG3ZYG3ZYG3ZYGS9Q5SQQQQQQQQQQQQQQQQSGQ2A25DXL"
                "5HRNTDTN6ZVYDT7D66HYZSYHQS4WDYNAVYS42XGL6SGX9C4G7ME86A27T07MDTFRY458RTJR0V92CNMSWPSJSCGT2"
                "VCSE3SGPZ3UAPA"
            ),
            "currency": "bc",
            "timestamp": 1496314658,
            "payment_hash": "0001020304050607080900010203040506070809000102030405060708090102",
            "payment_secret": "1111111111111111111111111111111111111111111111111111111111111111",
            "amount": 2_500_000_000,
            "description": "coffee beans",
            "payee": "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
            "features": {"var_onion_optin": "required", "payment_secret": "required", "extra_31": "supported"},
            "feature_list": {
                Feature.var_onion_optin: FeatureState.required,
                Feature.payment_secret: FeatureState.required,
                Feature.extra_31: FeatureState.supported,
            },
            "signature": (
                "5755469bf4b8e6b6ae7a1308d5f9bad5c82812e0855cd24fac242aa323fa820c5c551ede4faeabcb7fb6d5a46"
                "4ad0e35c86f615589ee0e0c250c216a662198c1"
            ),
            "private_key": "e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734",
        }

        decoded = decode(ex["payment_request"])
        assert decoded.currency == ex["currency"]
        assert decoded.timestamp == ex["timestamp"]
        assert decoded.payment_hash == ex["payment_hash"]
        assert decoded.payment_secret == ex["payment_secret"]
        assert decoded.amount == ex["amount"]
        assert decoded.description == ex["description"]
        assert decoded.payee == ex["payee"]
        assert decoded.signature
        assert decoded.signature.hex == ex["signature"]
        assert decoded.features
        assert decoded.features.readable == ex["features"]

        re_encoded = encode(decoded)
        assert re_encoded == ex["payment_request"].lower()

        invoice = Bolt11(
            currency=ex["currency"],
            amount=ex["amount"],
            timestamp=ex["timestamp"],
            tags={
                "p": ex["payment_hash"],
                "d": ex["description"],
                "s": ex["payment_secret"],
                "9": Features.from_feature_list(ex["feature_list"]),
                "n": ex["payee"],
            },
        )

        encoded = encode(invoice, ex["private_key"])
        print(encoded)
        print(ex["payment_request"])
        assert encoded == ex["payment_request"].lower()

    def test_example_13(self):
        """
        Same, but including fields which must be ignored.
        """
        ex = {
            "payment_request": (
                "lnbc25m1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdq5vdhkven9v5sxyetp"
                "deessp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygs9q5sqqqqqqqqqqqqqqqqsgq2qrqqqf"
                "ppnqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqppnqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
                "pp4qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqhpnqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
                "qqqqqqqqqqqqqqqqqqqqqhp4qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqspnqqqqqqqqq"
                "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqsp4qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
                "qqqqqqqqqnp5qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnpkqqqqqqqqqqqqqqqqqqqqqq"
                "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqz599y53s3ujmcfjp5xrdap68qxymkqphwsexhmhr8wdz5usdzkzrse33c"
                "hw6dlp3jhuhge9ley7j2ayx36kawe7kmgg8sv5ugdyusdcqzn8z9x"
            ),
            "currency": "bc",
            "timestamp": 1496314658,
            "payment_hash": "0001020304050607080900010203040506070809000102030405060708090102",
            "payment_secret": "1111111111111111111111111111111111111111111111111111111111111111",
            "amount": 2_500_000_000,
            "description": "coffee beans",
            "payee": "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
            "features": {"var_onion_optin": "required", "payment_secret": "required", "extra_31": "supported"},
            "feature_list": {
                Feature.var_onion_optin: FeatureState.required,
                Feature.payment_secret: FeatureState.required,
                Feature.extra_31: FeatureState.supported,
            },
            "signature": (
                "150a5252308f25bc2641a186de87470189bb003774326beee33b9a2a720d1584386631c5dda6fc3"
                "195f97464bfc93d2574868eadd767d6da1078329c4349c837"
            ),
            "private_key": "e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734",
        }

        decoded = decode(ex["payment_request"])
        assert decoded.currency == ex["currency"]
        assert decoded.timestamp == ex["timestamp"]
        assert decoded.payment_hash == ex["payment_hash"]
        assert decoded.payment_secret == ex["payment_secret"]
        assert decoded.amount == ex["amount"]
        assert decoded.description == ex["description"]
        assert decoded.payee == ex["payee"]
        assert not decoded.fallback
        assert decoded.features
        assert decoded.features.readable == ex["features"]
        assert decoded.signature
        assert decoded.signature.hex == ex["signature"]

    def test_example_14(self):
        """
        Please send 0.01 BTC with payment metadata 0x01fafaf0
        """
        ex = {
            "payment_request": (
                "lnbc10m1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdp9wpshjmt9de6zqmt9"
                "w3skgct5vysxjmnnd9jx2mq8q8a04uqsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygs9q2"
                "gqqqqqqsgq7hf8he7ecf7n4ffphs6awl9t6676rrclv9ckg3d3ncn7fct63p6s365duk5wrk202cfy3aj5xnnp5gs"
                "3vrdvruverwwq7yzhkf5a3xqpd05wjc"
            ),
            "currency": "bc",
            "timestamp": 1496314658,
            "payment_hash": "0001020304050607080900010203040506070809000102030405060708090102",
            "payment_secret": "1111111111111111111111111111111111111111111111111111111111111111",
            "amount": 1_000_000_000,
            "description": "payment metadata inside",
            "metadata": "01fafaf0",
            "payee": "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad",
            "features": {"var_onion_optin": "required", "payment_secret": "required", "extra_6": "required"},
            "feature_list": {
                Feature.var_onion_optin: FeatureState.required,
                Feature.payment_secret: FeatureState.required,
                Feature.extra_6: FeatureState.required,
            },
            "signature": (
                "f5d27be7d9c27d3aa521bc35d77cabd6bda18f1f61716445b19e27e4e17a887508ea8de5a8e1d94f561248f65"
                "434e61a221160dac1f1991b9c0f1057b269d898"
            ),
            "private_key": "e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734",
        }

        decoded = decode(ex["payment_request"])
        assert decoded.currency == ex["currency"]
        assert decoded.timestamp == ex["timestamp"]
        assert decoded.payment_hash == ex["payment_hash"]
        assert decoded.payment_secret == ex["payment_secret"]
        assert decoded.amount == ex["amount"]
        assert decoded.description == ex["description"]
        assert decoded.metadata == ex["metadata"]
        assert decoded.payee == ex["payee"]
        assert decoded.signature
        assert decoded.signature.hex == ex["signature"]
        assert decoded.features
        assert decoded.features.readable == ex["features"]

        re_encoded = encode(decoded)
        assert re_encoded == ex["payment_request"]

        invoice = Bolt11(
            currency=ex["currency"],
            amount=ex["amount"],
            timestamp=ex["timestamp"],
            tags={
                "p": ex["payment_hash"],
                "d": ex["description"],
                "m": ex["metadata"],
                "s": ex["payment_secret"],
                "9": Features.from_feature_list(ex["feature_list"]),
                "n": ex["payee"],
            },
        )
        encoded = encode(invoice, ex["private_key"])
        assert encoded == ex["payment_request"]
