import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 法律諮詢", page_icon="⚖️", layout="centered")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("取得 API Key：[Groq Console](https://console.groq.com/)")

st.title("⚖️ AI 法律諮詢助手")

st.warning(
    "⚠️ **重要免責聲明**\n\n"
    "本工具僅提供一般性法律資訊參考，**不構成正式法律建議**。"
    "每個案件的具體情況不同，建議您諮詢專業律師以獲得正確的法律協助。"
    "AI 生成的內容可能有誤，請勿直接作為法律行動依據。"
)

# --- 糾紛類型 ---
dispute_type = st.selectbox(
    "📋 糾紛類型",
    ["消費糾紛", "勞資糾紛", "租屋糾紛", "交通糾紛", "鄰居糾紛"],
    index=0,
)

# --- 糾紛描述 ---
situation = st.text_area(
    "📝 請描述您的糾紛情況",
    height=200,
    placeholder="請盡量詳細描述事件經過、時間、涉及的人物與目前狀況...",
)

if st.button("🔍 取得法律分析", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not situation.strip():
        st.error("請描述您的糾紛情況。")
    else:
        prompt = (
            f"你是一位台灣法律諮詢助手，專精於台灣法律。使用者遇到一個「{dispute_type}」的問題。\n\n"
            f"糾紛描述：\n{situation}\n\n"
            "請以繁體中文提供以下分析：\n"
            "1. **情況分析**：簡要分析此糾紛的法律性質\n"
            "2. **相關法律條文**：列出可能適用的台灣法律條文（含法條名稱與條號）\n"
            "3. **權利與義務**：說明當事人的法律權利與義務\n"
            "4. **建議處理步驟**：提供具體的處理步驟建議\n"
            "5. **可尋求的協助管道**：列出可以尋求幫助的管道（如法律扶助基金會、調解委員會等）\n\n"
            "最後請再次提醒使用者，此為一般性參考，建議諮詢專業律師。"
        )

        try:
            client = Groq(api_key=api_key)
            with st.spinner("AI 正在分析您的法律問題..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是一位專業的台灣法律諮詢助手，熟悉台灣各類法律。請用繁體中文回答，提供準確且實用的法律資訊。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.4,
                    max_tokens=2048,
                )
            result = response.choices[0].message.content
            st.markdown("---")
            st.subheader("📄 法律分析結果")
            st.markdown(result)

            st.markdown("---")
            st.error(
                "⚠️ **再次提醒**：以上內容僅供參考，不構成法律建議。"
                "請務必諮詢專業律師以獲得針對您個案的正確法律協助。"
            )
        except Exception as e:
            st.error(f"發生錯誤：{e}")
