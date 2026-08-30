🤖 Razorpay TrustGate
          Subtitle: An NPCI UAP-Compliant Agentic Trust Gateway & Cryptographic M2M Settlement Protocol
 Prototype for the Razorpay AI Buildathon 2026 (AI Growth & Agentic Commerce Track)
📌 Project Overview

The Razorpay Agentic Payments & Trust Gateway Suite is an end-to-end payment service and trust coordination network designed to transition digital commerce from human-centric "browsing and clicking" to autonomous, machine-to-machine (M2M) interactions.

By wrapping Razorpay's Test-Mode APIs (Orders, Refunds, Route/Split) with stateful multi-agent orchestrators, this suite implements a futuristic payment gateway aligned with India's upcoming Unified Agent Protocol (UAP) by NPCI and the global Agentic Commerce Protocol (ACP). It systematically resolves the industry's largest agentic commerce bottlenecks: unstructured natural language parsing, autonomous volume haggling, cross-merchant collaborative upselling, agent spend limits, and real-time self-healing disputes.

🛑 The Core Problem Statement

As digital commerce transitions to autonomous AI agents acting on behalf of consumers, traditional payment gateways and checkout experiences fail due to several core architectural limits:

The Parsing & Intent-Binding Bottleneck: Standard search systems and rigid regular expressions fail to interpret complex, conversational human requests (e.g., "Order fifty office chairs for forty thousand rupees"), often collapsing or falling back to default values.
The Fixed List-Price Constraint: Existing checkout models are designed only for static, fixed list prices. However, in wholesale, bulk, or B2B procurement, dynamic price haggling and negotiation are standard practices.
The Multi-Store Scrapyard: Buying agents waste massive computational resources, time, and bandwidth scraping and crawling dozens of individual merchant websites to discover inventory.
The Security & Liability Gap: If an autonomous agent hallucinates or goes rogue, there are no guardrails to prevent it from overspending, causing severe financial liability.
The Post-Purchase Dispute Loop: Traditional credit card disputes and chargeback cycles require manual intervention and take 7–15 business days. If an agent orders a premium item but receives a sub-standard product, a 15-day bank hold severely disrupts automated business supply chains.

🌟 The 5-Stage Agentic Solution

Our Trust Gateway Suite systematically addresses these limitations by organizing the payment flow into 5 secure, explainable, and cryptographically bounded stages:

 [ Stage 1: Instruct & Bind ] ──► [ Stage 2: Discovery & Haggle ] ──► [ Stage 3: Authorization ]
             │                                     │                                    │
             ▼                                     ▼                                    ▼
  • Natural Language Console            • Reverse Auction Bidding            • Shared Payment Token
  • NPCI UAP Spend Limits               • A2A Conversational Haggle          • Cryptographic Bounds
  • WebAuthn Biometric Gate             • Signed JSON "Deal Memo"            • Live Policy Check
                                                                                        │
 [ Stage 5: Self-Healing Dispute ] ◄── [ Stage 4: Execution & Escrow ] ◄────────────────┘
             │                                     │
             ▼                                     ▼
  • Proof-of-Intent (PoI) Audit         • Single-Click Razorpay Order
  • Escrow Lock & Release               • Cross-Merchant Syndicate Split
  • Automated Refunds API               • RazorpayX Escrow+ Pool

Stage 1: Instruct & Bind (Pre-Transaction)

The Interface: Users specify their purchasing goals in plain, unstructured English using a clean Natural Language Instruction Console (voice/microphone bridges are bypassed to ensure 100% browser and presentation stability).
The AI Parser: Your FastAPI backend runs the prompt through an advanced AI extraction engine (powered by Claude 3.5 Sonnet via .env or a robust local fallback). It maps keywords to database schema models, converts written words (e.g. "fifty", "forty thousand") to numeric integers, and binds them to strict parameters (item, quantity, max_budget, category).
The Gates: Users register a strict spending limit (mimicking NPCI's UAP UPI AutoPay mandates) and complete a WebAuthn Biometric Passkey Verification to bind the human owner to the agentic session.

Stage 2: Discovery & Haggle

Reverse Auction Broadcast: The Buyer Agent broadcasts the signed intent. Matching Merchant Bidding Agents programmatically evaluate stock, compute quotes with seeded variance, and respond with dynamic, short-lived Razorpay Payment Links valid for 3 minutes to maintain inventory lock-safety.
Agent-to-Agent (A2A) Negotiation: The Buyer Agent selects the best bid and opens a stateful negotiation channel. The agents haggle over margins in exchange for concessions (e.g., "We'll pay immediately if you grant a 10% volume discount").
The Deal Memo: Upon consensus, the agents sign and compile a cryptographic, human-auditable "Deal Memo" (JSON) accompanied by an HMAC-SHA256 signature to prevent tampering.

Stage 3: Authorization & Spend-Control Checks

Shared Payment Token (SPT): The gateway generates an SPT modeled after the Stripe/OpenAI ACP standard. This token is base64 encoded, cryptographically signed, and strictly micro-scoped to a single merchant_id, a single precise amount, and carries a strict 15-minute Time-To-Live (ttl_seconds = 900) expiration stamp.
Policy Verification Gate: Before routing, the backend compares the SPT amount against the user's locked UPI-UAP spend limit. If the bargained price exceeds the pre-authorized ceiling, the SPT is blocked and the transaction fails gracefully, preventing rogue agent spend.

Stage 4: Payment Execution & Syndicate Splitting

Collaborative Syndicate Upsell: The gateway scans the network for non-competing, complementary merchants (e.g., a logistics provider when buying bulk office chairs). The agents negotiate a combined syndicate bundle discount in real-time.
Razorpay Split Settlements: On checkout, the user makes a single consolidated payment. The gateway leverages Razorpay's Route / Split API to automatically calculate shares and disperse payouts directly to the primary merchant and the syndicate partner.
Smart Escrow Pool: The principal funds are routed and locked inside a simulated RazorpayX Escrow+ Pool, held securely until successful post-delivery verification.
Proof-of-Intent (PoI) Bundle: The Buyer Agent packages and signs a PoI bundle (storing the original user instructions and reasoning logs) and attaches it directly to the transaction payload.

Stage 5: Self-Healing Disputes (Post-Transaction)

The Mismatch: A merchant fails to deliver the specified goods or delivers a mismatched SKU (e.g. delivering "recycled paper" instead of the authorized "premium printing paper").
Autonomous Resolution: Upon user flag, the Dispute Agent parses the PoI bundle and compares keywords against the delivered catalog specifications.
Instant Automated Refund: Finding a quality mismatch, the Dispute Agent programmatically triggers an instant automated refund via the Razorpay Refunds API directly from the escrow pool, bypassing manual support wait times.

🛠️ Complete Directory Structure

Below is the directory tree of the repository, highlighting where the stateful agentic code, database schemas, and frontend interfaces are located:

razorpay-agentic-commerce/
├── .env                              # Secure API keys (ANTHROPIC_API_KEY)
├── run.py                            # Central Orchestrator launcher (starts Backend & Frontend)
├── requirements.txt                  # Python dependency manifest
├── backend/
│   ├── __init__.py
│   ├── main.py                       # FastAPI application router & REST endpoints (Stages 1-5)
│   ├── models.py                     # Pydantic schemas for endpoint data-contracts
│   ├── agents.py                     # Core AI Layer (NL parser, Haggle transcript, Dispute validation)
│   ├── security.py                   # Cryptographic signing, WebAuthn Passkeys, and SPT generation
│   └── razorpay_mock.py              # Mock interfaces for Razorpay Orders, Route Splits, and Refunds
├── database/
│   ├── db.py                         # SQLite engine loader, seeding, and path overrides
│   ├── schema.sql                    # SQL relational schemas for ACID database tables
│   └── agentic_commerce.db           # Live SQL database file storing transaction trails (created on boot)
└── frontend/
    ├── Home.py                       # Streamlit multi-stage landing dashboard
    ├── shared.py                     # Brand color palette, sidebar journey logs, and unified API caller
    └── pages/
        ├── 1_Stage1_Instruct_and_Bind.py # Text-based NL instruction input console & Passkey verification
        ├── 2_Stage2_Discovery_and_Haggle.py # Interactive Reverse Bidding lists and A2A Haggle chat window
        ├── 3_Stage3_Authorization.py    # Dual spend limit checking, policy gate, and SPT JSON rendering
        ├── 4_Stage4_Payment_and_Escrow.py # Syndicate upsell, Razorpay Checkout, Route Splits & Escrow details
        ├── 5_Stage5_Dispute_Resolution.py # Simulated delivery mismatch input and instant auto-refunds
        └── 6_Use_Cases.py                # Visual use cases displaying applicability of this PSP pattern

💾 Relational Database Schema (database/schema.sql)

The gateway guarantees absolute explainability by persisting all agent thought-paths and transactions in an ACID-compliant SQLite ledger:

users: Manages customer profiles, UPI handles, registered bank accounts, spend limits, and biometric passkey status.
agents: Manages state, roles, and status of active network bots (buyer, merchant, dispute).
merchants: Stores partner merchant catalogs, geographic locations, and base item pricing.
intents: Stores original user raw prompts, parsed quantities, and the structured JSON output.
bids: Tracks dynamic merchant response proposals, quoted prices, and delivery times.
deals: Captures finalized bargained agreements, conversational logs, and HMAC-SHA256 signatures.
orders: Records the active Razorpay Order IDs, the issued SPT token, and settlement totals.
splits: Maps dynamic routing splits for primary merchants and collaborative syndicate partners.
escrow: Tracks holding records and status (held, released, refunded) of the funds pool.
poi_bundles: Stores cryptographically signed bundles linking the order to the original prompt.
disputes: Logs transaction complaints, delivered descriptions, dispute statuses, and automated refund IDs.

🚀 Local Setup & Installation
To run the Razorpay Agentic Payments & Trust Gateway Suite on your local machine, follow this step-by-step setup:

1. Clone the repository
Navigate to your developer directory:

cd C:\Users\poojakc\razorpay-agentic-commerce\razorpay-agentic-commerce
2. Install Python dependencies
Install all required libraries, including FastAPI, Streamlit, and python-dotenv:

python -m pip install -r requirements.txt
(Alternatively, install them manually):

python -m pip install fastapi uvicorn streamlit pydantic requests python-dotenv anthropic
3. Create and configure your .env file
Create a text file named .env in the root directory (matching the folder tree above) and insert your Anthropic API key to enable Claude 3.5 Sonnet to parse your commands:

ANTHROPIC_API_KEY=your-actual-claude-api-key-here
Note: Do not add quotation marks or spaces around the = sign in your .env file. If the key is missing or invalid, the backend will gracefully fall back to the built-in, robust local offline parsing engine.

4. Prevent Process/Port Conflicts
If you have previously launched the server, older python subprocesses might be holding onto port 8000 or 8501. Clear them forcefully:

taskkill /F /IM python.exe
5. Launch the Platform
Start the central runner to boot both the FastAPI backend and Streamlit frontend concurrently:

python run.py
6. Run the Demo
Open your web browser (Chrome or Edge recommended) and navigate to: 👉 http://localhost:8501

👨‍⚖️ What the Buildathon Panel Needs to Know
When reviewing this project, the judges should focus on these engineering standards:

Direct Alignment with NPCI UAP & stripe/OpenAI ACP: 
The project is built specifically to address the global 2026 agentic commerce standards. Stage 1's spend ceiling maps directly to UAP UPI AutoPay policies, while Stage 3's Shared Payment Token mimics the exact secure cryptographic token structures designed by Stripe and OpenAI.

No Hand-Waving: 100% Active Database Integration: 
The UI does not use hardcoded static mockups. All data—including parsed intents, dynamic bids, haggled deal transcripts, splits, and dispute statuses—is actively saved, updated, and queried from a local SQLite database in real-time.

Real Cryptography:
 Every crucial transaction step is mathematically secured. The deal memo, SPT, and PoI bundles are genuinely signed and verified using HMAC-SHA256 signatures via Python’s hmac and hashlib libraries, protecting the gateway against agent fraud or tampering.

Excellent Developer Experience (DX): 
The sandbox mock files (backend/razorpay_mock.py and backend/security.py) are structured as explicit plug-and-play drop-in points. To scale this from a local prototype to a production-grade system, developers only need to swap the simulated endpoints inside razorpay_mock.py with the real Razorpay Python SDK (razorpay.Client(auth=(key, secret))), keeping the rest of the multi-agent state-machine entirely untouched!



Project created for the Razorpay AI Buildathon, August 2026