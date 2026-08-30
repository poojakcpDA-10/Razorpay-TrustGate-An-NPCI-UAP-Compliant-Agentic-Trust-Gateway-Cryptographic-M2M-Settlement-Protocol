"""
Use Cases — real-world scenarios this architecture generalizes to.
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from shared import inject_theme, hero, init_session_state, sidebar_nav, RZP_BLUE_DARK

st.set_page_config(page_title="Use Cases", page_icon="📊", layout="wide")
inject_theme()
init_session_state()
sidebar_nav(current_stage=0)

hero("Use Cases", "Where this Instruct → Negotiate → Split-Pay → Escrow → Self-Heal pattern applies")

cases = [
    ("🏢", "B2B Procurement (this demo)",
     "Office managers order bulk supplies — paper, furniture, IT hardware — under a "
     "pre-approved budget. The agent shops around, negotiates, and bundles shipping automatically.",
     ["Multi-vendor reverse auctions cut procurement cycle time from days to minutes",
      "Spend-control slider maps directly to existing approval-matrix policies",
      "Auto-refund on mismatched SKUs removes manual PO reconciliation work"]),
    ("🛒", "Grocery & household replenishment",
     "\"Reorder my usual groceries, don't spend more than ₹3,000\" — the agent compares "
     "nearby kirana/quick-commerce merchants and negotiates delivery-slot bundling.",
     ["Recurring UPI AutoPay-style mandates fit the UAP spend-control model directly",
      "Syndicate bundling matches real quick-commerce partner-delivery models",
      "Dispute agent handles wrong/missing items without a support call"]),
    ("✈️", "Travel booking",
     "\"Book a Bengaluru–Delhi return flight under ₹15,000, flexible dates\" — Buyer Agent "
     "negotiates fare classes and bundles airport transfer with a partner cab operator.",
     ["A2A haggle maps to real fare-negotiation/upgrade-offer flows",
      "PoI bundle protects against date/class booking errors",
      "Escrow hold suits pre-travel cancellation windows"]),
    ("🏠", "Subscription & utility management",
     "An agent renegotiates recurring subscriptions (broadband, SaaS seats) against your "
     "spend ceiling, switching providers automatically when a better bundle appears.",
     ["UAP spend limits prevent runaway agent-driven renewals",
      "Deal Memo gives an auditable trail for every auto-switch decision",
      "Works with NPCI's existing UPI AutoPay mandate infrastructure"]),
    ("🏭", "Manufacturing raw-material sourcing",
     "A plant's purchasing agent sources raw materials across a supplier network within "
     "a locked budget, syndicating logistics with a shared freight partner.",
     ["Reverse auction fits existing RFQ/e-tender workflows",
      "Route API split settles supplier + freight partner in one transaction",
      "Dispute agent flags quality-spec mismatches against the original RFQ intent"]),
]

for icon, title, desc, points in cases:
    st.markdown(f"""
    <div class="rzp-card">
        <div style="font-size:26px;">{icon}</div>
        <h4 style="margin:6px 0;color:{RZP_BLUE_DARK};">{title}</h4>
        <p style="color:#445;">{desc}</p>
        <ul style="color:#334;font-size:14px;">
            {''.join(f'<li>{p}</li>' for p in points)}
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.page_link("Home.py", label="🏠 Back to Home")