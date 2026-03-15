import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 標題產生器", page_icon="📰", layout="centered")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("取得 API Key：[Groq Console](https://console.groq.com/)")

st.title("📰 AI 標題產生器")
st.caption("根據內容摘要，產生 10 個吸睛標題並排名")

# --- 內容摘要 ---
summary = st.text_area(
    "📝 內容摘要",
    height=180,
    placeholder="請描述你的文章/影片/貼文的主要內容...\n例如：分享我從月薪 3 萬到年薪百萬的轉職經歷，包含如何學習新技能、面試技巧和薪資談判的心得...",
)

# --- 平台選擇 ---
col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox(
        "📱 目標平台",
        ["YouTube", "部落格", "新聞媒體", "Dcard", "PTT", "Facebook", "Medium"],
    )
with col2:
    category = st.selectbox(
        "📂 內容分類",
        ["科技", "生活", "財經", "旅遊", "美食", "教學", "職場", "感情", "時事", "娛樂", "其他"],
    )

# --- 風格偏好 ---
st.subheader("🎨 標題偏好")
col3, col4 = st.columns(2)
with col3:
    style = st.multiselect(
        "標題風格（可多選）",
        ["引發好奇", "數字型", "提問型", "故事型", "對比型", "教學型", "情緒型"],
        default=["引發好奇"],
    )
with col4:
    avoid = st.multiselect(
        "避免的風格",
        ["過度誇張", "標題黨", "負面情緒", "太長", "太短"],
    )

target_audience = st.text_input(
    "🎯 目標受眾（選填）",
    placeholder="例如：20-30 歲上班族、大學生、新手爸媽...",
)

if st.button("🎯 產生標題", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not summary.strip():
        st.error("請輸入內容摘要。")
    else:
        style_str = "、".join(style) if style else "不限"
        avoid_str = "、".join(avoid) if avoid else "無"
        prompt = (
            f"你是台灣頂尖的標題撰寫專家，熟悉各平台的流量密碼。\n\n"
            f"內容摘要：\n{summary}\n\n"
            f"目標平台：{platform}\n"
            f"內容分類：{category}\n"
            f"偏好風格：{style_str}\n"
            f"避免風格：{avoid_str}\n"
            f"目標受眾：{target_audience if target_audience.strip() else '一般大眾'}\n\n"
            "請產生 10 個標題，並依照「吸引力」從高到低排名。每個標題請提供：\n\n"
            "格式：\n"
            "**排名. 標題文字**\n"
            "- 吸引力評分：⭐ X/10\n"
            "- 使用技巧：（說明用了什麼標題技巧）\n"
            "- 適合原因：（為什麼這個標題適合此平台和受眾）\n\n"
            "最後請提供 2-3 個「下標小技巧」的總結建議。\n"
            "標題請符合該平台的文化特色（例如 Dcard 較口語、新聞較正式）。\n"
            "請用繁體中文撰寫。"
        )

        try:
            client = Groq(api_key=api_key)
            with st.spinner("AI 正在為你產生吸睛標題..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是台灣頂尖的標題撰寫專家，熟悉各社群平台的流量密碼。請用繁體中文撰寫。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.8,
                    max_tokens=2048,
                )
            result = response.choices[0].message.content
            st.markdown("---")
            st.subheader("🏆 標題排行榜")
            st.markdown(result)
            st.success("💡 好標題是成功的一半！選一個最適合的，也可以混搭不同標題的元素。")
        except Exception as e:
            st.error(f"發生錯誤：{e}")
