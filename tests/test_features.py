import pytest

from bolt11.decode import decode
from bolt11.models.features import Feature, Features, FeatureState


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
                {Feature.var_onion_optin: FeatureState.required, Feature.payment_secret: FeatureState.required},
            ),
            (
                (
                    "lnbc25m1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdq5vdhkven9v5sxyetp"
                    "deessp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygs9q5sqqqqqqqqqqqqqqqqsgq2a25dxl"
                    "5hrntdtn6zvydt7d66hyzsyhqs4wdynavys42xgl6sgx9c4g7me86a27t07mdtfry458rtjr0v92cnmswpsjscgt2"
                    "vcse3sgpz3uapa"
                ),
                {"var_onion_optin": "required", "payment_secret": "required", "extra_31": "supported"},
                {
                    Feature.var_onion_optin: FeatureState.required,
                    Feature.payment_secret: FeatureState.required,
                    Feature.extra_31: FeatureState.supported,
                },
            ),
            (
                (
                    "lnbc10m1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypqdp9wpshjmt9de6zqmt9"
                    "w3skgct5vysxjmnnd9jx2mq8q8a04uqsp5zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zygs9q2"
                    "gqqqqqqsgq7hf8he7ecf7n4ffphs6awl9t6676rrclv9ckg3d3ncn7fct63p6s365duk5wrk202cfy3aj5xnnp5gs"
                    "3vrdvruverwwq7yzhkf5a3xqpd05wjc"
                ),
                {"var_onion_optin": "required", "payment_secret": "required", "extra_6": "required"},
                {
                    Feature.var_onion_optin: FeatureState.required,
                    Feature.payment_secret: FeatureState.required,
                    Feature.extra_6: FeatureState.required,
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
