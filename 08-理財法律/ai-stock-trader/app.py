"""AI Stock Trader — Streamlit Dashboard"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from modules.data_fetcher import fetch_stock, add_indicators
from modules.predictor import train_predictor
from modules.rl_trader import TradingEnvironment, DQNTrader, train_trader

st.set_page_config(page_title="AI Stock Trader", layout="wide")

# ── Sidebar ──
st.sidebar.title("AI Stock Trader")
st.sidebar.markdown("---")

ticker = st.sidebar.text_input("股票代號", value="AAPL")
start = st.sidebar.date_input("開始日期", value=pd.to_datetime("2022-01-01"))
end = st.sidebar.date_input("結束日期", value=pd.to_datetime("2024-01-01"))
initial_balance = st.sidebar.number_input("初始資金 ($)", value=100000, step=10000)
episodes = st.sidebar.slider("RL 訓練回合數", min_value=10, max_value=200, value=50, step=10)

run = st.sidebar.button("開始分析", type="primary", use_container_width=True)

# ── Feature columns ──
FEATURE_COLS = [
    "SMA_5", "SMA_20", "MACD", "MACD_Signal",
    "RSI", "BB_Width", "Volume_Change", "Daily_Return",
]


def run_analysis(ticker, start, end, initial_balance, episodes):
    # ── Step 1: 資料 ──
    progress = st.progress(0, text="[1/4] 下載股價資料...")
    df = fetch_stock(ticker, str(start), str(end))
    if len(df) < 50:
        st.error(f"資料不足：只有 {len(df)} 筆，至少需要 50 筆")
        return
    df = add_indicators(df)

    # ── Step 2: 預測模型 ──
    progress.progress(25, text="[2/4] 訓練預測模型...")
    _, _, _, pred_accuracy = train_predictor(df, FEATURE_COLS, window=20)

    # ── Step 3: RL 訓練 ──
    progress.progress(50, text="[3/4] 訓練 RL 交易員...")
    env = TradingEnvironment(df, FEATURE_COLS, initial_balance)
    agent, rl_results = train_trader(env, episodes=episodes)

    # 用訓練好的 agent 跑一次最終回測
    progress.progress(75, text="[4/4] 產出報表...")
    state = env.reset()
    while True:
        action = agent.act(state, training=False)
        state, _, done = env.step(action)
        if done:
            break

    history = pd.DataFrame(env.history)
    progress.progress(100, text="完成！")

    # ── 計算指標 ──
    final_value = history["portfolio_value"].iloc[-1]
    total_return = (final_value - initial_balance) / initial_balance
    buy_hold_return = float((df["Close"].iloc[-1] - df["Close"].iloc[0]) / df["Close"].iloc[0])
    excess = total_return - buy_hold_return
    daily_rets = history["portfolio_value"].pct_change().dropna()
    sharpe = float(daily_rets.mean() / (daily_rets.std() + 1e-8) * np.sqrt(252))
    max_dd = float(((history["portfolio_value"] - history["portfolio_value"].cummax()) / history["portfolio_value"].cummax()).min())
    total_trades = history[history["action"] != 0].shape[0]
    win_trades = len([r for r in rl_results if r > 0])

    # ══════════════════════════════════════════
    #  Dashboard
    # ══════════════════════════════════════════
    st.markdown("---")

    # ── KPI Cards ──
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("AI 報酬率", f"{total_return:+.1%}", f"vs 買入持有 {buy_hold_return:+.1%}")
    col2.metric("超額報酬", f"{excess:+.1%}")
    col3.metric("Sharpe Ratio", f"{sharpe:.2f}")
    col4.metric("最大回撤", f"{max_dd:.1%}")
    col5.metric("總交易次數", f"{total_trades}")

    st.markdown("---")

    # ── Chart 1: 股價 + 買賣訊號 ──
    fig1 = make_subplots(rows=2, cols=1, shared_xaxes=True,
                         row_heights=[0.7, 0.3],
                         subplot_titles=[f"{ticker} 股價 & AI 交易訊號", "成交量"])

    dates = df.index[1:len(history) + 1] if len(df.index) > len(history) else list(range(len(history)))

    fig1.add_trace(go.Candlestick(
        x=dates,
        open=df["Open"].values[1:len(history) + 1],
        high=df["High"].values[1:len(history) + 1],
        low=df["Low"].values[1:len(history) + 1],
        close=df["Close"].values[1:len(history) + 1],
        name="K線",
    ), row=1, col=1)

    buys = history[history["action"] == 1]
    sells = history[history["action"] == 2]

    if len(buys) > 0:
        buy_dates = [dates[i] for i in buys.index if i < len(dates)]
        fig1.add_trace(go.Scatter(
            x=buy_dates, y=buys["price"].values[:len(buy_dates)],
            mode="markers", name="買入",
            marker=dict(color="#00E676", size=10, symbol="triangle-up"),
        ), row=1, col=1)

    if len(sells) > 0:
        sell_dates = [dates[i] for i in sells.index if i < len(dates)]
        fig1.add_trace(go.Scatter(
            x=sell_dates, y=sells["price"].values[:len(sell_dates)],
            mode="markers", name="賣出",
            marker=dict(color="#FF1744", size=10, symbol="triangle-down"),
        ), row=1, col=1)

    fig1.add_trace(go.Bar(
        x=dates,
        y=df["Volume"].values[1:len(history) + 1],
        name="成交量", marker_color="rgba(100,100,255,0.3)",
    ), row=2, col=1)

    fig1.update_layout(height=600, template="plotly_dark", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig1, use_container_width=True)

    # ── Chart 2: 績效比較 ──
    left, right = st.columns(2)

    with left:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=dates, y=history["portfolio_value"].values,
            name="AI 策略", line=dict(color="#00E676", width=2),
            fill="tozeroy", fillcolor="rgba(0,230,118,0.1)",
        ))
        bh = initial_balance * (df["Close"].values[1:len(history) + 1] / df["Close"].values[1])
        fig2.add_trace(go.Scatter(
            x=dates, y=bh,
            name="買入持有", line=dict(color="#FF9800", width=2, dash="dash"),
        ))
        fig2.update_layout(title="投資組合價值", height=400, template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)

    with right:
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            y=[r * 100 for r in rl_results],
            mode="lines+markers",
            name="報酬率 %",
            line=dict(color="#BB86FC"),
            marker=dict(size=4),
        ))
        # 移動平均
        if len(rl_results) > 5:
            ma = pd.Series([r * 100 for r in rl_results]).rolling(5).mean()
            fig3.add_trace(go.Scatter(
                y=ma.values, name="5回合平均",
                line=dict(color="#03DAC6", width=3),
            ))
        fig3.update_layout(title="RL 學習曲線", height=400, template="plotly_dark",
                          xaxis_title="Episode", yaxis_title="Return %")
        st.plotly_chart(fig3, use_container_width=True)

    # ── Chart 3: Drawdown ──
    dd = (history["portfolio_value"] - history["portfolio_value"].cummax()) / history["portfolio_value"].cummax() * 100
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=dates, y=dd.values,
        fill="tozeroy", name="回撤 %",
        line=dict(color="#FF1744"),
        fillcolor="rgba(255,23,68,0.2)",
    ))
    fig4.update_layout(title="回撤 (Drawdown)", height=300, template="plotly_dark")
    st.plotly_chart(fig4, use_container_width=True)

    # ── 摘要表格 ──
    st.markdown("### 模型表現摘要")
    summary = pd.DataFrame({
        "指標": ["AI 策略報酬率", "買入持有報酬率", "超額報酬", "Sharpe Ratio",
                "最大回撤", "總交易次數", "預測模型準確率", "RL 勝率"],
        "數值": [f"{total_return:+.2%}", f"{buy_hold_return:+.2%}", f"{excess:+.2%}",
                f"{sharpe:.2f}", f"{max_dd:.2%}", str(total_trades),
                f"{pred_accuracy:.1%}", f"{win_trades}/{episodes} ({win_trades/episodes:.0%})"],
    })
    st.dataframe(summary, use_container_width=True, hide_index=True)

    # ── 交易明細 ──
    with st.expander("查看交易明細"):
        trades = history[history["action"] != 0].copy()
        trades["action"] = trades["action"].map({1: "買入", 2: "賣出"})
        trades["price"] = trades["price"].round(2)
        trades["portfolio_value"] = trades["portfolio_value"].round(2)
        trades["balance"] = trades["balance"].round(2)
        st.dataframe(trades, use_container_width=True, hide_index=True)


# ── Main ──
if not run:
    st.title("AI Stock Trader")
    st.markdown("""
    ### 系統架構

    | 模組 | 功能 | 技術 |
    |------|------|------|
    | 資料收集 | Yahoo Finance 即時抓取 | yfinance + 技術指標 |
    | 股價預測 | 預測明日漲跌方向 | GBM + Random Forest 集成 |
    | RL 交易 | 自主學習買/賣/持有 | Deep Q-Network |
    | 報表 | 互動式績效分析 | Plotly + Streamlit |

    **使用方式：** 在左側設定參數，點「開始分析」
    """)
else:
    st.title(f"AI Stock Trader — {ticker}")
    with st.spinner("AI 正在分析..."):
        run_analysis(ticker, start, end, initial_balance, episodes)
