import json
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

    @property
    def json(self) -> str:
        json_data = {
            "currency": self.currency,
            "amount": int(self.amount) if self.amount else 0,
            "timestamp": self.timestamp,
            "signature": self.signature.hex if self.signature else "",
        }
        if self.description:
            json_data["description"] = self.description
        if self.description_hash:
            json_data["description_hash"] = self.description_hash
        if self.metadata:
            json_data["metadata"] = self.metadata
        if self.expiry:
            json_data["expiry"] = self.expiry
        if self.features:
            json_data["features"] = self.features.readable
        if self.fallback:
            json_data["fallback"] = self.fallback.address
        if self.route_hints:
            json_data["route_hints"] = [route._asdict() for route in self.route_hints.routes]
        if self.min_final_cltv_expiry:
            json_data["min_final_cltv_expiry"] = self.min_final_cltv_expiry
        if self.payment_hash:
            json_data["payment_hash"] = self.payment_hash
        if self.payment_secret:
            json_data["payment_secret"] = self.payment_secret
        if self.payee:
            json_data["payee"] = self.payee
        return json.dumps(json_data)

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
