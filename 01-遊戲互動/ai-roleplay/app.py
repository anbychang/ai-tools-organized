import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 角色扮演", page_icon="🎭")

# --- 角色資料 ---
CHARACTERS = {
    "孔子": "你是孔子，春秋時期的思想家與教育家。說話引用《論語》，語氣溫和睿智，常用「子曰」開頭，善用比喻教導弟子。",
    "愛因斯坦": "你是愛因斯坦，偉大的物理學家。喜歡用簡單的比喻解釋複雜的科學概念，偶爾幽默，對宇宙充滿好奇心。",
    "拿破崙": "你是拿破崙，法國皇帝與軍事天才。說話充滿自信與霸氣，常提及戰略思維，偶爾感嘆命運。",
    "武則天": "你是武則天，中國歷史上唯一的女皇帝。說話威嚴而睿智，深諳權謀之術，對女性地位有獨到見解。",
    "賈伯斯": "你是賈伯斯（Steve Jobs），蘋果公司創辦人。說話充滿激情，追求極致與簡約，常強調設計與用戶體驗。",
}

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    character = st.selectbox("🎭 選擇歷史人物", list(CHARACTERS.keys()))
    if st.button("🗑️ 清除對話"):
        st.session_state.rp_messages = []
        st.rerun()
    st.markdown("🔑 請先取得 [Groq API Key](https://console.groq.com/)")

st.title("🎭 AI 角色扮演")
st.markdown(f"你正在與 **{character}** 對話！試著問他/她問題吧。")

# --- 初始化 ---
if "rp_messages" not in st.session_state:
    st.session_state.rp_messages = []
if "rp_character" not in st.session_state:
    st.session_state.rp_character = character

# 切換角色時清除對話
if st.session_state.rp_character != character:
    st.session_state.rp_messages = []
    st.session_state.rp_character = character

# --- 顯示聊天紀錄 ---
for msg in st.session_state.rp_messages:
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🎭"):
        st.markdown(msg["content"])

# --- 使用者輸入 ---
if user_input := st.chat_input(f"對{character}說些什麼..."):
    if not api_key:
        st.warning("⚠️ 請先在側邊欄輸入 Groq API Key。")
        st.stop()

    st.session_state.rp_messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    system_prompt = (
        f"{CHARACTERS[character]}\n"
        f"請始終保持角色扮演，用繁體中文回應。\n"
        f"回答要符合該人物的時代背景、語氣和知識範圍。\n"
        f"回答長度適中，約 50-200 字。"
    )

    messages = [{"role": "system", "content": system_prompt}]
    # 只保留最近 20 條訊息以節省 token
    for msg in st.session_state.rp_messages[-20:]:
        messages.append({"role": msg["role"], "content": msg["content"]})

    client = Groq(api_key=api_key)
    with st.chat_message("assistant", avatar="🎭"):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.8,
                max_tokens=600,
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.rp_messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"❌ 發生錯誤：{e}")
