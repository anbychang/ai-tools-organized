import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 請假理由", page_icon="📋")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("使用 Llama 3.3 70B 模型")


def generate_excuse(leave_type, days, company_culture, extra):
    """呼叫 Groq API 產生請假理由"""
    client = Groq(api_key=api_key)

    prompt = f"""你是一位職場溝通專家。請根據以下條件，產生一個合理的請假理由和請假申請文字：

- 請假類型：{leave_type}
- 請假天數：{days} 天
- 公司文化：{company_culture}
- 額外說明：{extra if extra else '無'}

請提供：
1. 一個合理且可信的請假理由（簡短說明）
2. 一段正式的請假申請文字（可以直接傳給主管）
3. 如果主管追問的應對建議
4. 請假前後的注意事項

重要提醒：請假理由要合理可信，不要太誇張。

請用繁體中文回答，格式清晰美觀。"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1500,
    )
    return response.choices[0].message.content


# 主頁面
st.title("📋 AI 請假理由產生器")
st.markdown("需要請假卻想不到理由？讓 AI 幫你想一個合理的說法！")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    leave_type = st.selectbox("請假類型", [
        "事假（私人事務）", "病假（身體不適）", "家庭因素（家人需要照顧）",
        "搬家/處理房屋", "政府機關辦事", "心理健康假"
    ])
with col2:
    days = st.number_input("請假天數", min_value=0.5, max_value=14.0, value=1.0, step=0.5)

company_culture = st.radio(
    "公司文化",
    ["嚴格正式（需要詳細理由）", "一般（簡單說明即可）", "輕鬆彈性（不太過問）"],
    horizontal=True,
)

extra = st.text_area(
    "額外說明（選填）",
    placeholder="例如：最近已經請過一次假、主管比較嚴格...",
    height=80,
)

if st.button("📝 產生請假理由", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key！")
    else:
        with st.spinner("AI 正在幫你想理由..."):
            try:
                result = generate_excuse(leave_type, days, company_culture, extra)
                st.markdown("### 📝 請假方案")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")

st.markdown("---")
st.caption("⚠️ 本工具僅供參考，請假仍需誠實面對，頻繁不當請假可能影響工作表現。")
