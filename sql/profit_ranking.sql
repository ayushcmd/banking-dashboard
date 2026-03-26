-- Profit rank all banks FY2024
SELECT bank_name, net_profit,
       RANK() OVER (ORDER BY net_profit DESC) AS profit_rank
FROM income_statement
WHERE year = 2024;

-- Top 4 profit growth from 2020 to 2024
SELECT 
    a.bank_name,
    a.net_profit AS profit_2020,
    b.net_profit AS profit_2024,
    ROUND(((b.net_profit - a.net_profit) / a.net_profit) * 100, 2) AS growth_pct
FROM income_statement a
JOIN income_statement b ON a.bank_name = b.bank_name
WHERE a.year = 2020 AND b.year = 2024
ORDER BY growth_pct DESC
LIMIT 4;

-- Year-wise total profit by bank type
SELECT bank_type, year, ROUND(SUM(net_profit), 2) AS total_profit
FROM income_statement
GROUP BY bank_type, year
ORDER BY year;

-- Banks that were loss-making any year
SELECT bank_name, year, net_profit
FROM income_statement
WHERE net_profit < 0
ORDER BY year;

-- Most consistent profitable bank (profit > 0 all 5 years)
SELECT bank_name, COUNT(*) AS profitable_years
FROM income_statement
WHERE net_profit > 0
GROUP BY bank_name
HAVING profitable_years = 5;