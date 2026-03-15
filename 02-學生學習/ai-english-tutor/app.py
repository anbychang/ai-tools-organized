import streamlit as st
from groq import Groq

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(page_title="AI 英文家教", page_icon="📚", layout="centered")

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ 設定")

    api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")

    st.divider()

    difficulty = st.selectbox(
        "難度等級",
        options=["初級", "中級", "高級"],
        index=1,
    )

    scenario = st.selectbox(
        "練習情境",
        options=["日常對話", "商業英文", "旅遊英文", "面試準備"],
    )

    st.divider()

    if st.button("🔄 開始新對話", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---------------------------------------------------------------------------
# Difficulty / scenario mappings
# ---------------------------------------------------------------------------
DIFFICULTY_MAP = {
    "初級": "beginner (A1-A2). Use simple vocabulary and short sentences. Speak slowly and clearly.",
    "中級": "intermediate (B1-B2). Use moderately complex sentences and common idioms.",
    "高級": "advanced (C1-C2). Use sophisticated vocabulary, complex grammar, and natural expressions.",
}

SCENARIO_MAP = {
    "日常對話": "casual daily conversation between friends or acquaintances",
    "商業英文": "professional business English in a workplace setting",
    "旅遊英文": "travel English for tourists visiting an English-speaking country",
    "面試準備": "job interview preparation and practice",
}

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = f"""You are a patient and encouraging English tutor helping a Taiwanese student practice English conversation.

Current setting:
- Student level: {DIFFICULTY_MAP[difficulty]}
- Conversation scenario: {SCENARIO_MAP[scenario]}

Rules for EVERY response:
1. First, reply naturally in English to continue the conversation (keep it relevant to the scenario).
2. Then, in a clearly separated section, provide feedback using EXACTLY this format:

---
📝 **Grammar Corrections / 文法修正**
- (If the student made grammar mistakes, list each one with the correction. If no mistakes, write "Great job! No grammar errors! 太棒了，沒有文法錯誤！")

💡 **Better Ways to Say It / 更好的說法**
- (Suggest 1-3 more natural or advanced ways to express what the student said, with brief Chinese explanation)

📖 **New Vocabulary / 新單字**
- **word** (part of speech) – English definition – 中文翻譯
- (List 2-4 useful words or phrases from YOUR response that the student might not know)
---

Important:
- Always be encouraging and positive.
- Adjust your English complexity to the student's level.
- Keep the conversation going by asking follow-up questions.
- The feedback section headers and Chinese translations are always included.
- If this is the very first message in the conversation, start by greeting the student and setting up the scenario.
"""

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------
st.title("📚 AI 英文家教")
st.caption("用英文和 AI 對話，即時獲得文法修正與學習建議")

# ---------------------------------------------------------------------------
# Display chat history
# ---------------------------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------------------------------------------------------
# Auto-start: if no messages yet, get the AI to open the conversation
# ---------------------------------------------------------------------------
def call_groq(messages: list[dict]) -> str:
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"API 呼叫失敗：{e}")
        st.stop()


if not api_key:
    st.info("👈 請先在側邊欄輸入你的 Groq API Key 以開始練習。")
    st.stop()

if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        with st.spinner("正在準備對話情境..."):
            opening = call_groq([
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "Please greet me and start the conversation based on the scenario. (Do NOT include the feedback section for this first greeting.)"},
            ])
        st.markdown(opening)
    st.session_state.messages.append({"role": "assistant", "content": opening})

# ---------------------------------------------------------------------------
# Chat input
# ---------------------------------------------------------------------------
if user_input := st.chat_input("用英文輸入你想說的話..."):
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Build messages for API
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in st.session_state.messages:
        api_messages.append({"role": msg["role"], "content": msg["content"]})

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            reply = call_groq(api_messages)
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
