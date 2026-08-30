# 🤖 Razorpay TrustGate

### An NPCI UAP-Compliant Agentic Trust Gateway & Cryptographic M2M Settlement Protocol

## 📌 About the Project

**Razorpay TrustGate** is an AI-powered agentic payment gateway that enables AI agents to perform secure and autonomous purchasing on behalf of users.

The system converts natural-language instructions into structured purchase intents, discovers merchant offers, negotiates prices, verifies spending limits, executes payments, and handles disputes automatically.

The project demonstrates a **5-stage agentic commerce workflow**:

```text
Instruct & Bind
      ↓
Discovery & Haggle
      ↓
Authorization
      ↓
Payment & Escrow
      ↓
Dispute Resolution
```

---

## ✨ Key Features

* 🧠 Natural-language purchase instructions
* 🤖 AI-based intent extraction
* 🏪 Multi-merchant discovery
* 🤝 Agent-to-agent price negotiation
* 🔐 Spending-limit protection
* 🔑 WebAuthn/Passkey verification
* 🛡️ HMAC-SHA256 transaction signing
* 💳 Razorpay payment simulation
* 💰 Split settlement simulation
* 🔒 Escrow workflow
* 📜 Proof-of-Intent (PoI)
* 🔄 Automated dispute resolution
* 💸 Automated refund simulation
* 🗄️ SQLite transaction database

---

## 🛠️ Technology Stack

### Backend

* Python
* FastAPI
* Pydantic
* SQLite

### Frontend

* Streamlit

### AI

* Claude 3.5 Sonnet
* Natural Language Processing
* Agentic workflows
* Local fallback parser

### Security

* HMAC-SHA256
* WebAuthn Passkeys
* Spend-limit validation
* Signed payment tokens

### Payment

* Razorpay Test/Mock APIs
* Orders
* Refunds
* Route/Split
* Escrow simulation

---

## 📂 Project Structure

```text
razorpay-agentic-commerce/
│
├── run.py
├── requirements.txt
│
├── backend/
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
    └── pages/
        ├── 1_Stage1_Instruct_and_Bind.py
        ├── 2_Stage2_Discovery_and_Haggle.py
        ├── 3_Stage3_Authorization.py
        ├── 4_Stage4_Payment_and_Escrow.py
        ├── 5_Stage5_Dispute_Resolution.py
        └── 6_Use_Cases.py
```

---

## 🚀 How to Run

### 1. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY=your-api-key
```

The application can also use the local fallback parser if the API key is unavailable.

### 3. Start the Application

```bash
python run.py
```

### 4. Open the Application

Open your browser and visit:

```text
http://localhost:8501
```

---

## 🔄 Basic Workflow

```text
User
 ↓
Natural Language Instruction
 ↓
AI Intent Parser
 ↓
Buyer Agent
 ↓
Merchant Discovery
 ↓
Price Negotiation
 ↓
Authorization & Spend Check
 ↓
Payment
 ↓
Escrow
 ↓
Delivery Verification
 ↓
Refund / Settlement
```

---

## 🔐 Security

The project uses cryptographic signing to protect important transaction information.

Key security mechanisms include:

* HMAC-SHA256 signatures
* Spending-limit validation
* Time-limited payment authorization
* WebAuthn Passkey verification
* Proof-of-Intent records

---

## ⚠️ Note

This project is a **prototype / proof of concept** for demonstrating an agentic commerce and payment architecture.

Razorpay payment, split settlement, and refund functionality are implemented using mock/test interfaces where applicable.

---

## 👩‍💻 Author

**Pooja K C**

AI & Data Science | Machine Learning | Agentic AI
