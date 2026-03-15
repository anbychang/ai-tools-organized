"""模組 D：報表 & 視覺化 — 產出績效報告"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def generate_report(df, env_history, ticker, lstm_accuracy, rl_results, output_dir="output"):
    """產出完整的交易績效報告"""
    print("[報表] 產出績效報告...")

    history = pd.DataFrame(env_history)

    # === 計算績效指標 ===
    final_value = history["portfolio_value"].iloc[-1]
    initial_value = history["portfolio_value"].iloc[0]
    total_return = (final_value - initial_value) / initial_value
    max_value = history["portfolio_value"].cummax()
    drawdown = (history["portfolio_value"] - max_value) / max_value
    max_drawdown = drawdown.min()

    # 買入持有比較
    first_price = df["Close"].iloc[0]
    last_price = df["Close"].iloc[-1]
    buy_hold_return = (last_price - first_price) / first_price

    total_trades = history[history["action"] != 0].shape[0]
    daily_returns = history["portfolio_value"].pct_change().dropna()
    sharpe = daily_returns.mean() / (daily_returns.std() + 1e-8) * np.sqrt(252)

    # === 建立圖表 ===
    fig = make_subplots(
        rows=4, cols=1,
        subplot_titles=(
            f"{ticker} 股價 & AI 交易訊號",
            "投資組合價值 vs 買入持有",
            "RL 訓練學習曲線",
            "回撤 (Drawdown)",
        ),
        vertical_spacing=0.08,
        row_heights=[0.35, 0.25, 0.2, 0.2],
    )

    # 1. 股價 + 買賣點
    fig.add_trace(go.Scatter(
        x=list(range(len(df))), y=df["Close"].values,
        name="股價", line=dict(color="#2196F3"),
    ), row=1, col=1)

    buys = history[history["action"] == 1]
    sells = history[history["action"] == 2]
    if len(buys) > 0:
        fig.add_trace(go.Scatter(
            x=buys["step"].values, y=buys["price"].values,
            mode="markers", name="買入",
            marker=dict(color="green", size=10, symbol="triangle-up"),
        ), row=1, col=1)
    if len(sells) > 0:
        fig.add_trace(go.Scatter(
            x=sells["step"].values, y=sells["price"].values,
            mode="markers", name="賣出",
            marker=dict(color="red", size=10, symbol="triangle-down"),
        ), row=1, col=1)

    # 2. 投組價值 vs 買入持有
    fig.add_trace(go.Scatter(
        x=list(range(len(history))), y=history["portfolio_value"].values,
        name="AI 策略", line=dict(color="#4CAF50"),
    ), row=2, col=1)

    buy_hold_values = 100000 * (df["Close"].values / df["Close"].values[0])
    fig.add_trace(go.Scatter(
        x=list(range(len(buy_hold_values))), y=buy_hold_values,
        name="買入持有", line=dict(color="#FF9800", dash="dash"),
    ), row=2, col=1)

    # 3. RL 學習曲線
    fig.add_trace(go.Scatter(
        x=list(range(len(rl_results))), y=[r * 100 for r in rl_results],
        name="每回合報酬率 %", line=dict(color="#9C27B0"),
    ), row=3, col=1)

    # 4. Drawdown
    fig.add_trace(go.Scatter(
        x=list(range(len(drawdown))), y=drawdown.values * 100,
        name="回撤 %", fill="tozeroy",
        line=dict(color="#F44336"),
    ), row=4, col=1)

    fig.update_layout(
        height=1200,
        title_text=f"AI Stock Trader — {ticker} 績效報告",
        showlegend=True,
        template="plotly_dark",
    )

    chart_path = f"{output_dir}/report_{ticker}.html"
    fig.write_html(chart_path)

    # === 文字報告 ===
    report = f"""
╔══════════════════════════════════════════╗
║        AI Stock Trader 績效報告           ║
╠══════════════════════════════════════════╣
║  標的：{ticker:<35s}║
╠══════════════════════════════════════════╣
║  [交易績效]                                ║
║  ─────────────────────────────           ║
║  AI 策略報酬率：{total_return:>+10.2%}                  ║
║  買入持有報酬率：{float(buy_hold_return):>+10.2%}                  ║
║  超額報酬：    {float(total_return - buy_hold_return):>+10.2%}                  ║
║  Sharpe Ratio：{float(sharpe):>10.2f}                  ║
║  最大回撤：    {float(max_drawdown):>10.2%}                  ║
║  總交易次數：  {total_trades:>10d}                  ║
╠══════════════════════════════════════════╣
║  [AI 模型表現]                             ║
║  ─────────────────────────────           ║
║  預測模型方向準確率：{lstm_accuracy:>7.1%}              ║
║  RL 最終回合報酬率：{rl_results[-1]:>+8.1%}              ║
╠══════════════════════════════════════════╣
║  [互動圖表]：{chart_path:<27s}║
╚══════════════════════════════════════════╝
"""
    print(report)

    report_path = f"{output_dir}/report_{ticker}.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    return {
        "total_return": total_return,
        "buy_hold_return": float(buy_hold_return),
        "sharpe": float(sharpe),
        "max_drawdown": float(max_drawdown),
        "total_trades": total_trades,
        "chart_path": chart_path,
    }
