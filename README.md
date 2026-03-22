# <img src="rbi.png" width="40" style="border-radius:50%"/> India's Banking Dashboard

<div align="center">

![Dashboard Preview](dashboard.png)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://india-banking-dashboard.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-orange?logo=plotly)
![Streamlit](https://img.shields.io/badge/Streamlit-1.55-red?logo=streamlit)


**A comprehensive financial analytics dashboard comparing 10 Indian banks across FY 2020–2024**

[🚀 Live Demo](https://india-banking-dashboard.streamlit.app) · [📊 Data Sources](#data-sources) · [🛠️ Tech Stack](#tech-stack)

</div>

---

## 📌 Overview

India's Banking Dashboard is a data analytics project built to visualize and compare the financial performance of **10 major Indian banks** — both public and private — across **5 fiscal years (FY 2020–2024)**.

It tells the story of **India's banking sector recovery** — bad loans falling, profits rising, and the gap between public and private sector banks.

---

## 🏛️ Banks Covered

| Public Sector | Private Sector |
|---|---|
| State Bank of India (SBI) | HDFC Bank |
| Punjab National Bank (PNB) | ICICI Bank |
| Bank of Baroda (BoB) | Axis Bank |
| UCO Bank | Kotak Mahindra Bank |
| Central Bank of India (CBI) | |
| Indian Overseas Bank (IOB) | |

---

## 📊 Key Metrics & Visualizations

### Page 1 — Overview Dashboard
- **5 KPI Cards** — Total Assets, Best Net Profit, Lowest NPA, Best ROE, Avg CAR
- **Net Profit by Bank** — Horizontal bar chart with Public/Private color coding
- **Asset Share** — Donut chart (Public vs Private)
- **Gross NPA %** — Conditional color bars (Green < 2% / Amber < 3.5% / Red > 3.5%)
- **ROA vs ROE Scatter** — Bubble size = Total Assets

### Trend Analysis
- NPA Recovery 2020–2024 — All 10 banks line chart
- Net Profit Growth — Top 4 banks area chart

### Features
- 🎛️ **Interactive Filters** — Year selector + Bank Type (All/Public/Private)
- 🤖 **AI Sector Insight** — Groq LLaMA powered analysis
- 📄 **PDF Export** — Download bank-wise report
- 🔍 **Bank Deep Dive** — Individual bank performance page

---

## 📖 Key Data Stories

```
📉 NPA Recovery    → All banks reduced bad loans from 2020 to 2024
💰 SBI 4x Growth   → Profit grew from ₹14,488 Cr to ₹61,077 Cr
🏆 ICICI Turnaround → NPA fell from 5.53% to 2.16%
🐘 SBI Dominance   → Larger than all 3 private banks combined
🌱 Small Bank Recovery → UCO, CBI, IOB recovering from RBI's PCA
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit, Custom CSS |
| **Charts** | Plotly Express, Plotly Graph Objects |
| **Data** | Pandas, CSV (RBI Annual Reports) |
| **AI Insights** | Groq API (LLaMA 3.3 70B) |
| **PDF Export** | fpdf2 |
| **Deployment** | Streamlit Cloud |

---

## 📂 Data Sources

- **RBI Annual Reports** — Reserve Bank of India
- **BSE Filings** — Bombay Stock Exchange
- **Fiscal Years** — FY 2020 to FY 2024

> ⚠️ Data is curated from public sources for educational/portfolio purposes.

---

## 🎨 Design

- **Color Palette** — Cream (`#FDF6EC`) + Brown (`#4A2309`) + Pink (`#F4A7B9`)
- **Typography** — Playfair Display (headers) + Outfit (body)
- **Background** — Animated ₹ particle effect
- **Theme** — Warm, premium, RBI-inspired

---

## 👨‍💻 Author

**Ayush Raj**
BSc CSDA (Computer Science & Data Analytics)
IIT Patna | CPI 8.7

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://linkedin.com/in/ayush08iitp)
[![GitHub](https://img.shields.io/badge/GitHub-ayushcmd-black?logo=github)](https://github.com/ayushcmd)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-green)](https://ayushcmd.github.io/portfolio-website)

---

<div align="center">

**⭐ Star this repo if you found it useful!**



</div>
