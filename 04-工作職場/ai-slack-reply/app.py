import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Slack 回覆產生器", page_icon="💬")

st.title("💬 AI Slack 回覆產生器")
st.markdown("輸入同事的訊息、選擇語氣，AI 幫你產生多種回覆選項。")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("### Slack 回覆小技巧")
    st.markdown(
        "- 及時回覆表示尊重\n"
        "- 善用 emoji 增添溫度\n"
        "- 複雜問題建議開 thread\n"
        "- 重要決定留下文字紀錄\n"
        "- 避免過度簡短造成誤會"
    )

# --- 主要輸入 ---
message = st.text_area(
    "📩 同事的訊息",
    placeholder="貼上同事傳給你的 Slack 訊息...",
    height=120,
)

col1, col2 = st.columns(2)
with col1:
    tone = st.selectbox(
        "🎭 回覆語氣",
        ["專業正式", "友善親切", "簡潔俐落"],
    )
with col2:
    relationship = st.selectbox(
        "👥 對方身分",
        ["同事", "主管", "下屬", "跨部門同事", "外部合作夥伴"],
    )

col3, col4 = st.columns(2)
with col3:
    intent = st.selectbox(
        "🎯 你想要的回覆方向",
        ["同意/接受", "婉拒/推遲", "詢問更多資訊", "提出不同意見",
         "表達感謝", "確認進度", "分配任務", "一般回覆"],
    )
with col4:
    urgency = st.selectbox(
        "⚡ 訊息急迫程度",
        ["一般", "有點急", "很急"],
    )

context = st.text_input(
    "📝 補充背景（選填）",
    placeholder="例如：這是關於 Q4 行銷專案的討論...",
)

# --- 產生回覆 ---
if st.button("⚡ 產生回覆選項", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not message:
        st.error("請輸入同事的訊息。")
    else:
        prompt = (
            f"你是一位職場溝通專家。請根據以下情境，產生 Slack 回覆訊息。\n\n"
            f"同事的訊息：{message}\n"
            f"回覆語氣：{tone}\n"
            f"對方身分：{relationship}\n"
            f"回覆方向：{intent}\n"
            f"急迫程度：{urgency}\n"
            f"背景補充：{context if context else '無'}\n\n"
            f"請用繁體中文回答，提供 3 個不同版本的回覆：\n\n"
            f"**版本 A - 標準版**：最適合多數情境的回覆\n"
            f"**版本 B - 進階版**：更周到、更有策略的回覆\n"
            f"**版本 C - 精簡版**：最簡短但不失禮的回覆\n\n"
            f"每個版本請：\n"
            f"- 符合「{tone}」的語氣\n"
            f"- 適合 Slack 即時通訊的篇幅\n"
            f"- 可以適當使用 emoji\n"
            f"- 在回覆後簡短說明此版本的策略考量"
        )

        client = Groq(api_key=api_key)

        with st.spinner("AI 正在產生回覆選項..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是職場溝通專家，擅長撰寫即時通訊回覆。請用繁體中文回答。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.8,
                    max_tokens=2048,
                )
                result = response.choices[0].message.content
                st.markdown("---")
                st.subheader("💡 回覆選項")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
