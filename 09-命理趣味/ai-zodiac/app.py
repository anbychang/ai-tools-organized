import streamlit as st
import json
import re
from datetime import date
from groq import Groq
from data.zodiac_data import get_zodiac, get_element_compatibility

# ───────────────────────── 頁面設定 ─────────────────────────
st.set_page_config(
    page_title="AI 星座配對分析",
    page_icon="🌟",
    layout="centered",
)

# ───────────────────────── 自訂 CSS ─────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        font-family: 'Noto Sans TC', sans-serif;
    }

    .main-title {
        text-align: center;
        background: linear-gradient(90deg, #f5af19, #f12711, #f5af19);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        animation: shimmer 3s linear infinite;
    }

    @keyframes shimmer {
        to { background-position: 200% center; }
    }

    .sub-title {
        text-align: center;
        color: #b8b8d0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    .zodiac-card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .zodiac-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(245,175,25,0.15);
    }

    .zodiac-emoji {
        font-size: 3.5rem;
        display: block;
        margin-bottom: 0.4rem;
    }
    .zodiac-name {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f5af19;
    }
    .zodiac-element {
        display: inline-block;
        padding: 2px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin-top: 0.3rem;
        font-weight: 500;
    }
    .fire   { background: rgba(241,39,17,0.25); color: #ff6b6b; border: 1px solid rgba(241,39,17,0.4); }
    .earth  { background: rgba(76,175,80,0.25); color: #81c784; border: 1px solid rgba(76,175,80,0.4); }
    .air    { background: rgba(100,181,246,0.25); color: #90caf9; border: 1px solid rgba(100,181,246,0.4); }
    .water  { background: rgba(149,117,205,0.25); color: #b39ddb; border: 1px solid rgba(149,117,205,0.4); }

    .zodiac-traits {
        color: #ccc;
        font-size: 0.88rem;
        margin-top: 0.6rem;
        line-height: 1.6;
    }

    .result-section {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.8rem;
        margin-top: 1.5rem;
        backdrop-filter: blur(10px);
    }
    .result-section h3 {
        color: #f5af19;
        margin-bottom: 1rem;
    }

    .score-label {
        color: #e0e0e0;
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 0.2rem;
    }
    .score-value {
        font-size: 1.3rem;
        font-weight: 700;
        margin-left: 0.5rem;
    }

    .advice-box {
        background: linear-gradient(135deg, rgba(245,175,25,0.1), rgba(241,39,17,0.08));
        border-left: 4px solid #f5af19;
        border-radius: 0 12px 12px 0;
        padding: 1.2rem 1.5rem;
        margin-top: 1rem;
        color: #e0e0e0;
        line-height: 1.8;
    }

    .heart-divider {
        text-align: center;
        font-size: 2rem;
        margin: 1rem 0;
        color: #f12711;
    }

    /* sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(15,12,41,0.95);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    section[data-testid="stSidebar"] .stMarkdown h2 {
        color: #f5af19;
    }

    /* progress bar colours */
    .stProgress > div > div > div > div {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ───────────────────────── 側邊欄 ─────────────────────────
with st.sidebar:
    st.markdown("## 設定")
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="前往 https://console.groq.com 取得免費 API Key",
    )
    st.divider()
    st.markdown("""
    ### 使用說明
    1. 輸入 Groq API Key
    2. 選擇兩人的生日
    3. 點擊 **開始分析配對**
    4. AI 將為你深度解析星座配對！

    ---
    *Powered by Groq LLaMA 3.3 70B*
    """)

# ───────────────────────── 工具函式 ─────────────────────────

ELEMENT_CSS = {"火象": "fire", "土象": "earth", "風象": "air", "水象": "water"}


def render_zodiac_card(label: str, zodiac: dict):
    """渲染星座資訊卡片"""
    css_class = ELEMENT_CSS.get(zodiac["element"], "fire")
    st.markdown(f"""
    <div class="zodiac-card">
        <span class="zodiac-emoji">{zodiac['emoji']}</span>
        <div class="zodiac-name">{label}：{zodiac['name']}</div>
        <span class="zodiac-element {css_class}">{zodiac['element']}</span>
        <div class="zodiac-traits">{zodiac['traits']}</div>
    </div>
    """, unsafe_allow_html=True)


def score_color(score: int) -> str:
    if score >= 80:
        return "#4caf50"
    elif score >= 60:
        return "#f5af19"
    elif score >= 40:
        return "#ff9800"
    else:
        return "#f44336"


def render_score_bar(label: str, emoji: str, score: int):
    """渲染分數條"""
    color = score_color(score)
    st.markdown(
        f'<div class="score-label">{emoji} {label} '
        f'<span class="score-value" style="color:{color}">{score}%</span></div>',
        unsafe_allow_html=True,
    )
    st.progress(score / 100)


def call_groq(api_key: str, zodiac_a: dict, zodiac_b: dict):
    """呼叫 Groq API 進行星座配對分析"""
    element_compat = get_element_compatibility(zodiac_a["element"], zodiac_b["element"])

    prompt = f"""你是一位專業的星座命理分析師。請根據以下兩人的星座資訊，進行詳細的配對分析。

Person A: {zodiac_a['name']}（{zodiac_a['element']}）
性格特質：{zodiac_a['traits']}
簡介：{zodiac_a['description']}

Person B: {zodiac_b['name']}（{zodiac_b['element']}）
性格特質：{zodiac_b['traits']}
簡介：{zodiac_b['description']}

元素相性參考：{element_compat}

請以繁體中文回覆，並嚴格按照以下 JSON 格式輸出（不要加任何其他文字）：
{{
  "love_score": <0-100整數>,
  "friendship_score": <0-100整數>,
  "work_score": <0-100整數>,
  "overall_analysis": "<150-250字的整體配對分析>",
  "advice": "<100-150字的相處建議>"
}}"""

    try:
        client = Groq(api_key=api_key)
        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "你是專業星座分析師，只輸出 JSON，不加任何額外文字或 markdown 標記。"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        raw = chat.choices[0].message.content.strip()
        # 嘗試從回應中提取 JSON
        json_match = re.search(r'\{[\s\S]*\}', raw)
        if json_match:
            return json.loads(json_match.group())
        return json.loads(raw)
    except json.JSONDecodeError:
        st.error("AI 回傳格式異常，請重新嘗試。")
        return None
    except Exception as e:
        st.error(f"API 呼叫失敗：{e}")
        return None


# ───────────────────────── 主介面 ─────────────────────────

st.markdown('<div class="main-title">AI 星座配對分析</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">輸入兩人生日，讓 AI 為你揭開星座配對的秘密</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Person A")
    birthday_a = st.date_input(
        "選擇生日",
        value=date(2000, 1, 1),
        min_value=date(1940, 1, 1),
        max_value=date.today(),
        key="bday_a",
    )

with col2:
    st.markdown("#### Person B")
    birthday_b = st.date_input(
        "選擇生日",
        value=date(2000, 6, 15),
        min_value=date(1940, 1, 1),
        max_value=date.today(),
        key="bday_b",
    )

# 自動偵測星座
zodiac_a = get_zodiac(birthday_a.month, birthday_a.day)
zodiac_b = get_zodiac(birthday_b.month, birthday_b.day)

st.markdown("")  # spacer

col_a, col_heart, col_b = st.columns([5, 1, 5])
with col_a:
    render_zodiac_card("A", zodiac_a)
with col_heart:
    st.markdown('<div class="heart-divider"><br><br></div>', unsafe_allow_html=True)
with col_b:
    render_zodiac_card("B", zodiac_b)

st.markdown("")  # spacer

# 分析按鈕
analyze = st.button("開始分析配對", type="primary", use_container_width=True)

if analyze:
    if not api_key:
        st.warning("請先在左側欄輸入 Groq API Key！")
    else:
        with st.spinner("AI 正在深度解析星座配對中..."):
            result = call_groq(api_key, zodiac_a, zodiac_b)

        if result:
            st.markdown('<div class="result-section">', unsafe_allow_html=True)
            st.markdown(f"### {zodiac_a['emoji']} {zodiac_a['name']}  &  {zodiac_b['emoji']} {zodiac_b['name']}  配對結果")

            st.markdown("")
            render_score_bar("戀愛契合度", "💕", result.get("love_score", 50))
            st.markdown("")
            render_score_bar("友誼契合度", "🤝", result.get("friendship_score", 50))
            st.markdown("")
            render_score_bar("工作契合度", "💼", result.get("work_score", 50))

            avg = round(
                (result.get("love_score", 50)
                 + result.get("friendship_score", 50)
                 + result.get("work_score", 50)) / 3
            )
            st.markdown("")
            render_score_bar("綜合評分", "⭐", avg)

            st.markdown("---")
            st.markdown("#### 整體分析")
            st.markdown(
                f'<div class="advice-box">{result.get("overall_analysis", "")}</div>',
                unsafe_allow_html=True,
            )

            st.markdown("#### 相處建議")
            st.markdown(
                f'<div class="advice-box">{result.get("advice", "")}</div>',
                unsafe_allow_html=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)
