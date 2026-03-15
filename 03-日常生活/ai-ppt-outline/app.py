import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI PPT 大綱產生器", page_icon="📊")

st.title("📊 AI PPT 大綱產生器")
st.markdown("輸入簡報主題、時間長度與對象，AI 幫你產生逐頁大綱與講者備註。")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("### 使用說明")
    st.markdown(
        "1. 輸入 Groq API Key\n"
        "2. 填寫簡報主題、時間與對象\n"
        "3. 點擊「產生大綱」"
    )

# --- 主要輸入 ---
topic = st.text_input("📌 簡報主題", placeholder="例如：2024 年度行銷策略報告")

col1, col2 = st.columns(2)
with col1:
    duration = st.selectbox(
        "⏱️ 簡報時間長度",
        ["5 分鐘", "10 分鐘", "15 分鐘", "20 分鐘", "30 分鐘", "45 分鐘", "60 分鐘"],
        index=2,
    )
with col2:
    audience = st.text_input("🎯 簡報對象", placeholder="例如：公司高階主管")

extra_notes = st.text_area(
    "📝 額外需求（選填）",
    placeholder="例如：需要包含數據圖表建議、希望風格輕鬆活潑...",
    height=80,
)

# --- 產生大綱 ---
if st.button("🚀 產生大綱", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not topic:
        st.error("請輸入簡報主題。")
    elif not audience:
        st.error("請輸入簡報對象。")
    else:
        prompt = (
            f"你是一位專業的簡報顧問。請根據以下資訊，產生一份完整的 PPT 簡報大綱。\n\n"
            f"簡報主題：{topic}\n"
            f"簡報時間：{duration}\n"
            f"簡報對象：{audience}\n"
            f"額外需求：{extra_notes if extra_notes else '無'}\n\n"
            f"請用繁體中文回答，格式如下：\n"
            f"每一頁投影片請包含：\n"
            f"- 頁碼與標題\n"
            f"- 該頁重點內容（3-5 個要點）\n"
            f"- 建議的視覺元素（圖表、圖片等）\n"
            f"- 講者備註（該頁要講什麼、如何銜接下一頁）\n"
            f"- 建議花費時間\n\n"
            f"請根據簡報時間合理分配頁數與內容量。"
        )

        client = Groq(api_key=api_key)

        with st.spinner("AI 正在產生簡報大綱..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是專業的簡報設計顧問，擅長規劃簡報架構與內容。請用繁體中文回答。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.7,
                    max_tokens=4096,
                )
                result = response.choices[0].message.content
                st.markdown("---")
                st.subheader("📋 簡報大綱")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
