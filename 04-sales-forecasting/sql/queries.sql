-- Sales Performance - SQL (for loaded sales data)
-- Table: sales (date, region, category, sales, profit)

-- YoY growth by region
-- SELECT region, EXTRACT(YEAR FROM date) AS year, SUM(sales) AS total_sales,
--        LAG(SUM(sales)) OVER (PARTITION BY region ORDER BY EXTRACT(YEAR FROM date)) AS prev_year,
--        ROUND(100.0 * (SUM(sales) - LAG(SUM(sales)) OVER (PARTITION BY region ORDER BY EXTRACT(YEAR FROM date))) / LAG(SUM(sales)) OVER (PARTITION BY region ORDER BY EXTRACT(YEAR FROM date)), 2) AS yoy_growth_pct
-- FROM sales
-- GROUP BY region, EXTRACT(YEAR FROM date);
