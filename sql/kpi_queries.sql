-- Best CAR bank per year
SELECT bank_name, year, car
FROM kpi_ratios
ORDER BY year, car DESC;

-- Average ROE by bank type per year
SELECT bank_type, year, ROUND(AVG(roe), 2) AS avg_roe
FROM kpi_ratios
GROUP BY bank_type, year
ORDER BY year;

-- Banks with ROE above 10 consistently
SELECT bank_name, COUNT(*) AS years_above_10
FROM kpi_ratios
WHERE roe > 10
GROUP BY bank_name
ORDER BY years_above_10 DESC;

-- Top 3 banks by ROA in FY2024
SELECT bank_name, roa
FROM kpi_ratios
WHERE year = 2024
ORDER BY roa DESC
LIMIT 3;

-- Public vs Private avg CAR comparison
SELECT bank_type, ROUND(AVG(car), 2) AS avg_car
FROM kpi_ratios
GROUP BY bank_type;