import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 症狀檢查", page_icon="🩺")
st.title("🩺 AI 症狀檢查")
st.caption("選擇您的症狀，AI 協助初步分析可能原因")

st.error(
    "⚠️ **重要聲明：本工具僅供參考，絕非醫療診斷。"
    "如有身體不適，請務必就醫諮詢專業醫師。**"
)

# 側邊欄設定
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入您的 Groq API Key")
    st.markdown("---")
    st.markdown("### 使用說明")
    st.markdown(
        "1. 輸入您的 Groq API Key\n"
        "2. 勾選相關症狀並補充描述\n"
        "3. 點擊「AI 分析症狀」\n"
        "4. 查看建議（僅供參考）"
    )

SYMPTOMS = [
    "頭痛", "發燒", "咳嗽", "喉嚨痛", "流鼻涕",
    "胸悶", "腹痛", "噁心/嘔吐", "腹瀉", "便秘",
    "疲倦", "失眠", "頭暈", "皮膚癢/紅疹", "關節痛",
    "背痛", "眼睛不適", "耳鳴", "心悸", "呼吸困難",
]


def check_symptoms(selected: list, details: str, age: str, gender: str) -> str:
    client = Groq(api_key=api_key)
    symptoms_str = "、".join(selected)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一位醫療資訊助手（非醫師）。使用者會描述症狀，"
                    "請以繁體中文回覆：\n"
                    "1. 可能的原因（列出 2-4 種可能）\n"
                    "2. 建議就診的科別\n"
                    "3. 就醫前的注意事項\n"
                    "務必在回覆開頭和結尾強調這不是醫療診斷，必須就醫確認。"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"年齡：{age}\n性別：{gender}\n"
                    f"症狀：{symptoms_str}\n"
                    f"詳細描述：{details if details else '無額外描述'}"
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
    age = st.text_input("年齡", placeholder="例如：35")
with col2:
    gender = st.selectbox("性別", ["男", "女", "其他"])

st.subheader("請勾選您目前的症狀")
cols = st.columns(4)
selected_symptoms = []
for i, symptom in enumerate(SYMPTOMS):
    with cols[i % 4]:
        if st.checkbox(symptom):
            selected_symptoms.append(symptom)

details = st.text_area("補充描述（症狀持續多久、程度等）", height=100, placeholder="例如：頭痛已經持續三天，主要在右側太陽穴")

if st.button("AI 分析症狀", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not selected_symptoms:
        st.warning("請至少勾選一個症狀。")
    else:
        with st.spinner("AI 正在分析您的症狀..."):
            try:
                result = check_symptoms(selected_symptoms, details, age, gender)
                st.markdown("---")
                st.subheader("📋 初步分析結果")
                st.markdown(result)
            except Exception as e:
                st.error(f"分析時發生錯誤：{e}")

st.markdown("---")
st.caption("⚠️ 本工具不構成任何醫療建議，如有不適請立即就醫。")
