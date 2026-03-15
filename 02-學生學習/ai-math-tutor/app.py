import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 數學解題", page_icon="🔢")

# --- 側邊欄 ---
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    st.markdown("AI 數學家教，逐步解題與追問")

st.title("🔢 AI 數學解題")
st.markdown("輸入數學題目，AI 將逐步解題。你也可以繼續追問！")

# --- 初始化聊天記錄 ---
if "messages" not in st.session_state:
    st.session_state.messages = []

SYSTEM_MSG = {
    "role": "system",
    "content": (
        "你是一位耐心的數學家教老師，請用繁體中文回覆。"
        "解題時請分步驟說明，每一步都要解釋原因。"
        "使用清楚的數學符號，必要時用 LaTeX 格式。"
        "如果學生追問，請針對不懂的地方再詳細解釋。"
    ),
}

def get_response(api_key: str, messages: list) -> str:
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[SYSTEM_MSG] + messages,
        temperature=0.5,
        max_tokens=2048,
    )
    return response.choices[0].message.content

# --- 顯示歷史訊息 ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 數學題輸入 ---
if not st.session_state.messages:
    problem = st.text_area("請輸入數學題目", height=120, placeholder="例如：解方程式 2x + 5 = 13")
    if st.button("開始解題", type="primary", use_container_width=True):
        if not api_key:
            st.error("請先在側邊欄輸入 Groq API Key。")
        elif not problem.strip():
            st.warning("請先輸入數學題目。")
        else:
            st.session_state.messages.append({"role": "user", "content": problem})
            with st.chat_message("user"):
                st.markdown(problem)
            with st.chat_message("assistant"):
                with st.spinner("解題中..."):
                    try:
                        reply = get_response(api_key, st.session_state.messages)
                        st.markdown(reply)
                        st.session_state.messages.append({"role": "assistant", "content": reply})
                    except Exception as e:
                        st.error(f"發生錯誤：{e}")
else:
    # 追問模式
    follow_up = st.chat_input("繼續追問（例如：為什麼第二步要這樣做？）")
    if follow_up:
        if not api_key:
            st.error("請先在側邊欄輸入 Groq API Key。")
        else:
            st.session_state.messages.append({"role": "user", "content": follow_up})
            with st.chat_message("user"):
                st.markdown(follow_up)
            with st.chat_message("assistant"):
                with st.spinner("思考中..."):
                    try:
                        reply = get_response(api_key, st.session_state.messages)
                        st.markdown(reply)
                        st.session_state.messages.append({"role": "assistant", "content": reply})
                    except Exception as e:
                        st.error(f"發生錯誤：{e}")

    if st.sidebar.button("清除對話，重新出題"):
        st.session_state.messages = []
        st.rerun()
