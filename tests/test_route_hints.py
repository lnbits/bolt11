from bolt11.decode import decode
from bolt11.encode import encode
from bolt11.types import Bolt11, RouteHint

from .helpers import check_decoded_routes

ex = {
    "payment_request": (
        "lnbc20m1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygspp"
        "5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqhp58yjmdan79s6qqdhd"
        "zgynm4zwqd5d7xmw5fk98klysy043l2ahrqsr9yq20q82gphp2nflc7jtzrcazrra7wwgzxq"
        "c8u7754cdlpfrmccae92qgzqvzq2ps8pqqqqqqpqqqqq9qqqvpeuqafqxu92d8lr6fvg0r5g"
        "v0heeeqgcrqlnm6jhphu9y00rrhy4grqszsvpcgpy9qqqqqqgqqqqq7qqzqr9yq20q82gphp"
        "2nflc7jtzrcazrra7wwgzxqc8u7754cdlpfrmccae92qgzqvzq2ps8pqqqqqqpqqqqq9qqqv"
        "peuqafqxu92d8lr6fvg0r5gv0heeeqgcrqlnm6jhphu9y00rrhy4grqszsvpcgpy9qqqqqqg"
        "qqqqq7qqzqlqkuumdsr62lvjtxtudqgd4mvrnrkxch89ysjey8rsyxrayj9ver5zhjspfg3r"
        "yvhteg66ksmtfau3an020rn0cjetdjgk22vq4t4yspg629pd"
    ),
    "private_key": (
        "e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734"
    ),
    "currency": "bc",
    "date": 1496314658,
    "payment_hash": (
        "0001020304050607080900010203040506070809000102030405060708090102"
    ),
    "payment_secret": (
        "1111111111111111111111111111111111111111111111111111111111111111"
    ),
    "amount_msat": 2_000_000_000,
    "description_hash": (
        "3925b6f67e2c340036ed12093dd44e0368df1b6ea26c53dbe4811f58fd5db8c1"
    ),
    "route_hints": [[
        {
            "public_key": (
                "029e03a901b85534ff1e92c43c74431f7ce72"
                "046060fcf7a95c37e148f78c77255"
            ),
            "short_channel_id": "66051x263430x1800",
            "base_fee": 1,
            "ppm_fee": 20,
            "cltv_expiry_delta": 3,
        },
        {
            "public_key": (
                "039e03a901b85534ff1e92c43c74431f7ce"
                "72046060fcf7a95c37e148f78c77255"
            ),
            "short_channel_id": "197637x395016x2314",
            "base_fee": 2,
            "ppm_fee": 30,
            "cltv_expiry_delta": 4,
        },
    ],[
        {
            "public_key": (
                "029e03a901b85534ff1e92c43c74431f7ce72"
                "046060fcf7a95c37e148f78c77255"
            ),
            "short_channel_id": "66051x263430x1800",
            "base_fee": 42,
            "ppm_fee": 21,
            "cltv_expiry_delta": 3,
        },
        {
            "public_key": (
                "039e03a901b85534ff1e92c43c74431f7ce"
                "72046060fcf7a95c37e148f78c77255"
            ),
            "short_channel_id": "197637x395016x2314",
            "base_fee": 666,
            "ppm_fee": 21,
            "cltv_expiry_delta": 4,
        },
    ]],
    }


class TestRouteHints:
    """ Test Route hints """

    def test_route_hint_unordered(self):
        """
        Test route hints passed with Bolt11(route_hints)
        """
        decoded = decode(ex["payment_request"])
        check_decoded_routes(decoded.route_hints, ex["route_hints"])

        re_encoded = encode(decoded)
        assert re_encoded == ex["payment_request"]

        invoice = Bolt11(
            currency=ex["currency"],
            amount_msat=ex["amount_msat"],
            date=ex["date"],
            tags={
                "s": ex["payment_secret"],
                "p": ex["payment_hash"],
                "h": ex["description_hash"],
                "r0": RouteHint.from_list(ex["route_hints"][0]),
                "r1": RouteHint.from_list(ex["route_hints"][0]),
            },
        )

        encoded = encode(invoice, ex["private_key"])
        assert encoded == ex["payment_request"]
