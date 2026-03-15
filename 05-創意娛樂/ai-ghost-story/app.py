import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 鬼故事", page_icon="👻")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    st.markdown("🔑 請先取得 [Groq API Key](https://console.groq.com/)")

st.title("👻 AI 鬼故事產生器")
st.markdown("選擇場景與恐怖程度，讓 AI 為你撰寫一段毛骨悚然的鬼故事。")

# --- 參數選擇 ---
col1, col2 = st.columns(2)
with col1:
    scene = st.selectbox("🏚️ 場景", ["學校", "醫院", "山上", "老房子"])
with col2:
    horror_level = st.selectbox("😱 恐怖程度", ["微恐", "中等", "極恐"])

# --- 恐怖程度對應描述 ---
horror_map = {
    "微恐": "輕微的懸疑氛圍，適合膽小的人，不要太嚇人",
    "中等": "有明顯的恐怖元素和緊張氣氛，會讓人起雞皮疙瘩",
    "極恐": "極度恐怖，充滿驚悚、詭異、令人毛骨悚然的細節描寫",
}

generate = st.button("🖊️ 產生鬼故事", use_container_width=True)

if generate:
    if not api_key:
        st.warning("⚠️ 請先在側邊欄輸入 Groq API Key。")
        st.stop()

    prompt = (
        f"你是一位專業的恐怖小說作家，擅長用繁體中文寫作。\n"
        f"請根據以下條件撰寫一篇約 500-800 字的恐怖短篇故事：\n"
        f"- 場景：{scene}\n"
        f"- 恐怖程度：{horror_level}（{horror_map[horror_level]}）\n\n"
        f"要求：\n"
        f"1. 故事要有完整的開頭、發展、高潮和結尾\n"
        f"2. 善用環境描寫營造氛圍\n"
        f"3. 加入出人意料的轉折\n"
        f"4. 結尾要令人回味或毛骨悚然\n"
        f"5. 全文使用繁體中文"
    )

    client = Groq(api_key=api_key)

    with st.spinner("👻 正在召喚故事中..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "你是一位擅長撰寫恐怖故事的繁體中文作家。"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.9,
                max_tokens=2048,
            )
            story = response.choices[0].message.content
            st.divider()
            st.subheader(f"📖 {scene}鬼故事 — {horror_level}")
            st.markdown(story)
        except Exception as e:
            st.error(f"❌ 發生錯誤：{e}")
