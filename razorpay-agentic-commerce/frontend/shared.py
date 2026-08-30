
import os
import time
import requests
import streamlit as st

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

# ---------------------------------------------------------------------------
# Verified Razorpay brand palette (Razorpay official brand assets, 2026):
#   Primary blue   #0D94FB  (Dodger Blue)
#   Deep navy      #0C2451  (Space Cadet / Prussian Blue family)
#   Near-black ink #0F0F0F
# ---------------------------------------------------------------------------
RZP_BLUE = "#0D94FB"
RZP_BLUE_DARK = "#0C2451"
RZP_NAVY = "#0A1F3D"
RZP_INK = "#0F0F0F"
RZP_BG = "#F7F9FC"
RZP_CARD_BORDER = "#E4EAF5"
RZP_GREEN = "#22C55E"
RZP_AMBER = "#F5A623"
RZP_RED = "#EF4444"

STAGES = [
    ("Home", "🏠", "Home.py"),
    ("Stage 1 · Instruct & Bind", "📝", "pages/1_Stage1_Instruct_and_Bind.py"),
    ("Stage 2 · Discovery & Haggle", "🤝", "pages/2_Stage2_Discovery_and_Haggle.py"),
    ("Stage 3 · Authorization", "🔑", "pages/3_Stage3_Authorization.py"),
    ("Stage 4 · Payment & Escrow", "💳", "pages/4_Stage4_Payment_and_Escrow.py"),
    ("Stage 5 · Dispute Resolution", "⚖️", "pages/5_Stage5_Dispute_Resolution.py"),
    ("Use Cases", "📊", "pages/6_Use_Cases.py"),
]


def inject_theme():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

        html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
        .stApp {{ background-color: {RZP_BG}; }}
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {RZP_NAVY} 0%, {RZP_BLUE_DARK} 100%);
        }}
        section[data-testid="stSidebar"] * {{ color: #FFFFFF !important; }}

        h1, h2, h3 {{ color: {RZP_BLUE_DARK}; font-weight: 700; }}

        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes pulse {{
            0% {{ box-shadow: 0 0 0 0 rgba(51,149,255,0.5); }}
            70% {{ box-shadow: 0 0 0 8px rgba(51,149,255,0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(51,149,255,0); }}
        }}
        @keyframes livedot {{
            0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }}
        }}
        @keyframes shimmer {{
            0% {{ background-position: -400px 0; }}
            100% {{ background-position: 400px 0; }}
        }}

        .rzp-hero {{
            background: linear-gradient(120deg, {RZP_BLUE_DARK} 0%, {RZP_BLUE} 100%);
            padding: 26px 30px; border-radius: 16px; margin-bottom: 22px;
            animation: fadeInUp 0.5s ease-out;
        }}
        .rzp-hero h1 {{ color: white !important; margin: 0; font-size: 28px; font-weight: 800; }}
        .rzp-hero p {{ color: #DCEBFF; margin: 6px 0 0 0; font-size: 14px; }}

        .rzp-card {{
            background: white; border: 1px solid {RZP_CARD_BORDER}; border-radius: 14px;
            padding: 20px 22px; margin-bottom: 16px;
            box-shadow: 0 1px 3px rgba(10,37,64,0.06);
            animation: fadeInUp 0.4s ease-out;
            transition: box-shadow 0.2s ease, transform 0.2s ease;
        }}
        .rzp-card:hover {{ box-shadow: 0 6px 18px rgba(10,37,64,0.10); transform: translateY(-1px); }}

        .rzp-badge {{
            display: inline-block; padding: 4px 12px; border-radius: 20px;
            font-size: 12px; font-weight: 700; color: white; background: {RZP_BLUE};
            letter-spacing: 0.2px;
        }}
        .rzp-badge-green {{ background: {RZP_GREEN}; }}
        .rzp-badge-amber {{ background: {RZP_AMBER}; }}
        .rzp-badge-navy {{ background: {RZP_BLUE_DARK}; }}
        .rzp-badge-red {{ background: {RZP_RED}; }}

        .rzp-live {{
            display: inline-flex; align-items: center; gap: 6px;
            font-size: 12px; font-weight: 700; color: {RZP_RED};
        }}
        .rzp-live .dot {{
            width: 8px; height: 8px; border-radius: 50%; background: {RZP_RED};
            animation: livedot 1.2s infinite;
        }}

        div.stButton > button {{
            background-color: {RZP_BLUE}; color: white; border: none;
            border-radius: 9px; font-weight: 700; padding: 9px 20px;
            transition: all 0.15s ease;
        }}
        div.stButton > button:hover {{
            background-color: {RZP_BLUE_DARK}; color: white; transform: translateY(-1px);
            animation: pulse 1.2s infinite;
        }}

        .stProgress > div > div > div > div {{ background-color: {RZP_BLUE}; }}

        .rzp-step {{
            padding: 9px 12px; border-radius: 9px; margin-bottom: 4px;
            font-size: 13.5px; transition: background 0.2s ease;
        }}
        .rzp-step-active {{ background: rgba(255,255,255,0.15); font-weight: 700; }}
        .rzp-step-done {{ opacity: 0.75; }}
        .rzp-step-todo {{ opacity: 0.45; }}

        .rzp-logmark {{
            font-family: 'Courier New', monospace; font-size: 12.5px;
            color: #4B5A73; padding: 3px 0; border-left: 2px solid {RZP_BLUE};
            padding-left: 10px; margin-bottom: 2px; animation: fadeInUp 0.3s ease-out;
        }}
    </style>
    """, unsafe_allow_html=True)


def hero(title: str, subtitle: str):
    st.markdown(f"""
    <div class="rzp-hero">
        <h1>🔵 {title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def api(method, path, **kwargs):
    url = f"{BACKEND_URL}{path}"
    try:
        r = requests.request(method, url, timeout=15, **kwargs)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        st.error(f"⚠️ Cannot reach backend at {BACKEND_URL}. Start it with: "
                 f"`python -m uvicorn backend.main:app --reload --port 8000`")
        st.stop()
    except requests.exceptions.HTTPError as e:
        st.error(f"Backend error: {e.response.text}")
        st.stop()


def init_session_state():
    defaults = {
        "stage": 1, "intent": None, "bids": None, "selected_bid": None,
        "deal": None, "spend_check": None, "syndicate": None,
        "checkout": None, "dispute_result": None, "passkey_ok": False,
        "spend_limit": 50000, "activity_log": [], "_last_activity_message": None,
    }
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default


def log_activity(message: str):
    
    if st.session_state.get("_last_activity_message") == message:
        return
    st.session_state._last_activity_message = message
    st.session_state.activity_log.insert(0, f"{time.strftime('%H:%M:%S')}  {message}")
    st.session_state.activity_log = st.session_state.activity_log[:12]


# Stage number -> page path, used to build clickable back/forward navigation.
_STAGE_PAGES = {
    1: "pages/1_Stage1_Instruct_and_Bind.py",
    2: "pages/2_Stage2_Discovery_and_Haggle.py",
    3: "pages/3_Stage3_Authorization.py",
    4: "pages/4_Stage4_Payment_and_Escrow.py",
    5: "pages/5_Stage5_Dispute_Resolution.py",
}


def sidebar_nav(current_stage: int = 0):
    with st.sidebar:
        st.markdown("### 🧭 Transaction Journey")
        labels = [
            "1️⃣ Instruct & Bind", "2️⃣ Discovery & Haggle", "3️⃣ Authorization",
            "4️⃣ Payment & Escrow", "5️⃣ Dispute Resolution",
        ]
        # Highest stage the user has actually reached — any stage up to this
        # point has data to show, so it's safe to jump straight back to it.
        reached = st.session_state.get("stage", 1)
        for i, label in enumerate(labels, start=1):
            if i == current_stage:
                st.markdown(f'<div class="rzp-step rzp-step-active">👉 {label}</div>',
                            unsafe_allow_html=True)
            elif i <= reached:
                # Visited stage — always clickable, so you can go back (or
                # jump forward again) at any point, even mid-flow.
                st.page_link(_STAGE_PAGES[i], label=f"✅ {label}")
            else:
                st.markdown(f'<div class="rzp-step rzp-step-todo">▫️ {label}</div>',
                            unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="rzp-live"><span class="dot"></span> LIVE ACTIVITY</div>',
                    unsafe_allow_html=True)
        if st.session_state.get("activity_log"):
            for entry in st.session_state.activity_log:
                st.markdown(f'<div class="rzp-logmark">{entry}</div>', unsafe_allow_html=True)
        else:
            st.caption("No activity yet — start in Stage 1.")

        st.markdown("---")
        st.caption(f"Backend: `{BACKEND_URL}`")
        if st.button("🔄 Reset demo", key="reset_demo_btn"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()