import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 情書產生器", page_icon="💌")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    st.markdown("🔑 請先取得 [Groq API Key](https://console.groq.com/)")

st.title("💌 AI 情書產生器")
st.markdown("選擇年代風格，輸入對象名字，讓 AI 為你撰寫一封動人的情書。")

# --- 參數設定 ---
style = st.selectbox("📜 年代風格", ["古典文言", "民國風", "現代", "搞笑"])
name = st.text_input("💕 對象名字", placeholder="例如：小美")

style_desc = {
    "古典文言": "使用古典文言文風格，引用詩詞典故，文辭優雅古樸，如古代才子佳人書信往來",
    "民國風": "使用民國時期的書信風格，帶有含蓄深情的語調，如徐志摩、林徽因般的浪漫文筆",
    "現代": "使用現代白話文，真摯感人，帶有都市愛情的氛圍，溫暖而深情",
    "搞笑": "使用幽默搞笑的風格，充滿諧音梗、網路用語和令人莞爾的表白方式，但底層仍是真摯的情感",
}

generate = st.button("💝 產生情書", use_container_width=True)

if generate:
    if not api_key:
        st.warning("⚠️ 請先在側邊欄輸入 Groq API Key。")
        st.stop()
    if not name.strip():
        st.warning("⚠️ 請輸入對象名字。")
        st.stop()

    prompt = (
        f"你是一位擅長撰寫情書的繁體中文作家。\n"
        f"請根據以下條件撰寫一封約 300-500 字的情書：\n"
        f"- 風格：{style}（{style_desc[style]}）\n"
        f"- 對象名字：{name}\n\n"
        f"要求：\n"
        f"1. 情書要有稱呼開頭和署名結尾\n"
        f"2. 內容要真摯感人，符合所選風格\n"
        f"3. 善用比喻和意象\n"
        f"4. 全文使用繁體中文\n"
        f"5. 署名用「你的秘密仰慕者」"
    )

    client = Groq(api_key=api_key)

    with st.spinner("💌 正在醞釀情感中..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "你是一位擅長用繁體中文撰寫各種風格情書的作家。"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.9,
                max_tokens=1500,
            )
            letter = response.choices[0].message.content
            st.divider()
            st.subheader(f"💌 致 {name} 的{style}情書")
            st.markdown(letter)
        except Exception as e:
            st.error(f"❌ 發生錯誤：{e}")
