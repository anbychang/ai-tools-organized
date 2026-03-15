import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 留言回覆助手", page_icon="💬", layout="centered")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("取得 API Key：[Groq Console](https://console.groq.com/)")

st.title("💬 AI 留言回覆助手")
st.caption("幫你快速產生得體又有質感的留言回覆")

# --- 留言內容 ---
comment = st.text_area(
    "📩 留言內容",
    height=150,
    placeholder="貼上你收到的留言內容...",
)

# --- 設定 ---
col1, col2 = st.columns(2)
with col1:
    identity = st.selectbox(
        "👤 你的身份",
        ["個人帳號", "品牌/企業", "網紅/KOL", "店家/商家"],
    )
    platform = st.selectbox(
        "📱 留言平台",
        ["Instagram", "Facebook", "YouTube", "Dcard", "PTT", "Google 評論", "其他"],
    )
with col2:
    tone = st.selectbox(
        "🎨 回覆語氣",
        ["友善親切", "專業正式", "幽默風趣", "溫暖感性", "簡潔俐落"],
    )
    reply_count = st.slider("📝 產生幾則回覆", min_value=1, max_value=5, value=3)

context = st.text_input(
    "📋 補充背景（選填）",
    placeholder="例如：這則留言是在我的美食分享貼文下...",
)

if st.button("✍️ 產生回覆", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not comment.strip():
        st.error("請輸入留言內容。")
    else:
        prompt = (
            f"你是社群媒體回覆專家，擅長撰寫各種情境的留言回覆。\n\n"
            f"收到的留言：\n「{comment}」\n\n"
            f"回覆者身份：{identity}\n"
            f"留言平台：{platform}\n"
            f"回覆語氣：{tone}\n"
            f"補充背景：{context if context.strip() else '無'}\n\n"
            f"請產生 {reply_count} 則不同風格的回覆，每則回覆需要：\n"
            "1. 符合指定的語氣風格\n"
            "2. 適合該平台的文化與用語\n"
            "3. 展現真誠與專業\n"
            "4. 長度適中（不要太長也不要太短）\n\n"
            "每則回覆請標註適用情境（例如：適合快速回覆、適合深度互動等）。\n"
            "請用繁體中文撰寫。"
        )

        try:
            client = Groq(api_key=api_key)
            with st.spinner("AI 正在為你撰寫回覆..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是社群媒體回覆專家，熟悉各平台文化。請用繁體中文撰寫自然得體的回覆。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.7,
                    max_tokens=1536,
                )
            result = response.choices[0].message.content
            st.markdown("---")
            st.subheader("💬 建議回覆")
            st.markdown(result)
            st.success("💡 選一個最適合的回覆，可以再根據自己的風格微調！")
        except Exception as e:
            st.error(f"發生錯誤：{e}")
