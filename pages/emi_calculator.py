import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import math

st.set_page_config(page_title="EMI Calculator", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=DM+Sans:wght@400;500;600&display=swap');
html,body,[class*="css"],.stApp { font-family:'DM Sans',sans-serif !important; background:#653900 !important; color:#1A0A00 !important; }
#MainMenu,footer,header,[data-testid="stSidebar"],[data-testid="collapsedControl"],.stDeployButton { display:none !important; }
.main .block-container { padding:16px 24px !important; max-width:100% !important; }
.page-header { background:#1A0A00; padding:22px 28px; margin-bottom:20px; border-bottom:3px solid #C4783A; }
.page-title { font-family:'Playfair Display',serif; font-size:26px; font-weight:800; color:#FAF7F2; }
.page-sub { font-size:10px; color:#C4783A; margin-top:5px; letter-spacing:1.5px; text-transform:uppercase; font-weight:600; }
.emi-card { background:#fff; border:1px solid #E8DDD4; border-top:3px solid #1A0A00; padding:14px 18px; }
.emi-card.best { border-top-color:#1A4A1A; }
.emi-card.worst { border-top-color:#8B1A1A; }
.emi-card.savings { border-top-color:#C4783A; }
.emi-lbl { font-size:9px; font-weight:700; color:#8B6347; letter-spacing:1px; text-transform:uppercase; margin-bottom:4px; }
.emi-val { font-family:'Playfair Display',serif; font-size:26px; font-weight:700; color:#1A0A00; }
.emi-sub { font-size:10px; color:#8B6347; margin-top:3px; }
button[kind="secondary"], .stButton>button { background:#1A0A00 !important; color:#FAF7F2 !important; border:none !important; border-radius:0 !important; font-size:11px !important; font-weight:600 !important; }
[data-testid="stSelectbox"]>div>div { border-radius:0 !important; border-color:#C4A882 !important; }
::-webkit-scrollbar { display:none; }
</style>
""", unsafe_allow_html=True)

if st.button("Back to Dashboard"):
    st.switch_page("app.py")

st.markdown("""
<div class="page-header">
  <div class="page-title">EMI Calculator — Compare All Banks</div>
  <div class="page-sub">Monthly EMI &amp; Total Interest Across 10 Banks Simultaneously</div>
</div>
""", unsafe_allow_html=True)

LOAN_RATES = {
    "SBI":              {"Home Loan": 8.40, "Personal Loan": 12.00, "Car Loan": 8.70, "Education Loan": 8.50},
    "HDFC Bank":        {"Home Loan": 8.35, "Personal Loan": 10.50, "Car Loan": 8.50, "Education Loan": 9.00},
    "ICICI Bank":       {"Home Loan": 8.35, "Personal Loan": 10.65, "Car Loan": 8.65, "Education Loan": 9.20},
    "Axis Bank":        {"Home Loan": 8.75, "Personal Loan": 10.25, "Car Loan": 8.70, "Education Loan": 9.40},
    "Kotak Mahindra":   {"Home Loan": 8.70, "Personal Loan": 10.99, "Car Loan": 8.80, "Education Loan": 9.50},
    "PNB":              {"Home Loan": 8.40, "Personal Loan": 11.40, "Car Loan": 8.75, "Education Loan": 8.55},
    "Bank of Baroda":   {"Home Loan": 8.40, "Personal Loan": 11.40, "Car Loan": 8.60, "Education Loan": 8.85},
    "Central Bank":     {"Home Loan": 8.45, "Personal Loan": 11.50, "Car Loan": 8.90, "Education Loan": 8.70},
    "Indian Overseas":  {"Home Loan": 8.40, "Personal Loan": 11.30, "Car Loan": 8.85, "Education Loan": 8.60},
    "IndusInd Bank":    {"Home Loan": 8.80, "Personal Loan": 10.49, "Car Loan": 8.70, "Education Loan": 9.30},
}

def calc_emi(principal, annual_rate, tenure_months):
    r = annual_rate / 12 / 100
    if r == 0:
        return principal / tenure_months
    emi = principal * r * (1 + r)**tenure_months / ((1 + r)**tenure_months - 1)
    return round(emi, 2)

c1, c2, c3, c4 = st.columns([2, 1.5, 1.5, 1])
with c1:
    loan_type = st.selectbox("Loan Type", ["Home Loan", "Personal Loan", "Car Loan", "Education Loan"])
with c2:
    amount_lakh = st.number_input("Loan Amount (Rs. Lakh)", min_value=1.0, max_value=5000.0, value=50.0, step=1.0)
with c3:
    tenure_yr = st.number_input("Tenure (Years)", min_value=1, max_value=30, value=20 if loan_type == "Home Loan" else 5)
with c4:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    calc = st.button("Compare", use_container_width=True, type="primary")

principal = amount_lakh * 100000
tenure_months = tenure_yr * 12

results = []
for bank, rates in LOAN_RATES.items():
    rate = rates[loan_type]
    emi = calc_emi(principal, rate, tenure_months)
    total_pay = emi * tenure_months
    total_int = total_pay - principal
    results.append({"Bank": bank, "Rate (%)": rate, "Monthly EMI (Rs.)": emi,
                    "Total Interest (Rs.)": total_int, "Total Payment (Rs.)": total_pay})

res_df = pd.DataFrame(results).sort_values("Monthly EMI (Rs.)")
best = res_df.iloc[0]
worst = res_df.iloc[-1]
savings = worst["Monthly EMI (Rs.)"] - best["Monthly EMI (Rs.)"]
total_savings = worst["Total Interest (Rs.)"] - best["Total Interest (Rs.)"]

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f'<div class="emi-card best"><div class="emi-lbl">Cheapest EMI</div><div class="emi-val">Rs.{best["Monthly EMI (Rs.)"]:,.0f}</div><div class="emi-sub">{best["Bank"]} at {best["Rate (%)"]:.2f}%</div></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="emi-card worst"><div class="emi-lbl">Costliest EMI</div><div class="emi-val">Rs.{worst["Monthly EMI (Rs.)"]:,.0f}</div><div class="emi-sub">{worst["Bank"]} at {worst["Rate (%)"]:.2f}%</div></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="emi-card savings"><div class="emi-lbl">Monthly Savings</div><div class="emi-val">Rs.{savings:,.0f}</div><div class="emi-sub">Best vs worst</div></div>', unsafe_allow_html=True)
with k4:
    st.markdown(f'<div class="emi-card savings"><div class="emi-lbl">Total Interest Saved</div><div class="emi-val">Rs.{total_savings/100000:,.1f}L</div><div class="emi-sub">Over {tenure_yr} years</div></div>', unsafe_allow_html=True)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
ch1, ch2 = st.columns(2)

DARK = "#1A0A00"; ACCENT = "#C4783A"; RED = "#8B1A1A"; GREEN = "#1A4A1A"

with ch1:
    st.markdown('<p style="font-size:9px;font-weight:700;color:#8B6347;letter-spacing:1px;text-transform:uppercase;">Monthly EMI Comparison</p>', unsafe_allow_html=True)
    bar_colors = [GREEN if i == 0 else RED if i == len(res_df)-1 else DARK for i in range(len(res_df))]
    fig1 = go.Figure(go.Bar(
        x=res_df["Bank"], y=res_df["Monthly EMI (Rs.)"],
        marker_color=bar_colors, marker_line_width=0,
        text=[f"Rs.{v:,.0f}" for v in res_df["Monthly EMI (Rs.)"]],
        textposition="outside", textfont=dict(size=8)
    ))
    fig1.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FAF7F2",
        font=dict(family="DM Sans", size=9), height=280,
        margin=dict(l=4, r=10, t=10, b=70),
        xaxis=dict(tickangle=-35, tickfont=dict(size=8, color="#4A3728"), gridcolor="#EDE5DC"),
        yaxis=dict(gridcolor="#EDE5DC", tickfont=dict(size=8, color="#8B6347"), title="EMI (Rs.)"),
        showlegend=False, bargap=0.3)
    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

with ch2:
    st.markdown('<p style="font-size:9px;font-weight:700;color:#8B6347;letter-spacing:1px;text-transform:uppercase;">Principal vs Total Interest</p>', unsafe_allow_html=True)
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(name="Principal", x=res_df["Bank"], y=[principal/100000]*len(res_df),
                          marker_color=DARK, text=[f"Rs.{principal/100000:.0f}L"]*len(res_df),
                          textposition="auto", textfont=dict(size=7)))
    fig2.add_trace(go.Bar(name="Total Interest", x=res_df["Bank"], y=res_df["Total Interest (Rs.)"]/100000,
                          marker_color=ACCENT, text=[f"Rs.{v/100000:.1f}L" for v in res_df["Total Interest (Rs.)"]],
                          textposition="auto", textfont=dict(size=7)))
    fig2.update_layout(barmode="stack", paper_bgcolor="#FFFFFF", plot_bgcolor="#FAF7F2",
        font=dict(family="DM Sans", size=9), height=280,
        margin=dict(l=4, r=10, t=10, b=70),
        xaxis=dict(tickangle=-35, tickfont=dict(size=8, color="#4A3728"), gridcolor="#EDE5DC"),
        yaxis=dict(gridcolor="#EDE5DC", tickfont=dict(size=8, color="#8B6347"), title="Amount (Rs. Lakh)"),
        legend=dict(orientation="h", y=1.05, font=dict(size=9)), bargap=0.25)
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

st.markdown(f'<p style="font-size:9px;font-weight:700;color:#8B6347;letter-spacing:1px;text-transform:uppercase;">Amortization — {best["Bank"]} (Best Rate)</p>', unsafe_allow_html=True)

r = best["Rate (%)"] / 12 / 100
balance = principal
amort = []
for month in range(1, tenure_months + 1):
    interest = balance * r
    principal_pay = best["Monthly EMI (Rs.)"] - interest
    balance = max(0, balance - principal_pay)
    if month % 12 == 0:
        amort.append({"Year": month // 12, "Outstanding Balance (Rs.L)": round(balance / 100000, 1)})

amort_df = pd.DataFrame(amort)
fig3 = px.area(amort_df, x="Year", y="Outstanding Balance (Rs.L)", color_discrete_sequence=[DARK])
fig3.update_traces(line=dict(width=2), fillcolor="rgba(26,10,0,0.1)")
fig3.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FAF7F2",
    font=dict(family="DM Sans", size=9), height=180,
    margin=dict(l=4, r=10, t=6, b=10),
    xaxis=dict(gridcolor="#EDE5DC", tickfont=dict(size=8, color="#8B6347"), title="Year"),
    yaxis=dict(gridcolor="#EDE5DC", tickfont=dict(size=8, color="#8B6347"), title="Balance (Rs. Lakh)"),
    showlegend=False)
st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
display_df = res_df.copy()
display_df["Monthly EMI (Rs.)"] = display_df["Monthly EMI (Rs.)"].apply(lambda x: f"Rs.{x:,.0f}")
display_df["Total Interest (Rs.)"] = display_df["Total Interest (Rs.)"].apply(lambda x: f"Rs.{x/100000:,.1f}L")
display_df["Total Payment (Rs.)"] = display_df["Total Payment (Rs.)"].apply(lambda x: f"Rs.{x/100000:,.1f}L")
st.dataframe(display_df, use_container_width=True, hide_index=True, height=250)