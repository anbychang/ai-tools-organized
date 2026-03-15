import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 租屋合約檢查", page_icon="🏠")
st.title("🏠 AI 租屋合約檢查")
st.caption("貼上租屋合約內容，AI 幫您找出潛在問題與不合理條款")

st.info("📌 本工具以台灣租賃相關法規為基準進行分析，幫助您了解租屋權益。")

# 側邊欄設定
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入您的 Groq API Key")
    st.markdown("---")
    st.markdown("### 使用說明")
    st.markdown(
        "1. 輸入您的 Groq API Key\n"
        "2. 將租屋合約內容貼到文字框\n"
        "3. 點擊「檢查合約」\n"
        "4. 查看 AI 的分析結果"
    )
    st.markdown("### 常見合約陷阱")
    st.markdown(
        "- 提前解約罰金過高\n"
        "- 押金超過兩個月\n"
        "- 不合理的修繕責任\n"
        "- 禁止遷入戶籍\n"
        "- 任意調漲租金條款"
    )


def check_contract(contract: str, role: str, concern: str) -> str:
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一位熟悉台灣租賃法規的法律顧問。請分析使用者提供的租屋合約，"
                    "以繁體中文回覆：\n"
                    "1. 合約總體評估（安全/需注意/有風險）\n"
                    "2. 不合理或對租客不利的條款（逐條標出）\n"
                    "3. 合約中缺少的重要項目\n"
                    "4. 租客權益提醒（依據台灣民法與租賃住宅市場發展及管理條例）\n"
                    "5. 修改建議與協商要點\n"
                    "6. 簽約前的注意事項\n"
                    "請特別注意：押金上限、提前解約、修繕責任、"
                    "戶籍遷入、租金調漲、水電費計算等常見爭議點。"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"我的身份：{role}\n"
                    f"特別擔心的部分：{concern if concern else '無特別指定'}\n"
                    f"合約內容如下：\n{contract}"
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
    role = st.selectbox("您的身份", ["租客（房客）", "房東"])
with col2:
    concern = st.text_input("特別擔心的部分", placeholder="例如：提前解約、押金退還")

contract_input = st.text_area(
    "請貼上租屋合約內容",
    height=300,
    placeholder=(
        "將您的租屋合約內容貼在這裡...\n\n"
        "範例：\n"
        "租賃期間自 2024 年 1 月 1 日起至 2024 年 12 月 31 日止。\n"
        "每月租金新台幣壹萬伍仟元整，押金參個月...\n"
        "乙方如提前解約，押金不予退還..."
    ),
)

if st.button("檢查合約", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not contract_input.strip():
        st.warning("請貼上租屋合約內容。")
    else:
        with st.spinner("AI 正在檢查您的合約..."):
            try:
                result = check_contract(contract_input, role, concern)
                st.markdown("---")
                st.subheader("📋 合約檢查結果")
                st.markdown(result)
            except Exception as e:
                st.error(f"檢查時發生錯誤：{e}")

st.markdown("---")
st.caption("⚠️ 本工具僅供參考，不構成法律建議。如有糾紛請諮詢律師或法律扶助基金會。")
