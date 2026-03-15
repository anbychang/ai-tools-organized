import streamlit as st
from groq import Groq

# --- 頁面設定 ---
st.set_page_config(page_title="AI 網紅企劃", page_icon="📱", layout="centered")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("使用 **Llama 3.3 70B** 模型")
    st.markdown("AI 幫你規劃 7 天內容日曆！")

# --- 主頁面 ---
st.title("📱 AI 網紅企劃")
st.markdown("輸入你的主題和平台，AI 幫你產生 7 天完整內容企劃！")

col1, col2 = st.columns(2)
with col1:
    niche = st.text_input("🎯 主題 / Niche", placeholder="例如：健身、美食、科技開箱")
with col2:
    platform = st.selectbox("📲 平台", ["Instagram", "YouTube", "TikTok", "Facebook", "小紅書", "Threads"])

target_audience = st.text_input("👥 目標受眾", placeholder="例如：18-30歲大學生、上班族媽媽")
tone = st.selectbox("🎨 風格調性", ["輕鬆幽默", "專業知性", "溫暖療癒", "潮流時尚", "熱血激勵"])

if st.button("🚀 產生 7 天企劃", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key！")
    elif not niche.strip():
        st.error("請輸入主題！")
    else:
        try:
            client = Groq(api_key=api_key)
            prompt = f"""你是一位專業的社群媒體行銷企劃師。請根據以下資訊產生 7 天的內容日曆。

主題/Niche：{niche}
平台：{platform}
目標受眾：{target_audience if target_audience.strip() else "一般大眾"}
風格調性：{tone}

請為每一天提供：
1. 📅 日期（Day 1 ~ Day 7）
2. 📌 貼文主題
3. 📝 貼文文案（含 hashtag）
4. 🎨 建議的視覺/影片內容描述
5. ⏰ 最佳發布時間
6. 💡 互動策略小技巧

最後請附上一個整週的策略總結和 KPI 建議。
全部用繁體中文，格式清楚，使用 markdown 表格或條列。"""

            with st.spinner("📋 AI 正在規劃內容日曆..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是專業的社群媒體行銷企劃師，專精於繁體中文市場的內容策略。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.8,
                    max_tokens=2048,
                )
            result = response.choices[0].message.content
            st.markdown("---")
            st.subheader("📅 7 天內容日曆")
            st.markdown(result)

        except Exception as e:
            st.error(f"發生錯誤：{e}")

# --- 頁尾 ---
st.markdown("---")
st.caption("AI 網紅企劃 — 讓 AI 幫你成為下一個人氣網紅 📱")
