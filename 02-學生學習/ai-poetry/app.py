import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 詩詞賞析", page_icon="📜")
st.title("📜 AI 詩詞賞析")
st.caption("輸入一首中國古典詩詞，AI 為你提供白話翻譯、寫作背景、修辭分析與情感解讀")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    st.markdown("### 📖 使用說明")
    st.markdown(
        "1. 輸入 Groq API Key\n"
        "2. 輸入古典詩詞內容\n"
        "3. 可選填詩人與詩名\n"
        "4. 點擊「開始賞析」"
    )

# 範例詩詞
examples = {
    "自行輸入": "",
    "靜夜思 — 李白": "床前明月光，疑是地上霜。\n舉頭望明月，低頭思故鄉。",
    "登鸛雀樓 — 王之渙": "白日依山盡，黃河入海流。\n欲窮千里目，更上一層樓。",
    "春曉 — 孟浩然": "春眠不覺曉，處處聞啼鳥。\n夜來風雨聲，花落知多少。",
    "楓橋夜泊 — 張繼": "月落烏啼霜滿天，江楓漁火對愁眠。\n姑蘇城外寒山寺，夜半鐘聲到客船。",
}

selected = st.selectbox("📋 選擇範例詩詞或自行輸入", list(examples.keys()))

col1, col2 = st.columns(2)
with col1:
    poet_name = st.text_input("✍️ 詩人（選填）", placeholder="例如：李白")
with col2:
    poem_title = st.text_input("📛 詩名（選填）", placeholder="例如：靜夜思")

poem_text = st.text_area(
    "📝 請輸入詩詞內容",
    value=examples[selected],
    height=150,
    placeholder="在此輸入古典詩詞..."
)

analysis_focus = st.multiselect(
    "🔍 選擇賞析重點",
    ["白話翻譯", "寫作背景", "修辭分析", "情感解讀", "意象分析", "格律說明"],
    default=["白話翻譯", "寫作背景", "修辭分析", "情感解讀"]
)

if st.button("🚀 開始賞析", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key！")
    elif not poem_text.strip():
        st.error("請輸入詩詞內容！")
    else:
        try:
            client = Groq(api_key=api_key)
            meta = ""
            if poet_name:
                meta += f"詩人：{poet_name}\n"
            if poem_title:
                meta += f"詩名：{poem_title}\n"

            sections = "\n".join([f"## {f}" for f in analysis_focus])
            prompt = f"""你是一位中國古典文學教授，精通詩詞賞析。請對以下詩詞進行深入賞析。
全部使用繁體中文回覆。

{meta}
詩詞內容：
{poem_text}

請按照以下章節進行賞析（每個章節都要詳細說明）：
{sections}

請確保分析深入、用詞優美，適合文學愛好者閱讀。"""

            with st.spinner("AI 正在賞析詩詞中..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是中國古典文學教授，專精詩詞賞析，回覆使用繁體中文。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,
                    max_tokens=4096,
                )
            result = response.choices[0].message.content
            st.divider()
            st.markdown(result)

        except Exception as e:
            st.error(f"發生錯誤：{e}")
