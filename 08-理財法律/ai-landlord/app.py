import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 房東回覆", page_icon="🏠")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("使用 Llama 3.3 70B 模型")


def generate_reply(scenario, role, description, goal):
    """呼叫 Groq API 產生房東/房客回覆"""
    client = Groq(api_key=api_key)

    prompt = f"""你是一位租屋溝通專家，熟悉台灣租屋法規與慣例。請根據以下情境，幫忙撰寫一段得體的回覆：

- 情境類型：{scenario}
- 我的身份：{role}
- 具體狀況：{description}
- 我的目標：{goal if goal else '妥善處理此事'}

請提供：
1. 一段禮貌但立場堅定的回覆訊息（適合 LINE 或簡訊傳送）
2. 相關的法律權益提醒（台灣租賃相關）
3. 協商策略建議
4. 如果對方不配合的後續處理建議

要求：
- 語氣禮貌但不軟弱
- 有理有據
- 保護自身權益
- 維持良好關係

請用繁體中文回答，格式清晰美觀。"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=1800,
    )
    return response.choices[0].message.content


# 主頁面
st.title("🏠 AI 房東/房客回覆助手")
st.markdown("租屋糾紛不用怕！讓 AI 幫你寫出得體又有力的回覆！")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    scenario = st.selectbox("情境類型", [
        "房東要漲房租", "要求房東維修", "提前退租",
        "鄰居噪音問題", "押金退還爭議", "房東要求搬離",
        "水電費爭議", "房屋設備損壞責任", "其他"
    ])
with col2:
    role = st.selectbox("你的身份", ["房客", "房東"])

description = st.text_area(
    "描述具體狀況",
    placeholder="例如：房東說下個月開始房租要從 15000 漲到 18000，合約還有半年...",
    height=120,
)

goal = st.text_input(
    "你的目標（選填）",
    placeholder="例如：希望維持原租金、希望房東負責修繕費用...",
)

if st.button("📝 產生回覆", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key！")
    elif not description:
        st.warning("請描述具體狀況！")
    else:
        with st.spinner("AI 正在幫你撰寫回覆..."):
            try:
                result = generate_reply(scenario, role, description, goal)
                st.markdown("### 📝 建議回覆")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")

st.markdown("---")
st.caption("⚠️ 本工具提供的法律資訊僅供參考，如遇嚴重糾紛建議諮詢專業律師。")
