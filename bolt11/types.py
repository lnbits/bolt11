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
    date: int
    tags: Dict[str, Any]
    amount_msat: Optional[MilliSatoshi] = None
    signature: Optional[Signature] = None

    def validate(self) -> None:
        if "p" not in self.tags:
            raise Bolt11NoPaymentHashException("Missing 'payment_hash'")
        if "d" in self.tags and "h" in self.tags:
            raise Bolt11DescriptionException("Cannot include both 'description' and 'description_hash'")
        if "d" not in self.tags and "h" not in self.tags:
            raise Bolt11DescriptionException("Must include either 'description' or 'description_hash'")

    def has_expired(self) -> bool:
        if self.expiry is None:
            return False
        return time.time() > self.date + self.expiry

    def is_mainnet(self) -> bool:
        return self.currency == "bc"

    def is_testnet(self) -> bool:
        return self.currency == "tb"

    def is_regtest(self) -> bool:
        return self.currency == "bcrt"

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
        return datetime.fromtimestamp(self.date)

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
        return self.tags["p"] if "p" in self.tags else None

    @property
    def payment_secret(self) -> Optional[str]:
        return self.tags["s"] if "s" in self.tags else None

    @property
    def payee(self) -> Optional[str]:
        return self.tags["n"] if "n" in self.tags else None

    @property
    def data(self) -> dict:
        data = {
            "currency": self.currency,
            "amount_msat": int(self.amount_msat) if self.amount_msat else 0,
            "date": self.date,
            "signature": self.signature.hex if self.signature else "",
        }
        if self.description:
            data["description"] = self.description
        if self.description_hash:
            data["description_hash"] = self.description_hash
        if self.metadata:
            data["metadata"] = self.metadata
        if self.expiry:
            data["expiry"] = self.expiry
        if self.features:
            data["features"] = self.features.readable
        if self.fallback:
            data["fallback"] = self.fallback.address
        if self.route_hints:
            data["route_hints"] = [route._asdict() for route in self.route_hints.routes]
        if self.min_final_cltv_expiry:
            data["min_final_cltv_expiry"] = self.min_final_cltv_expiry
        if self.payment_hash:
            data["payment_hash"] = self.payment_hash
        if self.payment_secret:
            data["payment_secret"] = self.payment_secret
        if self.payee:
            data["payee"] = self.payee
        return data

    @property
    def json(self) -> str:
        return json.dumps(self.data)


class Bolt11NoPaymentHashException(Exception):
    pass


class Bolt11DescriptionException(Exception):
    pass
