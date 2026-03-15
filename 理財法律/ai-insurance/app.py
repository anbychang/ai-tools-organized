import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 保險建議", page_icon="🛡️")
st.title("🛡️ AI 保險建議")
st.caption("根據您的個人狀況，AI 提供保險規劃方向與注意事項")

st.warning(
    "⚠️ **免責聲明：本工具僅提供保險知識參考，不構成任何保險銷售或購買建議。"
    "實際投保前請諮詢合格的保險業務員或理財顧問。**"
)

# 側邊欄設定
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入您的 Groq API Key")
    st.markdown("---")
    st.markdown("### 使用說明")
    st.markdown(
        "1. 輸入您的 Groq API Key\n"
        "2. 填寫個人基本資料\n"
        "3. 點擊「取得保險建議」\n"
        "4. 查看 AI 的保險規劃方向"
    )


def get_insurance_advice(age: int, occupation: str, family: str, budget: int, existing: str, concern: str) -> str:
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一位保險知識顧問（非保險業務員）。請以繁體中文提供保險規劃方向，包含：\n"
                    "1. 根據使用者狀況，建議需要的保險類型（壽險、醫療險、意外險、癌症險等）\n"
                    "2. 各類保險的功能說明\n"
                    "3. 保額建議範圍\n"
                    "4. 選購保險時的注意事項\n"
                    "5. 常見陷阱提醒\n"
                    "6. 預算分配建議\n"
                    "以台灣保險市場為背景。務必在開頭和結尾加上免責聲明。"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"年齡：{age} 歲\n職業：{occupation}\n"
                    f"家庭狀況：{family}\n"
                    f"每月可負擔保費：{budget:,} 元\n"
                    f"已有的保險：{existing if existing else '無'}\n"
                    f"最擔心的風險：{concern if concern else '未指定'}"
                ),
            },
        ],
        temperature=0.5,
        max_tokens=2048,
    )
    return response.choices[0].message.content


# 主要介面
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("年齡", min_value=18, max_value=100, value=30)
    occupation = st.text_input("職業", placeholder="例如：軟體工程師")
    budget = st.number_input("每月可負擔保費（新台幣）", min_value=0, max_value=100000, value=3000, step=500)
with col2:
    family = st.selectbox("家庭狀況", ["單身", "已婚無小孩", "已婚有小孩", "單親", "需扶養長輩"])
    existing = st.text_input("目前已有的保險", placeholder="例如：公司團保、學生保險")
    concern = st.selectbox("最擔心的風險", ["重大疾病", "意外事故", "住院醫療費用", "家人經濟保障", "退休規劃", "其他"])

if st.button("取得保險建議", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    else:
        with st.spinner("AI 正在分析您的保險需求..."):
            try:
                result = get_insurance_advice(age, occupation, family, budget, existing, concern)
                st.markdown("---")
                st.subheader("📋 保險規劃建議")
                st.markdown(result)
            except Exception as e:
                st.error(f"分析時發生錯誤：{e}")

st.markdown("---")
st.caption("⚠️ 本工具僅供參考，不構成任何保險銷售建議。投保前請諮詢專業人士。")
