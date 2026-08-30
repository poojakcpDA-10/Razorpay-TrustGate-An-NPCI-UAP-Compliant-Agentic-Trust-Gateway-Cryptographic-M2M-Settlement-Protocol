
import json
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(str(Path(__file__).resolve().parent.parent))

from database.db import get_connection, init_db
from backend import agents, security, razorpay_mock
from backend.models import (
    VoiceCommandIn, SpendLimitIn, PasskeyIn, BroadcastIn,
    HaggleIn, SyndicateIn, CheckoutIn, DisputeIn,
)

app = FastAPI(title="Razorpay TrustGate-An NPCI UAP-Compliant Agentic Trust Gateway & Cryptographic M2M Settlement Protocol", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


def db():
    return get_connection()


# ---------------------------------------------------------------------------
# STAGE 1 — Pre-Transaction: Instruct & Bind
# ---------------------------------------------------------------------------
@app.post("/api/voice/parse")
def voice_parse(payload: VoiceCommandIn):
    parsed = agents.parse_voice_intent(payload.text)
    conn = db()
    cur = conn.execute(
        "INSERT INTO intents (user_id, raw_text, item, quantity, max_budget, parsed_json) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (payload.user_id, payload.text, parsed["item"], parsed["quantity"],
         parsed["max_budget"], json.dumps(parsed)),
    )
    conn.commit()
    intent_id = cur.lastrowid
    conn.close()
    return {"intent_id": intent_id, **parsed}


@app.post("/api/uap/spend-limit")
def set_spend_limit(payload: SpendLimitIn):
    conn = db()
    conn.execute("UPDATE users SET spend_limit = ? WHERE id = ?", (payload.limit, payload.user_id))
    conn.commit()
    conn.close()
    return {"user_id": payload.user_id, "spend_limit": payload.limit, "registered_with": "NPCI UAP Registry"}


@app.post("/api/passkey/verify")
def passkey_verify(payload: PasskeyIn):
    conn = db()
    conn.execute("UPDATE users SET passkey_verified = 1 WHERE id = ?", (payload.user_id,))
    conn.commit()
    conn.close()
    assertion = security.generate_passkey_assertion(payload.user_id)
    return {"status": "verified", "assertion": assertion}


# ---------------------------------------------------------------------------
# STAGE 2 — Discovery & Negotiation
# ---------------------------------------------------------------------------
@app.post("/api/discovery/broadcast")
def discovery_broadcast(payload: BroadcastIn):
    conn = db()
    intent = conn.execute("SELECT * FROM intents WHERE id = ?", (payload.intent_id,)).fetchone()
    if not intent:
        conn.close()
        raise HTTPException(404, "Intent not found")

    merchants = [dict(m) for m in conn.execute("SELECT * FROM merchants").fetchall()]
    parsed = json.loads(intent["parsed_json"])
    bids = agents.run_reverse_auction(merchants, parsed["quantity"], parsed["category"])

    for b in bids:
        payment_link = razorpay_mock.create_payment_link(b["merchant_name"], b["quoted_price"])
        offer = {**b, "payment_link": payment_link}
        conn.execute(
            "INSERT INTO bids (intent_id, merchant_id, quoted_price, delivery_days, offer_json) "
            "VALUES (?, ?, ?, ?, ?)",
            (payload.intent_id, b["merchant_id"], b["quoted_price"], b["delivery_days"], json.dumps(offer)),
        )
        b["payment_link"] = payment_link
    conn.commit()
    conn.close()
    return {"intent_id": payload.intent_id, "bids": bids}


@app.post("/api/negotiate/haggle")
def negotiate_haggle(payload: HaggleIn):
    conn = db()
    intent = conn.execute("SELECT * FROM intents WHERE id = ?", (payload.intent_id,)).fetchone()
    if not intent:
        conn.close()
        raise HTTPException(404, "Intent not found")
    parsed = json.loads(intent["parsed_json"])

    memo = agents.run_haggle(payload.bid, parsed)
    cur = conn.execute(
        "INSERT INTO deals (intent_id, merchant_id, original_price, final_price, concessions, "
        "deal_memo_json, signature) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (payload.intent_id, memo["merchant_id"], memo["original_price"], memo["final_price"],
         memo["concession"], json.dumps(memo), memo["signature"]),
    )
    conn.commit()
    deal_id = cur.lastrowid
    conn.close()
    return {"deal_id": deal_id, "deal_memo": memo}


# ---------------------------------------------------------------------------
# STAGE 3 — Authorization: SPT + spend control check
# ---------------------------------------------------------------------------
@app.get("/api/auth/spend-check")
def spend_check(deal_id: int, user_id: int = 1):
    conn = db()
    deal = conn.execute("SELECT * FROM deals WHERE id = ?", (deal_id,)).fetchone()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if not deal or not user:
        raise HTTPException(404, "Deal or user not found")

    within_limit = deal["final_price"] <= user["spend_limit"]
    spt = security.generate_spt(deal["merchant_id"], deal["final_price"])
    return {
        "deal_id": deal_id,
        "final_price": deal["final_price"],
        "spend_limit": user["spend_limit"],
        "within_limit": within_limit,
        "spt": spt,
    }


# ---------------------------------------------------------------------------
# STAGE 4 — Payment Execution: Syndicate split + Escrow + PoI
# ---------------------------------------------------------------------------
@app.post("/api/syndicate/offer")
def syndicate_offer(payload: SyndicateIn):
    conn = db()
    deal = conn.execute("SELECT * FROM deals WHERE id = ?", (payload.deal_id,)).fetchone()
    intent = conn.execute("SELECT * FROM intents WHERE id = ?", (deal["intent_id"],)).fetchone()
    merchants = [dict(m) for m in conn.execute("SELECT * FROM merchants").fetchall()]
    conn.close()
    parsed = json.loads(intent["parsed_json"])

    partner = agents.find_syndicate_partner(merchants, parsed["category"])
    if not partner:
        return {"available": False}

    bundle = agents.negotiate_syndicate_bundle(partner, deal["final_price"])
    return {"available": True, **bundle}


@app.post("/api/checkout")
def checkout(payload: CheckoutIn):
    conn = db()
    deal = conn.execute("SELECT * FROM deals WHERE id = ?", (payload.deal_id,)).fetchone()
    intent = conn.execute("SELECT * FROM intents WHERE id = ?", (deal["intent_id"],)).fetchone()
    merchant = conn.execute("SELECT * FROM merchants WHERE id = ?", (deal["merchant_id"],)).fetchone()
    merchants = [dict(m) for m in conn.execute("SELECT * FROM merchants").fetchall()]
    parsed = json.loads(intent["parsed_json"])

    splits = [{
        "merchant_id": merchant["id"], "merchant_name": merchant["name"],
        "amount": deal["final_price"], "role": "primary",
    }]

    total_amount = deal["final_price"]
    syndicate_bundle = None
    if payload.include_syndicate:
        partner = agents.find_syndicate_partner(merchants, parsed["category"])
        if partner:
            syndicate_bundle = agents.negotiate_syndicate_bundle(partner, deal["final_price"])
            total_amount = round(deal["final_price"] + syndicate_bundle["net_addon_cost"], 2)
            splits[0]["amount"] = round(deal["final_price"] - syndicate_bundle["primary_credit"], 2)
            splits.append({
                "merchant_id": syndicate_bundle["partner_merchant_id"],
                "merchant_name": syndicate_bundle["partner_name"],
                "amount": syndicate_bundle["addon_price"],
                "role": "syndicate_partner",
            })

    rzp_order = razorpay_mock.create_order(total_amount, notes={"deal_id": payload.deal_id})
    cur = conn.execute(
        "INSERT INTO orders (deal_id, razorpay_order_id, amount, status) VALUES (?, ?, ?, ?)",
        (payload.deal_id, rzp_order["id"], total_amount, "paid"),
    )
    order_id = cur.lastrowid

    transfers = razorpay_mock.route_split(rzp_order["id"], splits)
    for t in transfers:
        conn.execute(
            "INSERT INTO splits (order_id, merchant_id, amount, role, payout_status) VALUES (?, ?, ?, ?, ?)",
            (order_id, t["merchant_id"], t["amount"], t["role"], t["status"]),
        )

    escrow_rec = razorpay_mock.escrow_hold(rzp_order["id"], total_amount)
    conn.execute(
        "INSERT INTO escrow (order_id, amount, status) VALUES (?, ?, ?)",
        (order_id, total_amount, "held"),
    )

    deal_memo = json.loads(deal["deal_memo_json"])
    poi_bundle = {
        "order_id": order_id,
        "raw_voice_text": intent["raw_text"],
        "parsed_intent": parsed,
        "deal_memo": deal_memo,
        "reasoning_steps": [
            "Parsed voice command into structured shopping intent.",
            "Broadcast intent to merchant network; ran reverse auction.",
            f"Selected best bid from {deal_memo['merchant_name']} and negotiated final price.",
            "Verified negotiated amount against user's UAP spend control limit.",
            "Generated Shared Payment Token scoped to merchant + amount + 15-min expiry.",
            "Executed Route API split payout across merchant(s).",
            "Locked settlement funds in RazorpayX Escrow+ pending delivery confirmation.",
        ],
        "syndicate_bundle": syndicate_bundle,
    }
    poi_signature = security.sign_poi_bundle(poi_bundle)
    conn.execute(
        "INSERT INTO poi_bundles (order_id, bundle_json, signature) VALUES (?, ?, ?)",
        (order_id, json.dumps(poi_bundle), poi_signature),
    )

    conn.commit()
    conn.close()

    return {
        "order_id": order_id,
        "razorpay_order": rzp_order,
        "splits": transfers,
        "escrow": escrow_rec,
        "poi_bundle": poi_bundle,
        "poi_signature": poi_signature,
        "total_amount": total_amount,
    }


# ---------------------------------------------------------------------------
# STAGE 5 — Post-Transaction: Self-Healing Disputes
# ---------------------------------------------------------------------------
@app.post("/api/dispute/flag")
def dispute_flag(payload: DisputeIn):
    conn = db()
    order = conn.execute("SELECT * FROM orders WHERE id = ?", (payload.order_id,)).fetchone()
    if not order:
        conn.close()
        raise HTTPException(404, "Order not found")

    poi_row = conn.execute("SELECT * FROM poi_bundles WHERE order_id = ?", (payload.order_id,)).fetchone()
    poi_bundle = json.loads(poi_row["bundle_json"])

    validation = agents.validate_delivery_against_intent(poi_bundle, payload.delivered_desc)
    # Defensive default: guarantees this endpoint can never KeyError even if
    # a stale/older build of agents.py ends up loaded, or the function is
    # ever changed to omit this key by mistake.
    recommendation = validation.get("recommendation", "manual_review")

    cur = conn.execute(
        "INSERT INTO disputes (order_id, reason, delivered_desc, status) VALUES (?, ?, ?, ?)",
        (payload.order_id, payload.reason, payload.delivered_desc, "open"),
    )
    dispute_id = cur.lastrowid
    conn.commit()

    result = {"dispute_id": dispute_id, "validation": validation}

    if recommendation == "auto_refund":
        escrow_row = conn.execute("SELECT * FROM escrow WHERE order_id = ?", (payload.order_id,)).fetchone()
        refund = razorpay_mock.create_refund(order["razorpay_order_id"], escrow_row["amount"],
                                              reason="PoI validation mismatch — auto-approved")
        conn.execute("UPDATE escrow SET status = 'refunded', released_at = datetime('now') WHERE order_id = ?",
                     (payload.order_id,))
        conn.execute(
            "UPDATE disputes SET status = 'resolved', resolution = 'auto_refund', refund_amount = ?, "
            "resolved_at = datetime('now') WHERE id = ?",
            (escrow_row["amount"], dispute_id),
        )
        conn.execute("UPDATE orders SET status = 'refunded' WHERE id = ?", (payload.order_id,))
        conn.commit()
        result["refund"] = refund
        result["status"] = "auto_refunded"
    else:
        result["status"] = "manual_review"

    conn.close()
    return result


@app.get("/api/orders/{order_id}")
def get_order(order_id: int):
    conn = db()
    order = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    if not order:
        conn.close()
        raise HTTPException(404, "Order not found")
    splits = conn.execute("SELECT * FROM splits WHERE order_id = ?", (order_id,)).fetchall()
    escrow = conn.execute("SELECT * FROM escrow WHERE order_id = ?", (order_id,)).fetchone()
    disputes = conn.execute("SELECT * FROM disputes WHERE order_id = ?", (order_id,)).fetchall()
    conn.close()
    return {
        "order": dict(order),
        "splits": [dict(s) for s in splits],
        "escrow": dict(escrow) if escrow else None,
        "disputes": [dict(d) for d in disputes],
    }


@app.get("/")
def root():
    
    return {
        "service": "Razorpay Agentic Commerce Platform API",
        "status": "ok",
        "docs": "/docs",
        "frontend": "http://localhost:8501",
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}