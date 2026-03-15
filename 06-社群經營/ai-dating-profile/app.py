import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 交友檔案產生器", page_icon="💘", layout="centered")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("取得 API Key：[Groq Console](https://console.groq.com/)")

st.title("💘 AI 交友檔案產生器")
st.caption("打造吸引人的交友平台個人簡介")

# --- 基本資訊 ---
st.subheader("👤 關於你")

col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("性別", ["男", "女", "不想透露"])
    age = st.number_input("年齡", min_value=18, max_value=80, value=25)
    occupation = st.text_input("職業", placeholder="例如：軟體工程師、老師、設計師")
with col2:
    looking_for = st.selectbox("尋找對象", ["男", "女", "都可以"])
    location = st.text_input("所在地", placeholder="例如：台北、台中")
    height = st.text_input("身高（選填）", placeholder="例如：175cm")

interests = st.text_area(
    "🎯 興趣與嗜好",
    height=80,
    placeholder="例如：看電影、爬山、做甜點、打籃球、看漫畫、彈吉他...",
)

personality = st.text_area(
    "✨ 個性描述",
    height=80,
    placeholder="例如：外向、喜歡嘗試新事物、有點冷笑話王、很會照顧人...",
)

# --- 平台選擇 ---
platform = st.selectbox(
    "📱 交友平台",
    ["Tinder", "Bumble", "Pairs", "CMB（Coffee Meets Bagel）", "Hinge"],
)

# --- 風格偏好 ---
tone = st.selectbox(
    "🎨 自介風格",
    ["幽默風趣", "真誠溫暖", "神秘感", "陽光活潑", "文青知性"],
)

bio_count = st.slider("📝 產生幾組自介", min_value=1, max_value=5, value=3)

if st.button("💝 產生交友檔案", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not interests.strip():
        st.error("請至少填寫你的興趣與嗜好。")
    else:
        prompt = (
            f"你是交友平台個人檔案的專業寫手，擅長撰寫吸引人的自我介紹。\n\n"
            f"使用者資訊：\n"
            f"- 性別：{gender}，年齡：{age}歲\n"
            f"- 職業：{occupation if occupation else '未提供'}\n"
            f"- 所在地：{location if location else '未提供'}\n"
            f"- 身高：{height if height else '未提供'}\n"
            f"- 尋找：{looking_for}\n"
            f"- 興趣嗜好：{interests}\n"
            f"- 個性：{personality if personality.strip() else '未提供'}\n\n"
            f"目標平台：{platform}\n"
            f"自介風格：{tone}\n\n"
            f"請產生 {bio_count} 組不同的交友自介，注意：\n"
            f"1. 符合 {platform} 的字數限制與文化\n"
            "2. 要有個人特色，避免千篇一律\n"
            "3. 適當展現幽默感或獨特性\n"
            "4. 留下讓對方想聊天的「鉤子」\n"
            "5. 避免負面用語或太多條件限制\n\n"
            "每組自介請附上簡短的「使用建議」。請用繁體中文撰寫。"
        )

        try:
            client = Groq(api_key=api_key)
            with st.spinner("AI 正在為你打造交友檔案..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是交友平台個人檔案寫手，熟悉各平台文化。請用繁體中文撰寫吸引人的自介。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.8,
                    max_tokens=1536,
                )
            result = response.choices[0].message.content
            st.markdown("---")
            st.subheader("💝 你的交友自介")
            st.markdown(result)
            st.success("💡 選一個最符合你風格的自介，直接複製到交友平台上吧！")
        except Exception as e:
            st.error(f"發生錯誤：{e}")
