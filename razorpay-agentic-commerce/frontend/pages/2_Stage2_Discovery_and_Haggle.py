"""
Stage 2 — Discovery: Reverse Auction & A2A Haggle
"""
import sys, os, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import streamlit as st
from shared import inject_theme, hero, init_session_state, sidebar_nav, api, log_activity

st.set_page_config(page_title="Stage 2 · Discovery & Haggle", page_icon="🤝", layout="wide")
inject_theme()
init_session_state()
sidebar_nav(current_stage=2)

hero("Stage 2 · Discovery", "Reverse Auction &amp; A2A Haggle — merchant agents bid, your agent negotiates")
st.page_link("pages/1_Stage1_Instruct_and_Bind.py", label="⬅ Back to Stage 1")

if not st.session_state.intent:
    st.info("⬅️ Submit a shopping command in Stage 1 first.")
    st.page_link("pages/1_Stage1_Instruct_and_Bind.py", label="Go to Stage 1")
    st.stop()

st.markdown('<div class="rzp-card">', unsafe_allow_html=True)
st.markdown(f"**Broadcasting intent:** {st.session_state.intent['item']} × {st.session_state.intent['quantity']}")
if st.button("📡 Broadcast intent to merchant network"):
    with st.spinner("Buyer Agent broadcasting signed intent · Merchant agents bidding…"):
        time.sleep(0.6)
        resp = api("POST", "/api/discovery/broadcast", json={"intent_id": st.session_state.intent["intent_id"]})
    st.session_state.bids = resp["bids"]
    st.session_state.stage = max(st.session_state.stage, 2)
    log_activity(f"📡 {len(resp['bids'])} merchant bids received")
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.bids:
    st.markdown('<div class="rzp-card">', unsafe_allow_html=True)
    st.markdown("**📥 Live bids (reverse auction)**")
    df = pd.DataFrame(st.session_state.bids)[["merchant_name", "rating", "quoted_price", "delivery_days"]]
    df.columns = ["Merchant", "Rating", "Quoted price (₹)", "Delivery (days)"]
    st.dataframe(df, use_container_width=True, hide_index=True)

    best = st.session_state.bids[0]
    st.markdown(f"🏆 **Best bid:** {best['merchant_name']} — ₹{best['quoted_price']:,.0f}")

    if st.button("🤝 Run A2A haggle with best merchant"):
        with st.spinner("Buyer Agent ↔ Merchant Agent negotiating…"):
            time.sleep(0.8)
            deal = api("POST", "/api/negotiate/haggle",
                       json={"intent_id": st.session_state.intent["intent_id"], "bid": best})
        st.session_state.deal = deal
        st.session_state.stage = max(st.session_state.stage, 2)
        log_activity(f"🤝 Deal closed with {best['merchant_name']} at ₹{deal['deal_memo']['final_price']:,.0f}")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.deal:
    memo = st.session_state.deal["deal_memo"]
    st.markdown('<div class="rzp-card">', unsafe_allow_html=True)
    st.markdown("**📝 Signed Deal Memo**")
    for turn in memo["transcript"]:
        st.markdown(f"**{turn['speaker']}:** {turn['message']}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Original price", f"₹{memo['original_price']:,.0f}")
    c2.metric("Negotiated price", f"₹{memo['final_price']:,.0f}",
               delta=f"-₹{memo['original_price']-memo['final_price']:,.0f}")
    c3.metric("Concession won", memo["concession"])
    st.caption(f"Signature: `{memo['signature'][:32]}…`")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.page_link("pages/3_Stage3_Authorization.py", label="Continue to Stage 3 — Authorization →")