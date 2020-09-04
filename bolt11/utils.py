import bitstring  # type: ignore
import re

from decimal import Decimal
from typing import Union

from .types import MilliSatoshi


def amount_to_msat(amount: str) -> MilliSatoshi:
    """Given a shortened amount, convert it into millisatoshis."""
    if not re.fullmatch(r"\d+[pnum]?", amount):
        raise ValueError(f"Invalid amount `{amount}`")

    try:
        num = {"p": 10 ** 12, "n": 10 ** 9, "u": 10 ** 6, "m": 10 ** 3}[amount[-1]]
        return MilliSatoshi.from_btc(Decimal(amount[:-1]) / num)
    except KeyError:
        return MilliSatoshi.from_btc(Decimal(amount))


def amount_to_sat(amount: str) -> int:
    """Given a shortened amount, convert it into satoshis."""
    return amount_to_msat(amount).sat


def amount_to_btc(amount: str) -> Decimal:
    """Given a shortened amount, convert it into bitcoin."""
    return amount_to_msat(amount).btc


def msat_to_amount(msat: int) -> str:
    """Given an amount in millisatoshis, shorten it."""
    if not isinstance(msat, int):
        raise ValueError("`msat` should be an integer.")

    value = msat * 10

    for unit in ["p", "n", "u", "m", ""]:
        if value % 1000 == 0:
            value //= 1000
        else:
            break

    return f"{value}{unit}"


def sat_to_amount(sat: int) -> str:
    """Given an amount in satoshis, shorten it."""
    return msat_to_amount(sat * 1000)


def btc_to_amount(btc: Union[int, Decimal]) -> str:
    """Given an amount in bitcoin, shorten it."""
    return msat_to_amount(MilliSatoshi.from_btc(Decimal(btc)))


def bitarray_to_u5(barr):
    assert barr.len % 5 == 0
    ret = []
    s = bitstring.ConstBitStream(barr)
    while s.pos != s.len:
        ret.append(s.read(5).uint)
    return ret


def u5_to_bitarray(arr):
    """Bech32 spits out array of 5-bit values. Shim here."""
    ret = bitstring.BitArray()
    for a in arr:
        ret += bitstring.pack("uint:5", a)
    return ret


def trim_to_bytes(barr) -> bytes:
    """Adds a byte if necessary."""
    b = barr.tobytes()
    if barr.len % 8 != 0:
        return b[:-1]
    return b
