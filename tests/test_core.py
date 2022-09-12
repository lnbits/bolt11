from bolt11.core import decode
from hashlib import sha256


class TestDecode:
    """
    Examples: https://github.com/lightningnetwork/lightning-rfc/blob/master/11-payment-encoding.md#examples
    """

    def test_decode_ex1(self):
        payment_request = "lnbc1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdpl2pkx2ctnv5sxxmmwwd5kgetjypeh2ursdae8g6twvus8g6rfwvs8qun0dfjkxaq8rkx3yf5tcsyz3d73gafnh3cax9rn449d9p5uxz9ezhhypd0elx87sjle52x86fux2ypatgddc6k63n7erqz25le42c4u4ecky03ylcqca784w"

        invoice = decode(payment_request)
        assert invoice.currency == "bc"
        assert invoice.timestamp == 1496314658
        assert invoice.payment_hash == "0001020304050607080900010203040506070809000102030405060708090102"
        assert invoice.amount is None
        assert invoice.description == "Please consider supporting this project"
        assert invoice.payee_public_key == "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad"

    def test_decode_ex2(self):
        payment_request = "lnbc2500u1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdq5xysxxatsyp3k7enxv4jsxqzpuaztrnwngzn3kdzw5hydlzf03qdgm2hdq27cqv3agm2awhz5se903vruatfhq77w3ls4evs3ch9zw97j25emudupq63nyw24cg27h2rspfj9srp"

        invoice = decode(payment_request)
        assert invoice.currency == "bc"
        assert invoice.timestamp == 1496314658
        assert invoice.expiry_time == 60
        assert invoice.payment_hash == "0001020304050607080900010203040506070809000102030405060708090102"
        assert invoice.amount == 250000_000
        assert invoice.description == "1 cup coffee"
        assert invoice.payee_public_key == "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad"

    def test_decode_ex3(self):
        payment_request = "lnbc2500u1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdpquwpc4curk03c9wlrswe78q4eyqc7d8d0xqzpuyk0sg5g70me25alkluzd2x62aysf2pyy8edtjeevuv4p2d5p76r4zkmneet7uvyakky2zr4cusd45tftc9c5fh0nnqpnl2jfll544esqchsrny"

        invoice = decode(payment_request)
        assert invoice.currency == "bc"
        assert invoice.timestamp == 1496314658
        assert invoice.expiry_time == 60
        assert invoice.payment_hash == "0001020304050607080900010203040506070809000102030405060708090102"
        assert invoice.amount == 250000_000
        assert invoice.description == "ナンセンス 1杯"
        assert invoice.payee_public_key == "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad"

    def test_decode_ex4(self):
        payment_request = "lntb20m1pvjluezhp58yjmdan79s6qqdhdzgynm4zwqd5d7xmw5fk98klysy043l2ahrqspp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqfpp3x9et2e20v6pu37c5d9vax37wxq72un98kmzzhznpurw9sgl2v0nklu2g4d0keph5t7tj9tcqd8rexnd07ux4uv2cjvcqwaxgj7v4uwn5wmypjd5n69z2xm3xgksg28nwht7f6zspwp3f9t"

        invoice = decode(payment_request)
        assert not invoice.is_mainnet()
        assert invoice.timestamp == 1496314658
        assert invoice.expiry_time == 3600
        assert invoice.payment_hash == "0001020304050607080900010203040506070809000102030405060708090102"
        assert invoice.amount == 2000000_000
        assert invoice.description is None
        assert invoice.payee_public_key == "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad"
        assert invoice.signature.hex() == "b6c42b8a61e0dc5823ea63e76ff148ab5f6c86f45f9722af0069c7934daff70d5e315893300774c897995e3a7476c8193693d144a36e2645a0851e6ebafc9d0a"

    def test_decode_ex5(self):
        payment_request = "lnbc25m1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdq5vdhkven9v5sxyetpdeessp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygs9q5sqqqqqqqqqqqqqqqpqsq67gye39hfg3zd8rgc80k32tvy9xk2xunwm5lzexnvpx6fd77en8qaq424dxgt56cag2dpt359k3ssyhetktkpqh24jqnjyw6uqd08sgptq44qu"

        invoice = decode(payment_request)
        assert invoice.is_mainnet()
        assert invoice.timestamp == 1496314658
        assert invoice.expiry_time == 3600
        assert invoice.payment_hash == "0001020304050607080900010203040506070809000102030405060708090102"
        assert invoice.payment_secret == "1111111111111111111111111111111111111111111111111111111111111111"
        assert invoice.amount == 2500000_000
        assert invoice.description == "coffee beans"
        assert invoice.payee_public_key == "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad"
        assert invoice.signature.hex() == "d7904cc4b74a22269c68c1df68a96c214d651b9376e9f164d3604da4b7deccce0e82aaab4c85d358ea14d0ae342da30812f95d976082eaac813911dae01af3c1"

    def test_decode_ex6(self):
        payment_request = "lnbc20m1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqhp58yjmdan79s6qqdhdzgynm4zwqd5d7xmw5fk98klysy043l2ahrqsfppj3a24vwu6r8ejrss3axul8rxldph2q7z9kk822r8plup77n9yq5ep2dfpcydrjwzxs0la84v3tfw43t3vqhek7f05m6uf8lmfkjn7zv7enn76sq65d8u9lxav2pl6x3xnc2ww3lqpagnh0u"

        invoice = decode(payment_request)
        assert len(invoice.tags.keys()) == 3
        assert invoice.is_mainnet()
        assert invoice.timestamp == 1496314658
        assert invoice.expiry_time == 3600
        assert invoice.payment_hash == "0001020304050607080900010203040506070809000102030405060708090102"
        assert invoice.amount == 2000000_000
        assert invoice.description_hash == sha256("One piece of chocolate cake, one icecream cone, one pickle, one slice of swiss cheese, one slice of salami, one lollypop, one piece of cherry pie, one sausage, one cupcake, and one slice of watermelon".encode("utf-8")).hexdigest()
        assert invoice.payee_public_key == "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad"

    def test_decode_ex7(self):
        payment_request = "lnbc20u1p04ymq3pp5snc5x286nku220fnrwfl7yt0d79raw3vtq3nu6ytnmaltv9sl4uqdqqxq9p5hsqcqzyssp5324mt9549q3eurvccjrhyymdpgtrdq2ex6xkdtwd2gq6ae66zv8qrzjqtqft5rf2w8ed0c5chus7mqg2x7lx49qajrq8x3yhuu2w0msttwzczw3tcqqwdsqqyqqqqlgqqqq86qqpc9qy9qsqmtpgndlkz3mtjkfcdyak8qcr58t4nuqq7ywv85dm5yy5g3wpxjvq7aslsz5pn9atghaxruxg0s0pw5ekmkhqrw3y58s4fvfuh069t7cp5xtsjv"

        invoice = decode(payment_request)
        assert len(invoice.tags.keys()) == 5
        assert invoice.is_mainnet()
        assert invoice.timestamp == 1599237137
        assert invoice.expiry_time == 1728000
        assert invoice.min_final_cltv_expiry == 144
        assert invoice.payment_hash == "84f14328fa9db8a53d331b93ff116f6f8a3eba2c58233e688b9efbf5b0b0fd78"
        assert invoice.amount == 2000_000
        assert not invoice.description
        assert not invoice.description_hash
        assert invoice.payee_public_key == "02c16cca44562b590dd279c942200bdccfd4f990c3a69fad620c10ef2f8228eaff"

    def test_route_hints_ex1(self):
        payment_request = "lnbc9678785340p1pwmna7lpp5gc3xfm08u9qy06djf8dfflhugl6p7lgza6dsjxq454gxhj9t7a0sd8dgfkx7cmtwd68yetpd5s9xar0wfjn5gpc8qhrsdfq24f5ggrxdaezqsnvda3kkum5wfjkzmfqf3jkgem9wgsyuctwdus9xgrcyqcjcgpzgfskx6eqf9hzqnteypzxz7fzypfhg6trddjhygrcyqezcgpzfysywmm5ypxxjemgw3hxjmn8yptk7untd9hxwg3q2d6xjcmtv4ezq7pqxgsxzmnyyqcjqmt0wfjjq6t5v4khxxqyjw5qcqp2rzjq0gxwkzc8w6323m55m4jyxcjwmy7stt9hwkwe2qxmy8zpsgg7jcuwz87fcqqeuqqqyqqqqlgqqqqn3qq9qn07ytgrxxzad9hc4xt3mawjjt8znfv8xzscs7007v9gh9j569lencxa8xeujzkxs0uamak9aln6ez02uunw6rd2ht2sqe4hz8thcdagpleym0j"

        invoice = decode(payment_request)
        route = invoice.route_hints[0]
        assert len(invoice.route_hints) == 1
        assert route.public_key == "03d06758583bb5154774a6eb221b1276c9e82d65bbaceca806d90e20c108f4b1c7"
        assert route.short_channel_id == "589390x3312x1"
        assert route.base_fee == 1000
        assert route.ppm_fee == 2500
        assert route.cltv_expiry_delta == 40

    def test_route_hints_ex2(self):
        payment_request = "lnbc20m1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqhp58yjmdan79s6qqdhdzgynm4zwqd5d7xmw5fk98klysy043l2ahrqsfpp3qjmp7lwpagxun9pygexvgpjdc4jdj85fr9yq20q82gphp2nflc7jtzrcazrra7wwgzxqc8u7754cdlpfrmccae92qgzqvzq2ps8pqqqqqqpqqqqq9qqqvpeuqafqxu92d8lr6fvg0r5gv0heeeqgcrqlnm6jhphu9y00rrhy4grqszsvpcgpy9qqqqqqgqqqqq7qqzqj9n4evl6mr5aj9f58zp6fyjzup6ywn3x6sk8akg5v4tgn2q8g4fhx05wf6juaxu9760yp46454gpg5mtzgerlzezqcqvjnhjh8z3g2qqdhhwkj"

        invoice = decode(payment_request)
        route = invoice.route_hints[1]
        assert len(invoice.route_hints) == 2
        assert route.public_key == "039e03a901b85534ff1e92c43c74431f7ce72046060fcf7a95c37e148f78c77255"
        assert route.short_channel_id == "197637x395016x2314"
        assert route.base_fee == 2
        assert route.ppm_fee == 30
        assert route.cltv_expiry_delta == 4

    def test_testnet_invoice(self):
        payment_request = "lntb100u1p33ag6wpp57j334hcez9w0frtfh5wke43rf8vg9t5r96r6xaprvyax4jfrkd0sdqqcqzpgxqyz5vqsp5wur5sldjky8xn4wzphw6qjavyk7dgxy6rn6jkv3nyvsj3pnlll8q9qyyssqhcajgmyuwvzwylzghl0tep0p4axafjme5jdw8zjfnwm2r94atnhzjhys58t4agnml5x54zrfnqn8nxc6mgg466sh58vnpgs6j7rfjvcpplp0cq"

        invoice = decode(payment_request)
        assert invoice.is_testnet()
        assert invoice.timestamp == 1662952270
        assert invoice.expiry_time == 86400
        assert invoice.payment_hash == "f4a31adf19115cf48d69bd1d6cd62349d882ae832e87a37423613a6ac923b35f"
        assert invoice.amount == 10000_000
        assert invoice.payee_public_key == "020ec0c6a0c4fe5d8a79928ead294c36234a76f6e0dca896c35413612a3fd8dbf8"

    def test_regtest_invoice(self):
        payment_request = "lnbcrt10u1p33a84npp55l3pn5yujm4kry6xt99xkjmlzlgptw7afu6vzfehpg4zr4y2wmasdqqcqzpgxqyz5vqsp5tqnlapkc9afvhvu7l64sj2979n7jc5xwjt6x8gl45ccls9aqrm9s9qyyssq3eneyw5nch4fvwhqhy50vd3snpdxh2j8pmqnlqsmee27m7ehj4z9vf2s4welzz5n6pwferkweygk2sj4j7cttmnqe9m2pamcm26gkzgqt6uu8c"

        invoice = decode(payment_request)
        assert invoice.is_regtest()
        assert invoice.timestamp == 1662951091
        assert invoice.expiry_time == 86400
        assert invoice.payment_hash == "a7e219d09c96eb619346594a6b4b7f17d015bbdd4f34c127370a2a21d48a76fb"
        assert invoice.amount == 1000_000
        assert invoice.payee_public_key == "0229540ad2deab56aa506b0e4b649dea58b23eafc15048e6f63ba899a11266afb9"
