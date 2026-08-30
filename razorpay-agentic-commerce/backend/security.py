"""
Security layer — simulates the cryptographic primitives referenced in the
architecture doc:
  - Passkey / biometric-bound identity assertion
  - Shared Payment Token (SPT) generation (Stripe/OpenAI ACP style)
  - Proof-of-Intent (PoI) bundle signing
  - Deal Memo signing (A2A handshake)
"""
import hmac
import hashlib
import json
import time
import uuid
import base64

SECRET_KEY = b"razorpay-agentic-commerce-demo-secret-key"


def _sign(payload: dict) -> str:
    body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    digest = hmac.new(SECRET_KEY, body, hashlib.sha256).hexdigest()
    return digest


def verify_signature(payload: dict, signature: str) -> bool:
    return hmac.compare_digest(_sign(payload), signature)


def generate_passkey_assertion(user_id: int) -> dict:
    """Simulates a WebAuthn/passkey biometric assertion binding user -> session."""
    payload = {
        "user_id": user_id,
        "assertion_id": str(uuid.uuid4()),
        "method": "fingerprint",
        "issued_at": int(time.time()),
    }
    return {**payload, "signature": _sign(payload)}


def sign_deal_memo(memo: dict) -> str:
    return _sign(memo)


def generate_spt(merchant_id: int, amount: float, ttl_seconds: int = 900) -> dict:
    """
    Shared Payment Token — micro-scoped to a merchant, an exact amount,
    and a short expiry window (Stripe/OpenAI Agentic Commerce Protocol style).
    """
    now = int(time.time())
    payload = {
        "spt_id": f"spt_{uuid.uuid4().hex[:20]}",
        "merchant_id": merchant_id,
        "amount": round(amount, 2),
        "issued_at": now,
        "expires_at": now + ttl_seconds,
    }
    token = {**payload, "signature": _sign(payload)}
    token["encoded"] = base64.urlsafe_b64encode(
        json.dumps(token, sort_keys=True).encode()
    ).decode()
    return token


def spt_is_valid(token: dict) -> bool:
    payload = {k: v for k, v in token.items() if k not in ("signature", "encoded")}
    if not verify_signature(payload, token.get("signature", "")):
        return False
    return int(time.time()) <= token["expires_at"]


def sign_poi_bundle(bundle: dict) -> str:
    return _sign(bundle)