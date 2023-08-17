from datetime import datetime, timezone

import pytest
from bitstring import Bits

from bolt11 import (
    Bolt11,
    Feature,
    FeatureExtra,
    Features,
    FeatureState,
    Tag,
    TagChar,
    Tags,
    decode,
    encode,
)
from bolt11.exceptions import Bolt11FeatureException


class TestDecodeFeatures:
    """
    Test decoding of features.
    """

    @pytest.mark.parametrize(
        "bolt11, features, feature_list",
        [
            (
                (
                    "lnbc1pvjluezsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygspp5qqqsyqcy"
                    "q5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdpl2pkx2ctnv5sxxmmwwd5kgetjypeh2urs"
                    "dae8g6twvus8g6rfwvs8qun0dfjkxaq9qrsgq357wnc5r2ueh7ck6q93dj32dlqnls087fxdwk8qakd"
                    "yafkq3yap9us6v52vjjsrvywa6rt52cm9r9zqt8r2t7mlcwspyetp5h2tztugp9lfyql"
                ),
                {"var_onion_optin": "required", "payment_secret": "required"},
                {
                    Feature.var_onion_optin: FeatureState.required,
                    Feature.payment_secret: FeatureState.required,
                },
            ),
            (
                (
                    "lnbc10m1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdp9wpshjmt9de6zqmt9"
                    "w3skgct5vysxjmnnd9jx2mq8q8a04uqsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygs9q2"
                    "gqqqqqqsgq7hf8he7ecf7n4ffphs6awl9t6676rrclv9ckg3d3ncn7fct63p6s365duk5wrk202cfy3aj5xnnp5gs"
                    "3vrdvruverwwq7yzhkf5a3xqpd05wjc"
                ),
                {
                    "var_onion_optin": "required",
                    "payment_secret": "required",
                    "extra_24": "required",
                },
                {
                    Feature.var_onion_optin: FeatureState.required,
                    Feature.payment_secret: FeatureState.required,
                    FeatureExtra(24): FeatureState.required,
                },
            ),
            (
                # phoenix invoice
                (
                    "lnbc1950n1pjtrgxnpp5ye3lhh8ye8ywm85evshn9wyhdsdg9a350tdhm3dyw89mwfht8s9qdqqxqyj"
                    "w5q9q7sqqqqqqqqqqqqqqqqqqqqqqqqq9qsqsp5z22wjrrm0lgl32e0yes38dzmvjxnajrvanhw3hp4"
                    "duq4k55wl0gsrzjqwryaup9lh50kkranzgcdnn2fgvx390wgj5jd07rwr3vxeje0glclludsryzx7vv"
                    "vqqqqqlgqqqqqeqqjqqq3zq0d9kw8q4fhsgxh595f2l0ass4zaj2pdknzhxzzrlf7g5wgsk3nlgzzed"
                    "uhnp6mva9jehwcq9y4hrllwt6ffl822q5drdgvxtjspmgfnls"
                ),
                {
                    "var_onion_optin": "supported",
                    "payment_secret": "supported",
                    "basic_mpp": "supported",
                    "extra_74": "supported",
                },
                {
                    Feature.var_onion_optin: FeatureState.supported,
                    Feature.payment_secret: FeatureState.supported,
                    Feature.basic_mpp: FeatureState.supported,
                    FeatureExtra(74): FeatureState.supported,
                },
            ),
        ],
    )
    def test_decode_features(self, bolt11, features, feature_list):
        decoded = decode(bolt11)
        assert decoded.features
        assert decoded.features.readable == features
        new_features = Features.from_feature_list(feature_list)
        assert decoded.features.data == new_features.data

    def test_encode_features_and_compare_readable(self):
        features = Features.from_feature_list(
            {
                Feature.option_static_remotekey: FeatureState.required,
                Feature.option_support_large_channel: FeatureState.required,
                Feature.option_anchor_outputs: FeatureState.supported,
                Feature.option_channel_type: FeatureState.supported,
                FeatureExtra(26): FeatureState.supported,
            }
        )
        features_fromhex = Features.from_bitstring(Bits(hex="02000002024100"))
        assert features_fromhex.readable == features.readable

    def test_encode_feature_exception(self):
        Features.from_feature_list(
            {
                FeatureExtra(len(Feature)): FeatureState.supported,
            }
        )
        with pytest.raises(Bolt11FeatureException):
            Features.from_feature_list(
                {
                    FeatureExtra(len(Feature) - 1): FeatureState.supported,
                }
            )

    def test_encode_extra_features(self):
        bits = Bits(hex="02000002024100")
        features = Features.from_bitstring(bits)
        payment_hash = (
            "0001020304050607080900010203040506070809000102030405060708090102"
        )
        payment_secret = (
            "1111111111111111111111111111111111111111111111111111111111111111"
        )
        invoice = Bolt11(
            "bcrt",
            int(datetime.now(tz=timezone.utc).timestamp()),
            Tags(
                [
                    Tag(TagChar.payment_hash, payment_hash),
                    Tag(TagChar.payment_secret, payment_secret),
                    Tag(TagChar.description, "extra feature bits are broken"),
                    Tag(TagChar.features, features),
                ]
            ),
        )
        assert invoice.features
        assert invoice.features.data.bin == features.data.bin
        assert not invoice.features.data.len % 5
        encoded = encode(
            invoice,
            "e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734",
        )
        decoded = decode(encoded)
        assert decoded.features
        assert decoded.features.data.bin == features.data.bin
