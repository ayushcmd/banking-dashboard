import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="FD & Loan Rates", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=DM+Sans:wght@400;500;600&display=swap');
html,body,[class*="css"],.stApp { font-family:'DM Sans',sans-serif !important; background:#653900 !important; color:#1A0A00 !important; }
#MainMenu,footer,header,[data-testid="stSidebar"],[data-testid="collapsedControl"],.stDeployButton { display:none !important; }
.main .block-container { padding:16px 24px !important; max-width:100% !important; }
.page-header { background:#1A0A00; padding:22px 28px; margin-bottom:20px; border-bottom:3px solid #C4783A; }
.page-title { font-family:'Playfair Display',serif; font-size:26px; font-weight:800; color:#FAF7F2; }
.page-sub { font-size:10px; color:#C4783A; margin-top:5px; letter-spacing:1.5px; text-transform:uppercase; font-weight:600; }
.rate-card { background:#fff; border:1px solid #E8DDD4; border-top:3px solid #1A0A00; padding:12px 16px; }
.rate-card.best { border-top-color:#1A4A1A; }
.rate-card.worst { border-top-color:#8B1A1A; }
.rate-lbl { font-size:9px; font-weight:700; color:#8B6347; letter-spacing:1px; text-transform:uppercase; margin-bottom:3px; }
.rate-val { font-family:'Playfair Display',serif; font-size:22px; font-weight:700; color:#1A0A00; }
.rate-tag { font-size:9px; font-weight:700; padding:2px 10px; letter-spacing:0.5px; text-transform:uppercase; border:1px solid; display:inline-block; margin-top:5px; }
.rate-tag.good { color:#1A4A1A; border-color:#1A4A1A; }
.rate-tag.bad { color:#8B1A1A; border-color:#8B1A1A; }
button[kind="secondary"], .stButton>button { background:#1A0A00 !important; color:#FAF7F2 !important; border:none !important; border-radius:0 !important; font-size:11px !important; font-weight:600 !important; }
[data-testid="stSelectbox"]>div>div { border-radius:0 !important; border-color:#C4A882 !important; }
::-webkit-scrollbar { display:none; }
</style>
""", unsafe_allow_html=True)

if st.button("Back to Dashboard"):
    st.switch_page("app.py")

st.markdown("""
<div class="page-header">
  <div class="page-title">FD &amp; Loan Rate Comparison</div>
  <div class="page-sub">Fixed Deposit &amp; Lending Rates Across 10 Banks &nbsp;&middot;&nbsp; FY2024</div>
</div>
""", unsafe_allow_html=True)

RATES = {
    "SBI":              {"fd_gen": 6.50, "fd_senior": 7.00, "home_loan": 8.40, "personal_loan": 12.00, "car_loan": 8.70, "education_loan": 8.50},
    "HDFC Bank":        {"fd_gen": 7.10, "fd_senior": 7.60, "home_loan": 8.35, "personal_loan": 10.50, "car_loan": 8.50, "education_loan": 9.00},
    "ICICI Bank":       {"fd_gen": 7.00, "fd_senior": 7.50, "home_loan": 8.35, "personal_loan": 10.65, "car_loan": 8.65, "education_loan": 9.20},
    "Axis Bank":        {"fd_gen": 7.10, "fd_senior": 7.75, "home_loan": 8.75, "personal_loan": 10.25, "car_loan": 8.70, "education_loan": 9.40},
    "Kotak Mahindra":   {"fd_gen": 7.25, "fd_senior": 7.75, "home_loan": 8.70, "personal_loan": 10.99, "car_loan": 8.80, "education_loan": 9.50},
    "PNB":              {"fd_gen": 6.50, "fd_senior": 7.00, "home_loan": 8.40, "personal_loan": 11.40, "car_loan": 8.75, "education_loan": 8.55},
    "Bank of Baroda":   {"fd_gen": 6.85, "fd_senior": 7.35, "home_loan": 8.40, "personal_loan": 11.40, "car_loan": 8.60, "education_loan": 8.85},
    "Central Bank":     {"fd_gen": 6.25, "fd_senior": 6.75, "home_loan": 8.45, "personal_loan": 11.50, "car_loan": 8.90, "education_loan": 8.70},
    "Indian Overseas":  {"fd_gen": 6.50, "fd_senior": 7.00, "home_loan": 8.40, "personal_loan": 11.30, "car_loan": 8.85, "education_loan": 8.60},
    "IndusInd Bank":    {"fd_gen": 7.25, "fd_senior": 7.75, "home_loan": 8.80, "personal_loan": 10.49, "car_loan": 8.70, "education_loan": 9.30},
}

df = pd.DataFrame(RATES).T.reset_index()
df.columns = ["Bank", "FD General (%)", "FD Senior Citizen (%)", "Home Loan (%)", "Personal Loan (%)", "Car Loan (%)", "Education Loan (%)"]

DARK = "#1A0A00"; ACCENT = "#C4783A"; GREEN = "#1A4A1A"; RED = "#8B1A1A"; MED = "#6B3A2A"

tab1, tab2, tab3 = st.tabs(["Fixed Deposits", "Loan Rates", "Full Comparison"])

with tab1:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    k1, k2, k3 = st.columns(3)
    best_gen = df.loc[df["FD General (%)"].idxmax()]
    best_sr  = df.loc[df["FD Senior Citizen (%)"].idxmax()]
    worst_fd = df.loc[df["FD General (%)"].idxmin()]
    with k1:
        st.markdown(f'<div class="rate-card best"><div class="rate-lbl">Best FD Rate (General)</div><div class="rate-val">{best_gen["FD General (%)"]:.2f}%</div><span class="rate-tag good">{best_gen["Bank"]}</span></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="rate-card best"><div class="rate-lbl">Best FD Rate (Senior Citizen)</div><div class="rate-val">{best_sr["FD Senior Citizen (%)"]:.2f}%</div><span class="rate-tag good">{best_sr["Bank"]}</span></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="rate-card worst"><div class="rate-lbl">Lowest FD Rate</div><div class="rate-val">{worst_fd["FD General (%)"]:.2f}%</div><span class="rate-tag bad">{worst_fd["Bank"]}</span></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    fd_df = df.sort_values("FD General (%)", ascending=False)
    fig = go.Figure()
    fig.add_trace(go.Bar(name="General", x=fd_df["Bank"], y=fd_df["FD General (%)"],
                         marker_color=DARK, text=[f"{v:.2f}%" for v in fd_df["FD General (%)"]],
                         textposition="outside", textfont=dict(size=8)))
    fig.add_trace(go.Bar(name="Senior Citizen", x=fd_df["Bank"], y=fd_df["FD Senior Citizen (%)"],
                         marker_color=ACCENT, text=[f"{v:.2f}%" for v in fd_df["FD Senior Citizen (%)"]],
                         textposition="outside", textfont=dict(size=8)))
    fig.update_layout(barmode="group", paper_bgcolor="#FFFFFF", plot_bgcolor="#FAF7F2",
        font=dict(family="DM Sans", size=9), height=300,
        margin=dict(l=4, r=10, t=10, b=60),
        xaxis=dict(tickangle=-30, tickfont=dict(size=9, color="#4A3728"), gridcolor="#EDE5DC"),
        yaxis=dict(range=[0, 9], gridcolor="#EDE5DC", tickfont=dict(size=8, color="#8B6347"), title="Rate (%)"),
        legend=dict(orientation="h", y=1.05, font=dict(size=9)),
        bargap=0.15, bargroupgap=0.08)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("""
    <div style="background:#fff;border:1px solid #E8DDD4;border-left:3px solid #C4783A;padding:10px 16px;font-size:12px;color:#2C1810;">
      <strong>Note:</strong> Senior citizen rates are 0.25–0.75% higher. For 1–3 year tenures, private banks like Kotak, Axis and HDFC offer the most competitive rates.
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    loan_type = st.selectbox("Select Loan Type", ["Home Loan (%)", "Personal Loan (%)", "Car Loan (%)", "Education Loan (%)"], label_visibility="collapsed")
    k1, k2, k3 = st.columns(3)
    best_l  = df.loc[df[loan_type].idxmin()]
    worst_l = df.loc[df[loan_type].idxmax()]
    avg_r   = df[loan_type].mean()
    with k1:
        st.markdown(f'<div class="rate-card best"><div class="rate-lbl">Best (Lowest) Rate</div><div class="rate-val">{best_l[loan_type]:.2f}%</div><span class="rate-tag good">{best_l["Bank"]}</span></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="rate-card worst"><div class="rate-lbl">Highest Rate</div><div class="rate-val">{worst_l[loan_type]:.2f}%</div><span class="rate-tag bad">{worst_l["Bank"]}</span></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="rate-card"><div class="rate-lbl">Sector Average</div><div class="rate-val">{avg_r:.2f}%</div><div style="font-size:10px;color:#8B6347;margin-top:4px;">across 10 banks</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    loan_df = df.sort_values(loan_type)
    colors  = [GREEN if v == loan_df[loan_type].min() else RED if v == loan_df[loan_type].max() else DARK for v in loan_df[loan_type]]
    fig2 = go.Figure(go.Bar(x=loan_df["Bank"], y=loan_df[loan_type], marker_color=colors,
        marker_line_width=0, text=[f"{v:.2f}%" for v in loan_df[loan_type]],
        textposition="outside", textfont=dict(size=9)))
    fig2.add_hline(y=avg_r, line_dash="dot", line_color="rgba(0,0,0,0.25)", line_width=1.5,
                   annotation_text=f"Avg {avg_r:.2f}%", annotation_font_size=8)
    fig2.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FAF7F2",
        font=dict(family="DM Sans", size=9), height=300,
        margin=dict(l=4, r=10, t=10, b=60),
        xaxis=dict(tickangle=-30, tickfont=dict(size=9, color="#4A3728"), gridcolor="#EDE5DC"),
        yaxis=dict(gridcolor="#EDE5DC", tickfont=dict(size=8, color="#8B6347"), title="Rate (%)"),
        showlegend=False, bargap=0.3)
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

with tab3:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    styled = df.set_index("Bank").style\
        .background_gradient(subset=["FD General (%)", "FD Senior Citizen (%)"], cmap="YlOrBr", vmin=5, vmax=8)\
        .background_gradient(subset=["Home Loan (%)", "Personal Loan (%)", "Car Loan (%)", "Education Loan (%)"], cmap="YlOrBr_r", vmin=8, vmax=14)\
        .format("{:.2f}%")\
        .set_properties(**{"font-size": "12px", "font-family": "DM Sans"})
    st.dataframe(styled, use_container_width=True, height=380)
    st.markdown("""
    <div style="background:#1A0A00;padding:10px 16px;margin-top:8px;font-size:11px;color:#C4A882;">
      FD: Higher is better for depositors &nbsp;|&nbsp; Loans: Lower is cheaper for borrowers &nbsp;|&nbsp; Source: Bank websites &amp; RBI MPC announcements FY2024
    </div>
    """, unsafe_allow_html=True)