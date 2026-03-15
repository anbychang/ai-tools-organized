import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 密室逃脫", page_icon="🔐")
st.title("🔐 AI 密室逃脫")

with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    st.markdown("解開 5 道謎題即可逃出密室！")
    if st.button("🔄 重新開始"):
        st.session_state.puzzle_num = 0
        st.session_state.messages = []
        st.session_state.escaped = False
        st.rerun()

for key, val in [("puzzle_num", 0), ("messages", []), ("escaped", False)]:
    if key not in st.session_state:
        st.session_state[key] = val

TOTAL_PUZZLES = 5

def call_ai(client, messages):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.8,
        max_tokens=1000,
    )
    return response.choices[0].message.content

# Progress bar
if not st.session_state.escaped:
    st.progress(st.session_state.puzzle_num / TOTAL_PUZZLES, text=f"進度：{st.session_state.puzzle_num}/{TOTAL_PUZZLES} 道謎題已解開")
else:
    st.balloons()
    st.success("🎉 恭喜你成功逃出密室！")
    st.stop()

if not api_key:
    st.info("請在側邊欄輸入 Groq API Key 開始遊戲。")
    st.stop()

client = Groq(api_key=api_key)

# Generate first puzzle
if st.session_state.puzzle_num == 0 and not st.session_state.messages:
    system_msg = f"""你是一個密室逃脫遊戲的主持人。遊戲共有 {TOTAL_PUZZLES} 道謎題。
玩家必須依序解開每道謎題才能逃出密室。
規則：
1. 每次只給一道謎題，包含場景描述和謎題內容
2. 當玩家回答正確時，回覆「✅ 正確！」開頭，然後給下一道謎題
3. 當玩家回答錯誤時，回覆「❌ 再想想！」開頭，給一個提示
4. 謎題要有趣且多樣化（邏輯、文字、數學、觀察、密碼等）
5. 全部使用繁體中文
6. 密室主題：古老的魔法師書房
現在請描述密室場景，並給出第 1 道謎題。"""
    st.session_state.messages = [{"role": "system", "content": system_msg}]
    with st.spinner("正在建構密室..."):
        try:
            reply = call_ai(client, st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"發生錯誤：{e}")
            st.stop()

# Display chat history (skip system)
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if answer := st.chat_input("輸入你的答案..."):
    st.session_state.messages.append({"role": "user", "content": answer})
    with st.chat_message("user"):
        st.markdown(answer)

    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                reply = call_ai(client, st.session_state.messages)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.markdown(reply)
                if "✅" in reply or "正確" in reply:
                    st.session_state.puzzle_num += 1
                    if st.session_state.puzzle_num >= TOTAL_PUZZLES:
                        st.session_state.escaped = True
                        st.rerun()
            except Exception as e:
                st.error(f"發生錯誤：{e}")
