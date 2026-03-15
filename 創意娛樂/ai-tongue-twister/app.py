import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 繞口令", page_icon="👅")
st.title("👅 AI 繞口令產生器")
st.caption("輸入主題，AI 為你生成客製化的中文繞口令")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    st.markdown("### 📖 使用說明")
    st.markdown(
        "1. 輸入 Groq API Key\n"
        "2. 輸入主題或關鍵字\n"
        "3. 選擇難度等級\n"
        "4. 點擊「產生繞口令」"
    )
    st.divider()
    st.markdown("### 🏆 經典繞口令")
    st.markdown(
        "- 四是四，十是十...\n"
        "- 吃葡萄不吐葡萄皮...\n"
        "- 黑化肥發灰會揮發..."
    )

# 主介面
topic = st.text_input(
    "🎯 繞口令主題/關鍵字",
    placeholder="例如：程式設計師、貓和老鼠、下雨天"
)

col1, col2 = st.columns(2)
with col1:
    difficulty = st.selectbox(
        "📊 難度等級",
        ["初級（適合小朋友）", "中級（一般挑戰）", "高級（舌頭打結）", "地獄級（不可能的任務）"]
    )
with col2:
    num_twisters = st.slider("📊 產生數量", min_value=1, max_value=5, value=3)

twist_type = st.multiselect(
    "🔤 繞口令技巧",
    ["聲母相近", "韻母相近", "聲調變化", "疊字重複", "長句挑戰"],
    default=["聲母相近", "韻母相近"]
)

include_pinyin = st.checkbox("📝 附上注音/拼音", value=True)
include_tips = st.checkbox("💡 附上發音技巧提示", value=True)

if st.button("🚀 產生繞口令", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key！")
    elif not topic.strip():
        st.error("請輸入繞口令主題！")
    else:
        try:
            client = Groq(api_key=api_key)
            techniques = "、".join(twist_type) if twist_type else "不限"
            pinyin_req = "每個繞口令附上漢語拼音標注。" if include_pinyin else ""
            tips_req = "每個繞口令附上發音技巧提示和容易念錯的地方。" if include_tips else ""

            prompt = f"""你是繞口令創作大師。請根據以下條件創作 {num_twisters} 個原創中文繞口令。

主題/關鍵字：{topic}
難度等級：{difficulty}
繞口令技巧：{techniques}

格式要求（每個繞口令）：

### 繞口令 N：（取一個有趣的小標題）

**難度：** ⭐（1-5 顆星）

**繞口令內容：**
（繞口令正文，要有節奏感，朗朗上口但容易念錯）

{pinyin_req}

{tips_req}

**挑戰：** 嘗試連續念三遍不出錯！

要求：
1. 全部使用繁體中文
2. 原創內容，不要照搬經典繞口令
3. 必須與指定主題相關
4. 難度要符合選擇的等級
5. 利用指定的繞口令技巧
6. 要有趣味性，不只是難念"""

            with st.spinner("AI 正在創作繞口令..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是中文繞口令創作專家，擅長利用聲韻技巧創作有趣的繞口令，使用繁體中文。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8,
                    max_tokens=4096,
                )
            result = response.choices[0].message.content
            st.divider()
            st.markdown("### 🎉 你的專屬繞口令")
            st.markdown(result)

            st.divider()
            st.info("💪 挑戰：試著大聲念出來，每個連續念三遍不出錯才算過關！")

        except Exception as e:
            st.error(f"發生錯誤：{e}")
