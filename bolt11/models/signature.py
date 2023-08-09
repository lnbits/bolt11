from dataclasses import dataclass
from hashlib import sha256
from typing import Optional

from bitstring import Bits
from ecdsa import SECP256k1, VerifyingKey
from ecdsa.util import sigdecode_string
from secp256k1 import PrivateKey


@dataclass
class Signature:
    """An invoice signature."""

    signing_data: bytes
    signature_data: Optional[bytes] = None

    @classmethod
    def from_private_key(
        cls, private_key: str, hrp: str, signing_data: Bits
    ) -> "Signature":
        key = PrivateKey(bytes.fromhex(private_key))
        sig = key.ecdsa_sign_recoverable(
            bytearray([ord(c) for c in hrp]) + signing_data.tobytes()
        )
        sig, recid = key.ecdsa_recoverable_serialize(sig)
        signature_data = bytes(sig) + bytes([recid])
        return cls(signing_data=signing_data.tobytes(), signature_data=signature_data)

    def verify(self, payee: str) -> bool:
        key = VerifyingKey.from_string(bytes.fromhex(payee), curve=SECP256k1)
        return key.verify(
            self.sig, self.signing_data, sha256, sigdecode=sigdecode_string
        )

    def recover_public_key(self) -> str:
        keys = VerifyingKey.from_public_key_recovery(
            self.sig, self.signing_data, SECP256k1, sha256
        )
        key = keys[self.recovery_flag]
        return key.to_string("compressed").hex()

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
