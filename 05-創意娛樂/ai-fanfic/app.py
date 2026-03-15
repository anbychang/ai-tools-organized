import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 二創同人", page_icon="✍️")
st.title("✍️ AI 二創同人小說產生器")

with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    st.markdown("輸入你喜歡的作品、角色和情境，AI 幫你寫同人小說！")

if "fanfic_result" not in st.session_state:
    st.session_state.fanfic_result = ""

st.subheader("📖 作品設定")
source_work = st.text_input("原作作品名", placeholder="例如：鬼滅之刃、哈利波特、原神...")

col1, col2 = st.columns(2)
with col1:
    characters = st.text_input("角色名稱（用逗號分隔）", placeholder="例如：炭治郎, 禰豆子")
with col2:
    genre = st.selectbox("同人類型", ["友情向", "戀愛向", "冒險向", "日常向", "搞笑向", "虐心向", "治癒向"])

situation = st.text_area("情境描述", placeholder="例如：在現代咖啡廳偶遇的平行世界故事...", height=80)

col3, col4 = st.columns(2)
with col3:
    length = st.selectbox("篇幅", ["短篇（500字）", "中篇（1000字）", "長篇（1500字）"])
with col4:
    style = st.selectbox("文風", ["輕小說風", "純文學風", "電影劇本風", "日記體", "書信體"])

if st.button("📝 開始創作", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key。")
    elif not source_work or not characters:
        st.warning("請至少填寫作品名和角色名。")
    else:
        client = Groq(api_key=api_key)
        word_count = length.split("（")[1].replace("）", "")
        prompt = f"""你是一位才華橫溢的同人小說作家。請根據以下設定撰寫一篇同人小說。

原作：{source_work}
角色：{characters}
類型：{genre}
情境：{situation if situation else "自由發揮"}
篇幅：約 {word_count}
文風：{style}

要求：
1. 角色性格要忠於原作
2. 文筆流暢，有畫面感
3. 包含對話和心理描寫
4. 全部使用繁體中文
5. 開頭吸引人，結尾有餘韻
6. 加上一個有創意的標題"""

        with st.spinner("靈感湧現中..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.9,
                    max_tokens=3000,
                )
                st.session_state.fanfic_result = response.choices[0].message.content
            except Exception as e:
                st.error(f"發生錯誤：{e}")

if st.session_state.fanfic_result:
    st.markdown("---")
    st.markdown(st.session_state.fanfic_result)
    st.download_button(
        label="💾 下載小說",
        data=st.session_state.fanfic_result,
        file_name="fanfiction.txt",
        mime="text/plain",
    )
