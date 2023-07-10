from re import match
from typing import Any, Dict

from bech32 import CHARSET, bech32_decode
from bitstring import ConstBitStream

from .bit_utils import trim_to_bytes, u5_to_bitarray
from .models.fallback import Fallback
from .models.features import Features
from .models.routehint import RouteHint
from .models.signature import Signature
from .types import Bolt11
from .utils import amount_to_msat


def _pull_tagged(stream):
    tag = stream.read(5).uint
    length = stream.read(5).uint * 32 + stream.read(5).uint
    return (CHARSET[tag], stream.read(length * 5), stream)


def decode(pr: str) -> Bolt11:
    """bolt11 decoder,
    based on https://github.com/rustyrussell/lightning-payencode/blob/master/lnaddr.py
    """

    hrp, bech32_data = bech32_decode(pr)
    if hrp is None or bech32_data is None or hrp.startswith("ln") is None:
        raise ValueError("Bech32 is not valid")

    matches = match(r"ln(bcrt|bc|tb)(\w+)?", hrp)
    if matches is None:
        raise ValueError("Human readable part is not valid.")

    currency, amount_str = matches.groups()
    data = u5_to_bitarray(bech32_data)

    # final signature 65 bytes, split it off.
    if len(data) < 65 * 8:
        raise ValueError("Too short to contain signature")

    # extract the signature
    signature_data = data[-65 * 8 :].tobytes()

    # the tagged fields as a bitstream
    data_part = ConstBitStream(data[: -65 * 8])

    # decode the amount from the hrp
    amount_msat = amount_to_msat(amount_str) if amount_str else None

    timestamp = data_part.read(35).uint  # type: ignore

    tags: Dict[str, Any] = {}

    while data_part.pos != data_part.len:
        tag, tagdata, data_part = _pull_tagged(data_part)
        data_length = len(tagdata or []) / 5  # type: ignore

        # MUST skip over unknown fields, OR an f field with unknown version, OR p, h, s or n
        # fields that do NOT have data_lengths of 52, 52, 52 or 53, respectively.

        if tag == "p" and data_length == 52 and not hasattr(tags, "p"):
            tags["p"] = trim_to_bytes(tagdata).hex()  # type: ignore
        elif tag == "h" and data_length == 52 and not hasattr(tags, "h") and not hasattr(tags, "d"):
            tags["h"] = trim_to_bytes(tagdata).hex()  # type: ignore
        elif tag == "s" and data_length == 52 and not hasattr(tags, "s"):
            tags["s"] = trim_to_bytes(tagdata).hex()  # type: ignore
        elif tag == "n" and data_length == 53 and not hasattr(tags, "n"):
            tags["n"] = trim_to_bytes(tagdata).hex()  # type: ignore

        elif tag == "d" and not hasattr(tags, "d") and not hasattr(tags, "h"):
            tags["d"] = trim_to_bytes(tagdata).decode()  # type: ignore
        elif tag == "m":
            tags["m"] = trim_to_bytes(tagdata).hex()  # type: ignore
        elif tag == "x":
            tags["x"] = tagdata.uint  # type: ignore
        elif tag == "c":
            tags["c"] = tagdata.uint  # type: ignore
        elif tag == "f":
            tags["f"] = Fallback.from_bitstring(tagdata, currency)  # type: ignore
        elif tag == "9":
            tags["9"] = Features.from_bitstring(tagdata)  # type: ignore
        elif tag == "r":
            tags["r"] = RouteHint.from_bitstring(tagdata)  # type: ignore

    signature = Signature(signature_data=signature_data, signing_data=hrp.encode() + data_part.tobytes())

    # A reader MUST check that the `signature` is valid (see the `n` tagged field specified below).
    # A reader MUST use the `n` field to validate the signature instead of
    # performing signature recovery if a valid `n` field is provided.
    if hasattr(tags, "n"):
        # TODO: research why no test runs this?
        signature.verify(tags["n"])
    else:
        tags["n"] = signature.recover_public_key()

    return Bolt11(
        currency=currency,
        amount=amount_msat,
        timestamp=timestamp,
        signature=signature,
        tags=tags,
    )
