import base58  # type: ignore
import re

from bech32 import bech32_encode, bech32_decode, CHARSET  # type: ignore
from binascii import unhexlify
from bitstring import ConstBitStream  # type: ignore
from ecdsa import SECP256k1, VerifyingKey  # type: ignore
from ecdsa.util import sigdecode_string  # type: ignore
from hashlib import sha256

from .types import LightningInvoice, MilliSatoshi, Route, Signature
from .utils import amount_to_msat, trim_to_bytes, bitarray_to_u5, u5_to_bitarray


base58_prefix_map = {"bc": (0, 5), "tb": (111, 196)}


def _pull_tagged(stream):
    tag = stream.read(5).uint
    length = stream.read(5).uint * 32 + stream.read(5).uint

    return (CHARSET[tag], stream.read(length * 5), stream)


def _parse_fallback(fallback, currency):
    if currency in ["bc", "tb"]:
        wver = fallback[0:5].uint
        if wver == 17:
            addr = base58.b58encode_check(bytes([base58_prefix_map[currency][0]]) + fallback[5:].tobytes())
        elif wver == 18:
            addr = base58.b58encode_check(bytes([base58_prefix_map[currency][1]]) + fallback[5:].tobytes())
        elif wver <= 16:
            addr = bech32_encode(currency, bitarray_to_u5(fallback))
        else:
            return None
    else:
        addr = fallback.tobytes()
    return addr


def _readable_scid(short_channel_id: int) -> str:
    return "{blockheight}x{transactionindex}x{outputindex}".format(
        blockheight=((short_channel_id >> 40) & 0xFFFFFF),
        transactionindex=((short_channel_id >> 16) & 0xFFFFFF),
        outputindex=(short_channel_id & 0xFFFF),
    )


def encode():
    raise NotImplementedError


def decode(bech32_pr: str) -> LightningInvoice:
    hrp, bech32_data = bech32_decode(bech32_pr)
    route_hints = []
    tags = {}

    if not hrp or not bech32_data or not hrp.startswith("ln"):
        raise ValueError("Bech32 is not valid.")

    matches = re.match(r"ln(bc|bcrt|tb)(\w+)?", hrp)
    assert matches, "Human readable part is not valid."

    currency, amount_str = matches.groups()
    data_part = u5_to_bitarray(bech32_data)

    # Final signature is 65 bytes, split it off.
    # signature =>
    # "a valid 512-bit secp256k1 signature of the SHA2 256-bit hash of the human-readable part
    # represented as UTF-8 bytes, concatenated with the data part (excluding the signature) with 0 bits appended
    # to pad the data to the next byte boundary, with a trailing byte containing the recovery ID (0, 1, 2, or 3)"

    if len(data_part) < 65 * 8:
        raise ValueError("Too short to contain signature")

    signature_data = data_part[-65 * 8 :].tobytes()
    data = ConstBitStream(data_part[: -65 * 8])
    signature = Signature(data=signature_data, signing_data=(hrp.encode("utf-8") + data.tobytes()))
    timestamp = data.read(35).uint

    # Look for tags in data

    while data.pos != data.len:
        tag, tagdata, data = _pull_tagged(data)
        data_length = len(tagdata) // 5

        if tag == "p" and data_length == 52:
            # p (1): data_length 52. 256-bit SHA256 payment_hash. Preimage of this provides proof of payment.
            tags["p"] = trim_to_bytes(tagdata).hex()

        elif tag == "x":
            # x (6): data_length variable. expiry time in seconds (big-endian). Default is 3600.
            tags["x"] = tagdata.uint

        elif tag == "d":
            # d (13): data_length variable. Short description of purpose of payment (UTF-8).
            tags["d"] = trim_to_bytes(tagdata).decode("utf-8")

        elif tag == "h" and data_length == 52:
            # h (23): data_length 52. 256-bit description of purpose of payment (SHA256).
            tags["h"] = trim_to_bytes(tagdata).hex()

        elif tag == "s" and data_length == 52:
            # s (16): data_length 52. This 256-bit secret prevents forwarding nodes from probing the payment recipient.
            tags["s"] = trim_to_bytes(tagdata).hex()

        elif tag == "c":
            # c (24): data_length variable. min_final_cltv_expiry to use for the last HTLC in the route. Default is 9.
            tags["c"] = tagdata.uint

        elif tag == "n" and data_length == 53:
            # n (19): data_length 53. 33-byte public key of the payee node.
            tags["n"] = trim_to_bytes(tagdata).hex()

        elif tag == "f":
            # f (9): data_length variable, depending on version. Fallback on-chain address.
            tags["f"] = _parse_fallback(tagdata, currency)

        elif tag == "r":
            # r (3): `data_length` variable.
            # One or more entries containing extra routing information for a private route;
            # there may be more than one `r` field, too.
            #  * `pubkey` (264 bits)
            #  * `short_channel_id` (64 bits)
            #  * `feebase` (32 bits, big-endian)
            #  * `feerate` (32 bits, big-endian)
            #  * `cltv_expiry_delta` (16 bits, big-endian)
            s = ConstBitStream(tagdata)

            while s.pos + 264 + 64 + 32 + 32 + 16 < s.len:
                route_hints.append(
                    Route(
                        public_key=s.read(264).tobytes().hex(),
                        short_channel_id=_readable_scid(s.read(64).intbe),
                        base_fee=MilliSatoshi(s.read(32).intbe),
                        ppm_fee=s.read(32).intbe,
                        cltv_expiry_delta=s.read(16).intbe,
                    )
                )

    # A reader MUST use the `n` field to validate the signature instead of
    # performing signature recovery if a valid `n` field is provided.

    message = bytearray([ord(c) for c in hrp]) + data.tobytes()
    sig = signature_data[0:64]

    if "n" in tags:
        payee_public_key = tags["n"]
        vk = VerifyingKey.from_string(unhexlify(payee_public_key), curve=SECP256k1)
        if not vk.verify(sig, message, sha256, sigdecode=sigdecode_string):
            raise ValueError("Could not verify public key")
    else:
        vk = VerifyingKey.from_public_key_recovery(sig, message, SECP256k1, sha256)
        signaling_byte = signature_data[64]
        key = vk[int(signaling_byte)]
        payee_public_key = key.to_string("compressed").hex()

    return LightningInvoice(
        amount=amount_to_msat(amount_str) if amount_str else None,
        currency=currency,
        timestamp=timestamp,
        payee_public_key=payee_public_key,
        route_hints=route_hints,
        signature=signature,
        tags=tags,
    )
