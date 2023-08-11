from typing import Optional

from bech32 import CHARSET, bech32_encode
from bitstring import BitArray, Bits, pack

from .bit_utils import bitarray_to_u5
from .exceptions import (
    Bolt11InvalidDescriptionHashException,
    Bolt11NoSignatureException,
)
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


def _create_hrp(currency: str, amount_msat: Optional[MilliSatoshi]) -> str:
    hrp = "ln" + currency
    if amount_msat:
        hrp += msat_to_amount(amount_msat)
    return hrp


def encode(
    invoice: Bolt11,
    private_key: Optional[str] = None,
    ignore_exceptions: bool = False,
    strict: bool = False,
) -> str:
    try:
        if invoice.description_hash:
            bytes.fromhex(invoice.description_hash)
    except Exception as exc:
        raise Bolt11InvalidDescriptionHashException() from exc

    timestamp = BitArray(uint=invoice.date, length=35)
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

    hrp = _create_hrp(invoice.currency, invoice.amount_msat)
    data_part = timestamp + tags

    if private_key:
        invoice.signature = Signature.from_private_key(private_key, hrp, data_part)

    if not invoice.signature:
        raise Bolt11NoSignatureException()

    signature_part = BitArray(invoice.signature.signature_data)

    if not ignore_exceptions:
        invoice.validate(strict=strict)

    encoded = bech32_encode(hrp, bitarray_to_u5(data_part + signature_part))

    return encoded
