"""
Stage 5 — Post-Transaction: Self-Healing Disputes
"""
import sys, os, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from shared import inject_theme, hero, init_session_state, sidebar_nav, api, log_activity

st.set_page_config(page_title="Stage 5 · Dispute Resolution", page_icon="⚖️", layout="wide")
inject_theme()
init_session_state()
sidebar_nav(current_stage=5)

hero("Stage 5 · Post-Transaction", "Self-healing dispute resolution — Proof-of-Intent vs delivered goods")
st.page_link("pages/4_Stage4_Payment_and_Escrow.py", label="⬅ Back to Stage 4")

if not st.session_state.checkout:
    st.info("⬅️ Complete checkout in Stage 4 first.")
    st.page_link("pages/4_Stage4_Payment_and_Escrow.py", label="Go to Stage 4")
    st.stop()

order_id = st.session_state.checkout["order_id"]

st.markdown('<div class="rzp-card">', unsafe_allow_html=True)
st.markdown(f"**Simulate delivery for order `{order_id}`**")
delivered_desc = st.text_input(
    "What actually arrived? (try changing 'premium' → 'recycled' to trigger a mismatch)",
    value="Delivered: 100 boxes of recycled printing paper, sub-standard quality",
)
reason = st.selectbox("Dispute reason", ["Wrong item quality", "Wrong quantity", "Late delivery", "Other"])

if st.button("🚩 Flag issue with delivered goods"):
    with st.spinner("Dispute Agent parsing PoI bundle vs delivered catalog…"):
        time.sleep(0.8)
        resp = api("POST", "/api/dispute/flag",
                   json={"order_id": order_id, "reason": reason, "delivered_desc": delivered_desc})
    st.session_state.dispute_result = resp
    st.session_state.stage = 5
    log_activity(f"🚩 Dispute flagged: {reason}")
    if resp["status"] == "auto_refunded":
        log_activity(f"↩️ Auto-refund processed: ₹{resp['refund']['amount']/100:,.0f}")
    st.rerun()

if st.session_state.dispute_result:
    dr = st.session_state.dispute_result
    val = dr["validation"]
    if val["mismatch_found"]:
        st.markdown('<span class="rzp-badge rzp-badge-amber">⚠️ Intent mismatch detected</span>',
                    unsafe_allow_html=True)
        for e in val["evidence"]:
            st.write(f"- {e}")
    else:
        st.markdown('<span class="rzp-badge rzp-badge-navy">No mismatch detected — routed to manual review</span>',
                    unsafe_allow_html=True)

    if dr["status"] == "auto_refunded":
        st.success(f"✅ Refund auto-processed instantly: ₹{dr['refund']['amount']/100:,.0f} "
                   f"via Razorpay Refunds API (`{dr['refund']['id']}`)")
        st.balloons()
    else:
        st.warning("No automatic mismatch found — escalated for manual review.")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.page_link("Home.py", label="🏠 Back to Home")