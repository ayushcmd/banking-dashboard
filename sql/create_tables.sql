-- Assets & Liabilities
CREATE TABLE IF NOT EXISTS assets_liabilities (
    bank_name     TEXT,
    year          INTEGER,
    total_assets  REAL,
    total_loans   REAL,
    total_deposits REAL,
    net_worth     REAL,
    bank_type     TEXT
);

-- Income Statement
CREATE TABLE IF NOT EXISTS income_statement (
    bank_name       TEXT,
    year            INTEGER,
    net_profit      REAL,
    total_income    REAL,
    interest_income REAL,
    operating_cost  REAL,
    bank_type       TEXT
);

-- KPI Ratios
CREATE TABLE IF NOT EXISTS kpi_ratios (
    bank_name TEXT,
    year      INTEGER,
    npa       REAL,
    car       REAL,
    roe       REAL,
    roa       REAL,
    bank_type TEXT
);