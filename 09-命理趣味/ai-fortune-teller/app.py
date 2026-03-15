import streamlit as st
from groq import Groq

# --- 頁面設定 ---
st.set_page_config(page_title="AI 算命仙", page_icon="🧧", layout="centered")

# --- 傳統風格 CSS ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a0000, #3d0000, #1a0000);
        color: #ffd700;
    }
    h1, h2, h3 { color: #ff4444 !important; text-shadow: 0 0 10px rgba(255,68,68,0.5); }
    .fortune-card {
        background: rgba(139,0,0,0.2);
        border: 2px solid #ffd700;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 0 15px rgba(255,215,0,0.2);
    }
    .stMarkdown p { color: #ffe0b2; }
</style>
""", unsafe_allow_html=True)

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("使用 **Llama 3.3 70B** 模型")
    st.markdown("🧧 老仙覺得你有緣，來算一卦！")

# --- 主頁面 ---
st.title("🧧 AI 算命仙")
st.markdown("*老仙鐵口直斷，用台語風格幫你批命！*")

st.markdown("---")

birthday = st.date_input("🎂 你的生日")
col1, col2 = st.columns(2)
with col1:
    birth_hour = st.selectbox("🕐 出生時辰（如知道）", [
        "不確定", "子時 (23-01)", "丑時 (01-03)", "寅時 (03-05)",
        "卯時 (05-07)", "辰時 (07-09)", "巳時 (09-11)",
        "午時 (11-13)", "未時 (13-15)", "申時 (15-17)",
        "酉時 (17-19)", "戌時 (19-21)", "亥時 (21-23)"
    ])
with col2:
    gender = st.selectbox("👤 性別", ["男", "女", "不透露"])

question_type = st.selectbox("🔮 想算什麼", [
    "整體運勢", "感情姻緣", "事業財運", "健康運", "今年流年", "貴人運"
])
specific_q = st.text_input("❓ 有特定問題嗎（選填）", placeholder="例如：今年會升官嗎？")

if st.button("🧧 開始算命", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key！")
    else:
        try:
            client = Groq(api_key=api_key)
            prompt = f"""你是一位台灣廟口的老算命仙，說話帶有台語腔調和用詞。
請用台語風格的繁體中文幫人算命（不是寫台語，而是帶有台語口氣的中文）。

生日：{birthday}
時辰：{birth_hour}
性別：{gender}
想算：{question_type}
特定問題：{specific_q if specific_q.strip() else "無"}

請提供：
1. 🧧 開場白（用老算命仙的口吻，帶台語腔，例如「我看你面相喔...」）
2. ⭐ 命格分析（根據生日編造有趣的命格描述）
3. 🔮 {question_type}詳細解說
4. 📅 近期運勢（未來三個月）
5. ⚠️ 需要注意的事項
6. 🍀 開運建議（帶有台灣民俗色彩，例如拜什麼廟、帶什麼開運物）
7. 📝 算命仙的叮嚀（用台語口氣的結語）

語調要像廟口老仙：有智慧、有點神秘、偶爾幽默。
多用「啊」「喔」「齁」「嘿」等語氣詞。"""

            with st.spinner("🧧 老仙正在掐指一算..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是台灣廟口的老算命仙，用帶台語腔調的繁體中文說話，風趣有智慧。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.9,
                    max_tokens=1500,
                )
            result = response.choices[0].message.content
            st.markdown("---")
            st.markdown(f'<div class="fortune-card">{result}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"發生錯誤：{e}")

# --- 頁尾 ---
st.markdown("---")
st.caption("🧧 AI 算命仙 — 純屬娛樂，信不信由你，老仙只是跟你開講！")
