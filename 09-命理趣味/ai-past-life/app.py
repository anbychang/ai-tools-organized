import streamlit as st
from groq import Groq

# --- 頁面設定 ---
st.set_page_config(page_title="AI 前世今生", page_icon="🔮", layout="centered")

# --- 神秘風格 CSS ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #e0d7ff;
    }
    h1, h2, h3 { color: #ffd700 !important; text-shadow: 0 0 10px rgba(255,215,0,0.5); }
    .stMarkdown p { color: #e0d7ff; }
    .past-life-card {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,215,0,0.3);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 20px rgba(128,0,255,0.2);
    }
</style>
""", unsafe_allow_html=True)

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("🔮 使用 **Llama 3.3 70B** 模型")
    st.markdown("探索你的前世故事...")

# --- 主頁面 ---
st.title("🔮 AI 前世今生")
st.markdown("*輸入你的生日與姓名，讓 AI 揭開你前世的神秘面紗...*")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("✨ 你的姓名", placeholder="輸入你的名字")
with col2:
    birthday = st.date_input("🎂 你的生日")

zodiac_extra = st.selectbox("🌙 你最有感覺的元素", ["火 🔥", "水 💧", "風 🌬️", "土 🌍", "光 ✨", "暗 🌑"])

if st.button("🔮 揭開前世之謎", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key！")
    elif not name.strip():
        st.error("請輸入你的姓名！")
    else:
        try:
            client = Groq(api_key=api_key)
            prompt = f"""你是一位神秘的前世今生占卜師。請根據以下資訊，創造一個引人入勝的前世故事。

姓名：{name}
生日：{birthday}
親近元素：{zodiac_extra}

請產生：
1. 🏛️ 前世身份（歷史時期、國家、身份地位）
2. 📖 前世故事（200-300字，生動描述前世的一生重要經歷）
3. 💕 前世的愛情故事
4. ⚔️ 前世最大的挑戰與成就
5. 🔗 前世與今生的連結（性格、天賦、莫名的喜好或恐懼如何來自前世）
6. 🌟 來自前世的人生建議

故事要有趣、戲劇性、有歷史感。用繁體中文，語調神秘但溫暖。
可以參考真實歷史時期（古埃及、唐朝、文藝復興、維京時代等）。"""

            with st.spinner("🔮 正在穿越時空，尋找你的前世..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是神秘的前世占卜師，用繁體中文講述引人入勝的前世故事。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=1.0,
                    max_tokens=1500,
                )
            result = response.choices[0].message.content
            st.markdown("---")
            st.markdown(f'<div class="past-life-card">{result}</div>', unsafe_allow_html=True)
            st.balloons()

        except Exception as e:
            st.error(f"發生錯誤：{e}")

# --- 頁尾 ---
st.markdown("---")
st.caption("🔮 AI 前世今生 — 純屬娛樂，探索你靈魂的奇幻旅程")
