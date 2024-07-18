from dataclasses import dataclass
from hashlib import sha256
from typing import Optional

from bitstring import Bits
from coincurve import PrivateKey, PublicKey
from ecdsa import SECP256k1, VerifyingKey
from ecdsa.util import sigdecode_string


@dataclass
class Signature:
    """An invoice signature."""

    signing_data: bytes
    signature_data: Optional[bytes] = None

    @classmethod
    def from_private_key(
        cls, private_key: str, hrp: str, signing_data: Bits
    ) -> "Signature":
        key: PrivateKey = PrivateKey.from_hex(private_key)
        signature_data = key.sign_recoverable(
            bytearray([ord(c) for c in hrp]) + signing_data.tobytes()
        )
        return cls(signing_data=signing_data.tobytes(), signature_data=signature_data)

    def verify(self, payee: str) -> bool:
        if not self.signature_data:
            raise ValueError("No signature data")
        # key = PublicKey(bytes.fromhex(payee))
        # return key.verify(self.signature_data, self.signing_data)
        key = VerifyingKey.from_string(bytes.fromhex(payee), curve=SECP256k1)
        return key.verify(
            self.sig, self.signing_data, sha256, sigdecode=sigdecode_string
        )

    def recover_public_key(self) -> str:
        if not self.signature_data:
            raise ValueError("No signature data")
        key = PublicKey.from_signature_and_message(
            self.signature_data, self.signing_data
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
