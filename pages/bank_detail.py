import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.ai_insights import get_ai_insight

st.set_page_config(page_title="Bank Detail", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=DM+Sans:wght@400;500;600&display=swap');
html,body,[class*="css"],.stApp { font-family:'DM Sans',sans-serif !important; background:#EEF2F8 !important; color:#0A1628 !important; }
#MainMenu,footer,header,[data-testid="stSidebar"],[data-testid="collapsedControl"],.stDeployButton { display:none !important; }
.main .block-container { padding:16px 24px !important; max-width:100% !important; }
.bank-header { background:#0B2354; border-radius:10px; padding:18px 24px; margin-bottom:16px; display:flex; justify-content:space-between; align-items:center; }
.bank-name { font-family:'Bricolage Grotesque',sans-serif; font-size:22px; font-weight:800; color:#fff; }
.bank-type { font-size:11px; color:#93C5FD; background:rgba(147,197,253,0.15); border:1px solid rgba(147,197,253,0.3); padding:3px 12px; border-radius:20px; }
.metric-card { background:#fff; border:1px solid #D8E2F0; border-radius:8px; padding:12px 16px; }
.metric-lbl { font-size:9px; color:#94A3B8; font-weight:600; letter-spacing:0.8px; text-transform:uppercase; margin-bottom:3px; }
.metric-val { font-family:'Bricolage Grotesque',sans-serif; font-size:22px; font-weight:800; color:#0A1628; }
.insight-box { background:#fff; border:1px solid #D8E2F0; border-left:4px solid #0B2354; border-radius:8px; padding:16px; margin-top:12px; }
.insight-title { font-size:10px; font-weight:700; color:#0B2354; letter-spacing:1px; text-transform:uppercase; margin-bottom:8px; }
.insight-text { font-size:13px; color:#334155; line-height:1.7; }
::-webkit-scrollbar { display:none; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("data/indian_banks_kpi_ratios.csv")

kpi = load_data()

# ── BACK BUTTON ──
if st.button("← Back to Dashboard"):
    st.switch_page("app.py")

# ── BANK SELECT ──
col_sel, _ = st.columns([2, 5])
with col_sel:
    bank = st.selectbox("Select Bank", sorted(kpi["Bank"].unique()))

bdf = kpi[kpi["Bank"] == bank].sort_values("Year")
latest = bdf[bdf["Year"] == bdf["Year"].max()].iloc[0]

# ── BANK HEADER ──
st.markdown(f"""
<div class="bank-header">
  <div class="bank-name">🏦 {bank}</div>
  <div class="bank-type">{latest['Bank_Type']} Bank · {latest['Bank_Size']} Cap</div>
</div>
""", unsafe_allow_html=True)

# ── METRICS ──
m1,m2,m3,m4,m5 = st.columns(5)
metrics = [
    (m1, "Net Profit FY24", f"₹{latest['Net_Profit_Crore']:,.0f} Cr"),
    (m2, "Gross NPA",       f"{latest['Gross_NPA_Pct']:.2f}%"),
    (m3, "ROE",             f"{latest['Return_On_Equity_Pct']:.1f}%"),
    (m4, "NIM",             f"{latest['Net_Interest_Margin_Pct']:.1f}%"),
    (m5, "CAR",             f"{latest['Capital_Adequacy_Ratio_Pct']:.1f}%"),
]
for col, lbl, val in metrics:
    with col:
        st.markdown(f'<div class="metric-card"><div class="metric-lbl">{lbl}</div><div class="metric-val">{val}</div></div>', unsafe_allow_html=True)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ── CHARTS ──
NAVY="#0B2354"; BLUE="#2563EB"; GREEN="#059669"; RED="#DC2626"; AMBER="#F59E0B"

def ct(fig, h=220):
    fig.update_layout(
        paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC",
        font=dict(family="DM Sans", size=9, color="#0A1628"),
        height=h, margin=dict(l=4,r=10,t=6,b=4),
        xaxis=dict(gridcolor="#F0F4FA", tickfont=dict(size=8,color="#94A3B8"), title=""),
        yaxis=dict(gridcolor="#F0F4FA", tickfont=dict(size=8,color="#94A3B8"), title=""),
    )
    return fig

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<p style="font-size:9.5px;font-weight:600;color:#64748B;letter-spacing:0.5px;text-transform:uppercase;padding:4px;">Net Profit Trend</p>', unsafe_allow_html=True)
    fig1 = px.bar(bdf, x="Year", y="Net_Profit_Crore", color_discrete_sequence=[NAVY],
                  text="Net_Profit_Crore")
    fig1.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside", textfont=dict(size=8), marker_line_width=0)
    ct(fig1); fig1.update_layout(bargap=0.3)
    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar":False})

with c2:
    st.markdown('<p style="font-size:9.5px;font-weight:600;color:#64748B;letter-spacing:0.5px;text-transform:uppercase;padding:4px;">Gross NPA % Trend</p>', unsafe_allow_html=True)
    fig2 = px.line(bdf, x="Year", y="Gross_NPA_Pct", markers=True, color_discrete_sequence=[RED])
    fig2.update_traces(line=dict(width=2.5), marker=dict(size=7))
    fig2.add_hrect(y0=0, y1=2, fillcolor="rgba(5,150,105,0.07)", line_width=0)
    ct(fig2)
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})

with c3:
    st.markdown('<p style="font-size:9.5px;font-weight:600;color:#64748B;letter-spacing:0.5px;text-transform:uppercase;padding:4px;">ROE vs NIM Trend</p>', unsafe_allow_html=True)
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=bdf["Year"], y=bdf["Return_On_Equity_Pct"], name="ROE %", line=dict(color=BLUE, width=2), marker=dict(size=6)))
    fig3.add_trace(go.Scatter(x=bdf["Year"], y=bdf["Net_Interest_Margin_Pct"], name="NIM %", line=dict(color=GREEN, width=2), marker=dict(size=6)))
    ct(fig3)
    fig3.update_layout(legend=dict(orientation="h", y=1.1, font=dict(size=9)))
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar":False})

# ── AI INSIGHT ──
st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
if st.button("🤖 Generate AI Insight", type="primary"):
    with st.spinner("Analysing..."):
        insight = get_ai_insight(
            bank, int(latest["Year"]),
            latest["Gross_NPA_Pct"], latest["Return_On_Equity_Pct"],
            latest["Net_Profit_Crore"], latest["Net_Interest_Margin_Pct"],
            latest["Capital_Adequacy_Ratio_Pct"]
        )
    st.markdown(f"""
    <div class="insight-box">
      <div class="insight-title">🤖 AI Analyst — {bank}</div>
      <div class="insight-text">{insight.replace(chr(10), '<br>')}</div>
    </div>
    """, unsafe_allow_html=True)