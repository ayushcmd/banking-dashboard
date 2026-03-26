-- Highest NPA bank each year
SELECT year, bank_name, npa
FROM kpi_ratios k1
WHERE npa = (
    SELECT MAX(npa) FROM kpi_ratios k2
    WHERE k2.year = k1.year
)
ORDER BY year;

-- NPA recovery: banks that reduced NPA from 2020 to 2024
SELECT 
    a.bank_name,
    a.npa AS npa_2020,
    b.npa AS npa_2024,
    ROUND(a.npa - b.npa, 2) AS npa_reduction
FROM kpi_ratios a
JOIN kpi_ratios b ON a.bank_name = b.bank_name
WHERE a.year = 2020 AND b.year = 2024
ORDER BY npa_reduction DESC;

-- Banks still above 3.5% NPA in 2024 (danger zone)
SELECT bank_name, npa
FROM kpi_ratios
WHERE year = 2024 AND npa > 3.5
ORDER BY npa DESC;

-- Year-wise average NPA trend
SELECT year, ROUND(AVG(npa), 2) AS avg_npa
FROM kpi_ratios
GROUP BY year
ORDER BY year;

-- Public vs Private avg NPA per year
SELECT bank_type, year, ROUND(AVG(npa), 2) AS avg_npa
FROM kpi_ratios
GROUP BY bank_type, year
ORDER BY year;