import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 冷笑話", page_icon="🥶")
st.title("🥶 AI 冷笑話產生器")
st.caption("按下按鈕，讓 AI 給你來幾個超冷的笑話！")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    st.markdown("### 📖 使用說明")
    st.markdown(
        "1. 輸入 Groq API Key\n"
        "2. 選擇笑話類型與數量\n"
        "3. 點擊「產生冷笑話」\n"
        "4. 為笑話評分！"
    )

# 主介面
col1, col2 = st.columns(2)
with col1:
    category = st.selectbox(
        "🏷️ 笑話類型",
        ["隨機混搭", "諧音梗", "反轉梗", "知識型", "動物相關", "食物相關", "職業相關"]
    )
with col2:
    num_jokes = st.slider("📊 笑話數量", min_value=1, max_value=10, value=5)

topic = st.text_input("🎯 指定主題（選填）", placeholder="例如：程式設計師、貓咪、數學")

coldness = st.select_slider(
    "🌡️ 冷度等級",
    options=["微冷", "普通冷", "很冷", "極冷", "南極等級"],
    value="很冷"
)

# 初始化笑話記錄
if "jokes" not in st.session_state:
    st.session_state.jokes = []
if "ratings" not in st.session_state:
    st.session_state.ratings = {}

if st.button("🎲 產生冷笑話", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key！")
    else:
        try:
            client = Groq(api_key=api_key)
            topic_line = f"主題限定：{topic}" if topic else ""
            category_line = f"類型限定：{category}" if category != "隨機混搭" else "類型：混合各種類型（諧音梗、反轉梗、知識型等）"

            prompt = f"""你是冷笑話大師。請產生 {num_jokes} 個冷笑話。

{category_line}
{topic_line}
冷度等級：{coldness}

格式要求：
每個笑話使用以下格式：
### 笑話 N：【類型標籤】
（笑話內容，先是問題或鋪墊，然後空一行再給笑點）

要求：
1. 使用繁體中文
2. 笑話要夠「冷」，符合指定冷度
3. 諧音梗要標注諧音說明
4. 每個笑話獨立完整
5. 笑點要明確"""

            with st.spinner("AI 正在搜尋宇宙最冷的笑話..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是冷笑話達人，專門產生各種令人發冷的笑話，使用繁體中文。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.9,
                    max_tokens=4096,
                )
            result = response.choices[0].message.content
            st.session_state.jokes.append(result)
            st.session_state.ratings[len(st.session_state.jokes) - 1] = None

        except Exception as e:
            st.error(f"發生錯誤：{e}")

# 顯示笑話與評分
for idx, joke_set in enumerate(reversed(st.session_state.jokes)):
    real_idx = len(st.session_state.jokes) - 1 - idx
    st.divider()
    st.markdown(f"**第 {real_idx + 1} 批冷笑話**")
    st.markdown(joke_set)

    rating = st.radio(
        f"為第 {real_idx + 1} 批笑話評分",
        ["🥶 冷到發抖", "😐 普通冷", "😅 有點好笑", "🤣 太好笑了", "💀 冷到往生"],
        key=f"rate_{real_idx}",
        horizontal=True,
    )
    st.session_state.ratings[real_idx] = rating

# 清除紀錄
if st.session_state.jokes:
    if st.sidebar.button("🗑️ 清除所有笑話"):
        st.session_state.jokes = []
        st.session_state.ratings = {}
        st.rerun()
