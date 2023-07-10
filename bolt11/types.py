import time
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional

from .models.fallback import Fallback
from .models.features import Features
from .models.routehint import RouteHint
from .models.signature import Signature


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


@dataclass
class Bolt11:
    """Bolt11 Lightning invoice."""

    currency: str
    timestamp: int
    tags: Dict[str, Any]
    amount: Optional[MilliSatoshi] = None
    signature: Optional[Signature] = None

    @property
    def description(self) -> Optional[str]:
        return self.tags["d"] if "d" in self.tags else None

    @property
    def description_hash(self) -> Optional[str]:
        return self.tags["h"] if "h" in self.tags else None

    @property
    def metadata(self) -> Optional[str]:
        return self.tags["m"] if "m" in self.tags else None

    @property
    def dt(self) -> datetime:
        return datetime.fromtimestamp(self.timestamp)

    @property
    def expiry(self) -> Optional[int]:
        return self.tags["x"] if "x" in self.tags else None

    @property
    def features(self) -> Optional[Features]:
        return self.tags["9"] if "9" in self.tags else None

    @property
    def fallback(self) -> Optional[Fallback]:
        return self.tags["f"] if "f" in self.tags else None

    @property
    def route_hints(self) -> Optional[RouteHint]:
        return self.tags["r"] if "r" in self.tags else None

    @property
    def min_final_cltv_expiry(self) -> Optional[int]:
        return self.tags["c"] if "c" in self.tags else 9

    @property
    def payment_hash(self) -> Optional[str]:
        return self.tags["p"] or None

    @property
    def payment_secret(self) -> Optional[str]:
        return self.tags["s"] if "s" in self.tags else None

    @property
    def payee(self) -> Optional[str]:
        return self.tags["n"] if "n" in self.tags else None

    def has_expired(self) -> bool:
        if self.expiry is None:
            return False
        return time.time() > self.timestamp + self.expiry

    def is_mainnet(self) -> bool:
        return self.currency == "bc"

    def is_testnet(self) -> bool:
        return self.currency == "tb"

    def is_regtest(self) -> bool:
        return self.currency == "bcrt"
