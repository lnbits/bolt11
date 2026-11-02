from typing import List

from bitstring import BitArray, Bits, ReadError, pack


def int_to_scid(short_channel_id: int) -> str:
    blockheight = (short_channel_id >> 40) & 0xFFFFFF
    transactionindex = (short_channel_id >> 16) & 0xFFFFFF
    outputindex = short_channel_id & 0xFFFF
    return f"{blockheight}x{transactionindex}x{outputindex}"


def scid_to_int(short_channel_id: str) -> int:
    blockheight, transactionindex, outputindex = short_channel_id.split("x")
    scid = (int(blockheight) << 40) | (int(transactionindex) << 16) | int(outputindex)
    return scid


class BitReader:
    """Reads a bitstring left to right. Works with bitstring 3, 4 and 5,
    which removed ConstBitStream."""

    def __init__(self, bits: Bits):
        self.bits = Bits(bits)
        self.pos = 0

    def __len__(self) -> int:
        return len(self.bits)

    def read(self, length: int) -> Bits:
        if length < 0:
            raise ValueError("Cannot read negative amount.")
        if self.pos + length > len(self.bits):
            available = len(self.bits) - self.pos
            raise ReadError(f"Cannot read {length} bits, only {available} available.")
        out = self.bits[self.pos : self.pos + length]
        self.pos += length
        return out


def bitarray_to_u5(barr):
    assert len(barr) % 5 == 0
    ret = []
    s = BitReader(barr)
    while s.pos != len(s):
        ret.append(s.read(5).uint)
    return ret


def u5_to_bitarray(arr: List[int]) -> Bits:
    """Bech32 spits out array of 5-bit values. Shim here."""
    ret = BitArray()
    for a in arr:
        ret += pack("uint:5", a)
    return ret


def trim_to_bytes(barr: Bits) -> bytes:
    """Adds a byte if necessary."""
    b = barr.tobytes()
    if len(barr) % 8 != 0:
        return b[:-1]
    return b
