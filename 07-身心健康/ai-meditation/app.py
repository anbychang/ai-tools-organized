import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 冥想引導", page_icon="🧘")
st.title("🧘 AI 冥想引導")

with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    st.markdown("選擇冥想時長與主題，AI 為你產生個人化的冥想引導詞。")

if "meditation_script" not in st.session_state:
    st.session_state.meditation_script = ""

st.subheader("🌿 冥想設定")
col1, col2 = st.columns(2)
with col1:
    duration = st.selectbox("冥想時長", ["5 分鐘", "10 分鐘", "15 分鐘"])
with col2:
    theme = st.selectbox("冥想主題", ["放鬆身心", "提升專注", "幫助入睡", "感恩練習"])

mood = st.selectbox("目前的狀態", ["有點疲憊", "心情焦躁", "壓力很大", "需要平靜", "想要充電", "一般狀態"])

bg_scene = st.selectbox("引導場景", ["森林小溪", "海邊日落", "山頂雲海", "星空夜晚", "花園晨光", "雨天窗邊"])

if st.button("🕯️ 開始產生冥想引導", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key。")
    else:
        client = Groq(api_key=api_key)
        prompt = f"""你是一位溫柔而專業的冥想引導師。請根據以下設定產生一段完整的冥想引導詞。

時長：{duration}
主題：{theme}
使用者狀態：{mood}
引導場景：{bg_scene}

要求：
1. 語調溫柔、緩慢，使用第二人稱「你」
2. 開始時引導呼吸（吸氣...吐氣...）
3. 融入場景的感官描述（視覺、聽覺、觸覺、嗅覺）
4. 根據主題設計核心引導內容
5. 適當加入停頓提示（用「...」或「（停頓 10 秒）」標示）
6. 結束時慢慢引導回到現實
7. 全部使用繁體中文
8. 用分段落呈現，每段之間空一行
9. 段落標題用【】標示，如【開始・呼吸】【引導・場景】等"""

        with st.spinner("正在為你準備冥想引導..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=2500,
                )
                st.session_state.meditation_script = response.choices[0].message.content
            except Exception as e:
                st.error(f"發生錯誤：{e}")

if st.session_state.meditation_script:
    st.markdown("---")
    st.subheader("🕊️ 冥想引導詞")
    st.markdown(st.session_state.meditation_script)
    st.download_button(
        label="💾 下載冥想引導詞",
        data=st.session_state.meditation_script,
        file_name="meditation_guide.txt",
        mime="text/plain",
    )
