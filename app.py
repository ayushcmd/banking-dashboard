import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pages import sql_explorer

st.set_page_config(page_title="India's Banking Dashboard", page_icon="🏦", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Outfit:wght@300;400;500;600&display=swap');

*, html, body { margin:0; padding:0; box-sizing:border-box; }

html, body, [class*="css"], .stApp {
    font-family: 'Outfit', sans-serif !important;
    color: #1C0A00 !important;
    overflow: hidden !important;
}

#MainMenu, footer, header, [data-testid="stSidebar"],
[data-testid="collapsedControl"], .stDeployButton { display:none !important; }

.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
    overflow: hidden !important;
}

/* ── PARTICLE BACKGROUND ── */
.particle-bg {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    background: linear-gradient(135deg, #FDF6EC 0%, #F9EDE3 40%, #FDF0F5 100%);
    z-index: 0;
    overflow: hidden;
}

.particle {
    position: absolute;
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    color: rgba(139, 90, 60, 0.12);
    animation: floatUp linear infinite;
    user-select: none;
    pointer-events: none;
}

@keyframes floatUp {
    0%   { transform: translateY(100vh) rotate(0deg); opacity: 0; }
    10%  { opacity: 1; }
    90%  { opacity: 0.8; }
    100% { transform: translateY(-120px) rotate(25deg); opacity: 0; }
}

/* ── ALL CONTENT ABOVE BACKGROUND ── */
.stApp > div { position: relative; z-index: 1; }

/* ── NAV ── */
.nav {
    background: rgba(74, 35, 9, 0.92);
    backdrop-filter: blur(12px);
    padding: 0 20px;
    height: 46px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 2px solid #C4956A;
    position: relative;
    z-index: 10;
}

.nav-logo {
    font-family: 'Playfair Display', serif;
    font-size: 16px;
    font-weight: 700;
    color: #FDF6EC;
    letter-spacing: 0.2px;
}

.nav-logo em { color: #F4A7B9; font-style: normal; }

.nav-meta {
    font-size: 10px;
    color: rgba(253,246,236,0.45);
    letter-spacing: 0.5px;
}

/* ── FILTER ROW ── */
.frow-bg {
    background: rgba(253,246,236,0.85);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid rgba(196,149,106,0.3);
    height: 40px;
    display: flex;
    align-items: center;
    position: relative;
    z-index: 5;
}

/* ── KPI STRIP ── */
.kpi-strip {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0;
    background: rgba(196,149,106,0.2);
    border-bottom: 1px solid rgba(196,149,106,0.25);
    position: relative;
    z-index: 5;
}

.kpi-cell {
    background: rgba(253,246,236,0.88);
    backdrop-filter: blur(8px);
    padding: 10px 14px 9px 18px;
    border-right: 1px solid rgba(196,149,106,0.2);
    position: relative;
}

.kpi-cell:last-child { border-right: none; }

.kpi-bar {
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    background: #8B5A3C;
    border-radius: 0 2px 2px 0;
}

.kpi-cell:nth-child(2) .kpi-bar { background: #C4956A; }
.kpi-cell:nth-child(3) .kpi-bar { background: #E8637A; }
.kpi-cell:nth-child(4) .kpi-bar { background: #F4A7B9; }
.kpi-cell:nth-child(5) .kpi-bar { background: #D4956A; }

.kpi-lbl {
    font-size: 8.5px;
    color: #8B5A3C;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 2px;
}

.kpi-val {
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    font-weight: 700;
    color: #1C0A00;
    line-height: 1;
    letter-spacing: -0.3px;
}

.kpi-sub {
    font-size: 9px;
    color: #8B5A3C;
    margin-top: 2px;
    font-weight: 500;
}

/* ── CHART CONTAINER ── */
.chart-bg {
    background: rgba(253,246,236,0.82);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(196,149,106,0.25);
    border-radius: 6px;
    overflow: hidden;
}

.clbl {
    font-size: 9px;
    font-weight: 600;
    color: #5C3317;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    padding: 6px 8px 1px;
}

/* ── SELECTBOX ── */
[data-testid="stSelectbox"]>div>div {
    background: rgba(253,246,236,0.9) !important;
    border: 1px solid rgba(196,149,106,0.4) !important;
    border-radius: 6px !important;
    color: #1C0A00 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    min-height: 30px !important;
}

[data-testid="stSelectbox"] label, [data-testid="stMultiSelect"] label { display:none !important; }

[data-testid="stMultiSelect"]>div>div {
    background: rgba(253,246,236,0.9) !important;
    border: 1px solid rgba(196,149,106,0.4) !important;
    border-radius: 6px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 12px !important;
    min-height: 30px !important;
}

.stMultiSelect span[data-baseweb="tag"] {
    background: rgba(196,149,106,0.15) !important;
    color: #5C3317 !important;
    font-size: 11px !important;
    border-radius: 4px !important;
    border: 1px solid rgba(196,149,106,0.35) !important;
    font-weight: 500 !important;
}

/* ── BUTTON ── */
.stButton > button {
    background: rgba(74,35,9,0.88) !important;
    color: #F4A7B9 !important;
    border: 1px solid rgba(196,149,106,0.4) !important;
    border-radius: 6px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    height: 32px !important;
    width: 100% !important;
    letter-spacing: 0.3px !important;
    backdrop-filter: blur(8px) !important;
}

.stButton > button:hover {
    background: rgba(139,90,60,0.9) !important;
    color: #FDF6EC !important;
}

.stAlert {
    background: rgba(244,167,185,0.12) !important;
    border: 1px solid rgba(244,167,185,0.35) !important;
    border-radius: 6px !important;
    color: #1C0A00 !important;
    font-size: 12px !important;
}
            
[data-testid="stRadio"] p {
    color: #1C0A00 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}

[data-testid="stRadio"] label {
    color: #1C0A00 !important;
}

::-webkit-scrollbar { display:none; }
* { scrollbar-width:none; }
</style>

<!-- PARTICLE BACKGROUND -->
<div class="particle-bg" id="particleBg"></div>

<script>
(function() {
    const symbols = ['₹', '₹', '₹', '•', '◆', '₹', '▸', '₹'];
    const sizes   = [14, 18, 22, 28, 12, 16, 20, 24, 10];
    const container = document.getElementById('particleBg');
    if (!container) return;

    function spawn() {
        const el = document.createElement('div');
        el.className = 'particle';
        el.textContent = symbols[Math.floor(Math.random() * symbols.length)];
        el.style.left     = Math.random() * 100 + 'vw';
        el.style.fontSize = sizes[Math.floor(Math.random() * sizes.length)] + 'px';
        const dur = 8 + Math.random() * 12;
        const delay = Math.random() * -dur;
        el.style.animationDuration = dur + 's';
        el.style.animationDelay   = delay + 's';
        container.appendChild(el);
        setTimeout(() => el.remove(), (dur + Math.abs(delay)) * 1000 + 500);
    }

    for (let i = 0; i < 40; i++) spawn();
    setInterval(spawn, 600);
})();
</script>
""", unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────────────
@st.cache_data
def load_data():
    kpi    = pd.read_csv("data/indian_banks_kpi_ratios.csv")
    income = pd.read_csv("data/indian_banks_income_statement.csv")
    assets = pd.read_csv("data/indian_banks_assets_liabilities.csv")
    return kpi, income, assets

kpi, income, assets = load_data()

# ── CHART THEME ───────────────────────────────────────────
BG    = "rgba(253,246,236,0)"
GRID  = "rgba(196,149,106,0.15)"
TEXT  = "#1C0A00"
MUTED = "#8B5A3C"
BROWN = "#4A2309"
TAN   = "#C4956A"
PINK  = "#F4A7B9"
ROSE  = "#E8637A"
CREAM = "#FDF6EC"

def ct(fig, h=200, leg="top"):
    if leg == "top":
        legend = dict(bgcolor="rgba(0,0,0,0)", font=dict(size=8,color=MUTED),
                      orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    else:
        legend = dict(bgcolor="rgba(0,0,0,0)", font=dict(size=7.5,color=MUTED),
                      orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5,
                      itemsizing="constant")
    fig.update_layout(
        paper_bgcolor="rgba(253,246,236,0.0)",
        plot_bgcolor="rgba(253,246,236,0.0)",
        font=dict(family="Outfit", color=TEXT, size=9),
        height=h, margin=dict(l=4,r=10,t=6,b=4),
        legend=legend,
        xaxis=dict(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(size=8,color=MUTED), title="", color=TEXT),
        yaxis=dict(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(size=8,color=MUTED), title="", color=TEXT),
    )
    return fig

# ── NAV ───────────────────────────────────────────────────
RBI_LOGO = "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npBFxlYRKdy7gn2h9dgcgL9Uj2IxnMSzmWglSnKMURUbUBljOJDimRZw1qTFX6FcTq1qG4WWcj9pyVKirU1WKodRCUU4IJyUpM3K75KObSgCuTCrqNMBlOboG9qFQrcXTU1/84qNOQAdmaXrmnsNHOcPYGUEY3jizQxIc0H1ZHMnLh8Y5oKboDHALhrUb2HRBdyWBbA7YCRgVYBCSTHaARpIET4EQ1wXRFU7F9L8HNDYSLY8zDU4HJouRN1g0juPKwsivC/0EORKeGIq/m/QGIHuncrD6E080RoXblsnUfVkWfCHKA/aBEnfX0QLJK8dLmM+4VLmYhB3Z0OgQTHQIZDUSWHyF5fNQdDAEkHJAykq2HhsNoR179REpMhzF6vWBqbBLH2FNX4b5EDzsrcl/qOT9wkitx6k6cvtI1G/RPsB2ZMTnZ0wpBo+QfYhcMaqD2on6kctZln0Yp7ge4aXcV9jLFR7p+kvwNt3SN3lW7tFP3Fiz4mgl7s2E0tIKaFts/aKf61FSPFw+4Ry9FnkIABag8lfs6i7WnY9F95Ihf67u6rpJEj8E2+oHExutObfbNFUHLSyFeE9UFlAnnHu9TNYD3BLcIFvr4aYoCGbrg3uTLzniG1MTEWp+TY9ihrKGPeqLsxfSDWbtadP91hceElD5vUb4dPoIqj1DuwczzP9T5D+Cx6BJZCUVtgLL4OXDZrtDLHkjp6nocH2NPqnwBTXRQRQFK/uj/xEf/RP/9oADAMBAAIAAwAAABDzzzzzzzzzzzzzzzzzwf7zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzhHjusdf8Aqic+88888888888888888888888884Tv9ax+9upuMOzV88888888888888888888888CUIqe/Y4pFn+e8azkj888888888888888888885K7gQ1q3lw7btUvwNsEn888888888888888888B29K2jkfOvR/vxjgnG1PoY8888888888888888AG4a+E3z4f2d2ILM2DTcj0t0888888888888888NmVcP5zGWxt07b6f4ekFc6jb88888888888888tF0LNXV87nFpYGzDG2tXG428EJ8888888888888zIo0TYt9bEdJDlCERFZu5vqKAK8888888888888Yj8wc+Y1pIkVf3AmxNegZDx559888888888888x7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"
st.markdown(f'''
<div class="nav">
  <div style="display:flex;align-items:center;gap:10px;">
    <img src="data:image/jpeg;base64,{RBI_LOGO}" style="height:40px;width:40px;border-radius:50%;object-fit:cover;object-position:center;transform:scale(1.15);border:1.5px solid #C4956A;filter:sepia(0.4) contrast(1.1) brightness(0.85);"/>
    <div class="nav-logo">India's <em>Banking</em> Dashboard</div>
  </div>
  <div class="nav-meta">10 Banks · FY 2020–2024 · Public &amp; Private · Source: RBI Annual Reports</div>
</div>
''', unsafe_allow_html=True)

# ── FILTERS ───────────────────────────────────────────────
fc1, fc2, fc3 = st.columns([0.8, 1.2, 4])
with fc1:
    selected_year = st.selectbox("📅 Year", sorted(kpi["Year"].unique(), reverse=True), label_visibility="collapsed")
with fc2:
    bank_type_opt = st.radio("Type", ["All", "Public", "Private"], horizontal=True, label_visibility="collapsed")
with fc3:
    pass

st.markdown("<div style='height:1px;background:rgba(196,149,106,0.3);'></div>", unsafe_allow_html=True)

# ── FILTER ────────────────────────────────────────────────
sel_types = list(kpi["Bank_Type"].unique()) if bank_type_opt == "All" else [bank_type_opt]
kpi_f = kpi[(kpi["Year"]==selected_year) & (kpi["Bank_Type"].isin(sel_types))]

# ── KPI ───────────────────────────────────────────────────
sbi_a  = kpi[(kpi["Bank"]=="SBI")&(kpi["Year"]==selected_year)]["Total_Assets_Crore"].values
sbi_v  = f"₹{sbi_a[0]/100000:.1f}L Cr" if len(sbi_a) else "N/A"
best_p = kpi_f["Net_Profit_Crore"].max() if len(kpi_f) else 0
lo_npa = kpi_f["Gross_NPA_Pct"].min() if len(kpi_f) else 0
b_roe  = kpi_f["Return_On_Equity_Pct"].max() if len(kpi_f) else 0
av_car = kpi[(kpi["Bank_Type"]=="Private")&(kpi["Year"]==selected_year)]["Capital_Adequacy_Ratio_Pct"].mean()
bp_b   = kpi_f.loc[kpi_f["Net_Profit_Crore"].idxmax(),"Bank"] if len(kpi_f) else ""
npa_b  = kpi_f.loc[kpi_f["Gross_NPA_Pct"].idxmin(),"Bank"] if len(kpi_f) else ""
roe_b  = kpi_f.loc[kpi_f["Return_On_Equity_Pct"].idxmax(),"Bank"] if len(kpi_f) else ""

st.markdown(f"""
<div class="kpi-strip">
  <div class="kpi-cell"><div class="kpi-bar"></div><div class="kpi-lbl">Total Assets (SBI)</div><div class="kpi-val">{sbi_v}</div><div class="kpi-sub">▲ 15.2% vs FY23</div></div>
  <div class="kpi-cell"><div class="kpi-bar"></div><div class="kpi-lbl">Best Net Profit</div><div class="kpi-val">₹{best_p:,.0f} Cr</div><div class="kpi-sub">▲ {bp_b}</div></div>
  <div class="kpi-cell"><div class="kpi-bar"></div><div class="kpi-lbl">Lowest NPA</div><div class="kpi-val">{lo_npa:.2f}%</div><div class="kpi-sub">▲ {npa_b}</div></div>
  <div class="kpi-cell"><div class="kpi-bar"></div><div class="kpi-lbl">Best ROE</div><div class="kpi-val">{b_roe:.1f}%</div><div class="kpi-sub">▲ {roe_b}</div></div>
  <div class="kpi-cell"><div class="kpi-bar"></div><div class="kpi-lbl">Avg CAR (Private)</div><div class="kpi-val">{av_car:.1f}%</div><div class="kpi-sub">▲ vs 9% RBI Min</div></div>
</div>
""", unsafe_allow_html=True)

# ── ROW 1 ─────────────────────────────────────────────────
r1a, r1b, r1c = st.columns([3, 1.3, 1.7])

with r1a:
    st.markdown('<p class="clbl">Net Profit by Bank (₹ Crore)</p>', unsafe_allow_html=True)
    df1 = kpi_f.sort_values("Net_Profit_Crore")
    fig1 = px.bar(df1, x="Net_Profit_Crore", y="Bank", color="Bank_Type", orientation="h",
                  color_discrete_map={"Public": BROWN, "Private": TAN},
                  text=df1["Net_Profit_Crore"].apply(lambda x: f"₹{x:,.0f}"))
    fig1.update_traces(textposition="outside", textfont=dict(size=8, color=MUTED), marker_line_width=0)
    ct(fig1, 208, "top")
    fig1.update_layout(bargap=0.25, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=9,color=MUTED), title=dict(text="")))
    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

with r1b:
    st.markdown('<p class="clbl">Asset Share</p>', unsafe_allow_html=True)
    adf = kpi_f.groupby("Bank_Type")["Total_Assets_Crore"].sum().reset_index()
    fig2 = go.Figure(go.Pie(
        labels=adf["Bank_Type"], values=adf["Total_Assets_Crore"],
        hole=0.58,
        marker=dict(colors=[BROWN, TAN], line=dict(color="#FDF6EC", width=3)),
        textposition="outside",
        textinfo="label+percent",
        textfont=dict(size=10, color=TEXT),
        pull=[0.03, 0]
    ))
    ct(fig2, 208)
    fig2.update_layout(showlegend=False, margin=dict(l=20,r=20,t=10,b=10))
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

with r1c:
    st.markdown('<p class="clbl">Gross NPA % — Lower is Healthier</p>', unsafe_allow_html=True)
    df3 = kpi_f.sort_values("Gross_NPA_Pct")
    bar_colors = [TAN if v < 2 else PINK if v < 3.5 else ROSE for v in df3["Gross_NPA_Pct"]]
    fig3 = go.Figure(go.Bar(
        x=df3["Gross_NPA_Pct"], y=df3["Bank"], orientation="h",
        marker_color=bar_colors, marker_line_width=0,
        text=[f"{v:.2f}%" for v in df3["Gross_NPA_Pct"]],
        textposition="outside", textfont=dict(size=8, color=MUTED)
    ))
    ct(fig3, 208)
    fig3.update_layout(bargap=0.25, showlegend=False)
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

# ── ROW 2 ─────────────────────────────────────────────────
r2a, r2b, r2c = st.columns([2, 2, 2])

with r2a:
    st.markdown('<p class="clbl">NPA Recovery 2020–2024</p>', unsafe_allow_html=True)
    palette = [BROWN, TAN, ROSE, PINK, "#A0522D", "#CD853F", "#DEB887", "#D2691E", "#8B4513", "#BC8F5F"]
    fig4 = px.line(kpi, x="Year", y="Gross_NPA_Pct", color="Bank", markers=True,
                   color_discrete_sequence=palette)
    fig4.update_traces(line=dict(width=1.8), marker=dict(size=4))
    ct(fig4, 186, "bottom")
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

with r2b:
    st.markdown('<p class="clbl">Net Profit Growth — Top 4 Banks</p>', unsafe_allow_html=True)
    top4 = kpi[kpi["Bank"].isin(["SBI","HDFC Bank","ICICI Bank","Axis Bank"])]
    fig5 = px.area(top4, x="Year", y="Net_Profit_Crore", color="Bank",
                   color_discrete_map={"SBI":BROWN,"HDFC Bank":TAN,"ICICI Bank":ROSE,"Axis Bank":PINK})
    fig5.update_traces(line=dict(width=1.8))
    ct(fig5, 186, "bottom")
    st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})

with r2c:
    st.markdown('<p class="clbl">ROA vs ROE — Bubble = Total Assets</p>', unsafe_allow_html=True)
    kpi_sc = kpi_f.copy()
    kpi_sc["BankShort"] = (kpi_sc["Bank"]
        .str.replace(" Bank","").str.replace(" Mahindra","")
        .str.replace("Indian Overseas","IOB").str.replace("Central Bank of India","CBI")
        .str.replace("Punjab National","PNB"))
    fig6 = px.scatter(kpi_sc, x="Return_On_Assets_Pct", y="Return_On_Equity_Pct",
                      size="Total_Assets_Crore", color="Bank_Type", text="BankShort",
                      color_discrete_map={"Public":BROWN,"Private":TAN}, size_max=40)
    fig6.update_traces(textposition="top center", textfont=dict(size=8,color=MUTED),
                       marker=dict(line=dict(width=1.5,color="#FDF6EC")))
    fig6.add_hline(y=15, line_dash="dot", line_color=GRID, line_width=1)
    fig6.add_vline(x=1.0, line_dash="dot", line_color=GRID, line_width=1)
    ct(fig6, 186)
    fig6.update_layout(showlegend=False)
    st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar": False})

# ── ACTION ROW ────────────────────────────────────────────
st.markdown("<div style='height:1px;background:rgba(196,149,106,0.3);'></div>", unsafe_allow_html=True)
ba, bb, bc, bd = st.columns(4)

with ba:
    if st.button("🤖 AI Sector Insight", use_container_width=True):
        with st.spinner("Analysing..."):
            try:
                from utils.ai_insights import get_sector_insight
                insight = get_sector_insight(
                    kpi_f["Gross_NPA_Pct"].mean(),
                    kpi_f["Return_On_Equity_Pct"].mean(),
                    kpi_f["Total_Assets_Crore"].sum(),
                    selected_year
                )
                st.info(insight)
            except Exception as e:
                st.error(f"Check GROQ_API_KEY in .env — {e}")

with bb:
    if st.button("📄 Export PDF", use_container_width=True):
        try:
            from utils.pdf_export import generate_pdf
            pdf_bytes = generate_pdf(kpi_f, selected_year)
            st.download_button("⬇ Download PDF", pdf_bytes,
                               f"banking_dashboard_{selected_year}.pdf",
                               "application/pdf", use_container_width=True)
        except Exception as e:
            st.error(f"PDF error: {e}")

with bc:
    if st.button("🔍 Bank Deep Dive →", use_container_width=True):
        st.switch_page("pages/bank_detail.py")

with bd: 
    if st.button("🗄️ SQL Explorer →", use_container_width=True):
        st.switch_page("pages/sql_explorer.py")

# ── FOOTER ────────────────────────────────────────────────
st.markdown("""
<div style="background:rgba(74,35,9,0.85);backdrop-filter:blur(8px);border-top:1px solid rgba(196,149,106,0.3);padding:4px 20px;display:flex;justify-content:space-between;position:relative;z-index:5;">
  <span style="font-family:Outfit;font-size:9px;color:rgba(253,246,236,0.4);">Source: RBI Annual Reports · BSE Filings · FY 2020–2024</span>
  <span style="font-family:Outfit;font-size:9px;color:rgba(253,246,236,0.4);">India's Banking Dashboard</span>
</div>
""", unsafe_allow_html=True)