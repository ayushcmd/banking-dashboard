import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.ai_insights import get_ai_insight

st.set_page_config(page_title="Bank Detail", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=DM+Sans:wght@400;500;600&display=swap');
html,body,[class*="css"],.stApp { font-family:'DM Sans',sans-serif !important; background:#FAF7F2 !important; color:#1A0A00 !important; }
#MainMenu,footer,header,[data-testid="stSidebar"],[data-testid="collapsedControl"],.stDeployButton { display:none !important; }
.main .block-container { padding:16px 24px !important; max-width:100% !important; }
.bank-header { background:#1A0A00; padding:22px 28px; margin-bottom:20px; border-bottom:3px solid #C4783A; }
.bank-name { font-family:'Playfair Display',serif; font-size:26px; font-weight:800; color:#FAF7F2; }
.bank-type { font-size:10px; color:#C4783A; letter-spacing:1.5px; text-transform:uppercase; font-weight:700; margin-top:4px; }
.metric-card { background:#fff; border:1px solid #E8DDD4; border-top:3px solid #1A0A00; padding:14px 16px; }
.metric-lbl { font-size:9px; color:#8B6347; font-weight:700; letter-spacing:1px; text-transform:uppercase; margin-bottom:4px; }
.metric-val { font-family:'Playfair Display',serif; font-size:24px; font-weight:700; color:#1A0A00; }
.insight-box { background:#fff; border:1px solid #E8DDD4; border-left:3px solid #C4783A; padding:16px 20px; margin-top:12px; }
.insight-title { font-size:9px; font-weight:700; color:#8B6347; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:8px; }
.insight-text { font-size:13px; color:#2C1810; line-height:1.8; }
button[kind="secondary"], .stButton>button { background:#1A0A00 !important; color:#FAF7F2 !important; border:none !important; border-radius:0 !important; font-size:11px !important; font-weight:600 !important; }
[data-testid="stSelectbox"]>div>div { border-radius:0 !important; border-color:#C4A882 !important; }
::-webkit-scrollbar { display:none; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("data/indian_banks_kpi_ratios.csv")

kpi = load_data()

if st.button("Back to Dashboard"):
    st.switch_page("app.py")

col_sel, _ = st.columns([2, 5])
with col_sel:
    bank = st.selectbox("Select Bank", sorted(kpi["Bank"].unique()))

bdf = kpi[kpi["Bank"] == bank].sort_values("Year")
latest = bdf[bdf["Year"] == bdf["Year"].max()].iloc[0]

st.markdown(f"""
<div class="bank-header">
  <div class="bank-name">{bank}</div>
  <div class="bank-type">{latest['Bank_Type']} Bank &nbsp;&middot;&nbsp; {latest['Bank_Size']} Cap</div>
</div>
""", unsafe_allow_html=True)

m1,m2,m3,m4,m5 = st.columns(5)
metrics = [
    (m1, "Net Profit FY24", f"Rs.{latest['Net_Profit_Crore']:,.0f} Cr"),
    (m2, "Gross NPA",       f"{latest['Gross_NPA_Pct']:.2f}%"),
    (m3, "ROE",             f"{latest['Return_On_Equity_Pct']:.1f}%"),
    (m4, "NIM",             f"{latest['Net_Interest_Margin_Pct']:.1f}%"),
    (m5, "CAR",             f"{latest['Capital_Adequacy_Ratio_Pct']:.1f}%"),
]
for col, lbl, val in metrics:
    with col:
        st.markdown(f'<div class="metric-card"><div class="metric-lbl">{lbl}</div><div class="metric-val">{val}</div></div>', unsafe_allow_html=True)

st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

DARK = "#1A0A00"; MED = "#6B3A2A"; ACCENT = "#C4783A"; RED = "#8B1A1A"; GREEN = "#1A4A1A"

def ct(fig, h=220):
    fig.update_layout(
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FAF7F2",
        font=dict(family="DM Sans", size=9, color="#1A0A00"),
        height=h, margin=dict(l=4,r=10,t=6,b=4),
        xaxis=dict(gridcolor="#EDE5DC", tickfont=dict(size=8,color="#8B6347"), title=""),
        yaxis=dict(gridcolor="#EDE5DC", tickfont=dict(size=8,color="#8B6347"), title=""),
    )
    return fig

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<p style="font-size:9px;font-weight:700;color:#8B6347;letter-spacing:1px;text-transform:uppercase;padding:4px 0;">Net Profit Trend</p>', unsafe_allow_html=True)
    fig1 = px.bar(bdf, x="Year", y="Net_Profit_Crore", color_discrete_sequence=[DARK], text="Net_Profit_Crore")
    fig1.update_traces(texttemplate="Rs.%{text:,.0f}", textposition="outside", textfont=dict(size=8), marker_line_width=0)
    ct(fig1); fig1.update_layout(bargap=0.3)
    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar":False})

with c2:
    st.markdown('<p style="font-size:9px;font-weight:700;color:#8B6347;letter-spacing:1px;text-transform:uppercase;padding:4px 0;">Gross NPA % Trend</p>', unsafe_allow_html=True)
    fig2 = px.line(bdf, x="Year", y="Gross_NPA_Pct", markers=True, color_discrete_sequence=[RED])
    fig2.update_traces(line=dict(width=2.5), marker=dict(size=7))
    ct(fig2)
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})

with c3:
    st.markdown('<p style="font-size:9px;font-weight:700;color:#8B6347;letter-spacing:1px;text-transform:uppercase;padding:4px 0;">ROE vs NIM</p>', unsafe_allow_html=True)
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=bdf["Year"], y=bdf["Return_On_Equity_Pct"], name="ROE %", line=dict(color=DARK, width=2), marker=dict(size=6)))
    fig3.add_trace(go.Scatter(x=bdf["Year"], y=bdf["Net_Interest_Margin_Pct"], name="NIM %", line=dict(color=ACCENT, width=2), marker=dict(size=6)))
    ct(fig3)
    fig3.update_layout(legend=dict(orientation="h", y=1.1, font=dict(size=9)))
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar":False})

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
if st.button("Generate AI Analysis", type="primary"):
    with st.spinner("Analysing..."):
        insight = get_ai_insight(
            bank, int(latest["Year"]),
            latest["Gross_NPA_Pct"], latest["Return_On_Equity_Pct"],
            latest["Net_Profit_Crore"], latest["Net_Interest_Margin_Pct"],
            latest["Capital_Adequacy_Ratio_Pct"]
        )
    st.markdown(f"""
    <div class="insight-box">
      <div class="insight-title">AI Analyst — {bank}</div>
      <div class="insight-text">{insight.replace(chr(10), '<br>')}</div>
    </div>
    """, unsafe_allow_html=True)