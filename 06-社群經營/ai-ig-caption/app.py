import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI IG 文案產生器", page_icon="📸", layout="centered")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("取得 API Key：[Groq Console](https://console.groq.com/)")

st.title("📸 AI IG 文案產生器")
st.caption("描述你的照片或情境，AI 幫你寫出吸睛的 IG 文案")

# --- 照片/情境描述 ---
description = st.text_area(
    "🖼️ 描述你的照片或情境",
    height=150,
    placeholder="例如：跟朋友去墾丁玩，在海邊拍了一張夕陽照，穿白色洋裝，背景是橘紅色的天空...",
)

# --- 風格選擇 ---
col1, col2 = st.columns(2)
with col1:
    style = st.selectbox(
        "✨ 文案風格",
        ["文青風", "搞笑風", "勵志風", "日常風", "浪漫風", "厭世風", "網美風"],
    )
with col2:
    lang_style = st.selectbox(
        "🗣️ 語言風格",
        ["純中文", "中英混搭", "加入日文", "加入韓文"],
    )

col3, col4 = st.columns(2)
with col3:
    caption_count = st.slider("📝 產生幾組文案", min_value=1, max_value=5, value=3)
with col4:
    hashtag_count = st.slider("# Hashtag 數量", min_value=5, max_value=30, value=15)

include_emoji = st.checkbox("加入 Emoji 表情", value=True)

if st.button("✍️ 產生 IG 文案", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not description.strip():
        st.error("請描述你的照片或情境。")
    else:
        emoji_note = "請適當加入 emoji 表情符號讓文案更生動。" if include_emoji else "不要使用 emoji。"
        prompt = (
            f"你是一位專業的 Instagram 文案寫手，擅長撰寫吸引人的中文 IG 貼文。\n\n"
            f"照片/情境描述：{description}\n"
            f"文案風格：{style}\n"
            f"語言風格：{lang_style}\n"
            f"{emoji_note}\n\n"
            f"請產生 {caption_count} 組不同的 IG 文案，每組包含：\n"
            f"1. **文案內容**：符合風格的貼文文字（2-5 行）\n"
            f"2. **Hashtag**：{hashtag_count} 個相關的 hashtag（混合熱門與小眾標籤）\n\n"
            "每組文案請用分隔線隔開，方便使用者直接複製使用。\n"
            "請用繁體中文撰寫。"
        )

        try:
            client = Groq(api_key=api_key)
            with st.spinner("AI 正在為你撰寫 IG 文案..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是專業的 Instagram 文案寫手，熟悉台灣社群文化與流行用語。請用繁體中文撰寫。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.8,
                    max_tokens=1536,
                )
            result = response.choices[0].message.content
            st.markdown("---")
            st.subheader("📱 你的 IG 文案")
            st.markdown(result)
            st.success("💡 點選文案即可複製，直接貼到 IG 上使用！")
        except Exception as e:
            st.error(f"發生錯誤：{e}")
