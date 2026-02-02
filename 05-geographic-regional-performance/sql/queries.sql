-- Geographic & Regional Performance – SQL-style aggregations
-- (World Bank data is loaded via Python/wbdata; these queries illustrate the logic)

-- 1. GDP per capita by country (latest year)
-- SELECT country, GDP_per_capita
-- FROM regional_indicators
-- WHERE date = (SELECT MAX(date) FROM regional_indicators)
-- ORDER BY GDP_per_capita DESC;

-- 2. YoY GDP growth by country
-- WITH gdp_lag AS (
--   SELECT country, date, GDP,
--          LAG(GDP) OVER (PARTITION BY country ORDER BY date) AS prev_gdp
--   FROM regional_indicators
-- )
-- SELECT country, date, (GDP - prev_gdp) / prev_gdp * 100 AS yoy_growth_pct
-- FROM gdp_lag
-- WHERE prev_gdp IS NOT NULL
-- ORDER BY country, date;

-- 3. Urbanization trend by country
-- SELECT country, date, Urban_pop_pct
-- FROM regional_indicators
-- ORDER BY country, date;

-- 4. Top 5 countries by GDP (latest)
-- SELECT country, GDP
-- FROM regional_indicators
-- WHERE date = (SELECT MAX(date) FROM regional_indicators)
-- ORDER BY GDP DESC
-- LIMIT 5;

-- 5. Composite economic health score (example: GDP per capita + urbanization)
-- SELECT country, date,
--        (GDP_per_capita / 1000) * 0.6 + Urban_pop_pct * 0.4 AS health_score
-- FROM regional_indicators
-- ORDER BY country, date;
