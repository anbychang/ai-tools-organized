import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 故事接龍", page_icon="📖")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    if st.button("🗑️ 清除故事，重新開始"):
        st.session_state.story_parts = []
        st.session_state.story_input = ""
        st.rerun()
    st.markdown("🔑 請先取得 [Groq API Key](https://console.groq.com/)")

st.title("📖 AI 故事接龍")
st.markdown("你和 AI 輪流寫故事！你寫一段，AI 接一段，看看會發展出什麼奇妙的故事。")

# --- 初始化 session_state ---
if "story_parts" not in st.session_state:
    st.session_state.story_parts = []

# --- 顯示目前的故事 ---
if st.session_state.story_parts:
    st.subheader("📜 目前的故事")
    for i, part in enumerate(st.session_state.story_parts):
        role = part["role"]
        text = part["text"]
        if role == "user":
            st.markdown(f"**🧑 你（第 {i // 2 + 1} 回合）：**")
            st.info(text)
        else:
            st.markdown(f"**🤖 AI（第 {i // 2 + 1} 回合）：**")
            st.success(text)

# --- 使用者輸入 ---
st.divider()
if not st.session_state.story_parts:
    st.markdown("✨ **開始你的故事吧！寫下故事的開頭：**")
else:
    st.markdown("✨ **輪到你了！繼續寫下去：**")

user_input = st.text_area(
    "你的故事段落",
    placeholder="從前從前，在一個遙遠的國度裡...",
    height=120,
    key="story_input",
)

submit = st.button("📝 送出並讓 AI 接龍", use_container_width=True)

if submit:
    if not api_key:
        st.warning("⚠️ 請先在側邊欄輸入 Groq API Key。")
        st.stop()
    if not user_input.strip():
        st.warning("⚠️ 請寫一段故事再送出。")
        st.stop()

    # 記錄使用者段落
    st.session_state.story_parts.append({"role": "user", "text": user_input.strip()})

    # 組合完整故事
    full_story = "\n\n".join([p["text"] for p in st.session_state.story_parts])

    prompt = (
        f"以下是一個正在進行的故事接龍，由使用者和你輪流撰寫：\n\n"
        f"{full_story}\n\n"
        f"請接續寫下一段故事（約 100-200 字），要求：\n"
        f"1. 自然銜接前文情節\n"
        f"2. 加入新的劇情發展或轉折\n"
        f"3. 結尾留下懸念讓使用者可以繼續\n"
        f"4. 使用繁體中文\n"
        f"5. 只寫故事內容，不要加任何說明文字"
    )

    client = Groq(api_key=api_key)
    with st.spinner("🤖 AI 正在構思劇情..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "你是一位繁體中文故事接龍高手，擅長銜接劇情並加入有趣的轉折。"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.9,
                max_tokens=600,
            )
            ai_text = response.choices[0].message.content.strip()
            st.session_state.story_parts.append({"role": "ai", "text": ai_text})
            st.rerun()
        except Exception as e:
            st.error(f"❌ 發生錯誤：{e}")
            # 回退使用者的段落
            st.session_state.story_parts.pop()

# --- 統計 ---
if st.session_state.story_parts:
    total_chars = sum(len(p["text"]) for p in st.session_state.story_parts)
    rounds = (len(st.session_state.story_parts) + 1) // 2
    st.caption(f"📊 已進行 {rounds} 回合 | 總字數：{total_chars}")
