import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 禮物推薦", page_icon="🎁")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("使用 Llama 3.3 70B 模型")


def recommend_gifts(target, age, budget, occasion, extra):
    """呼叫 Groq API 推薦禮物"""
    client = Groq(api_key=api_key)

    prompt = f"""你是一位專業的禮物顧問。請根據以下條件，推薦 5 個最適合的禮物：

- 送禮對象：{target}
- 對方年齡：{age} 歲
- 預算範圍：{budget}
- 送禮場合：{occasion}
- 額外資訊：{extra if extra else '無'}

請為每個禮物提供：
1. 禮物名稱與大約價格
2. 推薦理由
3. 購買建議（在哪裡買、注意事項）

請用繁體中文回答，格式清晰美觀，考慮台灣的消費習慣。"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=2000,
    )
    return response.choices[0].message.content


# 主頁面
st.title("🎁 AI 禮物推薦")
st.markdown("不知道送什麼？讓 AI 幫你挑選最棒的禮物！")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    target = st.selectbox("送禮對象", ["男性朋友", "女性朋友", "長輩", "小孩", "男友/老公", "女友/老婆", "同事/主管"])
with col2:
    age = st.number_input("對方年齡", min_value=1, max_value=100, value=25)

col3, col4 = st.columns(2)
with col3:
    budget = st.selectbox("預算範圍", [
        "500 元以下", "500-1000 元", "1000-2000 元",
        "2000-5000 元", "5000-10000 元", "10000 元以上"
    ])
with col4:
    occasion = st.selectbox("送禮場合", [
        "生日", "聖誕節", "情人節", "結婚", "喬遷",
        "畢業", "母親節/父親節", "過年", "感謝", "其他"
    ])

extra = st.text_area(
    "額外資訊（選填）",
    placeholder="例如：對方喜歡運動、喜歡閱讀、最近在學烘焙...",
    height=80,
)

if st.button("🎯 推薦禮物", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key！")
    else:
        with st.spinner("AI 正在為你挑選禮物..."):
            try:
                result = recommend_gifts(target, age, budget, occasion, extra)
                st.markdown("### 🎁 禮物推薦清單")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
