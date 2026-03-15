import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 睡前故事", page_icon="🌙")
st.title("🌙 AI 睡前故事")

with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    st.markdown("為孩子（或自己）量身打造一個溫馨的睡前故事！")

if "bedtime_story" not in st.session_state:
    st.session_state.bedtime_story = ""

st.subheader("📖 故事設定")

col1, col2 = st.columns(2)
with col1:
    protagonist = st.text_input("主角名字", placeholder="例如：小星星")
with col2:
    age_group = st.selectbox("適合年齡", ["3-5 歲", "6-8 歲", "9-12 歲", "大人也適合"])

col3, col4 = st.columns(2)
with col3:
    story_type = st.selectbox("故事類型", ["奇幻魔法", "動物王國", "太空探險", "海底世界"])
with col4:
    story_mood = st.selectbox("故事氛圍", ["溫馨治癒", "輕鬆有趣", "充滿勇氣", "夢幻浪漫"])

extra_element = st.text_input("額外元素（選填）", placeholder="例如：會說話的貓咪、彩虹橋、魔法餅乾...")

if st.button("✨ 產生睡前故事", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key。")
    elif not protagonist:
        st.warning("請輸入主角的名字。")
    else:
        client = Groq(api_key=api_key)
        prompt = f"""你是一位溫柔的故事作家，專門寫睡前故事。請根據以下設定創作一個溫馨的睡前故事。

主角名字：{protagonist}
適合年齡：{age_group}
故事類型：{story_type}
故事氛圍：{story_mood}
額外元素：{extra_element if extra_element else "無"}

要求：
1. 故事要溫馨、正面，結尾讓人安心入睡
2. 語言要適合目標年齡層
3. 用生動的描述營造畫面感
4. 包含有趣的對話
5. 故事長度約 500-800 字
6. 故事結尾要有「安靜下來、準備入睡」的氛圍
7. 全部使用繁體中文
8. 開頭用一個有吸引力的標題
9. 最後加上「🌙 晚安，好夢。」"""

        with st.spinner("故事精靈正在編織故事..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.8,
                    max_tokens=2000,
                )
                st.session_state.bedtime_story = response.choices[0].message.content
            except Exception as e:
                st.error(f"發生錯誤：{e}")

if st.session_state.bedtime_story:
    st.markdown("---")
    st.markdown(st.session_state.bedtime_story)
    st.download_button(
        label="💾 下載故事",
        data=st.session_state.bedtime_story,
        file_name="bedtime_story.txt",
        mime="text/plain",
    )
