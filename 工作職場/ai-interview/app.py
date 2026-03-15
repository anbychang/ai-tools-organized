import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 面試模擬", page_icon="🎤")
st.title("🎤 AI 面試模擬器")
st.subheader("AI 擔任面試官，一題一題問你，給你即時回饋")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    position = st.text_input("💼 應徵職位", placeholder="例如：前端工程師")
    industry = st.selectbox("🏢 產業", ["科技業", "金融業", "製造業", "零售業", "醫療業", "教育業", "媒體業", "新創", "其他"])
    experience = st.selectbox("📊 年資", ["應屆畢業", "1-3 年", "3-5 年", "5-10 年", "10 年以上"])
    difficulty = st.selectbox("🎯 面試難度", ["初級（HR面）", "中級（主管面）", "高級（壓力面試）"])
    st.divider()
    if st.button("🔄 重新開始面試"):
        st.session_state.messages = []
        st.rerun()

# 初始化
if "messages" not in st.session_state:
    st.session_state.messages = []

# 顯示歷史訊息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑‍💼" if msg["role"] == "assistant" else "🙋"):
        st.markdown(msg["content"])

# 開始面試或繼續對話
if not api_key:
    st.info("請先在側邊欄輸入 Groq API Key 並設定面試資訊。")
elif not position:
    st.info("請在側邊欄輸入應徵職位。")
else:
    # 如果是新面試，先讓 AI 開場
    if len(st.session_state.messages) == 0:
        system_prompt = f"""你是一位專業的面試官，正在進行一場{difficulty}的模擬面試。
應徵者應徵的是{industry}的{position}職位，有{experience}的經驗。

規則：
1. 你每次只問一個問題
2. 等對方回答後，先給簡短回饋（優點和可改進之處），再問下一題
3. 全程使用繁體中文
4. 問題要符合該職位和產業
5. 從自我介紹開始，逐漸深入專業問題
6. 大約問 5-8 題後結束面試，給出總評

現在請開始面試，先打招呼並請對方自我介紹。"""

        try:
            client = Groq(api_key=api_key)
            with st.spinner("面試官準備中..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": system_prompt}],
                    temperature=0.7,
                    max_tokens=1000,
                )
            ai_msg = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": ai_msg})
            with st.chat_message("assistant", avatar="🧑‍💼"):
                st.markdown(ai_msg)
        except Exception as e:
            st.error(f"發生錯誤：{e}")

    # 使用者回答
    if user_input := st.chat_input("輸入你的回答..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🙋"):
            st.markdown(user_input)

        system_prompt = f"""你是一位專業的面試官，正在進行一場{difficulty}的模擬面試。
應徵者應徵的是{industry}的{position}職位，有{experience}的經驗。

規則：
1. 先對上一個回答給出簡短回饋（優點和可改進之處）
2. 然後問下一個問題（每次只問一個）
3. 全程使用繁體中文
4. 問題要有深度，符合該職位
5. 如果已經問了足夠多問題（5-8題），給出完整的面試總評和建議"""

        api_messages = [{"role": "system", "content": system_prompt}]
        for msg in st.session_state.messages:
            api_messages.append({"role": msg["role"], "content": msg["content"]})

        try:
            client = Groq(api_key=api_key)
            with st.spinner("面試官思考中..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=api_messages,
                    temperature=0.7,
                    max_tokens=1500,
                )
            ai_msg = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": ai_msg})
            with st.chat_message("assistant", avatar="🧑‍💼"):
                st.markdown(ai_msg)
        except Exception as e:
            st.error(f"發生錯誤：{e}")
