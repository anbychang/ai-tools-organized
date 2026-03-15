import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Podcast 腳本", page_icon="🎙️")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    st.markdown("🔑 請先取得 [Groq API Key](https://console.groq.com/)")

st.title("🎙️ AI Podcast 腳本產生器")
st.markdown("輸入主題和設定，讓 AI 幫你撰寫完整的 Podcast 腳本！")

# --- 參數設定 ---
topic = st.text_input("📝 Podcast 主題", placeholder="例如：為什麼年輕人不想結婚？")

col1, col2 = st.columns(2)
with col1:
    duration = st.selectbox("⏱️ 節目時長", ["5 分鐘", "10 分鐘", "15 分鐘", "20 分鐘", "30 分鐘"])
with col2:
    style = st.selectbox("🎨 節目風格", ["知識型", "閒聊", "訪談"])

style_desc = {
    "知識型": "以傳遞知識為主，結構嚴謹，引用數據和研究，像 TED Talk 風格",
    "閒聊": "輕鬆隨意的聊天風格，像跟朋友聊天一樣自然，穿插個人經驗和趣事",
    "訪談": "主持人與來賓對談的形式，有問有答，深入探討主題",
}

# --- 額外設定 ---
with st.expander("🔧 進階設定"):
    host_name = st.text_input("主持人名稱", value="主持人", placeholder="例如：小明")
    guest_name = st.text_input(
        "來賓名稱（訪談風格適用）", value="來賓", placeholder="例如：張教授"
    )
    target_audience = st.text_input("目標聽眾", placeholder="例如：20-30歲上班族")
    tone = st.selectbox("語調", ["輕鬆幽默", "專業嚴謹", "溫暖親切", "熱血激昂"])

generate = st.button("🎬 產生 Podcast 腳本", use_container_width=True)

if generate:
    if not api_key:
        st.warning("⚠️ 請先在側邊欄輸入 Groq API Key。")
        st.stop()
    if not topic.strip():
        st.warning("⚠️ 請輸入 Podcast 主題。")
        st.stop()

    audience_text = f"\n- 目標聽眾：{target_audience}" if target_audience.strip() else ""
    host_label = host_name if host_name.strip() else "主持人"
    guest_label = guest_name if guest_name.strip() else "來賓"

    prompt = (
        f"你是一位專業的 Podcast 腳本撰寫師。\n"
        f"請根據以下條件撰寫完整的 Podcast 腳本：\n"
        f"- 主題：{topic}\n"
        f"- 時長：{duration}\n"
        f"- 風格：{style}（{style_desc[style]}）\n"
        f"- 語調：{tone}\n"
        f"- 主持人：{host_label}\n"
        f"- 來賓：{guest_label}{audience_text}\n\n"
        f"腳本結構要求：\n"
        f"1. 🎬 開場白（自我介紹 + 主題引入）\n"
        f"2. 📋 內容段落（分 2-4 個段落，每段有小主題）\n"
        f"3. 💬 互動環節（提問或呼籲聽眾參與）\n"
        f"4. 🎤 結尾（總結 + 預告下集 + 呼籲訂閱）\n\n"
        f"格式要求：\n"
        f"- 用【{host_label}】【{guest_label}】標記說話者\n"
        f"- 用（）標記語氣或動作提示\n"
        f"- 用 --- 分隔段落\n"
        f"- 全文使用繁體中文"
    )

    client = Groq(api_key=api_key)
    with st.spinner("🎙️ AI 正在撰寫腳本..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "你是專業的繁體中文 Podcast 腳本撰寫師。"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.8,
                max_tokens=4096,
            )
            result = response.choices[0].message.content
            st.divider()
            st.subheader(f"🎙️ 《{topic}》Podcast 腳本")
            st.caption(f"⏱️ {duration} | 🎨 {style} | 🗣️ {tone}")
            st.markdown(result)
        except Exception as e:
            st.error(f"❌ 發生錯誤：{e}")
