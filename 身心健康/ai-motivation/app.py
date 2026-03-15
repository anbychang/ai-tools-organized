import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 正能量", page_icon="✨")
st.title("✨ AI 正能量")
st.caption("讓 AI 為您送上一句專屬的正能量鼓勵")

# 側邊欄設定
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入您的 Groq API Key")
    st.markdown("---")
    st.markdown("### 使用說明")
    st.markdown(
        "1. 輸入您的 Groq API Key\n"
        "2. 可選擇輸入目前的困擾\n"
        "3. 點擊按鈕獲得正能量\n"
        "4. 每次點擊都會產生新的鼓勵"
    )

# 初始化 session state
if "quote_count" not in st.session_state:
    st.session_state.quote_count = 0
if "last_quote" not in st.session_state:
    st.session_state.last_quote = ""


def get_motivation(concern: str, count: int) -> str:
    client = Groq(api_key=api_key)
    user_msg = "請給我一句正能量鼓勵。"
    if concern.strip():
        user_msg = f"我目前的困擾是：{concern}\n請針對這個困擾給我一段溫暖的鼓勵。"
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一位溫暖且富有智慧的心靈導師。請以繁體中文回覆。\n"
                    "回覆格式：\n"
                    "1. 一句原創的正能量語錄（加粗顯示）\n"
                    "2. 一段 2-3 句的溫暖解說\n"
                    "3. 一個今天可以做的小行動建議\n"
                    f"這是第 {count} 次請求，請給出不同的內容。"
                    "語氣溫暖、真誠，避免空洞的雞湯。"
                ),
            },
            {"role": "user", "content": user_msg},
        ],
        temperature=0.95,
        max_tokens=1024,
    )
    return response.choices[0].message.content


# 主要介面
concern = st.text_input(
    "目前的困擾（選填）",
    placeholder="例如：工作壓力大、感情問題、對未來迷茫...",
)

mood = st.select_slider(
    "今天的心情如何？",
    options=["😢 很低落", "😔 有點沮喪", "😐 普通", "🙂 還不錯", "😊 很開心"],
    value="😐 普通",
)

if st.button("🌟 給我正能量", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    else:
        st.session_state.quote_count += 1
        with st.spinner("AI 正在為您準備專屬鼓勵..."):
            try:
                result = get_motivation(concern, st.session_state.quote_count)
                st.session_state.last_quote = result
            except Exception as e:
                st.error(f"發生錯誤：{e}")

if st.session_state.last_quote:
    st.markdown("---")
    st.markdown(st.session_state.last_quote)
    st.markdown("---")
    st.caption(f"已為您生成 {st.session_state.quote_count} 次正能量 💪")

st.markdown("---")
st.caption("🌈 每一天都是新的開始，你比自己想像的更堅強。")
