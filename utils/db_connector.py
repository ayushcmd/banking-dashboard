import sqlite3
import pandas as pd
import os

DB_PATH = "banking.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    if os.path.exists(DB_PATH):
        return

    conn = get_connection()

    assets = pd.read_csv("data/indian_banks_assets_liabilities.csv")
    income = pd.read_csv("data/indian_banks_income_statement.csv")
    kpi    = pd.read_csv("data/indian_banks_kpi_ratios.csv")

    assets.to_sql("assets_liabilities", conn, if_exists="replace", index=False)
    income.to_sql("income_statement",   conn, if_exists="replace", index=False)
    kpi.to_sql("kpi_ratios",            conn, if_exists="replace", index=False)

    conn.close()
    print("Database initialized successfully.")

def run_query(query: str) -> pd.DataFrame:
    conn = get_connection()
    try:
        df = pd.read_sql_query(query, conn)
    finally:
        conn.close()
    return df