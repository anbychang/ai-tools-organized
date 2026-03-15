import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 歌詞創作", page_icon="🎵")
st.title("🎵 AI 歌詞創作")
st.caption("輸入主題與風格，AI 為你寫出完整的歌詞，包含主歌、副歌結構")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    st.markdown("### 📖 使用說明")
    st.markdown(
        "1. 輸入 Groq API Key\n"
        "2. 設定歌曲主題與風格\n"
        "3. 點擊「開始創作」"
    )

# 主介面
st.markdown("### 🎶 歌曲設定")

song_theme = st.text_input(
    "💡 歌曲主題",
    placeholder="例如：在城市中追尋夢想的孤獨旅人"
)

col1, col2 = st.columns(2)
with col1:
    style = st.selectbox("🎸 音樂風格", ["抒情", "嘻哈", "搖滾", "電子", "民謠", "R&B", "古風"])
with col2:
    mood = st.selectbox("🌈 情感基調", ["溫暖", "憂傷", "激昂", "甜蜜", "迷幻", "豪放", "淡然"])

col3, col4 = st.columns(2)
with col3:
    language_mix = st.selectbox("🌐 語言", ["純中文", "中英混搭", "帶方言感"])
with col4:
    structure = st.selectbox(
        "🏗️ 歌曲結構",
        ["Verse-Chorus-Verse-Chorus-Bridge-Chorus",
         "Verse-Chorus-Verse-Chorus",
         "Verse-PreChorus-Chorus-Verse-PreChorus-Chorus"]
    )

keywords = st.text_input(
    "🔑 關鍵意象/詞彙（選填，用逗號分隔）",
    placeholder="例如：星空, 咖啡, 末班車, 霓虹燈"
)

rhyme = st.checkbox("🎯 要求押韻", value=True)

if st.button("🚀 開始創作", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key！")
    elif not song_theme.strip():
        st.error("請輸入歌曲主題！")
    else:
        try:
            client = Groq(api_key=api_key)
            keywords_line = f"請盡量融入以下意象/詞彙：{keywords}" if keywords else ""
            rhyme_line = "每段歌詞需要押韻，韻腳自然不勉強。" if rhyme else ""

            prompt = f"""你是一位華語金曲等級的作詞人。請根據以下設定創作一首完整的歌詞。

歌曲主題：{song_theme}
音樂風格：{style}
情感基調：{mood}
語言：{language_mix}
歌曲結構：{structure}
{keywords_line}
{rhyme_line}

創作要求：
1. 嚴格按照指定的歌曲結構，標注每個段落（Verse 1/主歌一、Chorus/副歌、Bridge/橋段 等）
2. 歌詞意境優美，用字精煉
3. 副歌要有記憶點，適合傳唱
4. 風格符合所選的音樂類型
5. 全部使用繁體中文

請先給一個歌名，然後寫出完整歌詞。最後附上簡短的創作理念說明。"""

            with st.spinner("AI 正在創作歌詞中..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是頂尖華語作詞人，擅長各種風格的歌詞創作，使用繁體中文。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8,
                    max_tokens=4096,
                )
            result = response.choices[0].message.content
            st.divider()
            st.markdown(result)

        except Exception as e:
            st.error(f"發生錯誤：{e}")
