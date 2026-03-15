import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 穿搭建議", page_icon="👗")
st.title("👗 AI 穿搭建議師")
st.subheader("根據天氣、場合、風格，給你最佳穿搭組合")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    st.markdown("### 使用說明")
    st.markdown("1. 輸入 Groq API Key\n2. 設定天氣與場合\n3. 點擊取得建議")

# 主要內容
col1, col2 = st.columns(2)
with col1:
    weather = st.selectbox("🌤️ 天氣狀況", ["晴天", "陰天", "雨天", "大雨", "寒流", "悶熱"])
    temperature = st.slider("🌡️ 氣溫（°C）", -5, 42, 25)
    gender = st.selectbox("⚤ 性別", ["女性", "男性", "不限"])
with col2:
    occasion = st.selectbox("📍 場合", ["上班", "約會", "運動", "休閒", "面試", "婚禮", "朋友聚餐", "旅遊"])
    style = st.selectbox("🎨 風格偏好", ["簡約", "韓系", "日系", "街頭", "正式", "文青", "隨性"])
    body_type = st.selectbox("👤 體型（選填）", ["不指定", "嬌小", "高挑", "微胖", "纖瘦", "壯碩"])

extra_notes = st.text_input("💬 其他需求（選填）", placeholder="例如：不喜歡裙子、想要顯瘦、喜歡藍色系...")

if st.button("👔 取得穿搭建議", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key！")
    else:
        prompt = f"""你是一位專業時尚穿搭顧問。請根據以下條件，提供穿搭建議。

天氣：{weather}
氣溫：{temperature}°C
性別：{gender}
場合：{occasion}
風格偏好：{style}
體型：{body_type}
其他需求：{extra_notes if extra_notes else '無'}

請用繁體中文回答，提供 3 套完整穿搭組合，每套包含：
1. **整體造型名稱**
2. **上身** - 具體單品建議（含顏色）
3. **下身** - 具體單品建議（含顏色）
4. **外套/外搭**（如需要）
5. **鞋子**
6. **配件** - 包包、飾品、帽子等
7. **穿搭重點提示** - 為什麼這樣搭配適合該場合

最後給一個「今日穿搭小訣竅」的總結。"""

        try:
            client = Groq(api_key=api_key)
            with st.spinner("正在搭配最佳造型..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.8,
                    max_tokens=3000,
                )
            st.markdown("---")
            st.markdown("### 🎀 今日穿搭推薦")
            st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"發生錯誤：{e}")
