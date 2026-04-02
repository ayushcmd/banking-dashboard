import streamlit as st
import pandas as pd
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="RBI News & Actions", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=DM+Sans:wght@400;500;600&display=swap');
html,body,[class*="css"],.stApp { font-family:'DM Sans',sans-serif !important; background:#653900 !important; color:#1A0A00 !important; }
#MainMenu,footer,header,[data-testid="stSidebar"],[data-testid="collapsedControl"],.stDeployButton { display:none !important; }
.main .block-container { padding:16px 24px !important; max-width:100% !important; }
.page-header { background:#1A0A00; border-radius:0px; padding:22px 28px; margin-bottom:20px; border-bottom:3px solid #C4783A; }
.page-title { font-family:'Playfair Display',serif; font-size:26px; font-weight:800; color:#FAF7F2; letter-spacing:0.5px; }
.page-sub { font-size:11px; color:#C4783A; margin-top:5px; letter-spacing:1px; text-transform:uppercase; font-weight:600; }
.news-card { background:#fff; border:1px solid #E8DDD4; border-radius:0px; padding:16px 20px; margin-bottom:12px; border-left:3px solid #1A0A00; }
.news-card.penalty { border-left-color:#8B1A1A; }
.news-card.rate { border-left-color:#1A4A1A; }
.news-card.merger { border-left-color:#3D1A5C; }
.news-card.warning { border-left-color:#C4783A; }
.news-card.positive { border-left-color:#1A4A1A; }
.news-date { font-size:9px; font-weight:700; color:#8B6347; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:4px; }
.news-title { font-family:'Playfair Display',serif; font-size:15px; font-weight:700; color:#1A0A00; margin:4px 0 6px 0; line-height:1.4; }
.news-body { font-size:12px; color:#4A3728; line-height:1.7; }
.news-tags { display:flex; gap:6px; margin-top:8px; flex-wrap:wrap; }
.tag { font-size:9px; font-weight:700; padding:2px 10px; border-radius:0px; letter-spacing:0.8px; text-transform:uppercase; border:1px solid; }
.tag-penalty { background:transparent; color:#8B1A1A; border-color:#8B1A1A; }
.tag-rate { background:transparent; color:#1A4A1A; border-color:#1A4A1A; }
.tag-merger { background:transparent; color:#3D1A5C; border-color:#3D1A5C; }
.tag-warning { background:transparent; color:#C4783A; border-color:#C4783A; }
.tag-sector { background:transparent; color:#1A0A00; border-color:#1A0A00; }
.tag-positive { background:transparent; color:#1A4A1A; border-color:#1A4A1A; }
.divider { border:none; border-top:1px solid #E8DDD4; margin:8px 0; }
button[kind="secondary"], .stButton>button { background:#1A0A00 !important; color:#FAF7F2 !important; border:none !important; border-radius:0 !important; font-size:11px !important; font-weight:600 !important; letter-spacing:0.5px !important; }
[data-testid="stSelectbox"]>div>div { border-radius:0 !important; border-color:#C4A882 !important; background:#fff !important; }
::-webkit-scrollbar { display:none; }
</style>
""", unsafe_allow_html=True)

if st.button("Back to Dashboard"):
    st.switch_page("app.py")

st.markdown("""
<div class="page-header">
  <div class="page-title">RBI News & Regulatory Actions</div>
  <div class="page-sub">Circulars · Penalties · Rate Changes · Policy Actions · FY2023–2024</div>
</div>
""", unsafe_allow_html=True)

NEWS = [
    {"date": "Feb 2024", "bank": "Paytm Payments Bank", "type": "penalty", "title": "RBI Bans Paytm Payments Bank from Accepting New Deposits",
     "body": "RBI directed Paytm Payments Bank to stop accepting new customers and deposits from Feb 29, 2024, citing persistent non-compliance with KYC norms and supervisory concerns.",
     "tags": [("Penalty", "tag-penalty"), ("Compliance", "tag-warning")]},
    {"date": "Jan 2024", "bank": "All Banks", "type": "rate", "title": "RBI Keeps Repo Rate Unchanged at 6.5% — 6th Consecutive Hold",
     "body": "MPC unanimously held the benchmark repo rate at 6.5% focusing on withdrawal of accommodation to ensure inflation alignment. All bank lending and deposit rates remain broadly stable.",
     "tags": [("Rate Policy", "tag-rate"), ("Sector", "tag-sector")]},
    {"date": "Dec 2023", "bank": "HDFC Bank", "type": "penalty", "title": "HDFC Bank Fined Rs. 1 Crore for Non-Compliance",
     "body": "RBI imposed a Rs. 1 crore penalty on HDFC Bank for non-compliance with certain provisions relating to interest rate on deposits and FEMA regulations.",
     "tags": [("Penalty", "tag-penalty"), ("HDFC Bank", "tag-sector")]},
    {"date": "Oct 2023", "bank": "SBI", "type": "positive", "title": "SBI Gets RBI Nod for Rs. 20,000 Crore Capital Raise",
     "body": "State Bank of India received RBI approval to raise up to Rs. 20,000 Crore through long-term bonds and tier-2 capital to strengthen its capital adequacy ahead of Basel III norms.",
     "tags": [("Positive", "tag-positive"), ("SBI", "tag-sector"), ("Capital", "tag-rate")]},
    {"date": "Sep 2023", "bank": "Axis Bank", "type": "penalty", "title": "Axis Bank Penalised Rs. 90.92 Lakh",
     "body": "RBI levied a penalty of Rs. 90.92 lakh on Axis Bank for non-compliance with directions on customer service and transfer of unclaimed amounts to the Depositor Education and Awareness Fund.",
     "tags": [("Penalty", "tag-penalty"), ("Axis Bank", "tag-sector")]},
    {"date": "Aug 2023", "bank": "Bank of Baroda", "type": "warning", "title": "RBI Lifts Restrictions on Bank of Baroda BoB World App",
     "body": "RBI lifted restrictions imposed on Bank of Baroda's mobile app after the bank demonstrated compliance with data privacy and KYC norms. New user onboarding resumed.",
     "tags": [("Warning Lifted", "tag-positive"), ("Bank of Baroda", "tag-sector"), ("Digital", "tag-sector")]},
    {"date": "Jul 2023", "bank": "ICICI Bank", "type": "positive", "title": "ICICI Bank Credit Card Portfolio Cleared by RBI",
     "body": "After lifting earlier restrictions on credit card issuances, ICICI Bank's credit card portfolio grew 35% YoY, with RBI monitoring regulatory compliance closely.",
     "tags": [("Positive", "tag-positive"), ("ICICI Bank", "tag-sector")]},
    {"date": "Jun 2023", "bank": "All Banks", "type": "rate", "title": "RBI Raises Risk Weights on Consumer Credit to 125%",
     "body": "RBI increased risk weights on consumer credit and credit card receivables from 100% to 125%, tightening capital requirements for banks to cool unsecured lending boom.",
     "tags": [("Rate Policy", "tag-rate"), ("Sector", "tag-sector"), ("Risk Management", "tag-warning")]},
    {"date": "May 2023", "bank": "PNB", "type": "positive", "title": "PNB NPA Falls Below 5% — First Time in 7 Years",
     "body": "Punjab National Bank reported Gross NPA ratio below 5% for the first time since 2016, reflecting successful resolution under IBC and improved credit monitoring systems.",
     "tags": [("Positive", "tag-positive"), ("PNB", "tag-sector"), ("NPA Recovery", "tag-rate")]},
    {"date": "Apr 2023", "bank": "IndusInd Bank", "type": "positive", "title": "IndusInd Bank Gets RBI Approval for MFI Acquisition",
     "body": "RBI granted in-principle approval for IndusInd Bank's merger with Bharat Financial Inclusion, expanding its microfinance reach to 35 million borrowers.",
     "tags": [("Merger", "tag-merger"), ("IndusInd Bank", "tag-sector")]},
    {"date": "Mar 2023", "bank": "Kotak Mahindra", "type": "positive", "title": "Kotak Mahindra Wins Digital Banking License",
     "body": "Kotak Mahindra Bank received RBI nod to launch expanded digital-only banking services under the DIGI-bank framework, allowing paperless account opening with video KYC.",
     "tags": [("Positive", "tag-positive"), ("Kotak Mahindra", "tag-sector"), ("Digital", "tag-sector")]},
    {"date": "Feb 2023", "bank": "Central Bank", "type": "warning", "title": "Central Bank of India Placed Under PCA Framework",
     "body": "RBI placed Central Bank of India under Prompt Corrective Action (PCA) framework citing elevated NPA levels and insufficient capital buffers. Lending restrictions imposed.",
     "tags": [("Warning", "tag-warning"), ("Central Bank", "tag-sector"), ("PCA", "tag-penalty")]},
    {"date": "Dec 2022", "bank": "All Banks", "type": "rate", "title": "RBI Hikes Repo Rate by 35 bps to 6.25%",
     "body": "In its fight against post-pandemic inflation, RBI raised the repo rate by 35 basis points to 6.25%. All banks subsequently revised their MCLR and FD/lending rates upward.",
     "tags": [("Rate Hike", "tag-rate"), ("Sector", "tag-sector"), ("Inflation", "tag-warning")]},
    {"date": "Nov 2022", "bank": "Indian Overseas", "type": "positive", "title": "RBI Removes Indian Overseas Bank from PCA Framework",
     "body": "RBI took Indian Overseas Bank out of the Prompt Corrective Action framework after the bank demonstrated sustained improvement in NPA ratios and capital adequacy.",
     "tags": [("Positive", "tag-positive"), ("Indian Overseas", "tag-sector"), ("PCA Exit", "tag-rate")]},
]

banks_in_news = ["All Banks"] + sorted(set(n["bank"] for n in NEWS if n["bank"] != "All Banks" and n["bank"] != "Paytm Payments Bank"))
f1, f2, _ = st.columns([1.5, 2, 2])
with f1:
    bank_filter = st.selectbox("Filter by Bank", ["All"] + banks_in_news, label_visibility="collapsed")
with f2:
    type_filter = st.radio("News Type", ["All", "Penalty", "Rate Change", "Positive", "Warning"],
                           horizontal=True, label_visibility="collapsed")

type_map = {"All": None, "Penalty": "penalty", "Rate Change": "rate", "Positive": "positive", "Warning": "warning"}
t_filter = type_map[type_filter]

filtered = NEWS
if bank_filter != "All":
    filtered = [n for n in filtered if n["bank"] == bank_filter or n["bank"] == "All Banks"]
if t_filter:
    filtered = [n for n in filtered if n["type"] == t_filter]

col_ai, _ = st.columns([1, 4])
with col_ai:
    ai_btn = st.button("Generate Sector Analysis", use_container_width=True)

if ai_btn:
    with st.spinner("Generating analysis..."):
        try:
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            headlines = "\n".join([f"- {n['date']}: {n['title']}" for n in NEWS[:8]])
            prompt = f"""You are an RBI banking sector analyst. Based on these recent RBI actions and news headlines:

{headlines}

Give a 4-bullet sharp sector outlook:
- What is RBI's current regulatory stance?
- Which banks are under pressure and why?
- What does this mean for depositors?
- What should investors watch in the next 6 months?

Each bullet max 20 words. Start each with a dash."""
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300, temperature=0.4
            )
            summary = resp.choices[0].message.content.strip()
            st.markdown(f"""
            <div style="background:#fff;border:1px solid #8D5E37;border-left:3px solid #C4783A;padding:16px 20px;margin-bottom:14px;">
              <div style="font-size:9px;font-weight:700;color:#8B6347;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px;">Sector Outlook — AI Analysis</div>
              <div style="font-size:12px;color:#2C1810;line-height:1.9;">{summary.replace(chr(10), '<br>')}</div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Analysis unavailable — {e}")

st.markdown(f"<div style='font-size:10px;color:#8B6347;margin:8px 0;letter-spacing:0.5px;'>{len(filtered)} items</div>", unsafe_allow_html=True)
st.markdown("<hr class='divider'>", unsafe_allow_html=True)

if not filtered:
    st.info("No news items match your filters.")
else:
    for n in filtered:
        type_class = n["type"]
        tags_html = "".join([f'<span class="tag {tc}">{tl}</span>' for tl, tc in n["tags"]])
        st.markdown(f"""
        <div class="news-card {type_class}">
          <div class="news-date">{n['date']} &nbsp;&middot;&nbsp; {n['bank']}</div>
          <div class="news-title">{n['title']}</div>
          <div class="news-body">{n['body']}</div>
          <div class="news-tags">{tags_html}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div style="background:#1A0A00;padding:10px 16px;margin-top:12px;">
  <div style="font-size:10px;color:#C4A882;letter-spacing:0.5px;">Source: RBI press releases and public filings. For current actions visit rbi.org.in/press</div>
</div>
""", unsafe_allow_html=True)