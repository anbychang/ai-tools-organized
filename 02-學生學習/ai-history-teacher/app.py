import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 歷史老師", page_icon="🏛️")

# --- 側邊欄 ---
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    st.markdown("用說故事的方式學歷史")

st.title("🏛️ AI 歷史老師")
st.markdown("輸入歷史問題或主題，AI 用生動的故事方式為你講解。")

# --- 年代選擇 ---
era = st.selectbox("選擇歷史範疇", ["台灣史", "中國史", "世界史"])

# --- 問題輸入 ---
question = st.text_area(
    "輸入歷史問題或主題",
    height=120,
    placeholder="例如：為什麼會發生二二八事件？\n或：文藝復興如何改變歐洲？",
)

# --- 教學風格 ---
style = st.radio(
    "講解風格",
    ["故事敘述風格", "時間軸整理", "因果分析", "人物觀點"],
    horizontal=True,
)

def ask_history(api_key: str, question: str, era: str, style: str) -> str:
    client = Groq(api_key=api_key)

    style_instructions = {
        "故事敘述風格": "請用生動的故事方式講述，像在說一個精彩的故事一樣，讓歷史人物活起來。",
        "時間軸整理": "請用清楚的時間軸方式整理，標明每個重要事件的時間點和發展脈絡。",
        "因果分析": "請用因果分析的方式，清楚說明事件的背景原因、發展過程和影響結果。",
        "人物觀點": "請從關鍵歷史人物的視角出發，描述他們的想法、決策和行動。",
    }

    prompt = f"""你是一位精通{era}的歷史老師。

學生的問題：{question}

講解要求：{style_instructions[style]}

請包含：
1. 歷史背景簡介
2. 主要內容講解
3. 重要人物介紹
4. 歷史意義與影響
5. 有趣的歷史小知識或冷知識

請用繁體中文回覆，語氣親切有趣，適合高中生理解。"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": f"你是一位充滿熱情的{era}老師，擅長用故事讓歷史變得生動有趣，請用繁體中文回覆。"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.8,
        max_tokens=3072,
    )
    return response.choices[0].message.content

# --- 提問按鈕 ---
if st.button("開始講解", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not question.strip():
        st.warning("請輸入歷史問題或主題。")
    else:
        with st.spinner("歷史老師正在備課中..."):
            try:
                result = ask_history(api_key, question, era, style)
                st.markdown("---")
                st.subheader(f"📖 {era}講堂")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
