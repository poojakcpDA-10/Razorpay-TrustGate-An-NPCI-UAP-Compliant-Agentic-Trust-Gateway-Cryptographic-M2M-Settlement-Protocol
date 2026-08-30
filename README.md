# 🤖 Razorpay TrustGate

### An NPCI UAP-Compliant Agentic Trust Gateway & Cryptographic M2M Settlement Protocol

## 📌 Project Overview

**Razorpay TrustGate** is an end-to-end **Agentic Payment & Trust Gateway** designed to transition digital commerce from traditional human-driven browsing and checkout to autonomous **Machine-to-Machine (M2M)** transactions.

The platform wraps **Razorpay Test-Mode APIs** such as Orders, Refunds, and Route/Split with stateful multi-agent orchestration to demonstrate an agentic commerce architecture aligned with the emerging **Unified Agent Protocol (UAP)** ecosystem and global **Agentic Commerce Protocol (ACP)** concepts.

The system addresses key challenges in agentic commerce, including:

* Natural-language purchase intent parsing
* Autonomous price negotiation
* Multi-merchant collaboration
* Agent spending limits
* Cryptographic authorization
* Escrow-based settlement
* Automated dispute resolution

---

# 🛑 Problem Statement

As AI agents increasingly act on behalf of consumers, traditional payment gateways are not designed to safely handle autonomous decision-making.

### 1. Parsing & Intent-Binding Bottleneck

Traditional search systems and rigid regular expressions struggle to understand complex natural-language purchasing requests.

For example:

> "Order fifty office chairs for forty thousand rupees."

The system needs to correctly identify:

* Product
* Quantity
* Maximum budget
* Category
* Purchase intent

---

### 2. Fixed List-Price Constraint

Traditional checkout systems primarily operate using fixed prices.

However, wholesale and B2B procurement frequently require:

* Bulk discounts
* Dynamic pricing
* Negotiation
* Volume-based offers

---

### 3. Multi-Store Discovery Problem

An autonomous purchasing agent may need to search multiple merchants to find the best inventory, price, and delivery option.

This creates unnecessary:

* Crawling
* Scraping
* API requests
* Computational overhead

---

### 4. Security & Liability Gap

If an autonomous agent makes an incorrect decision or attempts to spend beyond the user's authorization, there must be strict financial guardrails.

Without spending limits and cryptographic authorization, autonomous payments create significant financial risk.

---

### 5. Post-Purchase Dispute Loop

Traditional payment disputes can require manual intervention and lengthy processing.

For autonomous commerce, dispute resolution needs to be faster and machine-readable.

---

# 🌟 5-Stage Agentic Architecture

```text
┌─────────────────────────────┐
│ Stage 1: Instruct & Bind    │
│                             │
│ • Natural Language Input    │
│ • Spend Limits              │
│ • WebAuthn Verification     │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Stage 2: Discovery & Haggle │
│                             │
│ • Merchant Discovery        │
│ • Reverse Auction           │
│ • A2A Negotiation           │
│ • Signed Deal Memo          │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Stage 3: Authorization      │
│                             │
│ • Shared Payment Token      │
│ • Cryptographic Bounds      │
│ • Policy Verification       │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Stage 4: Execution & Escrow │
│                             │
│ • Razorpay Order            │
│ • Syndicate Splitting       │
│ • Escrow Pool               │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Stage 5: Self-Healing       │
│ Dispute Resolution          │
│                             │
│ • Proof-of-Intent           │
│ • Delivery Verification     │
│ • Automated Refund          │
└─────────────────────────────┘
```

---

# 🔐 Stage 1 — Instruct & Bind

The user specifies a purchasing goal using **natural language**.

Example:

> "Buy 50 office chairs for a maximum budget of ₹40,000."

The AI parsing engine converts this unstructured request into structured parameters:

```json
{
  "item": "office chairs",
  "quantity": 50,
  "max_budget": 40000,
  "category": "office furniture"
}
```

The system also applies:

* User spending limits
* Agent authorization
* WebAuthn biometric/passkey verification

This establishes a secure relationship between the **human owner and autonomous agent**.

---

# 🤝 Stage 2 — Discovery & Haggle

The Buyer Agent broadcasts the signed purchasing intent to participating Merchant Agents.

Merchant Agents evaluate:

* Inventory
* Pricing
* Quantity
* Delivery time
* Discount possibilities

They respond with dynamic bids.

The Buyer Agent selects the most suitable offer and initiates an **Agent-to-Agent negotiation**.

Example:

> Buyer Agent: "We can complete payment immediately if you provide a 10% volume discount."

Once both agents reach an agreement, the system creates a cryptographically signed **Deal Memo**.

The Deal Memo is protected using:

**HMAC-SHA256**

to detect unauthorized modification.

---

# 🛡️ Stage 3 — Authorization & Spend Control

After negotiation, the gateway generates a **Shared Payment Token (SPT)**.

The token is:

* Base64 encoded
* Cryptographically signed
* Bound to a specific merchant
* Bound to a precise transaction amount
* Time-limited

The prototype uses:

```text
TTL = 900 seconds
```

or approximately **15 minutes**.

Before payment execution, the backend verifies:

```text
Requested Amount
        ≤
Authorized Spend Limit
```

If the negotiated price exceeds the user's authorized spending limit, the transaction is blocked.

This prevents an autonomous agent from exceeding its financial authority.

---

# 💳 Stage 4 — Payment Execution & Syndicate Splitting

The gateway supports collaborative purchasing between complementary merchants.

For example:

```text
Office Furniture Merchant
          +
Logistics Provider
          ↓
Collaborative Bundle
```

The buyer makes a single consolidated payment.

The system then demonstrates how **Razorpay Route/Split** can distribute the appropriate settlement shares between participating merchants.

The architecture also includes a simulated **RazorpayX Escrow+ Pool**.

Funds remain locked until the post-delivery verification stage.

---

# 📜 Proof-of-Intent (PoI)

The Buyer Agent generates a **Proof-of-Intent bundle** containing:

* Original user instruction
* Structured intent
* Transaction information
* Agent reasoning/audit information

The bundle is cryptographically signed and associated with the transaction.

This provides an auditable connection between:

```text
Human Intent
      ↓
AI Decision
      ↓
Negotiated Deal
      ↓
Payment
```

---

# 🔄 Stage 5 — Self-Healing Dispute Resolution

After delivery, the user can report a mismatch.

Example:

```text
Authorized:
Premium Printing Paper

Delivered:
Recycled Paper
```

The Dispute Agent analyzes the original Proof-of-Intent and compares it with the delivered product information.

If a mismatch is detected, the system can trigger an automated refund through the Razorpay Refunds API in the simulated environment.

This reduces dependency on manual dispute processing.

---

# 🧠 AI Architecture

The AI layer is responsible for:

```text
Natural Language Input
        ↓
Intent Extraction
        ↓
Structured Parameters
        ↓
Merchant Discovery
        ↓
Negotiation
        ↓
Deal Formation
        ↓
Transaction Validation
        ↓
Dispute Analysis
```

The backend supports an AI extraction engine using **Claude 3.5 Sonnet** through environment configuration, with a local fallback parser when the API key is unavailable.

---

# 🏗️ Technology Stack

## Backend

* Python
* FastAPI
* Pydantic
* SQLite
* python-dotenv

## AI

* Claude 3.5 Sonnet
* Natural Language Processing
* Agentic workflows
* Rule-based fallback parsing

## Security

* HMAC-SHA256
* Cryptographic signing
* WebAuthn Passkeys
* Time-limited authorization tokens
* Spend-limit enforcement

## Frontend

* Streamlit
* Python

## Payment Layer

* Razorpay Orders
* Razorpay Refunds
* Razorpay Route/Split
* Simulated Escrow
* Shared Payment Token

---

# 📁 Project Structure

```text
razorpay-agentic-commerce/
│
├── .env
├── run.py
├── requirements.txt
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── agents.py
│   ├── security.py
│   └── razorpay_mock.py
│
├── database/
│   ├── db.py
│   ├── schema.sql
│   └── agentic_commerce.db
│
└── frontend/
    ├── Home.py
    ├── shared.py
    │
    └── pages/
        ├── 1_Stage1_Instruct_and_Bind.py
        ├── 2_Stage2_Discovery_and_Haggle.py
        ├── 3_Stage3_Authorization.py
        ├── 4_Stage4_Payment_and_Escrow.py
        ├── 5_Stage5_Dispute_Resolution.py
        └── 6_Use_Cases.py
```

---

# 💾 Database Architecture

The system uses an **ACID-compliant SQLite database** to maintain transaction and agent state.

### Core Tables

| Table         | Purpose                               |
| ------------- | ------------------------------------- |
| `users`       | Customer profiles and spending limits |
| `agents`      | Agent roles and states                |
| `merchants`   | Merchant catalogs and pricing         |
| `intents`     | Original prompts and parsed intents   |
| `bids`        | Merchant offers                       |
| `deals`       | Negotiated agreements                 |
| `orders`      | Payment and order information         |
| `splits`      | Merchant settlement routing           |
| `escrow`      | Fund holding and release status       |
| `poi_bundles` | Proof-of-Intent records               |
| `disputes`    | Complaints and refund records         |

---

# 🚀 Installation & Setup

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd razorpay-agentic-commerce
```

---

## 2. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

Or:

```bash
python -m pip install fastapi uvicorn streamlit pydantic requests python-dotenv anthropic
```

---

## 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY=your-actual-claude-api-key-here
```

> ⚠️ Never commit your `.env` file or API keys to GitHub.

If the API key is unavailable, the system falls back to its local parsing engine.

---

## 4. Handle Port Conflicts

If previous Python processes are occupying ports:

```bash
taskkill /F /IM python.exe
```

---

## 5. Start the Application

```bash
python run.py
```

The central runner starts both the backend and frontend.

---

## 6. Open the Demo

Open:

```text
http://localhost:8501
```

---

# 🔒 Security Design

Security is implemented throughout the transaction lifecycle.

### Cryptographic Protection

The following components use cryptographic signing:

* Deal Memo
* Shared Payment Token
* Proof-of-Intent Bundle

The prototype uses:

```text
HMAC-SHA256
```

for integrity verification.

### Spending Protection

Every transaction is checked against the user's predefined spending limit.

```text
Agent Request
      ↓
Policy Check
      ↓
Spend Limit
      ↓
Cryptographic Authorization
      ↓
Payment
```

---

# 🌐 Agentic Commerce Flow

```text
                 HUMAN
                   │
                   ▼
          Natural Language Intent
                   │
                   ▼
             BUYER AGENT
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
 MERCHANT AGENT A       MERCHANT AGENT B
        │                     │
        └──────────┬──────────┘
                   ▼
              NEGOTIATION
                   │
                   ▼
               DEAL MEMO
                   │
                   ▼
           POLICY VERIFICATION
                   │
                   ▼
          SHARED PAYMENT TOKEN
                   │
                   ▼
           RAZORPAY PAYMENT
                   │
          ┌────────┴────────┐
          ▼                 ▼
     MERCHANT A        MERCHANT B
          │                 │
          └────────┬────────┘
                   ▼
                 ESCROW
                   │
                   ▼
             DELIVERY CHECK
                   │
          ┌────────┴────────┐
          ▼                 ▼
       SUCCESS            MISMATCH
          │                 │
          ▼                 ▼
    RELEASE FUNDS       AUTO REFUND
```

---

# 🎯 Key Innovations

### 1. Natural Language → Payment Intent

Converts conversational instructions into structured transaction parameters.

### 2. Autonomous Negotiation

Enables Buyer and Merchant Agents to negotiate prices.

### 3. Cryptographically Bound Transactions

Links user intent, negotiated deal, and payment authorization.

### 4. Agent Spending Guardrails

Prevents agents from spending beyond predefined limits.

### 5. Multi-Merchant Settlement

Supports collaborative merchant transactions and split settlements.

### 6. Proof-of-Intent

Maintains an auditable relationship between the user's original intent and the transaction.

### 7. Autonomous Dispute Resolution

Uses transaction intent and delivery information to initiate automated resolution.

---

# 📊 Why This Architecture Matters

Traditional commerce:

```text
Human → Search → Compare → Negotiate → Checkout → Dispute
```

Razorpay TrustGate:

```text
Human
  ↓
Intent
  ↓
Buyer Agent
  ↓
Discover
  ↓
Negotiate
  ↓
Authorize
  ↓
Pay
  ↓
Verify
  ↓
Resolve
```

The goal is to move from **human-driven checkout** toward **secure, policy-controlled autonomous commerce**.

---

# ⚠️ Prototype & Demo Disclaimer

This repository is a **prototype / proof-of-concept** demonstrating an agentic payment architecture.

Razorpay payment operations such as Orders, Route/Split, Refunds, and Escrow are represented through mock/sandbox interfaces where applicable.

The architecture is designed so that the mock interfaces can be replaced with production payment APIs without changing the core multi-agent workflow.

---

# 🚀 Future Enhancements

* Production Razorpay SDK integration
* Real merchant APIs
* Advanced fraud detection
* ML-based risk scoring
* Distributed agent identity
* Real-time inventory synchronization
* Multi-agent reputation scoring
* Blockchain-backed audit trails
* Production-grade escrow infrastructure
* Advanced multilingual voice interaction

---

# 👩‍💻 Author

**Pooja K C**

AI & Data Science | Machine Learning | Agentic AI

---

# ⭐ Project Vision

> **"The future of commerce is not humans clicking buttons. It is trusted AI agents transacting securely on behalf of humans."**

**Razorpay TrustGate** aims to provide the trust, authorization, cryptographic security, and dispute mechanisms required to make that future possible.
