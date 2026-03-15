import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 道歉產生器", page_icon="🙏")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("使用 Llama 3.3 70B 模型")


def generate_apology(target, severity, description, tone):
    """呼叫 Groq API 產生道歉訊息"""
    client = Groq(api_key=api_key)

    prompt = f"""你是一位溝通專家，擅長幫人撰寫真誠的道歉訊息。請根據以下情境產生一段道歉訊息：

- 道歉對象：{target}
- 嚴重程度：{severity}
- 事情經過：{description}
- 語氣偏好：{tone}

請產生一段道歉訊息，要求：
1. 語氣真誠、不做作
2. 承認錯誤但不過度自我貶低
3. 提出彌補方案
4. 適合用通訊軟體傳送的長度
5. 根據對象調整用詞

另外，請額外提供 3 個道歉小建議。

請用繁體中文回答，格式清晰美觀。"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1500,
    )
    return response.choices[0].message.content


# 主頁面
st.title("🙏 AI 道歉產生器")
st.markdown("做錯事不知道怎麼開口？讓 AI 幫你寫出真誠的道歉！")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    target = st.selectbox("道歉對象", ["伴侶/另一半", "父母", "朋友", "老闆/主管", "客戶", "同事", "鄰居"])
with col2:
    severity = st.selectbox("嚴重程度", ["小事（遲到、忘記事情）", "中等（誤會、失約）", "大事（嚴重傷害對方）"])

tone = st.radio("語氣偏好", ["真誠懇切", "輕鬆帶歉意", "正式嚴肅"], horizontal=True)

description = st.text_area(
    "描述事情經過",
    placeholder="例如：忘記了我們的紀念日，對方很生氣...",
    height=120,
)

if st.button("💌 產生道歉訊息", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key！")
    elif not description:
        st.warning("請描述事情經過！")
    else:
        with st.spinner("AI 正在幫你撰寫道歉訊息..."):
            try:
                result = generate_apology(target, severity, description, tone)
                st.markdown("### 💌 道歉訊息")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
