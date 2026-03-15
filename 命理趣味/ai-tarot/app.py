import random
import streamlit as st
from data.tarot_cards import MAJOR_ARCANA

try:
    from groq import Groq
except ImportError:
    Groq = None

# ---------- 頁面設定 ----------
st.set_page_config(
    page_title="AI 塔羅牌占卜",
    page_icon="🔮",
    layout="centered",
)

# ---------- 自訂 CSS ----------
st.markdown(
    """
    <style>
    /* 整體背景 */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }

    /* 標題樣式 */
    h1 {
        text-align: center;
        background: linear-gradient(90deg, #f5af19, #f12711, #f5af19);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem !important;
        margin-bottom: 0.2rem !important;
    }

    /* 副標題 */
    .subtitle {
        text-align: center;
        color: #b8b8d0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* 塔羅牌卡片 */
    .tarot-card {
        background: linear-gradient(145deg, #1a1a3e, #2d2b55);
        border: 2px solid #6c63ff;
        border-radius: 16px;
        padding: 1.5rem 1rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(108, 99, 255, 0.25);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        min-height: 220px;
    }
    .tarot-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 40px rgba(108, 99, 255, 0.4);
    }
    .tarot-card .emoji {
        font-size: 3.5rem;
        display: block;
        margin-bottom: 0.5rem;
    }
    .tarot-card .card-name {
        font-size: 1.3rem;
        font-weight: 700;
        color: #f5af19;
        margin-bottom: 0.3rem;
    }
    .tarot-card .orientation {
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .tarot-card .orientation.upright { color: #00e676; }
    .tarot-card .orientation.reversed { color: #ff5252; }
    .tarot-card .meaning {
        font-size: 0.85rem;
        color: #ccc;
        line-height: 1.5;
    }

    /* 解讀區塊 */
    .reading-box {
        background: linear-gradient(145deg, #1a1a3e, #2d2b55);
        border: 1px solid #6c63ff;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        color: #e0e0e0;
        line-height: 1.8;
        font-size: 1.05rem;
        margin-top: 1rem;
        box-shadow: 0 4px 20px rgba(108, 99, 255, 0.15);
    }

    /* 按鈕 */
    .stButton > button {
        background: linear-gradient(90deg, #6c63ff, #e040fb) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 0.6rem 2.5rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        letter-spacing: 1px;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 25px rgba(108, 99, 255, 0.5) !important;
    }

    /* 側邊欄 */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a3e, #0f0c29);
    }

    /* 分隔線 */
    .divider {
        text-align: center;
        color: #6c63ff;
        font-size: 1.5rem;
        letter-spacing: 8px;
        margin: 1.5rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- 側邊欄 ----------
with st.sidebar:
    st.markdown("## 🔑 API 設定")
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="輸入你的 Groq API Key...",
        help="前往 https://console.groq.com 取得免費 API Key",
    )
    st.markdown("---")
    st.markdown("### 🎴 關於")
    st.markdown(
        "本應用使用 **22 張大阿爾克那**塔羅牌，"
        "透過 AI 為你解讀牌陣，提供靈性指引。"
    )
    st.markdown(
        "模型：`llama-3.3-70b-versatile`"
    )
    st.markdown("---")
    st.markdown(
        "<small style='color:#888'>⚠️ 塔羅牌占卜僅供娛樂參考</small>",
        unsafe_allow_html=True,
    )

# ---------- 主畫面 ----------
st.markdown("# 🔮 AI 塔羅牌占卜")
st.markdown('<p class="subtitle">讓宇宙的智慧為你指引方向</p>', unsafe_allow_html=True)
st.markdown('<div class="divider">✦ ✦ ✦</div>', unsafe_allow_html=True)

# 使用者提問
question = st.text_input(
    "🙏 請輸入你的問題",
    placeholder="例如：我的感情未來會如何發展？",
    max_chars=200,
)

# ---------- 抽牌函式 ----------
def draw_cards(n: int = 3) -> list[dict]:
    """隨機抽取 n 張牌，並隨機決定正逆位。"""
    chosen = random.sample(MAJOR_ARCANA, n)
    result = []
    for card in chosen:
        is_upright = random.choice([True, False])
        result.append({**card, "is_upright": is_upright})
    return result


def render_card(card: dict, label: str) -> str:
    """產生單張牌的 HTML。"""
    orientation_class = "upright" if card["is_upright"] else "reversed"
    orientation_text = "正位" if card["is_upright"] else "逆位"
    meaning = card["upright"] if card["is_upright"] else card["reversed"]
    emoji_style = "" if card["is_upright"] else "display:inline-block;transform:rotate(180deg);"
    return f"""
    <div class="tarot-card">
        <div style="color:#8888aa;font-size:0.85rem;margin-bottom:0.3rem;">{label}</div>
        <span class="emoji" style="{emoji_style}">{card['emoji']}</span>
        <div class="card-name">{card['number']}. {card['name']}</div>
        <div class="orientation {orientation_class}">【{orientation_text}】</div>
        <div class="meaning">{meaning}</div>
    </div>
    """


def get_ai_reading(cards: list[dict], user_question: str, key: str) -> str:
    """呼叫 Groq API 取得 AI 塔羅解讀。"""
    card_descriptions = []
    for i, card in enumerate(cards, 1):
        pos = ["過去", "現在", "未來"][i - 1]
        orientation = "正位" if card["is_upright"] else "逆位"
        meaning = card["upright"] if card["is_upright"] else card["reversed"]
        card_descriptions.append(
            f"第{i}張（{pos}）：{card['name']}（{orientation}）— {meaning}"
        )

    cards_text = "\n".join(card_descriptions)

    prompt = f"""你是一位經驗豐富且富有靈性的塔羅牌占卜師。請用繁體中文為求問者進行深度解讀。

求問者的問題：{user_question}

抽到的三張牌（過去、現在、未來）：
{cards_text}

請依照以下格式進行解讀：
1. 先總覽三張牌的整體訊息
2. 分別解讀每張牌在其位置（過去/現在/未來）的意義，並結合求問者的問題
3. 給出綜合建議與指引
4. 最後用一句話總結這次占卜的核心訊息

請用溫暖、有智慧但不浮誇的語氣，讓求問者感到被理解與支持。"""

    if Groq is None:
        raise RuntimeError("groq 套件未安裝，請執行 pip install groq")
    client = Groq(api_key=key)
    chat_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=1500,
    )
    return chat_completion.choices[0].message.content


# ---------- 抽牌按鈕 ----------
col_btn = st.columns([1, 2, 1])
with col_btn[1]:
    draw = st.button("🎴 抽取塔羅牌", use_container_width=True)

if draw:
    if not question.strip():
        st.warning("請先輸入你的問題再抽牌！")
    else:
        # 抽牌
        cards = draw_cards(3)
        st.session_state["cards"] = cards
        st.session_state["question"] = question

        st.markdown('<div class="divider">✦ ✦ ✦</div>', unsafe_allow_html=True)
        st.markdown("### 🎴 你抽到的牌")

        # 顯示三張牌
        labels = ["🕰️ 過去", "⏳ 現在", "🔮 未來"]
        cols = st.columns(3, gap="medium")
        for idx, col in enumerate(cols):
            with col:
                st.markdown(
                    render_card(cards[idx], labels[idx]),
                    unsafe_allow_html=True,
                )

        st.markdown('<div class="divider">✦ ✦ ✦</div>', unsafe_allow_html=True)

        # AI 解讀（需要 API Key）
        if api_key:
            st.markdown("### 🌟 AI 占卜解讀")
            with st.spinner("占卜師正在解讀牌陣的奧秘..."):
                try:
                    reading = get_ai_reading(cards, question, api_key)
                    st.markdown(
                        f'<div class="reading-box">{reading}</div>',
                        unsafe_allow_html=True,
                    )
                except Exception as e:
                    st.error(f"AI 解讀時發生錯誤：{e}")
        else:
            st.info("💡 如需 AI 深度解讀，請在左側欄輸入 Groq API Key。")
