import streamlit as st
import re
from groq import Groq

st.set_page_config(page_title="AI Rap 歌詞", page_icon="🎤")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    st.markdown("🔑 請先取得 [Groq API Key](https://console.groq.com/)")

st.title("🎤 AI Rap 歌詞產生器")
st.markdown("輸入主題，選擇風格，讓 AI 為你寫出押韻的饒舌歌詞！")

# --- 參數設定 ---
topic = st.text_input("🎵 主題", placeholder="例如：夜市人生、追夢、台北下雨天")
rap_style = st.selectbox("🎧 風格", ["老派", "陷阱", "自由式"])

style_desc = {
    "老派": "Old School 風格，注重節奏韻律、flow 穩定，歌詞有故事性",
    "陷阱": "Trap 風格，節奏感強，使用重複的 hook，氛圍暗黑或炫富",
    "自由式": "Freestyle 風格，自由奔放，押韻密集，展現文字技巧",
}

generate = st.button("🔥 產生歌詞", use_container_width=True)

if generate:
    if not api_key:
        st.warning("⚠️ 請先在側邊欄輸入 Groq API Key。")
        st.stop()
    if not topic.strip():
        st.warning("⚠️ 請輸入主題。")
        st.stop()

    prompt = (
        f"你是一位專業的中文饒舌歌詞創作者。\n"
        f"請根據以下條件創作一首饒舌歌詞：\n"
        f"- 主題：{topic}\n"
        f"- 風格：{rap_style}（{style_desc[rap_style]}）\n\n"
        f"要求：\n"
        f"1. 歌詞分為 2-3 段 verse + 1 段 hook/chorus\n"
        f"2. 每段 verse 約 8-12 行\n"
        f"3. 注重押韻，每行結尾盡量押韻\n"
        f"4. 在每行押韻的字詞後面用【】標記，例如：走在街頭的夜【晚】\n"
        f"5. 全文使用繁體中文\n"
        f"6. 加上段落標題如 [Verse 1]、[Hook] 等"
    )

    client = Groq(api_key=api_key)

    with st.spinner("🎤 正在寫詞中..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "你是一位才華橫溢的繁體中文饒舌歌詞創作者。"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.9,
                max_tokens=2048,
            )
            lyrics = response.choices[0].message.content

            st.divider()
            st.subheader(f"🎵 《{topic}》— {rap_style}風格")

            # 將【】標記的押韻字詞高亮顯示
            highlighted = re.sub(
                r"【(.+?)】",
                r'<span style="background-color:#ff6b6b;color:white;padding:1px 4px;border-radius:3px;font-weight:bold">\1</span>',
                lyrics,
            )
            # 保留換行
            highlighted = highlighted.replace("\n", "<br>")
            st.markdown(highlighted, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ 發生錯誤：{e}")
