import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 自我介紹產生器", page_icon="👋")

st.title("👋 AI 自我介紹產生器")
st.markdown("選擇場合、輸入背景資料，AI 幫你量身打造完美的自我介紹。")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("### 好的自我介紹要素")
    st.markdown(
        "- 簡潔有力，抓住重點\n"
        "- 根據場合調整內容\n"
        "- 展現個人特色\n"
        "- 留下深刻印象"
    )

# --- 主要輸入 ---
occasion = st.selectbox(
    "🎯 自我介紹場合",
    ["面試", "社交場合", "開會（新團隊）", "相親", "演講開場", "社團活動", "商務交流"],
)

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("👤 你的名字", placeholder="例如：王小明")
with col2:
    duration = st.selectbox("⏱️ 介紹時間", ["30 秒", "1 分鐘", "2 分鐘", "3 分鐘"])

job = st.text_input("💼 目前職業/身分", placeholder="例如：軟體工程師、大學生、自由工作者")
background = st.text_area(
    "📝 背景資料",
    placeholder="例如：5 年工作經驗、擅長 Python、曾在 Google 實習、喜歡爬山...",
    height=100,
)
goal = st.text_input(
    "🎯 這次自我介紹的目的（選填）",
    placeholder="例如：希望獲得面試機會、想認識新朋友...",
)
style = st.selectbox(
    "🎭 風格偏好",
    ["專業穩重", "輕鬆幽默", "熱情活潑", "謙虛真誠"],
)

# --- 產生自我介紹 ---
if st.button("✨ 產生自我介紹", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not background:
        st.error("請填寫背景資料。")
    else:
        prompt = (
            f"你是一位專業的個人品牌顧問。請根據以下資訊，產生一段量身打造的自我介紹。\n\n"
            f"場合：{occasion}\n"
            f"姓名：{name if name else '未提供'}\n"
            f"職業/身分：{job if job else '未提供'}\n"
            f"介紹時間：{duration}\n"
            f"背景資料：{background}\n"
            f"介紹目的：{goal if goal else '未特別說明'}\n"
            f"風格偏好：{style}\n\n"
            f"請用繁體中文撰寫，要求：\n"
            f"1. 符合場合的語氣與用詞\n"
            f"2. 在指定時間內能自然說完\n"
            f"3. 突出個人亮點\n"
            f"4. 結尾有力，留下印象\n\n"
            f"請提供：\n"
            f"- 完整的自我介紹文稿\n"
            f"- 關鍵要點提示（方便記憶）\n"
            f"- 一個加分小技巧"
        )

        client = Groq(api_key=api_key)

        with st.spinner("AI 正在打造你的自我介紹..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是專業的個人品牌顧問，擅長打造各場合的自我介紹。請用繁體中文回答。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.8,
                    max_tokens=2048,
                )
                result = response.choices[0].message.content
                st.markdown("---")
                st.subheader("🎤 你的自我介紹")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
