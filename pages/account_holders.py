import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Account Holders", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=DM+Sans:wght@400;500;600&display=swap');
html,body,[class*="css"],.stApp { font-family:'DM Sans',sans-serif !important; background:#653900 !important; color:#1A0A00 !important; }
#MainMenu,footer,header,[data-testid="stSidebar"],[data-testid="collapsedControl"],.stDeployButton { display:none !important; }
.main .block-container { padding:16px 24px !important; max-width:100% !important; }
.page-header { background:#1A0A00; padding:22px 28px; margin-bottom:20px; border-bottom:3px solid #C4783A; }
.page-title { font-family:'Playfair Display',serif; font-size:26px; font-weight:800; color:#FAF7F2; }
.page-sub { font-size:10px; color:#C4783A; margin-top:5px; letter-spacing:1.5px; text-transform:uppercase; font-weight:600; }
.acct-card { background:#fff; border:1px solid #E8DDD4; border-top:3px solid #1A0A00; padding:12px 16px; }
.acct-lbl { font-size:9px; font-weight:700; color:#8B6347; letter-spacing:1px; text-transform:uppercase; margin-bottom:3px; }
.acct-val { font-family:'Playfair Display',serif; font-size:24px; font-weight:700; color:#1A0A00; }
.acct-sub { font-size:10px; color:#8B6347; margin-top:2px; }
button[kind="secondary"], .stButton>button { background:#1A0A00 !important; color:#FAF7F2 !important; border:none !important; border-radius:0 !important; font-size:11px !important; font-weight:600 !important; }
[data-testid="stSelectbox"]>div>div { border-radius:0 !important; border-color:#C4A882 !important; }
::-webkit-scrollbar { display:none; }
</style>
""", unsafe_allow_html=True)

if st.button("Back to Dashboard"):
    st.switch_page("app.py")

st.markdown("""
<div class="page-header">
  <div class="page-title">Account Holders Tracker</div>
  <div class="page-sub">Estimated Customer Base Growth &nbsp;&middot;&nbsp; 10 Indian Banks &nbsp;&middot;&nbsp; FY2020–2024 &nbsp;&middot;&nbsp; In Millions</div>
</div>
""", unsafe_allow_html=True)

DATA = {
    "SBI":             [450, 480, 505, 520, 540],
    "PNB":             [160, 170, 182, 195, 210],
    "Bank of Baroda":  [110, 118, 125, 132, 140],
    "HDFC Bank":       [56,  64,  73,  82,  93],
    "ICICI Bank":      [48,  54,  61,  68,  76],
    "Central Bank":    [70,  72,  74,  76,  78],
    "Indian Overseas": [52,  54,  56,  58,  61],
    "Axis Bank":       [28,  34,  40,  46,  54],
    "Kotak Mahindra":  [18,  22,  27,  33,  40],
    "IndusInd Bank":   [16,  19,  23,  28,  34],
}
YEARS = [2020, 2021, 2022, 2023, 2024]
TYPES = {
    "SBI": "Public", "PNB": "Public", "Bank of Baroda": "Public",
    "HDFC Bank": "Private", "ICICI Bank": "Private", "Central Bank": "Public",
    "Indian Overseas": "Public", "Axis Bank": "Private",
    "Kotak Mahindra": "Private", "IndusInd Bank": "Private"
}

rows = []
for bank, vals in DATA.items():
    for y, v in zip(YEARS, vals):
        rows.append({"Bank": bank, "Year": y, "Account_Holders_Mn": v, "Bank_Type": TYPES[bank]})
df = pd.DataFrame(rows)
df_2024 = df[df["Year"] == 2024].sort_values("Account_Holders_Mn", ascending=False)
df_2020 = df[df["Year"] == 2020].set_index("Bank")

DARK = "#1A0A00"; ACCENT = "#C4783A"; MED = "#6B3A2A"

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)
total_24 = df_2024["Account_Holders_Mn"].sum()
total_20 = df[df["Year"] == 2020]["Account_Holders_Mn"].sum()
fastest = df_2024.copy()
fastest["Growth_Pct"] = fastest.apply(
    lambda r: (r["Account_Holders_Mn"] - df_2020.loc[r["Bank"], "Account_Holders_Mn"]) / df_2020.loc[r["Bank"], "Account_Holders_Mn"] * 100, axis=1)
fastest_bank = fastest.loc[fastest["Growth_Pct"].idxmax()]
largest_bank = df_2024.iloc[0]

with k1:
    st.markdown(f'<div class="acct-card"><div class="acct-lbl">Total Accounts FY24</div><div class="acct-val">{total_24:.0f}M</div><div class="acct-sub">across 10 banks</div></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="acct-card"><div class="acct-lbl">Growth Since FY20</div><div class="acct-val">+{(total_24-total_20)/total_20*100:.1f}%</div><div class="acct-sub">{total_20:.0f}M to {total_24:.0f}M</div></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="acct-card"><div class="acct-lbl">Largest Bank (FY24)</div><div class="acct-val">{largest_bank["Account_Holders_Mn"]:.0f}M</div><div class="acct-sub">{largest_bank["Bank"]}</div></div>', unsafe_allow_html=True)
with k4:
    st.markdown(f'<div class="acct-card"><div class="acct-lbl">Fastest Growing</div><div class="acct-val">+{fastest_bank["Growth_Pct"]:.0f}%</div><div class="acct-sub">{fastest_bank["Bank"]} FY20–24</div></div>', unsafe_allow_html=True)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["Growth Trend", "FY2024 Ranking", "Public vs Private"])

palette = [DARK,"#3D1C02","#6B3A2A","#8B4513",ACCENT,"#4A3728","#2C1810","#A0522D","#8B6347","#D2691E"]

with tab1:
    btype_sel = st.radio("Bank Type", ["All", "Public", "Private"], horizontal=True, label_visibility="collapsed")
    trend_df = df if btype_sel == "All" else df[df["Bank_Type"] == btype_sel]
    fig1 = px.line(trend_df, x="Year", y="Account_Holders_Mn", color="Bank", markers=True,
                   color_discrete_sequence=palette, labels={"Account_Holders_Mn": "Account Holders (Millions)"})
    fig1.update_traces(line=dict(width=2.5), marker=dict(size=7))
    fig1.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FAF7F2",
        font=dict(family="DM Sans", size=9, color="#1A0A00"),
        height=280, margin=dict(l=4, r=10, t=10, b=10),
        xaxis=dict(gridcolor="#EDE5DC", tickfont=dict(size=9, color="#4A3728"), title=""),
        yaxis=dict(gridcolor="#EDE5DC", tickfont=dict(size=8, color="#8B6347"), title="Millions"),
        legend=dict(orientation="h", y=-0.25, xanchor="center", x=0.5, font=dict(size=8)))
    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

with tab2:
    fig2 = go.Figure(go.Bar(
        x=df_2024["Account_Holders_Mn"], y=df_2024["Bank"], orientation="h",
        marker_color=[DARK if t == "Public" else ACCENT for t in df_2024["Bank_Type"]],
        marker_line_width=0,
        text=[f"{v:.0f}M" for v in df_2024["Account_Holders_Mn"]],
        textposition="outside", textfont=dict(size=9)
    ))
    for i, (_, row) in enumerate(df_2024.iterrows()):
        g = (row["Account_Holders_Mn"] - df_2020.loc[row["Bank"], "Account_Holders_Mn"]) / df_2020.loc[row["Bank"], "Account_Holders_Mn"] * 100
        fig2.add_annotation(x=row["Account_Holders_Mn"] + 5, y=row["Bank"],
                            text=f"+{g:.0f}%", showarrow=False, font=dict(size=8, color="#4A3728"))
    fig2.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FAF7F2",
        font=dict(family="DM Sans", size=9), height=300,
        margin=dict(l=4, r=80, t=10, b=10),
        xaxis=dict(gridcolor="#EDE5DC", tickfont=dict(size=8, color="#8B6347"), title="Account Holders (Millions)"),
        yaxis=dict(gridcolor="#EDE5DC", tickfont=dict(size=9, color="#1A0A00"), title=""),
        showlegend=False, bargap=0.25)
    st.markdown(f'<div style="font-size:10px;color:#8B6347;margin-bottom:4px;">Dark = Public Bank &nbsp; Amber = Private Bank</div>', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

with tab3:
    pub_df  = df[df["Bank_Type"] == "Public"].groupby("Year")["Account_Holders_Mn"].sum().reset_index()
    priv_df = df[df["Bank_Type"] == "Private"].groupby("Year")["Account_Holders_Mn"].sum().reset_index()
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=pub_df["Year"], y=pub_df["Account_Holders_Mn"], name="Public Banks",
                              fill="tozeroy", fillcolor="rgba(26,10,0,0.08)",
                              line=dict(color=DARK, width=2.5), marker=dict(size=7)))
    fig3.add_trace(go.Scatter(x=priv_df["Year"], y=priv_df["Account_Holders_Mn"], name="Private Banks",
                              fill="tozeroy", fillcolor="rgba(196,120,58,0.08)",
                              line=dict(color=ACCENT, width=2.5), marker=dict(size=7)))
    fig3.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FAF7F2",
        font=dict(family="DM Sans", size=9), height=260,
        margin=dict(l=4, r=10, t=10, b=10),
        xaxis=dict(gridcolor="#EDE5DC", tickfont=dict(size=9, color="#4A3728"), title=""),
        yaxis=dict(gridcolor="#EDE5DC", tickfont=dict(size=8, color="#8B6347"), title="Total Accounts (Millions)"),
        legend=dict(orientation="h", y=1.05, font=dict(size=9)))
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    pub_growth  = (pub_df.iloc[-1]["Account_Holders_Mn"] - pub_df.iloc[0]["Account_Holders_Mn"]) / pub_df.iloc[0]["Account_Holders_Mn"] * 100
    priv_growth = (priv_df.iloc[-1]["Account_Holders_Mn"] - priv_df.iloc[0]["Account_Holders_Mn"]) / priv_df.iloc[0]["Account_Holders_Mn"] * 100
    g1, g2 = st.columns(2)
    with g1:
        st.markdown(f"""
        <div style="background:#fff;border:1px solid #E8DDD4;border-top:3px solid #1A0A00;padding:14px;text-align:center;">
          <div style="font-size:9px;font-weight:700;color:#8B6347;letter-spacing:1px;text-transform:uppercase;">Public Banks FY20 to FY24</div>
          <div style="font-family:'Playfair Display',serif;font-size:26px;font-weight:700;color:#1A0A00;">+{pub_growth:.1f}%</div>
          <div style="font-size:10px;color:#8B6347;">{pub_df.iloc[0]['Account_Holders_Mn']:.0f}M to {pub_df.iloc[-1]['Account_Holders_Mn']:.0f}M</div>
        </div>""", unsafe_allow_html=True)
    with g2:
        st.markdown(f"""
        <div style="background:#fff;border:1px solid #E8DDD4;border-top:3px solid #C4783A;padding:14px;text-align:center;">
          <div style="font-size:9px;font-weight:700;color:#8B6347;letter-spacing:1px;text-transform:uppercase;">Private Banks FY20 to FY24</div>
          <div style="font-family:'Playfair Display',serif;font-size:26px;font-weight:700;color:#C4783A;">+{priv_growth:.1f}%</div>
          <div style="font-size:10px;color:#8B6347;">{priv_df.iloc[0]['Account_Holders_Mn']:.0f}M to {priv_df.iloc[-1]['Account_Holders_Mn']:.0f}M</div>
        </div>""", unsafe_allow_html=True)

st.markdown("""
<div style="background:#1A0A00;padding:10px 16px;margin-top:14px;">
  <div style="font-size:10px;color:#C4A882;letter-spacing:0.5px;">Data Note: Account holder counts estimated from RBI Annual Reports and bank annual reports FY2020–2024. SBI figures include Jan Dhan Yojana accounts. Numbers in Millions.</div>
</div>
""", unsafe_allow_html=True)