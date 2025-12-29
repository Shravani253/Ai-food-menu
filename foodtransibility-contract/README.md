# 🍽️ AI + Blockchain Based Food Traceability System

## 📌 Project Overview
This project implements a **Food Traceability System** using **Artificial Intelligence (AI)** and **Blockchain** technology.

The main goal is to **track the complete journey of a food product** from production to the consumer and **store this history securely on blockchain** so that it cannot be altered.

AI is used to analyze food quality, and blockchain is used to **store these AI results and supply-chain events permanently**.

---

## 🎯 Problem Statement
In today’s food supply chain:
- Food history can be altered or hidden
- Consumers do not know the true origin or quality of food
- Fake labels and adulteration are common

There is **no trusted and transparent system** to verify food data.

---

## 💡 Proposed Solution
We propose a system where:
- **AI analyzes food quality**
- **Blockchain stores food history immutably**
- **QR codes link physical food to blockchain records**

This ensures **transparency, trust, and food safety**.

---

## 🧠 Technologies Used
- **Blockchain:** Ethereum (Smart Contracts using Solidity)
- **AI:** Food quality analysis (image-based)
- **Backend:** Node.js + Web3/Ethers.js
- **Frontend:** HTML / React
- **QR Code:** To fetch food history

---

## 👥 Actors in the System
The system supports multiple verified roles:

| Role | Responsibility |
|----|----|
| Farmer | Creates food batch |
| Manufacturer | Processes food |
| Transporter | Ships food |
| Retailer | Sells food |
| AI System | Analyzes food quality |
| Owner | Registers actors & recalls food |

Only **authorized actors** can add data to the blockchain.

---

## 🔁 How the System Works (Step by Step)

### 1️⃣ Contract Deployment
- The smart contract is deployed by the **Owner**
- Owner controls actor registration and recalls

---

### 2️⃣ Actor Registration
- Owner registers each actor with:
  - Wallet address
  - Role (Farmer, AI, etc.)
  - License ID
- Only registered actors can write data

---

### 3️⃣ Batch Creation
- Farmer creates a **unique Batch ID**
- Food name and batch status are recorded
- This batch ID is used throughout the lifecycle

---

### 4️⃣ Supply Chain Updates
Each actor adds records:
- Manufacturer → Processed
- Transporter → In Transit
- Retailer → For Sale

Each update:
- Is stored permanently
- Cannot be modified or deleted

---

### 5️⃣ AI Quality Analysis
- AI analyzes food image
- Generates:
  - Quality result
  - Confidence score
  - AI model hash
- AI result is stored on blockchain

This ensures **trust in automated decisions**.

---

### 6️⃣ Blockchain Storage
Blockchain ensures:
- Immutability
- Transparency
- Auditability

Once data is written, **no one can change it**.

---

### 7️⃣ QR Code Verification
- Batch ID is converted to a QR code
- QR code is printed on food package
- Anyone can scan QR to view full food history

---

### 8️⃣ Food Recall (Emergency Case)
- Owner can recall a batch if contamination is detected
- Batch is marked as **Recalled**
- No further records can be added
- Consumers are instantly informed

---

## 🔐 Why Blockchain is Used
Without blockchain:
- Data can be edited or deleted
- No trust in food records

With blockchain:
- Data is permanent
- Fully transparent
- Tamper-proof

Blockchain guarantees **data integrity**, not food quality itself.

---

## 🧠 Role of AI in the System
AI is responsible for:
- Food quality analysis
- Generating confidence score
- Providing automated inspection

Blockchain stores **AI outputs**, ensuring they cannot be manipulated later.

---

## ⚠️ Important Note
This system:
- Ensures **data cannot be changed**
- Does **not guarantee data authenticity**
- Depends on verified actors and correct input

---

## 🎓 Project Scope
This project is developed as a **college-level prototype**.

✔ Demonstrates AI + Blockchain integration  
✔ Implements smart contracts  
✔ Shows real-world supply chain logic  

❌ Not a production or government system  

---

## 🏁 Conclusion
The AI + Blockchain Food Traceability System provides:
- Transparent food history
- Trustworthy AI analysis
- Secure and immutable records
- Better consumer confidence

This project demonstrates how emerging technologies can improve **food safety and supply chain transparency**.

---

## 📜 License
This project is licensed under the MIT License.
