import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 消費糾紛助手", page_icon="🛒", layout="centered")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("取得 API Key：[Groq Console](https://console.groq.com/)")

st.title("🛒 AI 消費糾紛助手")
st.caption("幫助您處理消費問題，教您如何申訴並代擬申訴信函")

# --- 消費問題描述 ---
problem = st.text_area(
    "📝 請描述您的消費問題",
    height=180,
    placeholder="例如：我在某網購平台買了一台筆電，收到後發現是瑕疵品，聯繫客服後對方拒絕退貨退款...",
)

col1, col2 = st.columns(2)
with col1:
    purchase_channel = st.selectbox(
        "🏪 購買管道",
        ["網路購物", "實體店面", "電視購物", "電話行銷", "其他"],
    )
with col2:
    amount = st.text_input("💰 消費金額（約略）", placeholder="例如：NT$15,000")

action_type = st.radio(
    "📌 您需要什麼協助？",
    ["完整申訴教學", "代擬申訴信函", "兩者都要"],
    horizontal=True,
)

if st.button("🚀 取得協助", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not problem.strip():
        st.error("請描述您的消費問題。")
    else:
        instruction = ""
        if action_type == "完整申訴教學":
            instruction = (
                "請提供完整的申訴步驟教學，包含：\n"
                "1. 建議的處理順序（從與商家協商到向消保官申訴）\n"
                "2. 各申訴管道的詳細資訊（消保官、消基會、1950消費者服務專線、行政院消費者保護會線上申訴等）\n"
                "3. 需要準備的文件與證據\n"
                "4. 各步驟的注意事項與時效"
            )
        elif action_type == "代擬申訴信函":
            instruction = (
                "請幫我撰寫一封正式的消費申訴信函，包含：\n"
                "1. 正式的信函格式\n"
                "2. 事件經過的清楚陳述\n"
                "3. 法律依據（消費者保護法相關條文）\n"
                "4. 明確的訴求與期望處理方式\n"
                "5. 合理的回覆期限"
            )
        else:
            instruction = (
                "請同時提供：\n"
                "【Part 1 - 申訴步驟教學】\n"
                "完整的申訴步驟、各管道資訊、需準備文件、注意事項\n\n"
                "【Part 2 - 申訴信函範本】\n"
                "正式的申訴信函，含事件陳述、法律依據、訴求與期限"
            )

        prompt = (
            f"你是台灣消費者保護專家。使用者遇到以下消費問題：\n\n"
            f"問題描述：{problem}\n"
            f"購買管道：{purchase_channel}\n"
            f"消費金額：{amount if amount else '未提供'}\n\n"
            f"{instruction}\n\n"
            "請用繁體中文回答，提供實用且具體的建議。"
        )

        try:
            client = Groq(api_key=api_key)
            with st.spinner("AI 正在為您準備消費申訴方案..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是台灣消費者保護專家，熟悉消費者保護法及各種申訴管道。請用繁體中文提供專業且實用的建議。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.4,
                    max_tokens=2048,
                )
            result = response.choices[0].message.content
            st.markdown("---")
            st.subheader("📋 消費申訴方案")
            st.markdown(result)

            st.info("💡 **小提醒**：消費申訴有時效限制，建議盡早處理。如需進一步協助，可撥打 1950 消費者服務專線。")
        except Exception as e:
            st.error(f"發生錯誤：{e}")
