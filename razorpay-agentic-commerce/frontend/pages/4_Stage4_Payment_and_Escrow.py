"""
Stage 4 — Payment Execution: Syndicate Split & Smart Escrow
"""
import sys, os, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import streamlit as st
from shared import inject_theme, hero, init_session_state, sidebar_nav, api, log_activity

st.set_page_config(page_title="Stage 4 · Payment & Escrow", page_icon="💳", layout="wide")
inject_theme()
init_session_state()
sidebar_nav(current_stage=4)

hero("Stage 4 · Payment Execution", "Cross-merchant syndicate split &amp; RazorpayX Escrow+")
st.page_link("pages/3_Stage3_Authorization.py", label="⬅ Back to Stage 3")

if not st.session_state.spend_check or not st.session_state.spend_check.get("within_limit"):
    st.info("⬅️ Pass the spend-control check in Stage 3 first.")
    st.page_link("pages/3_Stage3_Authorization.py", label="Go to Stage 3")
    st.stop()

deal_id = st.session_state.deal["deal_id"]

st.markdown('<div class="rzp-card">', unsafe_allow_html=True)
st.markdown("**🔗 Cross-merchant syndicate offers**")
if st.button("Check syndicate bundle offers"):
    resp = api("POST", "/api/syndicate/offer", json={"deal_id": deal_id})
    st.session_state.syndicate = resp
    if resp.get("available"):
        log_activity(f"🔗 Syndicate offer found: {resp['partner_name']}")
    st.rerun()

include_syndicate = False
if st.session_state.syndicate and st.session_state.syndicate.get("available"):
    syn = st.session_state.syndicate
    st.write(f"**{syn['partner_name']}** offers: {syn['addon_description']} for ₹{syn['addon_price']:,.0f} · "
             f"primary merchant credits ₹{syn['primary_credit']:,.0f} → "
             f"net add-on cost **₹{syn['net_addon_cost']:,.0f}**")
    include_syndicate = st.checkbox("Add syndicate bundle to this order")
elif st.session_state.syndicate:
    st.caption("No syndicate partner available for this order category.")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="rzp-card">', unsafe_allow_html=True)
if st.button("💳 Single-click checkout"):
    with st.spinner("Executing Route split · locking Escrow+ · signing Proof-of-Intent…"):
        time.sleep(0.8)
        resp = api("POST", "/api/checkout", json={"deal_id": deal_id, "include_syndicate": include_syndicate})
    st.session_state.checkout = resp
    st.session_state.stage = max(st.session_state.stage, 4)
    log_activity(f"💳 Order {resp['razorpay_order']['id']} created · ₹{resp['total_amount']:,.0f}")
    log_activity(f"🔒 Escrow held: ₹{resp['escrow']['amount']:,.0f}")
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.checkout:
    co = st.session_state.checkout
    st.markdown('<div class="rzp-card">', unsafe_allow_html=True)
    st.markdown(f"**Order `{co['razorpay_order']['id']}`** — "
                f'<span class="rzp-badge rzp-badge-navy">Total ₹{co["total_amount"]:,.0f}</span>',
                unsafe_allow_html=True)

    split_df = pd.DataFrame(co["splits"])[["merchant_name", "role", "amount", "status"]]
    split_df.columns = ["Merchant", "Role", "Amount (₹)", "Payout status"]
    st.markdown("**Dynamic Split Visualization (Razorpay Route)**")
    st.dataframe(split_df, use_container_width=True, hide_index=True)
    st.bar_chart(split_df.set_index("Merchant")["Amount (₹)"])

    st.markdown(f'<span class="rzp-badge rzp-badge-amber">🔒 Escrow held: ₹{co["escrow"]["amount"]:,.0f} '
                f'(RazorpayX Escrow+)</span>', unsafe_allow_html=True)

    with st.expander("📜 How your AI agent got here (Proof-of-Intent)"):
        poi = co["poi_bundle"]
        memo = poi["deal_memo"]

        st.markdown(f"**What you asked for:** {poi['parsed_intent']['item']} × "
                    f"{poi['parsed_intent']['quantity']}")

        st.markdown("**Steps the agent took:**")
        for step in poi["reasoning_steps"]:
            st.markdown(f"- {step}")

        st.markdown("**Negotiation with the merchant:**")
        for turn in memo["transcript"]:
            st.markdown(f"- **{turn['speaker']}:** {turn['message']}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Original price", f"₹{memo['original_price']:,.0f}")
        c2.metric("Final price", f"₹{memo['final_price']:,.0f}")
        c3.metric("Concession", memo["concession"])

        if poi.get("syndicate_bundle"):
            syn = poi["syndicate_bundle"]
            st.markdown(f"**Syndicate add-on:** {syn['partner_name']} — "
                        f"{syn['addon_description']} for ₹{syn['addon_price']:,.0f} "
                        f"(net cost ₹{syn['net_addon_cost']:,.0f} after primary merchant credit)")

        st.caption(f"Cryptographically signed with HMAC-SHA256 · "
                    f"`{co['poi_signature'][:24]}…` (full signature verified on the backend)")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.page_link("pages/5_Stage5_Dispute_Resolution.py", label="Continue to Stage 5 — Dispute Resolution →")