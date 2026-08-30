
"""
Stage 3 — Authorization: Shared Payment Token & Spend Control Check
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
 
import streamlit as st
from shared import inject_theme, hero, init_session_state, sidebar_nav, api, log_activity
 
st.set_page_config(page_title="Stage 3 · Authorization", page_icon="🔑", layout="wide")
inject_theme()
init_session_state()
sidebar_nav(current_stage=3)
 
hero("Stage 3 · Authorization", "Shared Payment Token &amp; card-network spend control check")
st.page_link("pages/2_Stage2_Discovery_and_Haggle.py", label="⬅ Back to Stage 2")
 
if not st.session_state.deal:
    st.info("⬅️ Complete the haggle in Stage 2 first.")
    st.page_link("pages/2_Stage2_Discovery_and_Haggle.py", label="Go to Stage 2")
    st.stop()
 
st.markdown('<div class="rzp-card">', unsafe_allow_html=True)
if st.button("🔑 Generate SPT & run spend-control check"):
    deal_id = st.session_state.deal["deal_id"]
    with st.spinner("Generating Shared Payment Token · running spend-control check…"):
        resp = api("GET", "/api/auth/spend-check", params={"deal_id": deal_id, "user_id": 1})
    st.session_state.spend_check = resp
    st.session_state.stage = max(st.session_state.stage, 3)
    log_activity(f"🔑 SPT issued · within limit: {resp['within_limit']}")
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
 
if st.session_state.spend_check:
    sc = st.session_state.spend_check
    st.markdown('<div class="rzp-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.metric("Negotiated total", f"₹{sc['final_price']:,.0f}")
    c2.metric("Registered spend limit", f"₹{sc['spend_limit']:,.0f}")
    if sc["within_limit"]:
        st.markdown('<span class="rzp-badge rzp-badge-green">✅ Within spend policy — SPT authorized</span>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<span class="rzp-badge rzp-badge-amber">⚠️ Exceeds spend limit — blocked</span>',
                    unsafe_allow_html=True)
    st.markdown("**Shared Payment Token (Stripe/OpenAI ACP-style, micro-scoped)**")
    st.json({k: v for k, v in sc["spt"].items() if k != "encoded"})
    st.markdown('</div>', unsafe_allow_html=True)
 
    if sc["within_limit"]:
        st.markdown("---")
        st.page_link("pages/4_Stage4_Payment_and_Escrow.py", label="Continue to Stage 4 — Payment & Escrow →")
    else:
        st.warning("Lower the spend limit in Stage 1, or renegotiate a lower price in Stage 2, to proceed.")
 
