import streamlit as st
from groq import Groq
import json

st.set_page_config(page_title="AI 單字卡", page_icon="🃏")

# --- 側邊欄 ---
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    st.markdown("輸入英文單字，AI 產生中文意思、例句與記憶技巧")

st.title("🃏 AI 單字卡")
st.markdown("每行輸入一個英文單字，AI 幫你製作單字卡。")

# --- 單字輸入 ---
words_input = st.text_area(
    "輸入英文單字（每行一個）",
    height=200,
    placeholder="apple\nubiquitous\nserendipity\nprocrastinate",
)

def generate_cards(api_key: str, words: list) -> str:
    client = Groq(api_key=api_key)
    word_list = ", ".join(words)
    prompt = f"""請為以下英文單字製作單字卡。每個單字請提供：

1. **中文意思**：主要的中文翻譯（含詞性）
2. **例句**：一個實用的英文例句，附中文翻譯
3. **記憶技巧**：諧音、聯想、字根拆解等記憶方法

單字列表：{word_list}

請用以下格式回覆每個單字：

### 單字：[英文單字]
- **中文意思**：...
- **例句**：...（中文翻譯：...）
- **記憶技巧**：...

---

請用繁體中文回覆。"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "你是英文教學專家，擅長用有趣的方式幫助學生記憶單字，請用繁體中文回覆。"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=3072,
    )
    return response.choices[0].message.content

# --- 產生按鈕 ---
if st.button("產生單字卡", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not words_input.strip():
        st.warning("請至少輸入一個英文單字。")
    else:
        words = [w.strip() for w in words_input.strip().split("\n") if w.strip()]
        st.info(f"正在為 **{len(words)}** 個單字製作單字卡...")
        with st.spinner("AI 正在製作單字卡..."):
            try:
                result = generate_cards(api_key, words)
                # 將結果分割成個別單字卡
                cards = result.split("---")
                for i, card in enumerate(cards):
                    card = card.strip()
                    if not card:
                        continue
                    with st.container():
                        st.markdown(
                            f"""<div style="
                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                padding: 20px;
                                border-radius: 15px;
                                color: white;
                                margin-bottom: 15px;
                                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                            ">{card}</div>""",
                            unsafe_allow_html=True,
                        )
            except Exception as e:
                st.error(f"發生錯誤：{e}")

# --- 顯示已儲存的單字（session state）---
if "saved_words" not in st.session_state:
    st.session_state.saved_words = []
