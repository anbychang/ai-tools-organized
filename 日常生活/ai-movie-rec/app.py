import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 電影推薦", page_icon="🎬")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    st.markdown("🔑 請先取得 [Groq API Key](https://console.groq.com/)")

st.title("🎬 AI 電影推薦")
st.markdown("告訴 AI 你現在的心情和偏好，讓它為你推薦最適合的電影！")

# --- 參數設定 ---
col1, col2 = st.columns(2)
with col1:
    mood = st.selectbox("😊 你現在的心情", ["開心", "難過", "無聊", "刺激", "浪漫"])
with col2:
    genre = st.selectbox("🎥 類型偏好", [
        "不限",
        "動作片",
        "喜劇片",
        "劇情片",
        "恐怖片",
        "科幻片",
        "愛情片",
        "動畫片",
        "紀錄片",
    ])

extra = st.text_input("💬 其他偏好（選填）", placeholder="例如：想看亞洲電影、不要太長的、經典老片...")

generate = st.button("🍿 推薦電影", use_container_width=True)

if generate:
    if not api_key:
        st.warning("⚠️ 請先在側邊欄輸入 Groq API Key。")
        st.stop()

    extra_text = f"\n- 其他偏好：{extra}" if extra.strip() else ""

    prompt = (
        f"你是一位資深電影評論家與推薦專家。\n"
        f"請根據以下條件推薦 5 部電影：\n"
        f"- 心情：{mood}\n"
        f"- 類型偏好：{genre}{extra_text}\n\n"
        f"每部電影請提供：\n"
        f"1. 電影名稱（中英文）\n"
        f"2. 年份與導演\n"
        f"3. 推薦指數（用 ⭐ 表示，1-5 顆星）\n"
        f"4. 一句話推薦理由\n"
        f"5. 為什麼適合目前的心情\n\n"
        f"全文使用繁體中文。\n"
        f"格式範例：\n"
        f"### 1. 電影名稱（English Title）\n"
        f"📅 年份 | 🎬 導演\n"
        f"⭐⭐⭐⭐⭐ 推薦指數\n"
        f"💬 推薦理由：...\n"
        f"🎯 適合原因：..."
    )

    client = Groq(api_key=api_key)
    with st.spinner("🎬 AI 正在挑選電影..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "你是資深電影評論家，擅長用繁體中文推薦電影。"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.8,
                max_tokens=2048,
            )
            result = response.choices[0].message.content
            st.divider()
            st.subheader(f"🍿 心情「{mood}」的電影推薦")
            st.markdown(result)
        except Exception as e:
            st.error(f"❌ 發生錯誤：{e}")
