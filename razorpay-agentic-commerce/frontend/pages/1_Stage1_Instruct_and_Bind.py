"""
Stage 1 — Pre-Transaction: Instruct & Bind
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from shared import inject_theme, hero, init_session_state, sidebar_nav, api, log_activity

st.set_page_config(page_title="Stage 1 · Instruct & Bind", page_icon="📝", layout="wide")
inject_theme()
init_session_state()
sidebar_nav(current_stage=1)

hero("Stage 1 · Pre-Transaction", "Instruct & Bind — shopping command, spend limit, biometric consent")

col1, col2 = st.columns([3, 2])

# ---------------------------------------------------------------------------
# Command Panel
# ---------------------------------------------------------------------------
with col1:
    st.markdown('<div class="rzp-card">', unsafe_allow_html=True)
    st.markdown("**📝 Shopping Command Panel**")
    st.caption("Type your shopping goal in plain language, including an item, quantity, and budget.")

    default_cmd = "Order 100 boxes of premium printing paper from local suppliers. Do not spend more than ₹50,000"
    if "voice_text_area" not in st.session_state:
        st.session_state["voice_text_area"] = default_cmd

    command_text = st.text_area(
        "Describe your shopping goal",
        height=80, key="voice_text_area",
    )

    if st.button("📨 Submit command"):
        if not command_text or not command_text.strip():
            st.warning("Please type your shopping goal first — the box is empty.")
        else:
            with st.spinner("Parsing your command…"):
                result = api("POST", "/api/voice/parse", json={"user_id": 1, "text": command_text.strip()})
            st.session_state.intent = result
            st.session_state.stage = max(st.session_state.stage, 1)
            log_activity(f"📝 Intent parsed: \"{result['item']}\" × {result['quantity']}")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.intent:
        it = st.session_state.intent
        st.markdown('<div class="rzp-card">', unsafe_allow_html=True)
        st.markdown("**✅ Parsed intent**")
        st.json({k: v for k, v in it.items() if k != "raw_text"})
        if it.get("max_budget") is None:
            st.warning("No budget amount was detected in that command — try including e.g. '₹50,000'.")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Spend slider + passkey
# ---------------------------------------------------------------------------
with col2:
    st.markdown('<div class="rzp-card">', unsafe_allow_html=True)
    st.markdown("**📊 Pre-Authorization Spend Slider**")
    st.caption("NPCI UAP Registry / UPI AutoPay-style limit")
    spend_limit = st.slider("Max agent spend (₹)", 1000, 200000, st.session_state.spend_limit, step=1000)
    st.session_state.spend_limit = spend_limit
    if st.button("🔒 Lock spend limit"):
        api("POST", "/api/uap/spend-limit", json={"user_id": 1, "limit": spend_limit})
        log_activity(f"🔒 Spend limit registered: ₹{spend_limit:,}")
        st.success(f"Spend control registered: ₹{spend_limit:,} max")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="rzp-card">', unsafe_allow_html=True)
    st.markdown("**🔐 Biometric Passkey Consent**")
    consent = st.checkbox("I authorize my Buyer Agent via fingerprint / passkey")
    if consent and st.button("✅ Verify passkey"):
        resp = api("POST", "/api/passkey/verify", json={"user_id": 1})
        st.session_state.passkey_ok = True
        log_activity("🔐 Passkey verified — identity cryptographically bound")
        st.success(f"Identity cryptographically bound · assertion `{resp['assertion']['assertion_id'][:8]}…`")
    if st.session_state.passkey_ok:
        st.markdown('<span class="rzp-badge rzp-badge-green">Passkey verified</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
if st.session_state.intent:
    st.page_link("pages/2_Stage2_Discovery_and_Haggle.py", label="Continue to Stage 2 — Discovery & Haggle →")
else:
    st.caption("Submit a shopping command above to unlock Stage 2.")