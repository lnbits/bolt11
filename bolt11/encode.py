from typing import Optional

from bech32 import CHARSET, bech32_encode
from bitstring import BitArray, Bits, pack

from .bit_utils import bitarray_to_u5
from .models.signature import Signature
from .types import Bolt11, MilliSatoshi
from .utils import msat_to_amount


# Tagged field containing BitArray
def _tagged(char: str, bits: Bits):
    # Tagged fields need to be zero-padded to 5 bits.
    while bits.len % 5 != 0:
        bits.append("0b0")  # type: ignore
    return (
        pack(
            "uint:5, uint:5, uint:5",
            CHARSET.find(char),
            (bits.len / 5) / 32,
            (bits.len / 5) % 32,
        )
        + bits
    )


def _tagged_bytes(char: str, bits: bytes):
    return _tagged(char, BitArray(bits))


def _tagged_int(tag: bytes):
    """Get minimal length by trimming leading 5 bits at a time."""
    value = pack("intbe:64", tag)[4:64]
    while value.startswith("0b00000"):
        value = value[5:]
    return value


def _create_hrp(currency: str, amount: Optional[MilliSatoshi]) -> str:
    hrp = "ln" + currency
    if amount:
        hrp += msat_to_amount(amount)
    return hrp


def encode(invoice: Bolt11, private_key: Optional[str] = None) -> str:
    # A writer MUST include either a `d` or `h` field, and MUST NOT include
    if invoice.description and invoice.description_hash:
        raise ValueError("Cannot include both 'd' and 'h'")
    if not invoice.description and not invoice.description_hash:
        raise ValueError("Must include either 'd' or 'h'")

    timestamp = BitArray(uint=invoice.timestamp, length=35)
    tags = BitArray()

    for k, tag in invoice.tags.items():
        if k == "s":
            tags += _tagged_bytes("s", bytes.fromhex(tag))
        elif k == "p":
            tags += _tagged_bytes("p", bytes.fromhex(tag))
        elif k == "d":
            tags += _tagged_bytes("d", tag.encode())
        elif k == "h":
            tags += _tagged_bytes("h", bytes.fromhex(tag))
        elif k == "m":
            tags += _tagged_bytes("m", bytes.fromhex(tag))
        # elif k == "n":
        #     tags += _tagged_bytes("n", bytes.fromhex(tag))
        elif k == "9":
            tags += _tagged_bytes("9", tag.data)
        elif k == "f":
            if tag:
                tags += _tagged_bytes("f", tag.data)
        elif k == "c":
            tags += _tagged("c", _tagged_int(tag))
        elif k == "x":
            tags += _tagged("x", _tagged_int(tag))
        elif k == "r":
            tags += _tagged("r", tag.data)

    hrp = _create_hrp(invoice.currency, invoice.amount)

    if private_key:
        invoice.signature = Signature.from_private_key(private_key, hrp, timestamp + tags)

    if not invoice.signature:
        raise ValueError("Must include either 'signature' or 'private_key'")

    encoded = bech32_encode(hrp, bitarray_to_u5(timestamp + tags + BitArray(invoice.signature.signature_data)))
    return encoded
