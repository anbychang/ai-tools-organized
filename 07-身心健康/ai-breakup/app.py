import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 分手訊息", page_icon="💔")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("使用 Llama 3.3 70B 模型")


def generate_breakup(duration, reason, tone, extra):
    """呼叫 Groq API 產生分手訊息"""
    client = Groq(api_key=api_key)

    prompt = f"""你是一位感情顧問，擅長幫助人們用適當的方式表達分手的意願。請根據以下條件撰寫一段分手訊息：

- 交往時間：{duration}
- 分手原因：{reason}
- 希望的語氣：{tone}
- 補充說明：{extra if extra else '無'}

請提供：
1. 一段完整的分手訊息（適合傳訊息或面對面說）
2. 分手時的溝通建議
3. 可能會遇到的對方反應及應對方式

要求：
- 尊重對方感受
- 不要一味指責或貶低
- 表達清楚但不殘忍
- 適合用通訊軟體傳送或面對面說

請用繁體中文回答，格式清晰美觀。"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1500,
    )
    return response.choices[0].message.content


# 主頁面
st.title("💔 AI 分手訊息產生器")
st.markdown("分手不容易，讓 AI 幫你找到最適當的表達方式。")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    duration = st.selectbox("交往時間", [
        "不到 1 個月", "1-3 個月", "3-6 個月",
        "6 個月 - 1 年", "1-3 年", "3 年以上"
    ])
with col2:
    reason = st.selectbox("主要分手原因", [
        "個性不合", "感情淡了", "遠距離", "價值觀不同",
        "對方劈腿/不忠", "家庭因素", "工作/學業壓力", "其他"
    ])

tone = st.radio(
    "語氣風格",
    ["溫柔體貼", "直接坦白", "感性回憶", "理性分析"],
    horizontal=True,
)

extra = st.text_area(
    "補充說明（選填）",
    placeholder="例如：我們有共同朋友圈、還有一起養的寵物...",
    height=80,
)

if st.button("💌 產生分手訊息", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key！")
    else:
        with st.spinner("AI 正在幫你撰寫訊息..."):
            try:
                result = generate_breakup(duration, reason, tone, extra)
                st.markdown("### 💌 分手訊息")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")

st.markdown("---")
st.caption("⚠️ 分手是人生中的重要決定，建議面對面溝通。本工具僅提供文字參考。")
