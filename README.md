# 📊 NIFTY 50 Real-Time Contribution Dashboard

A real-time **NIFTY 50 contribution analysis dashboard** built using **Angel One SmartAPI**, **Python Flask backend**, and a **JavaScript frontend**.

This project shows **which stocks are pulling or dragging NIFTY 50 in real time**, something most platforms do not clearly provide.

---

## ❓ Problem Statement

Most trading platforms show:
- NIFTY index price
- Candles and indicators

But they **do NOT clearly show**:
- Which individual stocks are **pulling** NIFTY up
- Which stocks are **dragging** it down
- The **net contribution pressure** on the index

Because of this, traders often understand the trend **only after candles are formed**.

---

## ✅ Solution

This project builds a **real-time contribution engine** using:

- Stock **weightage**
- **Previous Close**
- **Live LTP (Last Traded Price)**

Each stock’s impact is calculated and classified as:
- 📈 **Puller** (Positive contribution)
- 📉 **Dragger** (Negative contribution)

The dashboard displays:
- Pullers
- Draggers
- **NetDiff = Pullers − Draggers**

This helps identify **index strength and pressure BEFORE candle confirmation**.

---

## 🧠 Contribution Logic

For each NIFTY 50 stock:
---------------------------------------------------------------------------------------------------------------------------
"Contribution = (LTP − Previous Close) × Weightage"
  
### Classification:
- Contribution > 0 → Puller
- Contribution < 0 → Dragger

### Aggregation:
- Total Pullers
- Total Draggers
- Net Difference (Market Pressure)

---

## 📊 Dashboard Preview
<img width="1777" height="926" alt="image" src="https://github.com/user-attachments/assets/7a942853-44eb-41c2-b34f-c153741e429a" />
<img width="1777" height="858" alt="image" src="https://github.com/user-attachments/assets/ac21d5f4-ddaf-45b8-9824-03b4778aa880" />
<img width="1777" height="915" alt="image" src="https://github.com/user-attachments/assets/8296955c-d609-43b5-af0f-27d2c6909c6f" />



Tech Stack
Backend
Python
Flask
Angel One SmartAPI
WebSocket (Real-time LTP)

Frontend
HTML
CSS
JavaScript



----------------------------------------------------------------------------
HOW TO RUN THIS PROJECT  


step :1
clone the repo

step 2:
Install Dependencies
pip install -r backend/requirements.txt

step 3:
Create .env file 

API_KEY=your_api_key_here
CLIENT_CODE=your_client_code_here
PASSWORD=your_password_here
TOTP_SECRET=your_totp_secret_here


run the project 
