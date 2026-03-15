import streamlit as st
from groq import Groq
from data.dream_symbols import DREAM_SYMBOLS, EXAMPLE_DREAMS, find_symbols
import random

# ---------------------------------------------------------------------------
# Page config & custom CSS
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI 夢境解析",
    page_icon="🌙",
    layout="centered",
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans TC', sans-serif;
}

.stApp {
    background: linear-gradient(160deg, #0d0221 0%, #150734 30%, #1a0a3e 60%, #0f0628 100%);
    color: #e0d5f5;
}

/* sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #120630 0%, #1c0a4a 100%);
    border-right: 1px solid #3d2a6e;
}

/* main title */
.dream-title {
    text-align: center;
    font-size: 2.6rem;
    font-weight: 700;
    background: linear-gradient(90deg, #b388ff, #7c4dff, #ea80fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}

.dream-subtitle {
    text-align: center;
    color: #9e8ec7;
    font-size: 1.05rem;
    margin-bottom: 2rem;
}

/* result cards */
.result-card {
    background: rgba(30, 15, 70, 0.65);
    border: 1px solid #3d2a6e;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(6px);
}

.result-card h3 {
    margin-top: 0;
    color: #ce93d8;
}

.symbol-tag {
    display: inline-block;
    background: rgba(124, 77, 255, 0.25);
    border: 1px solid #7c4dff;
    border-radius: 20px;
    padding: 0.3rem 0.9rem;
    margin: 0.2rem 0.3rem;
    font-size: 0.92rem;
    color: #d1c4e9;
}

.lucky-number {
    display: inline-block;
    background: rgba(234, 128, 252, 0.18);
    border: 1px solid #ea80fc;
    border-radius: 50%;
    width: 44px;
    height: 44px;
    line-height: 44px;
    text-align: center;
    margin: 0.2rem 0.35rem;
    font-size: 1.1rem;
    font-weight: 700;
    color: #f3e5f5;
}

.divider {
    border: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #7c4dff, transparent);
    margin: 1.6rem 0;
}

/* textarea & button tweaks */
textarea {
    background-color: rgba(20, 10, 50, 0.7) !important;
    color: #e0d5f5 !important;
    border: 1px solid #3d2a6e !important;
    border-radius: 10px !important;
}

div.stButton > button {
    background: linear-gradient(135deg, #7c4dff 0%, #b388ff 100%);
    color: #fff;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 2.4rem;
    font-size: 1.05rem;
    font-weight: 600;
    width: 100%;
    transition: all 0.3s;
}

div.stButton > button:hover {
    background: linear-gradient(135deg, #651fff 0%, #aa66ff 100%);
    box-shadow: 0 0 18px rgba(124, 77, 255, 0.45);
}

/* example buttons */
div.stButton > button[kind="secondary"] {
    background: rgba(30, 15, 70, 0.5);
    border: 1px solid #3d2a6e;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 設定")
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="前往 https://console.groq.com 取得免費 API Key",
    )
    style = st.radio(
        "解析風格",
        ["綜合分析", "心理學派", "神秘學派"],
        index=0,
    )
    st.markdown("---")
    st.markdown(
        "**關於本工具**\n\n"
        "AI 夢境解析結合心理學與神秘學觀點，"
        "為你的夢境提供多角度的解讀。\n\n"
        "結果僅供娛樂與自我探索參考，"
        "不構成任何醫療或心理諮詢建議。"
    )

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown('<div class="dream-title">AI 夢境解析</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="dream-subtitle">描述你的夢境，讓 AI 為你揭開潛意識的面紗</div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Example dreams
# ---------------------------------------------------------------------------
st.markdown("**快速範例** — 點擊填入範例夢境：")
example_cols = st.columns(len(EXAMPLE_DREAMS))
for idx, (col, ex) in enumerate(zip(example_cols, EXAMPLE_DREAMS)):
    with col:
        if st.button(ex["title"], key=f"ex_{idx}", use_container_width=True):
            st.session_state["dream_input"] = ex["content"]

# ---------------------------------------------------------------------------
# Dream input
# ---------------------------------------------------------------------------
dream_text = st.text_area(
    "描述你的夢境",
    key="dream_input",
    height=180,
    placeholder="盡量詳細地描述你的夢境內容，包括場景、人物、情緒和發生的事件...",
)

# ---------------------------------------------------------------------------
# Build prompt
# ---------------------------------------------------------------------------

STYLE_INSTRUCTIONS = {
    "心理學派": (
        "你是一位專業的心理學夢境分析師，擅長榮格分析心理學和佛洛伊德精神分析。"
        "請完全從心理學角度進行分析，引用相關心理學理論。"
    ),
    "神秘學派": (
        "你是一位神秘學夢境解讀大師，精通東西方占夢術、塔羅、星象與靈性解讀。"
        "請從神秘學和靈性角度進行分析，語氣帶有神秘感和詩意。"
    ),
    "綜合分析": (
        "你同時具備心理學專業知識和神秘學智慧，能從多重角度解讀夢境。"
        "請同時提供心理學分析和神秘學解讀，讓使用者獲得全面的視角。"
    ),
}


def build_prompt(dream: str, found_symbols: list[dict], interpretation_style: str) -> str:
    symbol_context = ""
    if found_symbols:
        symbol_context = "\n\n以下是在夢境中偵測到的已知符號及其參考含義：\n"
        for s in found_symbols:
            symbol_context += (
                f"\n【{s['name']}】\n"
                f"  心理學參考：{s['psychological']}\n"
                f"  神秘學參考：{s['mystical']}\n"
                f"  相關情緒：{s['emotion']}\n"
            )

    return f"""{STYLE_INSTRUCTIONS[interpretation_style]}

使用者描述了以下夢境：
「{dream}」
{symbol_context}

請用繁體中文，以下列格式回覆（使用 Markdown）：

## 夢境符號辨識
列出夢中出現的主要符號，每個符號用一句話簡述其象徵意義。

## 深度解析
根據你的專業角度，對整個夢境進行深入的解讀（3-5 段）。

## 情緒狀態分析
分析做夢者可能的情緒狀態和內在需求。

## 幸運數字
隨機給出 5 個 1-49 之間的幸運數字（純屬娛樂）。

## 給你的建議
根據夢境分析，提供 2-3 條實用的建議，幫助做夢者在現實生活中成長。

請確保回答溫暖、有深度、且具啟發性。"""


# ---------------------------------------------------------------------------
# Interpret button
# ---------------------------------------------------------------------------
if st.button("開始解夢", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在左側欄輸入 Groq API Key。")
    elif not dream_text.strip():
        st.warning("請先輸入你的夢境描述。")
    else:
        # Find known symbols
        found_symbols = find_symbols(dream_text)

        prompt = build_prompt(dream_text, found_symbols, style)

        # Show detected symbols
        if found_symbols:
            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            tags_html = "".join(
                f'<span class="symbol-tag">{s["name"]}</span>' for s in found_symbols
            )
            st.markdown(
                f'<div class="result-card"><h3>偵測到的夢境符號</h3>{tags_html}</div>',
                unsafe_allow_html=True,
            )

        # Call Groq
        with st.spinner("正在解析你的夢境..."):
            try:
                client = Groq(api_key=api_key)
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "你是一位專業的夢境解析師。回答請使用繁體中文。"
                                "回覆時使用 Markdown 格式。"
                            ),
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.8,
                    max_tokens=2048,
                )
                result = response.choices[0].message.content

                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown(result)

                # Lucky numbers as styled circles
                lucky_nums = random.sample(range(1, 50), 5)
                nums_html = "".join(
                    f'<span class="lucky-number">{n}</span>' for n in sorted(lucky_nums)
                )
                st.markdown(
                    f'<div class="result-card"><h3>今日幸運數字</h3>{nums_html}</div>',
                    unsafe_allow_html=True,
                )

            except Exception as e:
                st.error(f"呼叫 AI 時發生錯誤：{e}")

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown(
    '<div style="text-align:center;color:#6a5a8e;font-size:0.85rem;">'
    "AI 夢境解析 | 僅供娛樂與自我探索參考 | Powered by Groq + LLaMA"
    "</div>",
    unsafe_allow_html=True,
)
