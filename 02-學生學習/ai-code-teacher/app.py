import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 程式教學", page_icon="💻")
st.title("💻 AI 程式教學")
st.caption("選擇語言與主題，AI 互動式教學並提供練習題")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    language = st.selectbox("🌐 程式語言", ["Python", "JavaScript", "Java"])
    level = st.selectbox("📊 程度", ["初學者", "中級", "進階"])
    st.divider()
    topics = {
        "Python": ["變數與資料型態", "條件判斷", "迴圈", "函式", "列表與字典", "檔案處理", "類別與物件", "例外處理"],
        "JavaScript": ["變數與資料型態", "條件判斷", "迴圈", "函式", "陣列與物件", "DOM 操作", "非同步處理", "ES6+ 語法"],
        "Java": ["變數與資料型態", "條件判斷", "迴圈", "方法", "陣列", "類別與物件", "繼承與多型", "例外處理"],
    }
    topic = st.selectbox("📚 教學主題", topics[language])

# 初始化聊天記錄
if "messages" not in st.session_state:
    st.session_state.messages = []

# 顯示歷史訊息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 開始教學按鈕
if not st.session_state.messages:
    if st.button("🎓 開始教學", type="primary", use_container_width=True):
        if not api_key:
            st.error("請先在側邊欄輸入 Groq API Key！")
        else:
            starter = f"請開始教我 {language} 的「{topic}」，我的程度是{level}。請用淺顯易懂的方式講解，附上程式碼範例，最後給我一道練習題。"
            st.session_state.messages.append({"role": "user", "content": starter})
            try:
                client = Groq(api_key=api_key)
                system_msg = (
                    f"你是一位親切的 {language} 程式教師，使用繁體中文教學。"
                    f"學生程度為{level}。教學風格：循序漸進、多用範例、"
                    "每次回覆結尾附上一道練習題讓學生思考。程式碼用 markdown code block 標示。"
                )
                with st.spinner("AI 老師準備中..."):
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": system_msg},
                            {"role": "user", "content": starter}
                        ],
                        temperature=0.5,
                        max_tokens=4096,
                    )
                reply = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()
            except Exception as e:
                st.error(f"發生錯誤：{e}")

# 聊天輸入
if prompt := st.chat_input("輸入你的問題或練習答案..."):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key！")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        try:
            client = Groq(api_key=api_key)
            system_msg = (
                f"你是一位親切的 {language} 程式教師，使用繁體中文教學。"
                f"學生程度為{level}，目前學習主題為「{topic}」。"
                "如果學生提交練習答案，請批改並給予回饋，然後出下一題。"
            )
            api_messages = [{"role": "system", "content": system_msg}]
            for m in st.session_state.messages[-10:]:
                api_messages.append({"role": m["role"], "content": m["content"]})

            with st.chat_message("assistant"):
                with st.spinner("思考中..."):
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=api_messages,
                        temperature=0.5,
                        max_tokens=4096,
                    )
                reply = response.choices[0].message.content
                st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"發生錯誤：{e}")

# 清除對話
if st.session_state.messages:
    if st.sidebar.button("🗑️ 清除對話紀錄"):
        st.session_state.messages = []
        st.rerun()
