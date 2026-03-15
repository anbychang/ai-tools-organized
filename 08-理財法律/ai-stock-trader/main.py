"""
AI Stock Trader — 整合系統
==========================
整合四大模組：資料收集 → 股價預測 → RL 交易決策 → 績效報表

用法：python main.py --ticker AAPL --start 2022-01-01 --end 2024-01-01
"""
import argparse
from modules.data_fetcher import fetch_stock, add_indicators
from modules.predictor import train_predictor
from modules.rl_trader import TradingEnvironment, train_trader
from modules.report import generate_report


FEATURE_COLS = [
    "SMA_5", "SMA_20", "MACD", "MACD_Signal",
    "RSI", "BB_Width", "Volume_Change", "Daily_Return",
]


def run(ticker, start, end, rl_episodes):
    print("=" * 50)
    print(f"  AI Stock Trader")
    print(f"  標的: {ticker} | 期間: {start} ~ {end}")
    print("=" * 50)

    # ── 模組 A：資料收集 ──
    df = fetch_stock(ticker, start, end)
    df = add_indicators(df)
    print()

    # ── 模組 B：LSTM 股價預測 ──
    _, _, _, lstm_acc = train_predictor(df, FEATURE_COLS, window=20, epochs=30)
    print()

    # ── 模組 C：RL 交易決策 ──
    # 標準化特徵
    df_norm = df.copy()
    for col in FEATURE_COLS:
        mean = df_norm[col].mean()
        std = df_norm[col].std() + 1e-8
        df_norm[col] = (df_norm[col] - mean) / std

    env = TradingEnvironment(df_norm, FEATURE_COLS)
    agent, rl_results = train_trader(env, episodes=rl_episodes)
    print()

    # 最終跑一次（不探索）
    print("[最終測試] AI 用學到的策略跑一次...")
    agent.epsilon = 0  # 關閉探索
    state = env.reset()
    while True:
        action = agent.act(state, training=False)
        state, _, done = env.step(action)
        if done:
            break
    print(f"[最終測試] 報酬率: {env.total_return:+.2%} | 交易次數: {env.total_trades}")
    print()

    # ── 模組 D：績效報表 ──
    metrics = generate_report(
        df, env.history, ticker,
        lstm_accuracy=lstm_acc,
        rl_results=rl_results,
    )

    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Stock Trader")
    parser.add_argument("--ticker", type=str, default="AAPL", help="股票代碼")
    parser.add_argument("--start", type=str, default="2022-01-01", help="開始日期")
    parser.add_argument("--end", type=str, default="2024-01-01", help="結束日期")
    parser.add_argument("--episodes", type=int, default=50, help="RL 訓練回合數")
    args = parser.parse_args()

    run(args.ticker, args.start, args.end, args.episodes)
