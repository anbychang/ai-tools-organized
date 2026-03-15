"""模組 A：資料收集 — 抓取股價 & 計算技術指標"""
import yfinance as yf
import pandas as pd
import numpy as np


def fetch_stock(ticker: str, start: str, end: str) -> pd.DataFrame:
    """從 Yahoo Finance 下載股票數據"""
    print(f"[資料收集] 下載 {ticker} ({start} ~ {end})...")
    df = yf.download(ticker, start=start, end=end, progress=False)
    df = df.droplevel("Ticker", axis=1) if isinstance(df.columns, pd.MultiIndex) else df
    df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
    df.dropna(inplace=True)
    print(f"[資料收集] 取得 {len(df)} 筆日線資料")
    return df


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """計算技術指標"""
    close = df["Close"]

    # SMA
    df["SMA_5"] = close.rolling(5).mean()
    df["SMA_20"] = close.rolling(20).mean()

    # EMA
    df["EMA_12"] = close.ewm(span=12).mean()
    df["EMA_26"] = close.ewm(span=26).mean()

    # MACD
    df["MACD"] = df["EMA_12"] - df["EMA_26"]
    df["MACD_Signal"] = df["MACD"].ewm(span=9).mean()

    # RSI
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # Bollinger Bands
    sma20 = close.rolling(20).mean()
    std20 = close.rolling(20).std()
    df["BB_Upper"] = sma20 + 2 * std20
    df["BB_Lower"] = sma20 - 2 * std20
    df["BB_Width"] = (df["BB_Upper"] - df["BB_Lower"]) / sma20

    # 成交量變化
    df["Volume_Change"] = df["Volume"].pct_change()

    # 日報酬率
    df["Daily_Return"] = close.pct_change()

    df.dropna(inplace=True)
    print(f"[資料收集] 技術指標計算完成，共 {len(df.columns)} 個欄位")
    return df
