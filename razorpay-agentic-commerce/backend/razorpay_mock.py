"""
Simulated Razorpay Gateway Core.

"""
import uuid
import time


def create_order(amount: float, currency: str = "INR", notes: dict | None = None) -> dict:
    """Mocks POST /v1/orders"""
    return {
        "id": f"order_{uuid.uuid4().hex[:14]}",
        "entity": "order",
        "amount": int(amount * 100),  # paise
        "amount_paid": 0,
        "currency": currency,
        "status": "created",
        "notes": notes or {},
        "created_at": int(time.time()),
    }


def route_split(order_id: str, splits: list) -> list:
   
    results = []
    for s in splits:
        results.append({
            "transfer_id": f"trf_{uuid.uuid4().hex[:14]}",
            "order_id": order_id,
            "merchant_id": s["merchant_id"],
            "merchant_name": s["merchant_name"],
            "amount": s["amount"],
            "role": s["role"],
            "status": "processed",
        })
    return results


def escrow_hold(order_id: str, amount: float) -> dict:
    """Mocks a RazorpayX Escrow+ account hold."""
    return {
        "escrow_id": f"esc_{uuid.uuid4().hex[:14]}",
        "order_id": order_id,
        "amount": amount,
        "status": "held",
        "held_at": int(time.time()),
    }


def escrow_release(escrow_record: dict, to: str = "merchant") -> dict:
    escrow_record["status"] = "released_to_merchant" if to == "merchant" else "refunded_to_user"
    escrow_record["released_at"] = int(time.time())
    return escrow_record


def create_refund(order_id: str, amount: float, reason: str) -> dict:
    """Mocks POST /v1/refunds"""
    return {
        "id": f"rfnd_{uuid.uuid4().hex[:14]}",
        "entity": "refund",
        "order_id": order_id,
        "amount": int(amount * 100),
        "status": "processed",
        "reason": reason,
        "speed_processed": "instant",
        "created_at": int(time.time()),
    }


def create_payment_link(merchant_name: str, amount: float) -> dict:
    """Mocks a temporary Razorpay Payment Link used in the bid response."""
    return {
        "id": f"plink_{uuid.uuid4().hex[:12]}",
        "short_url": f"https://rzp.io/l/{uuid.uuid4().hex[:8]}",
        "merchant_name": merchant_name,
        "amount": int(amount * 100),
        "status": "created",
    }