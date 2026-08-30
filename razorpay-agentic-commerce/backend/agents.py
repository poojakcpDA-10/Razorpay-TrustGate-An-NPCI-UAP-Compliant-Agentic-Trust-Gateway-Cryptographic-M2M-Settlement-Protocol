"""
The 'AI' layer — Buyer Agent, Merchant Bidding Agents, and the Dispute Agent.

"""
import re
import json
import random
import time

from . import security

random.seed(42)



NUMBER_WORDS = {
    "hundred": 100, "fifty": 50, "twenty": 20, "ten": 10, "hundred": 100,
}


CATEGORY_KEYWORDS = {
    "furniture": ["desk", "chair", "table", "sofa", "cabinet", "shelf", "shelves",
                  "furniture", "wardrobe", "cupboard", "workstation"],
    "logistics": ["shipping", "courier", "logistics", "freight", "transport",
                  "delivery service", "cargo"],
    "decor": ["plant", "planter", "decor", "decoration", "vase", "artwork",
              "curtain", "rug", "lamp"],
    "stationery": ["paper", "pen", "pencil", "notebook", "stationery", "printer",
                   "ink", "folder", "envelope", "marker", "stapler"],
}


def detect_category(text: str) -> str:
    t = text.lower()
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in t for kw in keywords):
            return cat
    return "general"


def extract_budget(text: str):
    """
    Finds a spend-cap amount in free text and returns (value, match_span).
    Recognizes the ₹ symbol, the words Rs/Rupees/INR (before or after the
    number), and a bare number following a budget-indicating phrase like
    "under", "less than", "up to", "max", "budget of", etc. — so it isn't
    limited to one specific wording.
    """
    patterns = [
        r"₹\s?([\d,]+(?:\.\d+)?)\s?(k|K)?",
        r"\b(?:rs\.?|rupees?|inr)\s?([\d,]+(?:\.\d+)?)\s?(k|K)?\b",
        r"\b([\d,]+(?:\.\d+)?)\s?(k|K)?\s?(?:rs\.?|rupees?|inr)\b",
    ]
    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            raw_num = m.group(1).replace(",", "")
            val = float(raw_num)
            if m.group(2):
                val *= 1000
            return val, m.span()

    m = re.search(
        r"\b(?:under|below|less than|not\s+(?:spend|exceed)(?:\s+more\s+than)?|"
        r"max(?:imum)?(?:\s+budget)?|up to|within|budget of)\s*₹?\s?"
        r"([\d,]+(?:\.\d+)?)\s?(k|K)?\b",
        text, re.IGNORECASE,
    )
    if m:
        raw_num = m.group(1).replace(",", "")
        val = float(raw_num)
        if m.group(2):
            val *= 1000
        return val, m.span()

    
    m = re.search(
        r"\b(?:under|below|less than|not\s+(?:spend|exceed)(?:\s+more\s+than)?|"
        r"max(?:imum)?(?:\s+budget)?|up to|within|budget of|rs\.?|rupees?|inr)\b"
        r"(?:\s+\w+){0,4}?\s*₹?\s?([\d,]+(?:\.\d+)?)\s?(k|K)?\b",
        text, re.IGNORECASE,
    )
    if m:
        raw_num = m.group(1).replace(",", "")
        val = float(raw_num)
        if m.group(2):
            val *= 1000
        return val, m.span()

    return None, None


def parse_voice_intent(raw_text: str) -> dict:
    """Extracts {item, quantity, max_budget} from a free-form voice command."""
    text = raw_text.strip()

    budget, budget_span = extract_budget(text)

    
    text_wo_budget = text
    if budget_span:
        text_wo_budget = text[:budget_span[0]] + " " + text[budget_span[1]:]

    # quantity: first standalone integer left once the budget clause is masked out
    qty_match = re.search(r"\b(\d{1,5})\b", text_wo_budget)
    quantity = int(qty_match.group(1)) if qty_match else 1

    # item: strip filler words/currency words/remaining numbers to approximate the noun phrase
    item_text = text_wo_budget
    item_text = re.sub(r"(?:₹|\brs\.?\b|\brupees?\b|\binr\b)", "", item_text, flags=re.IGNORECASE)
    item_text = re.sub(
        r"(order|find me|get me|buy|i need|i want|i'd like|i would like|please|"
        r"(?:do not|don'?t) spend more than|not spend more than|under|below|less than|"
        r"max(?:imum)? budget|up to|within|budget of|"
        r"a bulk deal on|from local suppliers?|\bthe\b|\bof\b|\ba\b)",
        "", item_text, flags=re.IGNORECASE,
    )
    item_text = re.sub(r"\b\d+\b", "", item_text).strip(" .,")
    item_text = re.sub(r"\s{2,}", " ", item_text).strip()
    item = item_text if item_text else "requested item"

    category = detect_category(text)

    return {
        "item": item,
        "quantity": quantity,
        "max_budget": budget,
        "category": category,
        "raw_text": raw_text,
    }


# ---------------------------------------------------------------------------
# 2. Discovery — reverse auction bidding
# ---------------------------------------------------------------------------
def run_reverse_auction(merchants: list, quantity: int, category: str) -> list:
    """Each merchant agent computes a quote + delivery estimate, scaled by quantity."""
    bids = []
    if category == "general":
        pool = merchants
    else:
        pool = [m for m in merchants if m["category"] == category] or merchants
    for m in pool:
        variance = random.uniform(-0.08, 0.05)
        unit_price = m["base_price"] * (1 + variance)
        quoted_price = round(unit_price * quantity, 2)
        delivery_days = round(random.uniform(1.0, 5.0), 1)
        bids.append({
            "merchant_id": m["id"],
            "merchant_name": m["name"],
            "rating": m["rating"],
            "quoted_price": quoted_price,
            "delivery_days": delivery_days,
        })
    bids.sort(key=lambda b: (b["quoted_price"], -b["rating"]))
    return bids


# ---------------------------------------------------------------------------
# 3. A2A Haggle — Buyer Agent <-> best Merchant Agent
# ---------------------------------------------------------------------------
def run_haggle(best_bid: dict, intent: dict) -> dict:
    """Buyer agent negotiates a discount in exchange for a concession."""
    original_price = best_bid["quoted_price"]
    discount_pct = random.uniform(0.06, 0.11)
    final_price = round(original_price * (1 - discount_pct), 2)
    concession = "free expedited delivery" if random.random() > 0.4 else "immediate payment on confirmation"

    transcript = [
        {"speaker": "BuyerAgent", "message":
            f"We can close this deal now if you include {concession}."},
        {"speaker": "MerchantAgent", "message":
            f"Accepted. Revised total: ₹{final_price:,.0f} (was ₹{original_price:,.0f})."},
    ]

    memo = {
        "intent_item": intent["item"],
        "quantity": intent["quantity"],
        "merchant_id": best_bid["merchant_id"],
        "merchant_name": best_bid["merchant_name"],
        "original_price": original_price,
        "final_price": final_price,
        "concession": concession,
        "transcript": transcript,
        "negotiated_at": int(time.time()),
    }
    memo["signature"] = security.sign_deal_memo(memo)
    return memo


# ---------------------------------------------------------------------------
# 4. Syndicate bundling — cross-merchant collaboration
# ---------------------------------------------------------------------------
def find_syndicate_partner(merchants: list, category: str) -> dict | None:
    for m in merchants:
        if m.get("syndicate_partner_of") == category:
            return m
    return None


def negotiate_syndicate_bundle(partner: dict, primary_final_price: float) -> dict:
    """Partner merchant offers a bundle add-on; primary merchant credits a discount."""
    addon_price = round(partner["base_price"] * random.uniform(0.9, 1.1), 2)
    primary_credit = round(addon_price * random.uniform(0.2, 0.35), 2)
    return {
        "partner_merchant_id": partner["id"],
        "partner_name": partner["name"],
        "addon_description": f"{partner['category']} bundle add-on",
        "addon_price": addon_price,
        "primary_credit": primary_credit,
        "net_addon_cost": round(addon_price - primary_credit, 2),
    }


# ---------------------------------------------------------------------------
# 5. Dispute Agent — validates delivered goods against original intent
# ---------------------------------------------------------------------------
MISMATCH_SIGNALS = [
    ("premium", "recycled"), ("premium", "sub-standard"), ("premium", "substandard"),
    ("new", "used"), ("large", "small"), ("original", "duplicate"),
    ("genuine", "counterfeit"), ("a4", "a5"),
]

# Generic negative-quality / problem language. If the delivered description
# contains any of these, that's evidence of a mismatch on its own — it
# doesn't require the original request to have used a specific opposite word,
# so this works for whatever wording the user actually types, not just the
# handful of pairs above.
NEGATIVE_QUALITY_WORDS = [
    "recycled", "sub-standard", "substandard", "used", "duplicate", "counterfeit",
    "fake", "damaged", "broken", "defective", "faulty", "wrong", "incorrect",
    "incomplete", "missing", "short", "delayed", "late", "expired", "torn",
    "poor quality", "low quality", "mismatched", "cracked", "stained", "dented",
]

_STOPWORDS = {
    "a", "an", "the", "of", "for", "to", "from", "with", "on", "in", "and", "or",
    "order", "boxes", "box", "local", "suppliers", "supplier", "do", "not",
    "spend", "more", "than", "under", "max", "budget", "delivered", "buy",
    "get", "find", "me", "please", "arrived",
}


def _keywords(text: str) -> set:
    return {w for w in re.findall(r"[a-z]+", text.lower()) if len(w) > 2 and w not in _STOPWORDS}


def validate_delivery_against_intent(poi_bundle: dict, delivered_desc: str) -> dict:
    """
    Rule-based PoI-vs-catalog validation, mirroring the described Dispute
    Agent behavior: parse original intent keywords, diff against delivered
    description, and decide auto-refund eligibility.
    """
    original_text = (poi_bundle.get("raw_voice_text", "") + " " +
                      poi_bundle.get("deal_memo", {}).get("intent_item", "")).lower()
    delivered = delivered_desc.lower()
    evidence = []

    # 1. Known antonym-style contradictions — strong, explicit evidence.
    for expected_kw, bad_kw in MISMATCH_SIGNALS:
        if expected_kw in original_text and bad_kw in delivered:
            evidence.append(f"Requested '{expected_kw}' but delivered item described as '{bad_kw}'")

    # 2. Generic problem language in the delivered description, independent
    #    of whatever wording the original request used.
    for bad_word in NEGATIVE_QUALITY_WORDS:
        if bad_word in delivered and not any(bad_word in e for e in evidence):
            evidence.append(f"Delivered description flags a quality/spec issue: '{bad_word}'")
            break

    # 3. Quantity mismatch — compare any number mentioned in the delivered
    #    description against the quantity that was actually ordered.
    orig_qty = poi_bundle.get("deal_memo", {}).get("quantity")
    qty_match = re.search(r"\b(\d{1,5})\b", delivered)
    if orig_qty and qty_match and int(qty_match.group(1)) != orig_qty:
        evidence.append(f"Ordered quantity {orig_qty} but delivery describes {qty_match.group(1)}")

    # 4. Low keyword overlap between what was asked for and what arrived —
    #    catches free-form mismatches that don't hit any rule above.
    orig_kw = _keywords(original_text)
    if orig_kw and not evidence:
        deliv_kw = _keywords(delivered)
        overlap = len(orig_kw & deliv_kw) / len(orig_kw)
        if overlap < 0.34:
            evidence.append(
                "Delivered description shares very little in common with what was originally "
                "requested — item details look substantially different."
            )

    is_mismatch = len(evidence) > 0
    return {
        "mismatch_found": is_mismatch,
        "evidence": evidence,
        "recommendation": "auto_refund" if is_mismatch else "manual_review",
    }