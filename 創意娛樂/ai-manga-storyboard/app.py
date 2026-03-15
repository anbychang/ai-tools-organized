import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 漫畫分鏡", page_icon="🎬")
st.title("🎬 AI 漫畫分鏡產生器")

with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    st.markdown("輸入劇情概要與角色，AI 將為你產生逐格分鏡描述。")

if "storyboard" not in st.session_state:
    st.session_state.storyboard = ""

st.subheader("📝 劇情設定")
col1, col2 = st.columns(2)
with col1:
    genre = st.selectbox("漫畫類型", ["少年熱血", "少女戀愛", "奇幻冒險", "科幻未來", "懸疑推理", "日常搞笑"])
with col2:
    panel_count = st.slider("分鏡格數", min_value=4, max_value=12, value=6)

synopsis = st.text_area("劇情概要", placeholder="例如：勇者在森林中遭遇魔王的先遣部隊，展開激烈戰鬥...", height=100)
characters = st.text_input("角色名稱與特徵（用逗號分隔）", placeholder="例如：小明（黑髮劍士）, 小花（精靈法師）, 魔王（暗黑鎧甲）")

if st.button("🎨 產生分鏡", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key。")
    elif not synopsis or not characters:
        st.warning("請填寫劇情概要與角色資訊。")
    else:
        client = Groq(api_key=api_key)
        prompt = f"""你是一位專業漫畫分鏡師。請根據以下資訊產生 {panel_count} 格漫畫分鏡描述。
漫畫類型：{genre}
劇情概要：{synopsis}
角色：{characters}

請為每一格分鏡提供：
1. 場景描述（背景環境）
2. 角色動作與表情
3. 對白/旁白（用「」標示對白，用（）標示旁白）
4. 鏡頭角度（如：特寫、中景、遠景、俯瞰、仰角等）
5. 畫面氛圍/光影提示

請用以下格式輸出每一格：
【第 X 格】
🎬 鏡頭：...
🏞️ 場景：...
🧑 角色動作：...
💬 對白：...
🌟 氛圍：...

請確保分鏡之間有流暢的敘事節奏，全部使用繁體中文。"""

        with st.spinner("正在繪製分鏡腳本..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.8,
                    max_tokens=3000,
                )
                st.session_state.storyboard = response.choices[0].message.content
            except Exception as e:
                st.error(f"發生錯誤：{e}")

if st.session_state.storyboard:
    st.markdown("---")
    st.subheader("📋 分鏡腳本")
    st.markdown(st.session_state.storyboard)
    st.download_button(
        label="💾 下載分鏡腳本",
        data=st.session_state.storyboard,
        file_name="storyboard.txt",
        mime="text/plain",
    )
