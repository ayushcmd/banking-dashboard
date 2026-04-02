import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Bank Safety Score", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=DM+Sans:wght@400;500;600&display=swap');
html,body,[class*="css"],.stApp { font-family:'DM Sans',sans-serif !important; background:#653900 !important; color:#1A0A00 !important; }
#MainMenu,footer,header,[data-testid="stSidebar"],[data-testid="collapsedControl"],.stDeployButton { display:none !important; }
.main .block-container { padding:16px 24px !important; max-width:100% !important; }
.page-header { background:#1A0A00; padding:22px 28px; margin-bottom:20px; border-bottom:3px solid #C4783A; }
.page-title { font-family:'Playfair Display',serif; font-size:26px; font-weight:800; color:#FAF7F2; }
.page-sub { font-size:10px; color:#C4783A; margin-top:5px; letter-spacing:1.5px; text-transform:uppercase; font-weight:600; }
.safety-card { background:#fff; border:1px solid #E8DDD4; border-top:3px solid #1A0A00; padding:14px; text-align:center; }
.safety-card.safe { border-top-color:#1A4A1A; }
.safety-card.caution { border-top-color:#C4783A; }
.safety-card.risky { border-top-color:#8B1A1A; }
.safety-label { font-size:9px; font-weight:700; letter-spacing:1px; text-transform:uppercase; color:#8B6347; margin-bottom:5px; }
.safety-score { font-family:'Playfair Display',serif; font-size:32px; font-weight:700; color:#1A0A00; line-height:1; }
.safety-grade { font-size:11px; font-weight:600; margin-top:4px; color:#4A3728; }
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

st.markdown("""
<div class="page-header">
  <div class="page-title">Bank Safety Score</div>
  <div class="page-sub">Composite Safety Rating &nbsp;&middot;&nbsp; RBI-Mandated Indicators &nbsp;&middot;&nbsp; Lower NPA + Higher CAR = Safer</div>
</div>
""", unsafe_allow_html=True)

col_y, col_t, _ = st.columns([1, 1.5, 4])
with col_y:
    year = st.selectbox("Year", sorted(kpi["Year"].unique(), reverse=True), label_visibility="collapsed")
with col_t:
    btype = st.radio("Bank Type", ["All", "Public", "Private"], horizontal=True, label_visibility="collapsed")

sel_types = list(kpi["Bank_Type"].unique()) if btype == "All" else [btype]
df = kpi[(kpi["Year"] == year) & (kpi["Bank_Type"].isin(sel_types))].copy()

def safety_score(row):
    car_score = min(100, max(0, (row["Capital_Adequacy_Ratio_Pct"] - 8) / (20 - 8) * 100))
    npa_score = min(100, max(0, 100 - (row["Gross_NPA_Pct"] / 12 * 100)))
    net_npa_s = min(100, max(0, 100 - (row["Net_NPA_Pct"] / 6 * 100)))
    roa_score = min(100, max(0, (row["Return_On_Assets_Pct"] + 1) / 3 * 100))
    cdr = row["Credit_Deposit_Ratio_Pct"]
    cdr_score = min(100, max(0, 100 - abs(cdr - 75) * 2))
    return round(0.30 * car_score + 0.30 * npa_score + 0.20 * net_npa_s + 0.10 * roa_score + 0.10 * cdr_score, 1)

def grade(score):
    if score >= 75: return "AAA — Excellent", "safe"
    if score >= 60: return "AA — Very Safe", "safe"
    if score >= 50: return "A — Safe", "safe"
    if score >= 40: return "BBB — Moderate", "caution"
    if score >= 30: return "BB — Caution", "caution"
    return "B — High Risk", "risky"

df["Safety_Score"] = df.apply(safety_score, axis=1)
df["Grade"], df["GradeClass"] = zip(*df["Safety_Score"].map(lambda s: grade(s)))
df = df.sort_values("Safety_Score", ascending=False)

DARK = "#1A0A00"; ACCENT = "#C4783A"; GREEN = "#1A4A1A"; RED = "#8B1A1A"

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
c1, c2 = st.columns([3, 2])

with c1:
    st.markdown(f'<p style="font-size:9px;font-weight:700;color:#8B6347;letter-spacing:1px;text-transform:uppercase;">Safety Ranking FY{year}</p>', unsafe_allow_html=True)
    colors = [GREEN if s >= 50 else ACCENT if s >= 35 else RED for s in df["Safety_Score"]]
    fig = go.Figure(go.Bar(
        x=df["Safety_Score"], y=df["Bank"], orientation="h",
        marker_color=colors, marker_line_width=0,
        text=[f"{s:.1f}" for s in df["Safety_Score"]],
        textposition="outside", textfont=dict(size=9, color="#4A3728")
    ))
    fig.add_vline(x=50, line_dash="dot", line_color="rgba(0,0,0,0.2)", line_width=1.5,
                  annotation_text="Safe Threshold", annotation_font_size=8)
    fig.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FAF7F2",
        font=dict(family="DM Sans", size=9, color="#1A0A00"),
        height=320, margin=dict(l=4, r=60, t=10, b=10),
        xaxis=dict(range=[0, 110], gridcolor="#EDE5DC", tickfont=dict(size=8, color="#8B6347"), title=""),
        yaxis=dict(gridcolor="#EDE5DC", tickfont=dict(size=9, color="#1A0A00"), title=""),
        bargap=0.25, showlegend=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with c2:
    st.markdown('<p style="font-size:9px;font-weight:700;color:#8B6347;letter-spacing:1px;text-transform:uppercase;">Score Components — Top Bank</p>', unsafe_allow_html=True)
    top = df.iloc[0]
    car_s  = min(100, max(0, (top["Capital_Adequacy_Ratio_Pct"] - 8) / 12 * 100))
    npa_s  = min(100, max(0, 100 - top["Gross_NPA_Pct"] / 12 * 100))
    nnpa_s = min(100, max(0, 100 - top["Net_NPA_Pct"] / 6 * 100))
    roa_s  = min(100, max(0, (top["Return_On_Assets_Pct"] + 1) / 3 * 100))
    cdr_s  = min(100, max(0, 100 - abs(top["Credit_Deposit_Ratio_Pct"] - 75) * 2))
    cats = ["Capital Adequacy", "Gross NPA", "Net NPA", "ROA", "CDR"]
    vals = [car_s, npa_s, nnpa_s, roa_s, cdr_s]
    radar = go.Figure(go.Scatterpolar(
        r=vals + [vals[0]], theta=cats + [cats[0]],
        fill="toself", fillcolor="rgba(26,10,0,0.10)",
        line=dict(color=DARK, width=2), marker=dict(size=6, color=DARK)
    ))
    radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=7), gridcolor="#EDE5DC"),
                   angularaxis=dict(tickfont=dict(size=8, color="#4A3728"))),
        paper_bgcolor="#FFFFFF", font=dict(family="DM Sans"),
        height=320, margin=dict(l=30, r=30, t=30, b=10), showlegend=False,
        title=dict(text=f"{top['Bank']} — {top['Safety_Score']:.1f}/100",
                   font=dict(size=11, color=DARK, family="Playfair Display"), x=0.5)
    )
    st.plotly_chart(radar, use_container_width=True, config={"displayModeBar": False})

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
st.markdown('<p style="font-size:9px;font-weight:700;color:#8B6347;letter-spacing:1px;text-transform:uppercase;">Individual Bank Safety Cards</p>', unsafe_allow_html=True)

cols = st.columns(min(5, len(df)))
for i, (_, row) in enumerate(df.iterrows()):
    grade_text, cls = grade(row["Safety_Score"])
    with cols[i % 5]:
        st.markdown(f"""
        <div class="safety-card {cls}">
          <div class="safety-label">{row['Bank']}</div>
          <div class="safety-score">{row['Safety_Score']:.0f}</div>
          <div class="safety-grade">{grade_text.split('—')[0].strip()}</div>
          <div style="font-size:9px;color:#8B6347;margin-top:6px;">CAR {row['Capital_Adequacy_Ratio_Pct']:.1f}% &nbsp; NPA {row['Gross_NPA_Pct']:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
st.markdown('<p style="font-size:9px;font-weight:700;color:#8B6347;letter-spacing:1px;text-transform:uppercase;">Safety Score Trend 2020–2024</p>', unsafe_allow_html=True)

all_scores = []
for _, row in kpi.iterrows():
    score = safety_score(row)
    all_scores.append({"Bank": row["Bank"], "Year": row["Year"], "Safety_Score": score, "Bank_Type": row["Bank_Type"]})
score_df = pd.DataFrame(all_scores)

palette = [DARK,"#3D1C02","#6B3A2A","#8B4513","#C4783A","#4A3728","#2C1810","#A0522D","#8B6347","#D2691E"]
fig2 = px.line(score_df, x="Year", y="Safety_Score", color="Bank", markers=True, color_discrete_sequence=palette)
fig2.update_traces(line=dict(width=2), marker=dict(size=5))
fig2.add_hrect(y0=0, y1=35, fillcolor="rgba(139,26,26,0.05)", line_width=0)
fig2.add_hrect(y0=35, y1=50, fillcolor="rgba(196,120,58,0.05)", line_width=0)
fig2.add_hrect(y0=50, y1=110, fillcolor="rgba(26,74,26,0.04)", line_width=0)
fig2.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FAF7F2",
    font=dict(family="DM Sans", size=9, color="#1A0A00"),
    height=220, margin=dict(l=4, r=10, t=10, b=4),
    xaxis=dict(gridcolor="#EDE5DC", tickfont=dict(size=8, color="#8B6347"), title=""),
    yaxis=dict(gridcolor="#EDE5DC", tickfont=dict(size=8, color="#8B6347"), title="Safety Score"),
    legend=dict(orientation="h", y=-0.3, xanchor="center", x=0.5, font=dict(size=8)))
st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

st.markdown("""
<div style="background:#1A0A00;padding:12px 16px;margin-top:8px;">
  <div style="font-size:9px;font-weight:700;color:#C4783A;letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;">How the Safety Score Works</div>
  <div style="font-size:11px;color:#C4A882;line-height:1.7;">
    Capital Adequacy Ratio (30%) &nbsp;&middot;&nbsp; Gross NPA % (30%) &nbsp;&middot;&nbsp; Net NPA % (20%) &nbsp;&middot;&nbsp; Return on Assets (10%) &nbsp;&middot;&nbsp; Credit-Deposit Ratio (10%)
    &nbsp; Scores above 50 indicate a safe bank. CAR above RBI minimum 9% is essential. NPA below 3% signals strong asset quality.
  </div>
</div>
""", unsafe_allow_html=True)