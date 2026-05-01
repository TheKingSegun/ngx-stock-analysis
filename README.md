# NGX Stock Analysis & Screener

A Python-based stock analysis tool for the **Nigerian Exchange (NGX)**, identifying momentum signals, technical breakouts, and sector rotation patterns across banking, telecoms, oil & gas, and industrial sectors.

## Project Overview

This screener analyses NGX-listed equities using publicly available price data, computing technical indicators and ranking stocks by momentum and value signals.

## Key Features
- Momentum screening (RSI, MACD, 52-week high proximity)
- Sector-level rotation analysis (banking, telecoms, oil & gas, industrials)
- Moving average crossover signals (50-day / 200-day)
- Dividend yield vs. earnings growth scoring
- Exportable watchlist with buy/hold/watch flags

## Stocks Covered
| Sector | Tickers |
|--------|---------|
| Banking | GTCO, ZENITHBANK, UBA, ACCESSCORP, FBNH |
| Telecoms | MTNN, AIRTELAFRI |
| Oil & Gas | SEPLAT, TOTAL, CONOIL |
| Industrials | DANGCEM, BUACEMENT, NESTLE |
| Consumer Goods | NIGERIAN BREWERIES, UNILEVER |

## Tools & Technologies
- Python (pandas, numpy, matplotlib, mplfinance)
- TA-Lib for technical indicators
- Jupyter Notebook
- Power BI for sector dashboard

## How to Run
```bash
pip install -r requirements.txt
jupyter notebook notebooks/ngx_screener.ipynb
```

## Data Sources
- [NGX Group](https://ngxgroup.com/) — Daily price data
- [Investdata](https://investdata.com.ng/)
- [Proshare](https://proshareng.com/)
