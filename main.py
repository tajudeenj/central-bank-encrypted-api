"""
Central Bank Encrypted API Integration (Mock)
==============================================
AES-256 Encryption + Digital Signature + FastAPI
Author: Tajudeen Jalaudin
Inspired by UAE Central Bank API integration at ADIB (2024)
"""

import os
import base64
import hashlib
import hmac
import json
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Central Bank Encrypted API", version="1.0.0")

# --- AES-256 Encryption Utilities ---
class AESEncryption:
    """AES-256-CBC encryption/decryption — mirrors CBUAE integration pattern."""

    def __init__(self, key: bytes = None):
        self.key = key or os.urandom(32)  # 256-bit key

    def encrypt(self, plaintext: str) -> dict:
        iv = os.urandom(16)
        padder = padding.PKCS7(128).padder()
        padded = padder.update(plaintext.encode()) + padder.finalize()

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded) + encryptor.finalize()

        return {
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "iv": base64.b64encode(iv).decode(),
        }

    def decrypt(self, ciphertext_b64: str, iv_b64: str) -> str:
        ciphertext = base64.b64decode(ciphertext_b64)
        iv = base64.b64decode(iv_b64)

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        return (unpadder.update(padded) + unpadder.finalize()).decode()


# --- Digital Signature ---
class DigitalSigner:
    """HMAC-SHA256 digital signature for payload integrity."""

    def __init__(self, secret: str = "cbuae-secret-key"):
        self.secret = secret.encode()

    def sign(self, payload: str) -> str:
        return hmac.new(self.secret, payload.encode(), hashlib.sha256).hexdigest()

    def verify(self, payload: str, signature: str) -> bool:
        expected = self.sign(payload)
        return hmac.compare_digest(expected, signature)


# --- Globals ---
aes = AESEncryption()
signer = DigitalSigner()


# --- Models ---
class PaymentRequest(BaseModel):
    transaction_ref: str
    amount: float
    currency: str = "AED"
    beneficiary_iban: str
    beneficiary_name: str
    purpose: str


class EncryptedPayload(BaseModel):
    ciphertext: str
    iv: str
    signature: str
    timestamp: str


# --- Endpoints ---
@app.post("/api/v1/cbuae/payment/encrypt")
def encrypt_payment(request: PaymentRequest):
    """Encrypt a payment request for CBUAE submission."""
    payload = request.json()
    encrypted = aes.encrypt(payload)
    signature = signer.sign(encrypted["ciphertext"])

    return {
        "encrypted_payload": {
            "ciphertext": encrypted["ciphertext"],
            "iv": encrypted["iv"],
            "signature": signature,
            "timestamp": datetime.utcnow().isoformat(),
        },
        "message": "Payload encrypted and signed. Ready for CBUAE submission."
    }


@app.post("/api/v1/cbuae/payment/decrypt")
def decrypt_payment(payload: EncryptedPayload):
    """Decrypt and verify a CBUAE payment response."""
    if not signer.verify(payload.ciphertext, payload.signature):
        raise HTTPException(status_code=401, detail="Invalid digital signature. Payload tampered.")

    decrypted = aes.decrypt(payload.ciphertext, payload.iv)
    return {
        "status": "VERIFIED",
        "decrypted_payload": json.loads(decrypted),
        "message": "Signature verified. Payload decrypted successfully."
    }


@app.get("/api/v1/cbuae/health")
def health():
    return {"status": "ok", "service": "CBUAE Encrypted API", "timestamp": datetime.utcnow().isoformat()}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
