import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 劇本產生器", page_icon="🎬")
st.title("🎬 AI 劇本產生器")
st.caption("設定場景、角色與類型，AI 為你寫出一段含舞台指示的短劇本")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    st.markdown("### 📖 使用說明")
    st.markdown(
        "1. 輸入 Groq API Key\n"
        "2. 設定劇本參數\n"
        "3. 點擊「產生劇本」"
    )

# 主介面
st.markdown("### 🎭 劇本設定")

scene = st.text_input(
    "🏠 場景描述",
    placeholder="例如：深夜的便利商店、暴風雨中的孤島燈塔"
)

col1, col2 = st.columns(2)
with col1:
    genre = st.selectbox("🎪 劇本類型", ["喜劇", "悲劇", "荒謬劇", "懸疑", "溫馨", "黑色幽默"])
with col2:
    num_chars = st.number_input("👥 角色數量", min_value=2, max_value=6, value=3)

characters = []
st.markdown("### 👤 角色設定")
cols = st.columns(min(num_chars, 3))
for i in range(num_chars):
    with cols[i % 3]:
        name = st.text_input(f"角色 {i+1} 名稱", key=f"char_name_{i}", placeholder=f"角色 {i+1}")
        trait = st.text_input(f"角色 {i+1} 特徵", key=f"char_trait_{i}", placeholder="例如：神經質的")
        if name:
            characters.append(f"{name}（{trait}）" if trait else name)

st.markdown("### 📝 其他設定")

col3, col4 = st.columns(2)
with col3:
    conflict = st.text_input("⚡ 核心衝突（選填）", placeholder="例如：爭奪最後一個便當")
with col4:
    duration = st.selectbox("⏱️ 預估演出時長", ["5 分鐘", "10 分鐘", "15 分鐘"])

twist = st.checkbox("🔄 加入反轉結局", value=True)

if st.button("🚀 產生劇本", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key！")
    elif not scene.strip():
        st.error("請輸入場景描述！")
    elif len(characters) < 2:
        st.error("請至少設定 2 個角色名稱！")
    else:
        try:
            client = Groq(api_key=api_key)
            chars_desc = "\n".join([f"- {c}" for c in characters])
            conflict_line = f"核心衝突：{conflict}" if conflict else ""
            twist_line = "結尾要有出人意料的反轉。" if twist else ""

            prompt = f"""你是一位專業劇作家。請根據以下設定寫一段短劇本。

場景：{scene}
類型：{genre}
預估時長：{duration}
{conflict_line}

角色：
{chars_desc}

要求：
1. 使用標準劇本格式，包含舞台指示（用括號標注）
2. 開頭要有場景描述和燈光說明
3. 對話自然生動，符合角色性格
4. 有明確的開場、發展、高潮、結尾
5. {twist_line}
6. 舞台指示要具體（動作、表情、走位、音效等）
7. 全部使用繁體中文

劇本格式範例：
【第一幕】
（舞台指示：場景描述、燈光）

角色名：台詞
（舞台指示：動作描述）

請開始創作："""

            with st.spinner(f"AI 正在創作{genre}劇本中..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是專業劇作家，精通各類型戲劇創作，使用繁體中文。"},
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
