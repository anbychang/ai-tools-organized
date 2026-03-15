import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 稅務計算", page_icon="🧾")
st.title("🧾 AI 稅務計算")
st.caption("輸入收入與扣除額，AI 估算稅額並提供節稅建議（台灣稅制）")

st.info("📌 本工具以台灣綜合所得稅制度為基準進行估算，僅供參考。")

# 側邊欄設定
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入您的 Groq API Key")
    st.markdown("---")
    st.markdown("### 使用說明")
    st.markdown(
        "1. 輸入您的 Groq API Key\n"
        "2. 填寫年收入與扣除額資訊\n"
        "3. 點擊「計算稅額」\n"
        "4. 查看估算結果與節稅建議"
    )
    st.markdown("### 台灣所得稅級距")
    st.markdown(
        "- 0～56 萬：5%\n"
        "- 56～126 萬：12%\n"
        "- 126～252 萬：20%\n"
        "- 252～472 萬：30%\n"
        "- 472 萬以上：40%"
    )


def calculate_tax(income: int, filing: str, dependents: int, deductions: str, income_types: list, extra: str) -> str:
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一位台灣稅務專家。請根據使用者提供的資訊，以繁體中文：\n"
                    "1. 估算綜合所得稅額（列出計算過程）\n"
                    "2. 說明適用的免稅額、標準/列舉扣除額\n"
                    "3. 提供合法節稅建議\n"
                    "4. 提醒常被忽略的扣除項目\n"
                    "5. 報稅注意事項\n"
                    "以台灣最新稅制為準，金額以新台幣計算。"
                    "務必提醒使用者實際稅額以國稅局計算為準。"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"年收入總額：{income:,} 元\n"
                    f"申報方式：{filing}\n"
                    f"扶養親屬人數：{dependents}\n"
                    f"已知扣除項目：{deductions if deductions else '無特別項目'}\n"
                    f"收入類型：{'、'.join(income_types)}\n"
                    f"其他說明：{extra if extra else '無'}"
                ),
            },
        ],
        temperature=0.3,
        max_tokens=2048,
    )
    return response.choices[0].message.content


# 主要介面
col1, col2 = st.columns(2)
with col1:
    income = st.number_input("年收入總額（新台幣）", min_value=0, max_value=100000000, value=800000, step=10000)
    filing = st.selectbox("申報方式", ["單身", "夫妻合併申報", "夫妻分開申報"])
with col2:
    dependents = st.number_input("扶養親屬人數", min_value=0, max_value=20, value=0)
    income_types = st.multiselect(
        "收入類型",
        ["薪資所得", "執行業務所得", "利息所得", "股利所得", "租賃所得", "其他所得"],
        default=["薪資所得"],
    )

deductions = st.text_input(
    "已知的扣除項目",
    placeholder="例如：房貸利息 20 萬、保險費 5 萬、捐贈 3 萬",
)
extra = st.text_area("其他補充", height=80, placeholder="例如：有海外所得、有房屋出租等")

if st.button("計算稅額", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not income_types:
        st.warning("請至少選擇一種收入類型。")
    else:
        with st.spinner("AI 正在計算您的稅額..."):
            try:
                result = calculate_tax(income, filing, dependents, deductions, income_types, extra)
                st.markdown("---")
                st.subheader("📊 稅務估算結果")
                st.markdown(result)
            except Exception as e:
                st.error(f"計算時發生錯誤：{e}")

st.markdown("---")
st.caption("⚠️ 本工具僅供估算參考，實際稅額以國稅局核定為準。如有疑問請諮詢會計師。")
