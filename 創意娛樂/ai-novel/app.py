import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 小說產生器", page_icon="📖")
st.title("📖 AI 小說產生器")
st.caption("選擇類型、設定角色與場景，AI 為你創作一篇精彩短篇小說")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    st.markdown("### 📖 使用說明")
    st.markdown(
        "1. 輸入 Groq API Key\n"
        "2. 選擇小說類型\n"
        "3. 設定角色與場景\n"
        "4. 點擊「開始創作」"
    )

# 主介面
st.markdown("### 🎭 小說設定")

genre = st.selectbox(
    "📚 小說類型",
    ["奇幻", "推理", "愛情", "科幻", "恐怖"]
)

genre_emoji = {"奇幻": "🧙", "推理": "🔍", "愛情": "💕", "科幻": "🚀", "恐怖": "👻"}

col1, col2 = st.columns(2)
with col1:
    char_names = st.text_input(
        "👤 角色名稱（用逗號分隔）",
        placeholder="例如：林曉風, 陳雨桐, 老張"
    )
with col2:
    setting = st.text_input(
        "🏞️ 故事場景",
        placeholder="例如：雨夜的山中古廟"
    )

theme = st.text_input(
    "💡 故事主題/核心概念（選填）",
    placeholder="例如：信任與背叛、穿越時空的友誼"
)

col3, col4 = st.columns(2)
with col3:
    tone = st.selectbox("🎨 敘事風格", ["文學抒情", "輕鬆幽默", "緊張懸疑", "冷硬寫實", "詩意唯美"])
with col4:
    pov = st.selectbox("👁️ 視角", ["第三人稱", "第一人稱", "多視角"])

length = st.select_slider(
    "📏 篇幅",
    options=["短篇（約1000字）", "中短篇（約1500字）", "中篇（約2000字）"],
    value="短篇（約1000字）"
)

if st.button(f"{genre_emoji[genre]} 開始創作", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key！")
    elif not char_names.strip() or not setting.strip():
        st.error("請至少填寫角色名稱與故事場景！")
    else:
        try:
            client = Groq(api_key=api_key)
            theme_line = f"故事主題：{theme}" if theme else ""
            prompt = f"""你是一位才華橫溢的小說作家。請根據以下設定創作一篇繁體中文短篇小說。

小說類型：{genre}
角色名稱：{char_names}
故事場景：{setting}
{theme_line}
敘事風格：{tone}
視角：{pov}
篇幅要求：{length}

創作要求：
1. 故事要有完整的起承轉合
2. 角色性格鮮明，對話自然
3. 場景描寫生動細膩
4. 符合所選類型的風格特色
5. 結尾要有餘韻或反轉
6. 字數必須達到要求

請直接開始寫小說，開頭先寫一個吸引人的標題。"""

            with st.spinner(f"AI 正在創作{genre}小說中..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是專業小說作家，擅長各類型短篇小說創作，使用繁體中文。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8,
                    max_tokens=8192,
                )
            result = response.choices[0].message.content
            st.divider()
            st.markdown(result)

        except Exception as e:
            st.error(f"發生錯誤：{e}")
