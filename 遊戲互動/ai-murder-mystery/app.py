import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 劇情殺", page_icon="🔍")
st.title("🔍 AI 劇情殺")

with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    theme = st.selectbox("案件主題", ["豪門恩怨", "校園懸疑", "古風宮廷", "密室謀殺", "公司內鬥"])
    if st.button("🔄 開始新案件"):
        st.session_state.mm_messages = []
        st.rerun()
    st.markdown("---")
    st.markdown("透過提問調查案件，找出真兇！")

if "mm_messages" not in st.session_state:
    st.session_state.mm_messages = []

SYSTEM_PROMPT = f"""你是一個謀殺懸疑劇情遊戲的主持人（AI 劇情殺）。
主題：{theme}

規則：
1. 首先設定一個謀殺案場景，包含：受害者、5 位嫌疑人（各有動機）、案發時間地點
2. 你已經決定好誰是兇手（但不要透露）
3. 玩家可以詢問任何嫌疑人的不在場證明、動機、關係等
4. 根據玩家的提問，逐步揭露線索，有些線索互相矛盾
5. 如果玩家指控某人是兇手，判斷是否正確並揭曉真相
6. 保持懸疑感，不要太早洩漏答案
7. 全部使用繁體中文
8. 每次回覆保持簡潔，200字以內

請先描述案件場景和嫌疑人列表。"""

if not api_key:
    st.info("請在側邊欄輸入 Groq API Key 開始遊戲。")
    st.stop()

client = Groq(api_key=api_key)

def call_ai(messages):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_tokens=1000,
    )
    return response.choices[0].message.content

# Initialize game
if not st.session_state.mm_messages:
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    with st.spinner("正在佈置案發現場..."):
        try:
            reply = call_ai(full_messages)
            st.session_state.mm_messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"發生錯誤：{e}")
            st.stop()

# Display messages
for msg in st.session_state.mm_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if question := st.chat_input("詢問嫌疑人或指控兇手..."):
    st.session_state.mm_messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.mm_messages
    with st.chat_message("assistant"):
        with st.spinner("調查中..."):
            try:
                reply = call_ai(full_messages)
                st.session_state.mm_messages.append({"role": "assistant", "content": reply})
                st.markdown(reply)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
