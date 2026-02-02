# World Bank Development Indicators

## Data Source

**Primary:** World Bank Data API via `wbdata` Python package.

**Alternative:** [World Bank DataBank](https://databank.worldbank.org/) – select indicators, countries, time period; download as CSV/Excel.

## Indicators Used

| Code | Description |
|------|-------------|
| NY.GDP.MKTP.CD | GDP (current US$) |
| NY.GDP.PCAP.CD | GDP per capita (current US$) |
| SP.URB.TOTL.IN.ZS | Urban population (% of total) |

## Countries (Sample)

USA, DEU, FRA, GBR, NLD, BRA, IND, CHN, JPN – key markets for multinational analysis.

## Cached Data

If API fails, the script saves/loads from `data/raw/wb_indicators.csv` for offline use.
