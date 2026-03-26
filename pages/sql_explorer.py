import streamlit as st
import plotly.express as px
from utils.db_connector import run_query, init_db

init_db()

st.title("🗄️ SQL Explorer")
st.markdown("Run pre-built queries on the banking database or write your own.")

QUERIES = {
    "Top banks by profit in FY2024": """
        SELECT bank_name, net_profit,
               RANK() OVER (ORDER BY net_profit DESC) AS profit_rank
        FROM income_statement WHERE year = 2024
    """,
    "NPA recovery 2020 → 2024": """
        SELECT a.bank_name, a.npa AS npa_2020, b.npa AS npa_2024,
               ROUND(a.npa - b.npa, 2) AS npa_reduction
        FROM kpi_ratios a
        JOIN kpi_ratios b ON a.bank_name = b.bank_name
        WHERE a.year = 2020 AND b.year = 2024
        ORDER BY npa_reduction DESC
    """,
    "Average NPA trend by year": """
        SELECT year, ROUND(AVG(npa), 2) AS avg_npa
        FROM kpi_ratios GROUP BY year ORDER BY year
    """,
    "Public vs Private avg CAR": """
        SELECT bank_type, ROUND(AVG(car), 2) AS avg_car
        FROM kpi_ratios GROUP BY bank_type
    """,
    "Banks in danger zone (NPA > 3.5% in 2024)": """
        SELECT bank_name, npa FROM kpi_ratios
        WHERE year = 2024 AND npa > 3.5 ORDER BY npa DESC
    """,
    "Profit growth % from 2020 to 2024": """
        SELECT a.bank_name,
               ROUND(((b.net_profit - a.net_profit) / a.net_profit) * 100, 2) AS growth_pct
        FROM income_statement a
        JOIN income_statement b ON a.bank_name = b.bank_name
        WHERE a.year = 2020 AND b.year = 2024
        ORDER BY growth_pct DESC
    """,
}

mode = st.radio("Mode", ["Preset Queries", "Custom SQL"], horizontal=True)

if mode == "Preset Queries":
    selected = st.selectbox("Pick a query", list(QUERIES.keys()))
    query = QUERIES[selected]
    st.code(query.strip(), language="sql")

    if st.button("Run Query"):
        df = run_query(query)
        st.dataframe(df, use_container_width=True)

        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        text_cols = df.select_dtypes(include="object").columns.tolist()

        if numeric_cols and text_cols:
            fig = px.bar(
                df,
                x=text_cols[0],
                y=numeric_cols[0],
                color=text_cols[0],
                title=selected
            )
            st.plotly_chart(fig, use_container_width=True)

else:
    custom_query = st.text_area("Write your SQL query", height=150,
                                 placeholder="SELECT * FROM kpi_ratios LIMIT 10")
    if st.button("Run"):
        try:
            df = run_query(custom_query)
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Query failed: {e}")