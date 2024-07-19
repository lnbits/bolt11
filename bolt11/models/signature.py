from dataclasses import dataclass
from hashlib import sha256

from coincurve import PrivateKey, PublicKey


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
        message = bytearray([ord(c) for c in hrp]) + signing_data
        signature_data = key.sign_recoverable(message)
        return cls(hrp=hrp, signing_data=signing_data, signature_data=signature_data)

    def verify(self, payee: str) -> bool:
        if not self.signature_data:
            raise ValueError("No signature data")
        # TODO: couldnt make it work with PublicKey.verify :( without recovering
        if payee != self.recover_public_key():
            raise ValueError("Verifying payee public_key failed.")
        # pubkey = PublicKey( bytes.fromhex(payee))
        # message = bytearray([ord(c) for c in self.hrp]) + self.signing_data
        # pubkey.verify(self.signature_data, message)
        return True

    def recover_public_key(self) -> str:
        if not self.signature_data:
            raise ValueError("No signature data")
        if not self.signing_data:
            raise ValueError("No signing data")

        message = bytearray([ord(c) for c in self.hrp]) + self.signing_data
        key = PublicKey.from_signature_and_message(self.signature_data, message)
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
