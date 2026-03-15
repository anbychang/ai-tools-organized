import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 迷因解釋器", page_icon="😂")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    st.markdown("🔑 請先取得 [Groq API Key](https://console.groq.com/)")

st.title("😂 AI 迷因解釋器")
st.markdown("看到迷因看不懂？輸入迷因文字或描述，讓 AI 幫你解釋笑點、起源和文化背景！")

# --- 輸入方式 ---
input_mode = st.radio("輸入方式", ["📝 迷因文字", "🖼️ 描述迷因"], horizontal=True)

if input_mode == "📝 迷因文字":
    meme_input = st.text_area(
        "輸入迷因文字",
        placeholder="例如：\n上面：老師說考試很簡單\n下面：考試題目：",
        height=120,
    )
else:
    meme_input = st.text_area(
        "描述你看到的迷因",
        placeholder="例如：一隻柴犬坐在著火的房間裡說「This is fine」...",
        height=120,
    )

# --- 額外資訊 ---
context = st.text_input("📎 在哪裡看到的？（選填）", placeholder="例如：PTT、Twitter、朋友傳的...")

generate = st.button("🔍 解釋迷因", use_container_width=True)

if generate:
    if not api_key:
        st.warning("⚠️ 請先在側邊欄輸入 Groq API Key。")
        st.stop()
    if not meme_input.strip():
        st.warning("⚠️ 請輸入迷因文字或描述。")
        st.stop()

    context_text = f"\n來源平台：{context}" if context.strip() else ""
    mode_label = "迷因文字" if input_mode == "📝 迷因文字" else "迷因描述"

    prompt = (
        f"你是一位精通網路文化與迷因的專家。\n"
        f"以下是使用者提供的{mode_label}：\n\n"
        f"「{meme_input}」{context_text}\n\n"
        f"請用繁體中文詳細解釋這個迷因，包含：\n\n"
        f"## 😂 笑點解析\n"
        f"解釋這個迷因為什麼好笑，笑點在哪裡。\n\n"
        f"## 📜 起源與歷史\n"
        f"這個迷因的起源、最早出現的地方、怎麼流行起來的。\n\n"
        f"## 🌍 文化背景\n"
        f"相關的文化脈絡、為什麼特定群體會覺得有共鳴。\n\n"
        f"## 🔄 常見變體\n"
        f"這個迷因常見的改編或衍生版本。\n\n"
        f"如果你不確定具體是哪個迷因，請根據描述做最合理的推測並說明。"
    )

    client = Groq(api_key=api_key)
    with st.spinner("🔍 AI 正在分析迷因..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "你是網路迷因文化專家，精通各國迷因的歷史與背景，用繁體中文回答。"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=2048,
            )
            result = response.choices[0].message.content
            st.divider()
            st.subheader("🧠 迷因解析結果")
            st.markdown(result)
        except Exception as e:
            st.error(f"❌ 發生錯誤：{e}")
