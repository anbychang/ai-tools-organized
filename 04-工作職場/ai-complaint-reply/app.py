import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 客訴回覆產生器", page_icon="📞")

st.title("📞 AI 客訴回覆產生器")
st.markdown("輸入客訴內容、選擇回覆語氣，AI 幫你產生專業的客服回覆。")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("### 客訴回覆原則")
    st.markdown(
        "- 先同理，再處理\n"
        "- 不推卸責任\n"
        "- 提供具體解決方案\n"
        "- 保持專業禮貌\n"
        "- 給予後續追蹤承諾"
    )

# --- 主要輸入 ---
complaint = st.text_area(
    "😤 客訴內容",
    placeholder="貼上客戶的投訴文字...",
    height=150,
)

col1, col2 = st.columns(2)
with col1:
    tone = st.selectbox(
        "🎭 回覆語氣",
        ["道歉型（誠懇致歉）", "解釋型（說明原因）", "補償型（提供補償方案）"],
    )
with col2:
    channel = st.selectbox(
        "📱 回覆管道",
        ["Email", "社群媒體留言", "LINE / 即時通訊", "電話客服稿"],
    )

col3, col4 = st.columns(2)
with col3:
    industry = st.selectbox(
        "🏢 產業類別",
        ["電商/零售", "餐飲", "科技/軟體", "金融/保險", "旅遊/飯店",
         "醫療", "教育", "物流", "其他"],
    )
with col4:
    severity = st.selectbox(
        "🔥 客訴嚴重程度",
        ["輕微（小抱怨）", "中等（明確不滿）", "嚴重（威脅退貨/退款/投訴）"],
    )

solution = st.text_input(
    "💡 公司可提供的解決方案（選填）",
    placeholder="例如：可以退款、補發商品、提供折扣碼...",
)

# --- 產生回覆 ---
if st.button("✍️ 產生回覆", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not complaint:
        st.error("請輸入客訴內容。")
    else:
        tone_name = tone.split("（")[0]
        prompt = (
            f"你是一位專業的客服溝通顧問。請根據以下客訴內容，產生一封專業的回覆。\n\n"
            f"客訴內容：{complaint}\n"
            f"回覆語氣：{tone}\n"
            f"回覆管道：{channel}\n"
            f"產業類別：{industry}\n"
            f"嚴重程度：{severity}\n"
            f"可提供方案：{solution if solution else '由 AI 建議'}\n\n"
            f"請用繁體中文回答，要求：\n"
            f"1. 符合「{tone_name}」的語氣風格\n"
            f"2. 適合「{channel}」管道的篇幅與格式\n"
            f"3. 包含：表達理解 → 說明處理方式 → 提供解決方案 → 後續追蹤承諾\n"
            f"4. 語氣專業但有溫度\n"
            f"5. 避免制式化的罐頭回覆感\n\n"
            f"請提供 2 個版本的回覆供選擇。"
        )

        client = Groq(api_key=api_key)

        with st.spinner("AI 正在撰寫客服回覆..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是專業的客服溝通顧問，擅長處理客訴與撰寫回覆。請用繁體中文回答。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.7,
                    max_tokens=2048,
                )
                result = response.choices[0].message.content
                st.markdown("---")
                st.subheader("💌 客服回覆")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
