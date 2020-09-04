import time

from datetime import datetime
from decimal import Decimal
from hashlib import sha256
from typing import Any, Dict, List, NamedTuple, Optional


class LightningInvoice(NamedTuple):
    """Lightning invoice."""

    currency: str
    payee_public_key: str
    signature: "Signature"
    tags: Dict[str, Any]
    timestamp: int
    amount: Optional["MilliSatoshi"] = None
    route_hints: List["Route"] = []

    @property
    def description(self) -> Optional[str]:
        return self.tags["d"] if "d" in self.tags else None

    @property
    def description_hash(self) -> Optional[str]:
        return self.tags["h"] if "h" in self.tags else None

    @property
    def dt(self) -> datetime:
        return datetime.fromtimestamp(self.timestamp)

    @property
    def expiry_time(self) -> int:
        return self.tags["x"] if "x" in self.tags else 3600

    @property
    def fallback_on_chain_address(self) -> Optional[str]:
        return self.tags["f"] if "f" in self.tags else None

    @property
    def min_final_cltv_expiry(self) -> Optional[int]:
        return self.tags["c"] if "c" in self.tags else 9

    @property
    def payment_hash(self) -> str:
        return self.tags["p"]

    @property
    def payment_secret(self) -> Optional[str]:
        return self.tags["s"] if "s" in self.tags else None

    def has_expired(self) -> bool:
        return time.time() > self.timestamp + self.expiry_time

    def is_mainnet(self) -> bool:
        return self.currency == "bc"


class MilliSatoshi(int):
    """A thousandth of a satoshi."""

    @classmethod
    def from_btc(cls, btc: Decimal) -> "MilliSatoshi":
        return cls(btc * 100_000_000_000)

    @property
    def btc(self) -> Decimal:
        return Decimal(self) / 100_000_000_000

    @property
    def sat(self) -> int:
        return self // 1000


class Route(NamedTuple):
    public_key: str
    short_channel_id: str
    base_fee: MilliSatoshi
    ppm_fee: int
    cltv_expiry_delta: int


class Signature(NamedTuple):
    """An invoice signature."""

    data: bytes
    signing_data: bytes

    @property
    def r(self) -> str:
        return self.data[:32].hex()

    @property
    def s(self) -> str:
        return self.data[32:64].hex()

    @property
    def recovery_flag(self) -> int:
        return int(self.data[64])

    @property
    def preimage(self) -> bytes:
        return sha256(self.signing_data).digest()

    def hex(self) -> str:
        return self.data[:64].hex()
