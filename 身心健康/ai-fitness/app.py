import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 運動教練", page_icon="💪")
st.title("💪 AI 運動教練")
st.caption("根據您的目標與條件，AI 為您量身打造運動計畫")

# 側邊欄設定
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入您的 Groq API Key")
    st.markdown("---")
    st.markdown("### 使用說明")
    st.markdown(
        "1. 輸入您的 Groq API Key\n"
        "2. 選擇運動目標、可用器材與時間\n"
        "3. 點擊「生成運動計畫」\n"
        "4. AI 教練將為您規劃訓練菜單"
    )


def generate_plan(goal: str, equipment: str, duration: str, level: str, note: str) -> str:
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一位專業的運動教練。請根據使用者的目標、器材、時間與程度，"
                    "以繁體中文生成一份詳細的運動計畫，包含：\n"
                    "1. 熱身動作\n"
                    "2. 主要訓練（含組數、次數、休息時間）\n"
                    "3. 緩和收操\n"
                    "4. 注意事項與建議\n"
                    "請用清楚的格式呈現。"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"目標：{goal}\n可用器材：{equipment}\n"
                    f"可用時間：{duration}\n運動程度：{level}\n"
                    f"其他備註：{note if note else '無'}"
                ),
            },
        ],
        temperature=0.7,
        max_tokens=2048,
    )
    return response.choices[0].message.content


# 主要介面
col1, col2 = st.columns(2)
with col1:
    goal = st.selectbox("運動目標", ["減脂", "增肌", "體能提升", "柔軟度", "綜合訓練"])
    equipment = st.selectbox("可用器材", ["無器材（徒手）", "啞鈴", "彈力帶", "健身房全套器材"])
with col2:
    duration = st.selectbox("可用時間", ["15 分鐘", "30 分鐘", "45 分鐘", "60 分鐘", "90 分鐘"])
    level = st.selectbox("運動程度", ["初學者", "中等", "進階"])

note = st.text_input("其他備註（如傷病、偏好等）", placeholder="例如：膝蓋不太好、不喜歡跑步")

if st.button("生成運動計畫", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    else:
        with st.spinner("AI 教練正在為您規劃訓練菜單..."):
            try:
                result = generate_plan(goal, equipment, duration, level, note)
                st.markdown("---")
                st.subheader("🏋️ 您的運動計畫")
                st.markdown(result)
            except Exception as e:
                st.error(f"生成時發生錯誤：{e}")

st.markdown("---")
st.caption("⚠️ 運動前請確認身體狀況，如有不適請諮詢醫師。")
