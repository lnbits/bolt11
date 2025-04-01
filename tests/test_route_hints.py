from bolt11 import Bolt11, RouteHint, Tag, TagChar, Tags, decode, encode

from .helpers import check_decoded_routes

ex = {
    "payment_request": (
        "lnbc20m1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zy"
        "gspp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqhp58yjmdan7"
        "9s6qqdhdzgynm4zwqd5d7xmw5fk98klysy043l2ahrqsr9yq20q82gphp2nflc7jtzrc"
        "azrra7wwgzxqc8u7754cdlpfrmccae92qgzqvzq2ps8pqqqqqqpqqqqq9qqqvpeuqafq"
        "xu92d8lr6fvg0r5gv0heeeqgcrqlnm6jhphu9y00rrhy4grqszsvpcgpy9qqqqqqgqqq"
        "qq7qqzqr9yq20q82gphp2nflc7jtzrcazrra7wwgzxqc8u7754cdlpfrmccae92qgzqv"
        "zq2ps8pqqqqqp2qqqqq9gqqvpeuqafqxu92d8lr6fvg0r5gv0heeeqgcrqlnm6jhphu9"
        "y00rrhy4grqszsvpcgpy9qqqqzngqqqqq4qqzq4n4scm8c5dh5wzapwv32kwu77dk7zv"
        "uadrrq8w2x3xnl9759cfv3mekg9yw6xvttq9gmh3a2ak4pal0nskkpzt5m8ylaqchze4"
        "tmmlcpdxypch"
    ),
    "private_key": "e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734",
    "currency": "bc",
    "date": 1496314658,
    "payment_hash": "0001020304050607080900010203040506070809000102030405060708090102",
    "payment_secret": (
        "1111111111111111111111111111111111111111111111111111111111111111"
    ),
    "amount_msat": 2_000_000_000,
    "description_hash": (
        "3925b6f67e2c340036ed12093dd44e0368df1b6ea26c53dbe4811f58fd5db8c1"
    ),
    "route_hints": [
        [
            {
                "public_key": (
                    "029e03a901b85534ff1e92c43c74431f7ce72046060fcf7a95c37e148f78c77255"
                ),
                "short_channel_id": "66051x263430x1800",
                "base_fee": 1,
                "ppm_fee": 20,
                "cltv_expiry_delta": 3,
            },
            {
                "public_key": (
                    "039e03a901b85534ff1e92c43c74431f7ce72046060fcf7a95c37e148f78c77255"
                ),
                "short_channel_id": "197637x395016x2314",
                "base_fee": 2,
                "ppm_fee": 30,
                "cltv_expiry_delta": 4,
            },
        ],
        [
            {
                "public_key": (
                    "029e03a901b85534ff1e92c43c74431f7ce72046060fcf7a95c37e148f78c77255"
                ),
                "short_channel_id": "66051x263430x1800",
                "base_fee": 42,
                "ppm_fee": 21,
                "cltv_expiry_delta": 3,
            },
            {
                "public_key": (
                    "039e03a901b85534ff1e92c43c74431f7ce72046060fcf7a95c37e148f78c77255"
                ),
                "short_channel_id": "197637x395016x2314",
                "base_fee": 666,
                "ppm_fee": 21,
                "cltv_expiry_delta": 4,
            },
        ],
    ],
}


class TestRouteHints:
    """Test Route hints"""

    def test_route_hint_unordered(self):
        """
        Test route hints passed with Bolt11(route_hints)
        """
        tags = Tags(
            [
                Tag(TagChar.payment_secret, ex["payment_secret"]),
                Tag(TagChar.payment_hash, ex["payment_hash"]),
                Tag(TagChar.description_hash, ex["description_hash"]),
            ]
        )

        for route_hint in ex["route_hints"]:
            tags.add(TagChar.route_hint, RouteHint.from_list(route_hint))
        invoice = Bolt11(
            currency=ex["currency"],
            amount_msat=ex["amount_msat"],
            date=ex["date"],
            tags=tags,
        )
        encoded = encode(invoice, ex["private_key"])
        assert encoded == ex["payment_request"]
        decoded = decode(ex["payment_request"])
        check_decoded_routes(decoded.route_hints, ex["route_hints"])
        re_encoded = encode(decoded)
        assert re_encoded == ex["payment_request"]


class TestRouteHintsSize:
    def test_channel_id_size(self):
        big_channel_id = "16774490x12969991x22027"
        hints = RouteHint.from_list(
            [
                {
                    "public_key": (
                        "029e03a901b85534ff1e92c43c74431f7ce72046060fcf7a95c37e148f78c77255"
                    ),
                    "short_channel_id": big_channel_id,
                    "base_fee": 1,
                    "ppm_fee": 20,
                    "cltv_expiry_delta": 3,
                }
            ]
        )

        assert hints.data
