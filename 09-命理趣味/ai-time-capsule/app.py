import streamlit as st
from groq import Groq
from datetime import datetime

# --- 頁面設定 ---
st.set_page_config(page_title="AI 時間膠囊", page_icon="💊", layout="centered")

# --- 風格 CSS ---
st.markdown("""
<style>
    .capsule-card {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        border: 2px solid #42a5f5;
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(66,165,245,0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("使用 **Llama 3.3 70B** 模型")
    st.markdown("💊 寫給未來自己的一封信")

# --- 主頁面 ---
st.title("💊 AI 時間膠囊")
st.markdown("寫一封信給未來的自己，AI 會幫你潤飾並加入深度反思問題！")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("✨ 你的名字", placeholder="給未來自己的稱呼")
with col2:
    future_time = st.selectbox("⏰ 未來時間", ["1 年後", "3 年後", "5 年後", "10 年後", "20 年後"])

current_mood = st.selectbox("💭 現在的心情", [
    "充滿希望", "有點迷茫", "正在低潮", "平靜安穩", "興奮期待", "疲憊但堅持"
])

letter = st.text_area(
    "📝 寫給未來自己的信",
    placeholder="親愛的未來的我，\n\n現在的我正在...\n我希望未來的你...\n我想讓你知道...",
    height=250,
)

life_areas = st.multiselect(
    "🎯 你最關心的人生面向",
    ["事業發展", "感情關係", "家庭", "健康", "財務", "個人成長", "夢想", "友誼"],
    default=["個人成長"],
)

if st.button("💊 封存時間膠囊", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key！")
    elif not letter.strip():
        st.error("請寫下你想對未來自己說的話！")
    else:
        try:
            client = Groq(api_key=api_key)
            today = datetime.now().strftime("%Y年%m月%d日")
            areas_str = "、".join(life_areas) if life_areas else "人生整體"
            prompt = f"""你是一位溫暖而有智慧的文字工作者。請幫忙潤飾和增強這封寫給未來自己的信。

寫信人：{name if name.strip() else "一位寫信人"}
今天日期：{today}
未來時間：{future_time}
現在心情：{current_mood}
關心面向：{areas_str}

原始信件內容：
{letter}

請提供：
1. 💌 潤飾後的信件（保留原意但讓文字更優美動人，可以適當擴充但不要改變原始情感）
2. 🤔 5 個反思問題（讓未來的自己在讀信時思考的深度問題，與關心的面向相關）
3. 📊 時間膠囊紀錄卡（用條列整理目前的狀態：日期、心情、最大的擔憂、最大的期望、一句話形容現在的自己）
4. ✨ 給未來自己的一句祝福語

繁體中文回答，語調溫暖、真摯、有深度。"""

            with st.spinner("💊 正在封存你的時間膠囊..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是溫暖有智慧的文字工作者，用繁體中文潤飾信件，語調真摯動人。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.8,
                    max_tokens=1500,
                )
            result = response.choices[0].message.content
            st.markdown("---")
            st.subheader("💊 時間膠囊已封存")
            st.markdown(result)
            st.success(f"這封信將在 {future_time} 等待你開啟。記得截圖保存！")
            st.balloons()

        except Exception as e:
            st.error(f"發生錯誤：{e}")

# --- 頁尾 ---
st.markdown("---")
st.caption("💊 AI 時間膠囊 — 給未來的自己一份珍貴的禮物")
