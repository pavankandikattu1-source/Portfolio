-- Financial Data Analysis - SQL (for loaded stock/returns data)
-- Table: stock_returns (date, ticker, return_pct)

-- Volatility by ticker (std of daily returns, annualized)
-- SELECT ticker, STDDEV(return_pct) * SQRT(252) * 100 AS annual_vol_pct
-- FROM stock_returns
-- GROUP BY ticker;

-- Average return by ticker
-- SELECT ticker, AVG(return_pct) * 252 * 100 AS annual_return_pct
-- FROM stock_returns
-- GROUP BY ticker;
