from enum import Enum
from math import floor
from typing import Dict, NamedTuple, Optional

from bitstring import BitArray, Bits


class FeatureState(Enum):
    required = 0
    supported = 1


class Feature(Enum):
    option_data_loss_protect = 0
    initial_routing_sync = 1
    option_upfront_shutdown_script = 2
    gossip_queries = 3
    var_onion_optin = 4
    gossip_queries_ex = 5
    option_static_remotekey = 6
    payment_secret = 7
    basic_mpp = 8
    option_support_large_channel = 9
    option_anchor_outputs = 10
    option_anchors_zero_fee_htlc_tx = 11
    option_route_blinding = 13
    option_shutdown_anysegwit = 14
    option_channel_type = 15
    option_scid_alias = 16
    option_payment_metadata = 17
    option_zeroconf_chanids = 18
    extra_1 = 19
    extra_2 = 20
    extra_3 = 21
    extra_4 = 22
    extra_5 = 23
    extra_6 = 24
    extra_7 = 25
    extra_8 = 26
    extra_9 = 27
    extra_10 = 28
    extra_11 = 29
    extra_12 = 30
    extra_13 = 31
    extra_14 = 32
    extra_15 = 33
    extra_16 = 34
    extra_17 = 35
    extra_18 = 36
    extra_19 = 37
    extra_20 = 38
    extra_21 = 39
    extra_22 = 40
    extra_23 = 41
    extra_24 = 42
    extra_25 = 43
    extra_26 = 44
    extra_27 = 45
    extra_28 = 46
    extra_29 = 47
    extra_30 = 48
    extra_31 = 49


class Features(NamedTuple):
    data: Bits
    feature_list: Dict[Feature, FeatureState]

    @classmethod
    def from_bitstring(cls, data: Bits) -> "Features":
        length = data.length
        feature_list: Dict[Feature, FeatureState] = {}
        for i in range(0, length):
            feature_index = floor(i / 2)
            if floor(i / 2) > len(Feature):
                raise ValueError(f"Feature index ({i}) out of range, word_length: {length}")
            si = i + 1
            cut = data[-si : -si + 1] if i > 0 else data[-si:]
            if bool(cut):
                feature = Feature(floor(i / 2))
                if feature not in feature_list:
                    feature_list[Feature(feature_index)] = FeatureState.supported if i % 2 else FeatureState.required
        return cls(data, feature_list)

    @classmethod
    def from_feature_list(cls, feature_list: Dict[Feature, FeatureState]) -> "Features":
        length = max([feature.value + 1 for feature in feature_list]) * 2
        data = BitArray(length=length)
        for feature, feature_state in feature_list.items():
            if feature_state == FeatureState.required:
                data.invert(feature.value * 2)  # type: ignore
            elif feature_state == FeatureState.supported:
                data.invert(feature.value * 2 + 1)  # type: ignore
            else:
                raise ValueError("Unknown feature state")
        # Remove trailing zeroes
        while data[-1:] == "0b0":
            data = BitArray(data[:-1])
        # add zeroes
        while data.len % 5 != 0:
            data.append("0b0")  # type: ignore
        data.reverse()  # type: ignore
        return cls(data, feature_list)

    @property
    def readable(self) -> Dict[str, str]:
        json: Dict[str, str] = {}
        for feature, feature_state in self.feature_list.items():
            json[feature.name] = feature_state.name
        return json

    def has_feature(self, feature_string: str) -> Optional[str]:
        for feature, feature_state in self.feature_list.items():
            if feature.name == feature_string:
                return feature_state.name
        return None
