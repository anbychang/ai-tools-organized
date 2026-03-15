import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 存錢計畫", page_icon="🐷")
st.title("🐷 AI 存錢計畫")
st.caption("輸入目標與收支狀況，AI 為您規劃存錢策略與每月里程碑")

# 側邊欄設定
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入您的 Groq API Key")
    st.markdown("---")
    st.markdown("### 使用說明")
    st.markdown(
        "1. 輸入您的 Groq API Key\n"
        "2. 填寫存錢目標與財務資訊\n"
        "3. 點擊「生成存錢計畫」\n"
        "4. AI 會規劃每月里程碑"
    )


def generate_savings_plan(goal_amount: int, deadline: str, income: int, fixed_expense: int, purpose: str, extra: str) -> str:
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一位專業的理財規劃師。請根據使用者的目標與財務狀況，"
                    "以繁體中文制定存錢計畫，包含：\n"
                    "1. 財務現況分析（可動用金額）\n"
                    "2. 每月建議存款金額\n"
                    "3. 逐月里程碑進度表\n"
                    "4. 具體的開源節流策略\n"
                    "5. 存錢小技巧（如 52 週存錢法等）\n"
                    "6. 風險評估與備案\n"
                    "金額以新台幣計算，數字要合理可執行。"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"存錢目標：{goal_amount:,} 元\n"
                    f"目標期限：{deadline}\n"
                    f"月收入：{income:,} 元\n"
                    f"每月固定支出：{fixed_expense:,} 元\n"
                    f"存錢目的：{purpose}\n"
                    f"其他說明：{extra if extra else '無'}"
                ),
            },
        ],
        temperature=0.7,
        max_tokens=2048,
    )
    return response.choices[0].message.content


# 主要介面
purpose = st.text_input("存錢目的", placeholder="例如：買車、出國旅行、緊急預備金")

col1, col2 = st.columns(2)
with col1:
    goal_amount = st.number_input("目標金額（新台幣）", min_value=1000, max_value=100000000, value=100000, step=10000)
    income = st.number_input("每月收入（新台幣）", min_value=0, max_value=10000000, value=40000, step=1000)
with col2:
    deadline = st.selectbox("目標期限", ["3 個月", "6 個月", "1 年", "2 年", "3 年", "5 年"])
    fixed_expense = st.number_input("每月固定支出（新台幣）", min_value=0, max_value=10000000, value=25000, step=1000)

extra = st.text_area("其他補充說明", height=80, placeholder="例如：有其他收入來源、有負債要還等")

# 顯示可動用金額
disposable = income - fixed_expense
if disposable > 0:
    st.info(f"💡 您每月可動用金額約為 **{disposable:,}** 元")
else:
    st.warning("⚠️ 您的固定支出已超過收入，建議先檢視支出項目。")

if st.button("生成存錢計畫", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    else:
        with st.spinner("AI 正在為您規劃存錢策略..."):
            try:
                result = generate_savings_plan(goal_amount, deadline, income, fixed_expense, purpose, extra)
                st.markdown("---")
                st.subheader("📋 您的存錢計畫")
                st.markdown(result)
            except Exception as e:
                st.error(f"生成時發生錯誤：{e}")

st.markdown("---")
st.caption("💡 存錢最重要的是持之以恆，從今天開始就是最好的時機。")
