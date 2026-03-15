import streamlit as st
from groq import Groq

# --- Page Config ---
st.set_page_config(
    page_title="AI 吵架神器",
    page_icon="🔥",
    layout="wide",
)

# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700;900&display=swap');

    .stApp {
        font-family: 'Noto Sans TC', sans-serif;
    }

    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ff6b6b, #ffa502, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
        padding-top: 1rem;
    }

    .sub-title {
        text-align: center;
        font-size: 1.1rem;
        color: #888;
        margin-bottom: 2rem;
    }

    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        padding: 0.5rem 0;
        border-bottom: 3px solid #ff6b6b;
        margin-bottom: 1rem;
    }

    .weak-point-card {
        background: linear-gradient(135deg, #fff5f5, #ffe8e8);
        border-left: 4px solid #ff6b6b;
        padding: 1rem 1.2rem;
        border-radius: 0 10px 10px 0;
        margin-bottom: 0.8rem;
    }

    .counter-card {
        background: linear-gradient(135deg, #f0fff4, #e6ffed);
        border-left: 4px solid #38d9a9;
        padding: 1rem 1.2rem;
        border-radius: 0 10px 10px 0;
        margin-bottom: 0.8rem;
    }

    .response-card {
        background: linear-gradient(135deg, #f8f0ff, #ede0ff);
        border: 2px solid #b197fc;
        padding: 1.5rem;
        border-radius: 12px;
        font-size: 1.05rem;
        line-height: 1.8;
    }

    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #ff6b6b, #ee5a24) !important;
        color: white !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        padding: 0.7rem 2rem !important;
        border: none !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 20px rgba(255, 107, 107, 0.4) !important;
    }

    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e, #16213e);
    }

    div[data-testid="stSidebar"] .stMarkdown {
        color: #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("## ⚙️ 設定")
    st.markdown("---")

    api_key = st.text_input(
        "🔑 Groq API Key",
        type="password",
        placeholder="輸入你的 Groq API Key...",
        help="前往 https://console.groq.com 取得免費 API Key",
    )

    st.markdown("---")

    tone_options = {
        "溫和理性 🧠": "溫和理性",
        "犀利反擊 ⚔️": "犀利反擊",
        "幽默化解 😄": "幽默化解",
        "法律口吻 ⚖️": "法律口吻",
    }

    selected_tone_label = st.radio(
        "🎭 回覆語氣",
        options=list(tone_options.keys()),
        index=0,
    )
    selected_tone = tone_options[selected_tone_label]

    st.markdown("---")
    st.markdown(
        """
        <div style='text-align:center; color:#666; font-size:0.85rem; margin-top:2rem;'>
            Powered by Groq + Llama 3.3 70B<br/>
            讓 AI 幫你贏得每一場辯論 💪
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- Main Area ---
st.markdown('<div class="main-title">🔥 AI 吵架神器 🔥</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">貼上吵架內容，AI 幫你組織最強回擊！</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    argument_text = st.text_area(
        "📋 對方說了什麼？（貼上吵架內容）",
        height=200,
        placeholder="把對方的訊息、留言或對話貼在這裡...\n\n例如：「你根本不懂，每次都是你的問題，我跟你講過多少次了...」",
    )

with col2:
    context_text = st.text_area(
        "💬 你的立場 / 背景補充",
        height=200,
        placeholder="補充一些背景資訊或你的立場...\n\n例如：「我們在討論家事分工，我覺得應該要平均分擔...」",
    )

st.markdown("")
generate_btn = st.button("⚡ 產生最強回擊")

# --- Tone Descriptions for Prompt ---
TONE_INSTRUCTIONS = {
    "溫和理性": "請用冷靜、理性、有邏輯的方式回覆。語氣溫和但論點堅定，展現高 EQ 和說服力。避免人身攻擊，專注在事實和邏輯上。",
    "犀利反擊": "請用犀利、直接、一針見血的方式回覆。語氣強勢但不失風度，每一句都要有力量。適當使用反問句來增強效果。",
    "幽默化解": "請用幽默、風趣、輕鬆的方式回覆。用機智的比喻和巧妙的玩笑來化解對方的攻擊，讓氣氛緩和但同時表達立場。可以適度自嘲但不要示弱。",
    "法律口吻": "請用嚴謹、專業的法律口吻回覆。引用相關法律概念（如果適用），使用正式用語，語氣威嚴有權威感。讓對方感受到法律的壓力。",
}


def generate_response(api_key: str, argument: str, context: str, tone: str) -> str:
    """Call Groq API to analyze and generate response."""
    client = Groq(api_key=api_key)

    system_prompt = f"""你是一位專業的辯論教練和溝通策略師。你的任務是幫助使用者在爭論中佔上風。

請用**繁體中文**回覆，並使用以下格式：

## 🎯 對方的弱點分析
針對對方的論述，找出邏輯謬誤、矛盾之處、情緒化語言等弱點。每個弱點用一小段說明。

## 🛡️ 你的反擊要點
根據弱點分析，列出 3-5 個有力的反擊論點。

## 💬 建議回覆
根據以上分析，撰寫一段完整的回覆訊息。

語氣要求：{TONE_INSTRUCTIONS[tone]}

重要注意事項：
- 分析要精準到位
- 回覆要實用，可以直接複製貼上使用
- 保持風度，不要使用髒話或過度人身攻擊
- 如果對方有合理的點，也要承認，這樣更有說服力"""

    user_message = f"""對方說的話：
{argument}

我的立場/背景：
{context if context else "（未提供額外背景）"}

請幫我分析並產生回覆。"""

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        max_tokens=2000,
    )

    return chat_completion.choices[0].message.content


# --- Generate ---
if generate_btn:
    if not api_key:
        st.error("⚠️ 請先在左側欄輸入 Groq API Key！")
    elif not argument_text.strip():
        st.warning("📝 請先貼上對方的吵架內容！")
    else:
        with st.spinner("🤔 AI 正在分析對方弱點，組織最強反擊..."):
            try:
                result = generate_response(
                    api_key, argument_text, context_text, selected_tone
                )
                st.markdown("---")
                st.markdown(result)

                st.markdown("---")
                st.markdown(
                    """
                    <div style='text-align:center; padding:1rem; color:#888; font-size:0.9rem;'>
                        💡 <strong>小提示：</strong>吵架贏了不代表關係贏了。適時退一步，也是一種智慧。
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.error(f"❌ 發生錯誤：{str(e)}")

# --- Footer ---
st.markdown("---")
st.markdown(
    """
    <div style='text-align:center; padding:1rem 0; color:#aaa; font-size:0.8rem;'>
        AI 吵架神器 v1.0 ｜ 僅供娛樂參考，請理性溝通 ❤️
    </div>
    """,
    unsafe_allow_html=True,
)
