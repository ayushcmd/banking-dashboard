import streamlit as st
import pandas as pd
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Bank Advisor", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=DM+Sans:wght@400;500;600&display=swap');
html,body,[class*="css"],.stApp { font-family:'DM Sans',sans-serif !important; background:#653900 !important; color:#1A0A00 !important; }
#MainMenu,footer,header,[data-testid="stSidebar"],[data-testid="collapsedControl"],.stDeployButton { display:none !important; }
.main .block-container { padding:16px 24px !important; max-width:100% !important; }
.page-header { background:#1A0A00; padding:22px 28px; margin-bottom:20px; border-bottom:3px solid #C4783A; }
.page-title { font-family:'Playfair Display',serif; font-size:26px; font-weight:800; color:#FAF7F2; }
.page-sub { font-size:10px; color:#C4783A; margin-top:5px; letter-spacing:1.5px; text-transform:uppercase; font-weight:600; }
.advice-box { background:#fff; border:1px solid #E8DDD4; border-left:3px solid #C4783A; padding:20px 24px; margin-top:12px; }
.advice-title { font-size:9px; font-weight:700; color:#8B6347; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:10px; }
.advice-text { font-size:13px; color:#2C1810; line-height:1.9; }
.profile-card { background:#fff; border:1px solid #E8DDD4; border-top:3px solid #1A0A00; padding:14px 16px; margin-bottom:10px; }
.profile-lbl { font-size:9px; font-weight:700; color:#8B6347; letter-spacing:1px; text-transform:uppercase; margin-bottom:4px; }
button[kind="secondary"], .stButton>button { background:#1A0A00 !important; color:#FAF7F2 !important; border:none !important; border-radius:0 !important; font-size:11px !important; font-weight:600 !important; }
[data-testid="stSelectbox"]>div>div { border-radius:0 !important; border-color:#C4A882 !important; }
[data-testid="stSelectbox"] label, [data-testid="stRadio"] label, [data-testid="stMultiSelect"] label { display:none !important; }
section-label { font-size:10px; font-weight:700; color:#8B6347; letter-spacing:1px; text-transform:uppercase; }
::-webkit-scrollbar { display:none; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("data/indian_banks_kpi_ratios.csv")

kpi = load_data()

BANK_PROFILES = {
    "SBI":              {"type": "Public", "best_for": "Government employees, rural banking, home loans", "fd_rate": 6.50, "home_loan": 8.40, "npa_2024": 2.24},
    "HDFC Bank":        {"type": "Private", "best_for": "Premium banking, credit cards, NRI accounts", "fd_rate": 7.10, "home_loan": 8.35, "npa_2024": 1.26},
    "ICICI Bank":       {"type": "Private", "best_for": "Digital banking, mutual funds, investments", "fd_rate": 7.00, "home_loan": 8.35, "npa_2024": 2.16},
    "Axis Bank":        {"type": "Private", "best_for": "Personal loans, youth banking, international", "fd_rate": 7.10, "home_loan": 8.75, "npa_2024": 1.58},
    "Kotak Mahindra":   {"type": "Private", "best_for": "High-yield savings, digital-first, wealth mgmt", "fd_rate": 7.25, "home_loan": 8.70, "npa_2024": 1.73},
    "PNB":              {"type": "Public", "best_for": "Pensioners, small business, farm loans", "fd_rate": 6.50, "home_loan": 8.40, "npa_2024": 4.09},
    "Bank of Baroda":   {"type": "Public", "best_for": "Forex, international trade, farm loans", "fd_rate": 6.85, "home_loan": 8.40, "npa_2024": 3.51},
    "Central Bank":     {"type": "Public", "best_for": "Priority sector, MSME, agricultural loans", "fd_rate": 6.25, "home_loan": 8.45, "npa_2024": 4.50},
    "Indian Overseas":  {"type": "Public", "best_for": "South India, NRI remittances, agriculture", "fd_rate": 6.50, "home_loan": 8.40, "npa_2024": 3.90},
    "IndusInd Bank":    {"type": "Private", "best_for": "Auto loans, microfinance, affluent retail", "fd_rate": 7.25, "home_loan": 8.80, "npa_2024": 2.25},
}

if st.button("Back to Dashboard"):
    st.switch_page("app.py")

st.markdown("""
<div class="page-header">
  <div class="page-title">Bank Advisor — Should I Switch?</div>
  <div class="page-sub">Personalised Recommendation &nbsp;&middot;&nbsp; Powered by Groq Llama 3.3</div>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1.2, 2])

with left:
    st.markdown('<p style="font-size:10px;font-weight:700;color:#8B6347;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;">Your Profile</p>', unsafe_allow_html=True)
    current_bank = st.selectbox("Current Bank", list(BANK_PROFILES.keys()))
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    primary_need = st.selectbox("Primary Banking Need",
        ["Home Loan", "Fixed Deposit", "Personal Loan", "Car Loan",
         "Savings Account", "Wealth Management", "International Banking", "Business/MSME Loans"])
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    profile_type = st.radio("I am a",
        ["Salaried Employee", "Self-Employed / Business", "Student", "Senior Citizen", "NRI", "Government Employee"],
        label_visibility="collapsed")
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    priorities = st.multiselect("What matters most to you?",
        ["Low Interest Rates", "High FD Returns", "Digital Experience", "Branch Network",
         "Customer Service", "Low Charges", "Asset Safety", "Quick Loan Approval"],
        default=["Low Interest Rates", "Asset Safety"],
        label_visibility="collapsed")
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    monthly_income = st.selectbox("Monthly Income Range",
        ["Below Rs.25,000", "Rs.25,000-Rs.50,000", "Rs.50,000-Rs.1L", "Rs.1L-Rs.3L", "Above Rs.3L"])
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    risk_tol = st.radio("Risk Tolerance", ["Conservative", "Moderate", "Aggressive"], horizontal=True, label_visibility="collapsed")
    analyse = st.button("Get Recommendation", use_container_width=True, type="primary")

with right:
    cb = BANK_PROFILES[current_bank]
    latest_kpi = kpi[(kpi["Bank"] == current_bank) & (kpi["Year"] == 2024)]
    if len(latest_kpi) == 0:
        latest_kpi = kpi[(kpi["Bank"] == current_bank)].sort_values("Year").iloc[-1:]

    npa_color = '#1A4A1A' if cb['npa_2024'] < 2.5 else '#C4783A' if cb['npa_2024'] < 4 else '#8B1A1A'
    st.markdown(f"""
    <div class="profile-card">
      <div class="profile-lbl">Current Bank</div>
      <div style="font-family:'Playfair Display',serif;font-size:20px;font-weight:700;color:#1A0A00;margin-bottom:8px;">{current_bank}</div>
      <div style="display:flex;gap:20px;flex-wrap:wrap;font-size:12px;color:#2C1810;">
        <span>Type: <strong>{cb['type']}</strong></span>
        <span>NPA FY24: <strong style="color:{npa_color}">{cb['npa_2024']:.2f}%</strong></span>
        <span>FD Rate: <strong>{cb['fd_rate']:.2f}%</strong></span>
        <span>Home Loan: <strong>{cb['home_loan']:.2f}%</strong></span>
      </div>
      <div style="margin-top:8px;font-size:11px;color:#8B6347;border-top:1px solid #E8DDD4;padding-top:8px;">Best for: {cb['best_for']}</div>
    </div>
    """, unsafe_allow_html=True)

    if analyse:
        all_bank_data = []
        for bname, bdata in BANK_PROFILES.items():
            all_bank_data.append(f"- {bname} ({bdata['type']}): FD {bdata['fd_rate']}%, Home Loan {bdata['home_loan']}%, NPA {bdata['npa_2024']}%, Best for: {bdata['best_for']}")

        prompt = f"""You are a senior Indian personal finance advisor with deep knowledge of Indian banking.

Customer Profile:
- Current bank: {current_bank} ({cb['type']})
- Primary need: {primary_need}
- Profile type: {profile_type}
- Priorities: {', '.join(priorities) if priorities else 'Not specified'}
- Monthly income: {monthly_income}
- Risk tolerance: {risk_tol}

All 10 Bank Comparison Data (FY2024):
{chr(10).join(all_bank_data)}

Give a detailed, personalised 5-point recommendation:
1. Should they STAY or SWITCH? (direct answer with reason)
2. If switch — which bank and why (cite specific rates/metrics)
3. What they gain by switching (quantify if possible)
4. Any risks or watch-outs
5. One actionable step to take this week

Be specific, data-driven, and use real numbers. Format with clear numbered points."""

        with st.spinner("Analysing your profile against all 10 banks..."):
            try:
                client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500, temperature=0.5
                )
                advice = response.choices[0].message.content.strip()
                st.markdown(f"""
                <div class="advice-box">
                  <div class="advice-title">Personalised Recommendation — {current_bank} / {primary_need}</div>
                  <div class="advice-text">{advice.replace(chr(10), '<br>')}</div>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Analysis unavailable — check GROQ_API_KEY in .env · {e}")
                recs = []
                if primary_need == "Home Loan":
                    best = min(BANK_PROFILES.items(), key=lambda x: x[1]["home_loan"])
                    recs.append(f"Best home loan rate: {best[0]} at {best[1]['home_loan']:.2f}%")
                elif primary_need == "Fixed Deposit":
                    best = max(BANK_PROFILES.items(), key=lambda x: x[1]["fd_rate"])
                    recs.append(f"Best FD rate: {best[0]} at {best[1]['fd_rate']:.2f}%")
                if cb["npa_2024"] > 3.5 and risk_tol == "Conservative":
                    recs.append(f"{current_bank} NPA of {cb['npa_2024']}% is elevated — consider private banks for safety")
                recs.append(f"Your profile ({profile_type}, {risk_tol}) suggests {'private' if risk_tol != 'Conservative' else 'nationalised'} banks")
                st.markdown(f"""
                <div class="advice-box">
                  <div class="advice-title">Quick Analysis</div>
                  <div class="advice-text">{'<br>'.join(recs)}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#fff;border:1px solid #E8DDD4;border-top:3px solid #1A0A00;padding:28px;text-align:center;margin-top:8px;">
          <div style="font-family:'Playfair Display',serif;font-size:18px;font-weight:700;color:#1A0A00;margin-bottom:8px;">Your Bank Advisor</div>
          <div style="font-size:12px;color:#8B6347;line-height:1.8;">Fill in your profile and click Get Recommendation<br>to receive a personalised analysis across all 10 banks.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    st.markdown('<p style="font-size:9px;font-weight:700;color:#8B6347;letter-spacing:1px;text-transform:uppercase;">Bank Comparison</p>', unsafe_allow_html=True)
    cdf = pd.DataFrame([
        {"Bank": k, "Type": v["type"], "FD Rate": f"{v['fd_rate']:.2f}%",
         "Home Loan": f"{v['home_loan']:.2f}%", "NPA FY24": f"{v['npa_2024']:.2f}%"}
        for k, v in BANK_PROFILES.items()
    ])
    st.dataframe(cdf.set_index("Bank"), use_container_width=True, height=260)