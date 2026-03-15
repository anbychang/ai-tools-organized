import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 同事翻譯機", page_icon="🗣️")

st.title("🗣️ AI 同事翻譯機")
st.markdown("輸入同事說的話，AI 幫你翻譯真正的意思，還教你怎麼回應！")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("### 常見職場話術範例")
    st.markdown(
        "- 「這個我們再討論」\n"
        "- 「辛苦了」\n"
        "- 「你覺得呢？」\n"
        "- 「這個很有挑戰性」\n"
        "- 「我們保持彈性」"
    )

# --- 主要輸入 ---
colleague_words = st.text_area(
    "💬 同事說了什麼？",
    placeholder="例如：這個我們再討論看看...",
    height=100,
)

context = st.text_input(
    "🏢 情境補充（選填）",
    placeholder="例如：在會議上被主管對著全組人說的",
)

who = st.selectbox(
    "🧑‍💼 說這句話的人是",
    ["同事", "主管", "老闆", "客戶", "人資 HR", "下屬"],
)

# --- 翻譯 ---
if st.button("🔍 翻譯真正意思", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not colleague_words:
        st.error("請輸入同事說的話。")
    else:
        prompt = (
            f"你是一位深諳台灣職場文化的溝通專家。\n\n"
            f"有人在職場上聽到以下這句話：\n「{colleague_words}」\n\n"
            f"說話的人：{who}\n"
            f"情境補充：{context if context else '無'}\n\n"
            f"請用繁體中文，以幽默又精準的方式分析：\n"
            f"1. **表面意思**：字面上在說什麼\n"
            f"2. **真正意思**：實際上想表達什麼（潛台詞）\n"
            f"3. **潛在風險**：如果你會錯意可能發生什麼\n"
            f"4. **建議回應方式**：提供 2-3 種合適的回應（含適用情境）\n"
            f"5. **職場生存小提醒**：一句簡短的建議\n\n"
            f"語氣可以輕鬆幽默，但分析要到位。"
        )

        client = Groq(api_key=api_key)

        with st.spinner("AI 正在解讀職場密碼..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是台灣職場文化翻譯專家，擅長解讀職場潛台詞。請用繁體中文回答。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.8,
                    max_tokens=2048,
                )
                result = response.choices[0].message.content
                st.markdown("---")
                st.subheader("🔮 翻譯結果")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
