from dataclasses import dataclass
from hashlib import sha256

from coincurve import PrivateKey, PublicKey, verify_signature
from coincurve.ecdsa import cdata_to_der, deserialize_recoverable, recoverable_convert


def message(hrp: str, signing_data: bytes) -> bytes:
    return bytes([ord(c) for c in hrp]) + signing_data


@dataclass
class Signature:
    """An invoice signature."""

    hrp: str
    signing_data: bytes
    signature_data: bytes

    @classmethod
    def from_signature_data(
        cls, hrp: str, signature_data: bytes, signing_data: bytes
    ) -> "Signature":
        return cls(hrp=hrp, signature_data=signature_data, signing_data=signing_data)

    @classmethod
    def from_private_key(
        cls, hrp: str, private_key: str, signing_data: bytes
    ) -> "Signature":
        key = PrivateKey.from_hex(private_key)
        signature_data = key.sign_recoverable(message(hrp, signing_data))
        return cls(hrp=hrp, signing_data=signing_data, signature_data=signature_data)

    def verify(self, payee: str) -> bool:
        if not self.signature_data:
            raise ValueError("No signature data")
        if not self.signing_data:
            raise ValueError("No signing data")
        sig = deserialize_recoverable(self.signature_data)
        sig = recoverable_convert(sig)
        sig = cdata_to_der(sig)
        if not verify_signature(
            sig, message(self.hrp, self.signing_data), bytes.fromhex(payee)
        ):
            raise ValueError("Invalid signature")
        return True

    def recover_public_key(self) -> str:
        if not self.signature_data:
            raise ValueError("No signature data")
        if not self.signing_data:
            raise ValueError("No signing data")

        key = PublicKey.from_signature_and_message(
            self.signature_data, message(self.hrp, self.signing_data)
        )
        return key.format(compressed=True).hex()

    @property
    def r(self) -> str:
        if not self.signature_data:
            raise ValueError("No signature data")
        return self.signature_data[:32].hex()

    @property
    def s(self) -> str:
        if not self.signature_data:
            raise ValueError("No signature data")
        return self.signature_data[32:64].hex()

    @property
    def sig(self) -> bytes:
        if not self.signature_data:
            raise ValueError("No signature data")
        return self.signature_data[0:64]

    @property
    def recovery_flag(self) -> int:
        if not self.signature_data:
            raise ValueError("No signature data")
        return int(self.signature_data[64])

    @property
    def preimage(self) -> bytes:
        if not self.signature_data:
            raise ValueError("No signature data")
        return sha256(self.signature_data).digest()

    @property
    def hex(self) -> str:
        if not self.signature_data:
            raise ValueError("No signature data")
        return self.signature_data[:64].hex()
