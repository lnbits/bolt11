import json
import time
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional

from .exceptions import (
    Bolt11DescriptionException,
    Bolt11NoMinFinalCltvException,
    Bolt11NoPaymentHashException,
    Bolt11NoPaymentSecretException,
    Bolt11NoSignatureException,
)
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

    def validate(self, strict: bool = False) -> None:
        if "p" not in self.tags:
            raise Bolt11NoPaymentHashException()
        if "s" not in self.tags:
            raise Bolt11NoPaymentSecretException()
        if "d" in self.tags and "h" in self.tags or "d" not in self.tags and "h" not in self.tags:
            raise Bolt11DescriptionException()
        if not self.signature:
            raise Bolt11NoSignatureException()
        if strict and "c" not in self.tags:
            raise Bolt11NoMinFinalCltvException()

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
        return self.tags.get("d")

    @property
    def description_hash(self) -> Optional[str]:
        return self.tags.get("h")

    @property
    def metadata(self) -> Optional[str]:
        return self.tags.get("m")

    @property
    def dt(self) -> datetime:
        return datetime.fromtimestamp(self.date)

    @property
    def expiry(self) -> Optional[int]:
        return self.tags.get("x")

    @property
    def features(self) -> Optional[Features]:
        return self.tags.get("9")

    @property
    def fallback(self) -> Optional[Fallback]:
        return self.tags.get("f")

    @property
    def route_hints(self) -> Optional[RouteHint]:
        return self.tags.get("r")

    @property
    def min_final_cltv_expiry(self) -> Optional[int]:
        return self.tags.get("c", 18)

    @property
    def has_payment_hash(self) -> bool:
        return "p" in self.tags

    @property
    def payment_hash(self) -> str:
        if self.has_payment_hash is False:
            raise Bolt11NoPaymentHashException()
        return self.tags["p"]

    @property
    def payment_secret(self) -> Optional[str]:
        return self.tags.get("s")

    @property
    def payee(self) -> Optional[str]:
        return self.tags.get("n")

    @property
    def data(self) -> dict:
        data = {
            "currency": self.currency,
            "amount_msat": int(self.amount_msat) if self.amount_msat else 0,
            "date": self.date,
            "signature": self.signature.hex if self.signature else "",
        }
        if self.has_payment_hash:
            data["payment_hash"] = self.payment_hash
        if self.payment_secret:
            data["payment_secret"] = self.payment_secret
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
            json_data["route_hints"] = [
                route._asdict() for route in self.route_hints.routes
            ]
        if self.min_final_cltv_expiry:
            data["min_final_cltv_expiry"] = self.min_final_cltv_expiry
        if self.payee:
            data["payee"] = self.payee
        return data

    @property
    def json(self) -> str:
        return json.dumps(self.data)
