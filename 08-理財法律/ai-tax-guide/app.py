import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 報稅教學", page_icon="🧾", layout="centered")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("取得 API Key：[Groq Console](https://console.groq.com/)")

st.title("🧾 AI 報稅教學助手")
st.caption("根據您的身份，提供互動式報稅指南")

# --- 身份選擇 ---
identity = st.selectbox(
    "👤 請選擇您的身份",
    ["上班族（一般受薪階級）", "自由工作者（接案/freelancer）", "學生打工（兼職/工讀）"],
)

# --- 進階資訊 ---
st.subheader("📋 補充資訊（選填，填寫越多指引越精確）")

col1, col2 = st.columns(2)
with col1:
    marital = st.selectbox("婚姻狀態", ["未婚", "已婚", "不想透露"])
    has_dependents = st.selectbox("是否有扶養親屬", ["無", "有（父母）", "有（子女）", "有（父母+子女）"])
with col2:
    income_range = st.selectbox(
        "年收入範圍",
        ["40萬以下", "40-80萬", "80-120萬", "120-200萬", "200萬以上", "不想透露"],
    )
    special = st.multiselect(
        "特殊狀況",
        ["有租屋", "有房貸", "有保險費", "有捐款", "有股票投資", "有海外所得"],
    )

# --- 問題區 ---
question = st.text_area(
    "❓ 有其他報稅相關問題嗎？（選填）",
    height=100,
    placeholder="例如：我今年有換工作，該怎麼處理兩份扣繳憑單？",
)

if st.button("📚 開始報稅教學", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    else:
        special_str = "、".join(special) if special else "無"
        prompt = (
            f"你是台灣報稅教學專家。請為以下使用者提供完整的互動式報稅教學：\n\n"
            f"身份：{identity}\n"
            f"婚姻狀態：{marital}\n"
            f"扶養親屬：{has_dependents}\n"
            f"年收入範圍：{income_range}\n"
            f"特殊狀況：{special_str}\n"
            f"額外問題：{question if question.strip() else '無'}\n\n"
            "請提供以下內容：\n"
            "1. **報稅前準備**：需要準備的文件與資料清單\n"
            "2. **Step-by-Step 報稅步驟**：從登入報稅系統到完成申報的詳細步驟\n"
            "3. **可使用的扣除額**：根據使用者狀況，列出所有可以使用的扣除額與免稅額\n"
            "4. **節稅小技巧**：針對此身份的合法節稅建議\n"
            "5. **常見錯誤提醒**：新手常犯的報稅錯誤\n"
            "6. **重要日期與期限**：報稅相關的重要時程\n\n"
            "如果使用者有額外問題，請一併回答。請用繁體中文，語氣親切易懂。"
        )

        try:
            client = Groq(api_key=api_key)
            with st.spinner("AI 正在為您準備報稅教學..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是台灣報稅教學專家，熟悉台灣所得稅法與報稅流程。請用繁體中文、親切的語氣提供教學。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.4,
                    max_tokens=2048,
                )
            result = response.choices[0].message.content
            st.markdown("---")
            st.subheader("📖 您的報稅教學指南")
            st.markdown(result)

            st.info("💡 報稅系統網址：[財政部電子申報繳稅服務網](https://tax.nat.gov.tw/)")
        except Exception as e:
            st.error(f"發生錯誤：{e}")
