"""
NGX Stock Screener
Technical analysis and momentum screening for Nigerian Exchange listed equities.
"""
import pandas as pd
import numpy as np
from typing import Dict, List

NGX_STOCKS = {
    "Banking": ["GTCO", "ZENITHBANK", "UBA", "ACCESSCORP", "FBNH", "STANBIC"],
    "Telecoms": ["MTNN", "AIRTELAFRI"],
    "Oil & Gas": ["SEPLAT", "TOTAL", "CONOIL"],
    "Industrials": ["DANGCEM", "BUACEMENT"],
    "Consumer": ["NB", "UNILEVER", "NESTLE"],
}

def compute_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """Compute Relative Strength Index."""
    delta = prices.diff()
    gain = delta.clip(lower=0).rolling(window=period).mean()
    loss = (-delta.clip(upper=0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def compute_macd(prices: pd.Series, fast=12, slow=26, signal=9):
    """Compute MACD line and signal line."""
    ema_fast = prices.ewm(span=fast).mean()
    ema_slow = prices.ewm(span=slow).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal).mean()
    return macd, signal_line

def compute_moving_averages(prices: pd.Series) -> pd.DataFrame:
    """Compute 20, 50, and 200-day moving averages."""
    return pd.DataFrame({
        "price": prices,
        "ma20": prices.rolling(20).mean(),
        "ma50": prices.rolling(50).mean(),
        "ma200": prices.rolling(200).mean(),
    })

def generate_signal(row: pd.Series) -> str:
    """Generate BUY / HOLD / WATCH signal based on indicators."""
    if row["rsi"] < 35 and row["macd"] > row["signal"]:
        return "BUY"
    elif row["rsi"] > 70:
        return "OVERBOUGHT"
    elif row["price"] > row["ma50"]:
        return "HOLD"
    else:
        return "WATCH"

def screen_portfolio(price_data: Dict[str, pd.Series]) -> pd.DataFrame:
    """Run screening across all stocks and return ranked results."""
    results = []
    for ticker, prices in price_data.items():
        if len(prices) < 30:
            continue
        rsi = compute_rsi(prices).iloc[-1]
        macd, signal = compute_macd(prices)
        mas = compute_moving_averages(prices).iloc[-1]
        pct_52w_high = (prices.iloc[-1] / prices.rolling(252).max().iloc[-1]) * 100
        row = {
            "ticker": ticker,
            "price": round(prices.iloc[-1], 2),
            "rsi": round(rsi, 1),
            "macd": round(macd.iloc[-1], 4),
            "signal": round(signal.iloc[-1], 4),
            "ma50": round(mas["ma50"], 2),
            "pct_52w_high": round(pct_52w_high, 1),
        }
        row["recommendation"] = generate_signal(pd.Series(row))
        results.append(row)
    return pd.DataFrame(results).sort_values("rsi")

def generate_sample_prices(n=300, base=100, drift=0.0003, vol=0.015) -> pd.Series:
    """Generate realistic-looking price series for demo purposes."""
    np.random.seed(42)
    returns = np.random.normal(drift, vol, n)
    prices = base * np.exp(np.cumsum(returns))
    return pd.Series(prices)

if __name__ == "__main__":
    print("NGX Stock Screener - Sample Run")
    tickers = ["GTCO", "ZENITHBANK", "MTNN", "DANGCEM", "SEPLAT"]
    price_data = {t: generate_sample_prices(base=np.random.uniform(5, 800)) for t in tickers}
    results = screen_portfolio(price_data)
    print(results.to_string(index=False))
