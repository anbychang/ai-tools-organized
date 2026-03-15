import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 真心話大冒險", page_icon="🎯")
st.title("🎯 AI 真心話大冒險")

with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    level = st.radio("選擇尺度", ["溫和 😊", "普通 😄", "大膽 🔥"])
    st.markdown("---")
    st.markdown("選擇真心話或大冒險，AI 會根據尺度產生題目！")

if "current" not in st.session_state:
    st.session_state.current = None
if "history" not in st.session_state:
    st.session_state.history = []

level_name = level.split(" ")[0]

def generate(mode):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key。")
        return
    client = Groq(api_key=api_key)
    history_text = "\n".join(st.session_state.history[-10:]) if st.session_state.history else "無"
    prompt = f"""你是真心話大冒險遊戲主持人。
請產生一個「{mode}」的題目。
尺度等級：{level_name}
- 溫和：輕鬆有趣，適合家人朋友
- 普通：有點刺激但不過分
- 大膽：大膽刺激，讓人臉紅心跳

之前已出過的題目（請勿重複）：
{history_text}

規則：
1. 只輸出一個題目，不要多餘解釋
2. 題目要有趣、有創意
3. 使用繁體中文
4. 如果是大冒險，要是可以實際執行的挑戰"""

    with st.spinner("正在想題目..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=1.0,
                max_tokens=300,
            )
            result = response.choices[0].message.content
            st.session_state.current = {"mode": mode, "content": result}
            st.session_state.history.append(f"{mode}：{result}")
        except Exception as e:
            st.error(f"發生錯誤：{e}")

st.markdown("### 選擇你的命運...")
col1, col2 = st.columns(2)
with col1:
    if st.button("💬 真心話", use_container_width=True, type="primary"):
        generate("真心話")
        st.rerun()
with col2:
    if st.button("🏃 大冒險", use_container_width=True, type="secondary"):
        generate("大冒險")
        st.rerun()

if st.session_state.current:
    mode = st.session_state.current["mode"]
    content = st.session_state.current["content"]
    icon = "💬" if mode == "真心話" else "🏃"
    color = "blue" if mode == "真心話" else "red"
    st.markdown("---")
    st.markdown(f"### {icon} {mode}")
    st.info(content) if mode == "真心話" else st.warning(content)

st.markdown("---")
if st.session_state.history:
    with st.expander(f"📜 歷史紀錄（共 {len(st.session_state.history)} 題）"):
        for i, h in enumerate(reversed(st.session_state.history), 1):
            st.write(f"{i}. {h}")
