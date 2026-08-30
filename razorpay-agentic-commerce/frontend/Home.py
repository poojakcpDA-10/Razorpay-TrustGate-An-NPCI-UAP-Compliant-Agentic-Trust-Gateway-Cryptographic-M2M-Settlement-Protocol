"""
Home — landing page. Run with: streamlit run frontend/Home.py
"""
import streamlit as st
from shared import inject_theme, hero, init_session_state, sidebar_nav, RZP_BLUE, RZP_BLUE_DARK

st.set_page_config(page_title="Agentic Commerce | Razorpay", page_icon="💳", layout="wide")
inject_theme()
init_session_state()
sidebar_nav(current_stage=0)

hero("Agentic Commerce Platform",
     "Razorpay TrustGate- An NPCI UAP-Compliant Agentic Trust Gateway & Cryptographic M2M Settlement Protocol")

st.markdown("""
<div class="rzp-card">
<h3>What this demo shows</h3>
<p>An AI Buyer Agent that takes a single shopping instruction, negotiates with merchant agents
in real time, checks your spend policy, splits payment across multiple merchants, holds
funds in escrow, and — if something goes wrong — resolves the dispute and refunds you
automatically. No manual back-and-forth after you say the word.</p>
</div>
""", unsafe_allow_html=True)

cols = st.columns(5)
stage_cards = [
    ("📝", "Stage 1", "Instruct & Bind", "Describe your goal, set a spend limit, verify your passkey.", "pages/1_Stage1_Instruct_and_Bind.py"),
    ("🤝", "Stage 2", "Discovery & Haggle", "Merchants bid, your agent negotiates the best deal.", "pages/2_Stage2_Discovery_and_Haggle.py"),
    ("🔑", "Stage 3", "Authorization", "Shared Payment Token issued, spend policy verified.", "pages/3_Stage3_Authorization.py"),
    ("💳", "Stage 4", "Payment & Escrow", "Route split, escrow lock, signed Proof-of-Intent.", "pages/4_Stage4_Payment_and_Escrow.py"),
    ("⚖️", "Stage 5", "Dispute Resolution", "Auto-validated refund if delivery doesn't match intent.", "pages/5_Stage5_Dispute_Resolution.py"),
]
for col, (icon, num, title, desc, target) in zip(cols, stage_cards):
    with col:
        st.markdown(f"""
        <div class="rzp-card" style="min-height:190px;">
            <div style="font-size:28px;">{icon}</div>
            <div class="rzp-badge rzp-badge-navy" style="margin:8px 0;">{num}</div>
            <h4 style="margin:4px 0;color:{RZP_BLUE_DARK};">{title}</h4>
            <p style="font-size:13px;color:#556;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)
        st.page_link(target, label=f"Open {num} →")

st.markdown("<br>", unsafe_allow_html=True)
st.page_link("pages/6_Use_Cases.py", label="📊 See real-world use cases for this architecture →")

st.markdown("---")
st.caption("Prototype for demonstration purposes. Razorpay, NPCI UAP, and Stripe/OpenAI ACP integrations "
           "are simulated — see backend/razorpay_mock.py and backend/security.py for real-integration swap points.")