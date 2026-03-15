import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 戒癮助手", page_icon="🚫")
st.title("🚫 AI 戒癮助手")
st.caption("選擇想戒除的習慣，AI 為您制定個人化戒斷計畫")

# 側邊欄設定
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入您的 Groq API Key")
    st.markdown("---")
    st.markdown("### 使用說明")
    st.markdown(
        "1. 輸入您的 Groq API Key\n"
        "2. 選擇想戒除的習慣並填寫細節\n"
        "3. 點擊「生成戒斷計畫」\n"
        "4. AI 將提供每日目標與替代方案"
    )

ADDICTIONS = {
    "手機成癮": "📱",
    "咖啡因依賴": "☕",
    "糖分攝取過多": "🍬",
    "熬夜晚睡": "🌙",
    "社群媒體沉迷": "📲",
    "含糖飲料": "🥤",
    "零食暴食": "🍿",
    "拖延症": "⏰",
}


def generate_quit_plan(addiction: str, severity: str, duration: str, motivation: str, extra: str) -> str:
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一位行為改變專家。請根據使用者想戒除的習慣，"
                    "以繁體中文制定一份 21 天戒斷計畫，包含：\n"
                    "1. 現況分析\n"
                    "2. 第 1-7 天：漸進式減少目標\n"
                    "3. 第 8-14 天：替代行為建議\n"
                    "4. 第 15-21 天：鞏固新習慣\n"
                    "5. 每日具體可執行的小目標\n"
                    "6. 替代方案與獎勵機制\n"
                    "7. 遇到誘惑時的應對策略\n"
                    "語氣溫暖鼓勵，不要批判。"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"想戒除的習慣：{addiction}\n"
                    f"嚴重程度：{severity}\n"
                    f"持續時間：{duration}\n"
                    f"戒除動機：{motivation}\n"
                    f"其他說明：{extra if extra else '無'}"
                ),
            },
        ],
        temperature=0.7,
        max_tokens=2048,
    )
    return response.choices[0].message.content


# 主要介面
addiction = st.selectbox(
    "選擇想戒除的習慣",
    list(ADDICTIONS.keys()),
    format_func=lambda x: f"{ADDICTIONS[x]} {x}",
)

col1, col2 = st.columns(2)
with col1:
    severity = st.select_slider("嚴重程度", options=["輕微", "中等", "嚴重", "非常嚴重"])
with col2:
    duration = st.selectbox("這個習慣持續多久了", ["不到一個月", "1-6 個月", "6-12 個月", "1-3 年", "3 年以上"])

motivation = st.text_input("您的戒除動機", placeholder="例如：想要更健康、提升專注力")
extra = st.text_area("其他補充說明", height=80, placeholder="例如：之前嘗試過什麼方法、什麼時候最容易犯")

if st.button("生成戒斷計畫", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    else:
        with st.spinner("AI 正在為您制定專屬戒斷計畫..."):
            try:
                result = generate_quit_plan(addiction, severity, duration, motivation, extra)
                st.markdown("---")
                st.subheader("📋 您的 21 天戒斷計畫")
                st.markdown(result)
            except Exception as e:
                st.error(f"生成時發生錯誤：{e}")

st.markdown("---")
st.caption("💡 改變習慣需要時間，對自己有耐心，每一小步都是進步。")
