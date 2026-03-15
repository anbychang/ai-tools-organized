import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 對聯產生器", page_icon="🧧")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    st.markdown("🔑 請先取得 [Groq API Key](https://console.groq.com/)")

st.title("🧧 AI 對聯產生器")
st.markdown("輸入上聯讓 AI 對下聯，或輸入主題產生完整春聯！")

# --- 模式選擇 ---
mode = st.radio("選擇模式", ["✍️ 對下聯", "🧨 產生春聯"], horizontal=True)

if mode == "✍️ 對下聯":
    upper = st.text_input("📝 請輸入上聯", placeholder="例如：風吹柳絮滿天飛")
    generate = st.button("🖊️ AI 對下聯", use_container_width=True)

    if generate:
        if not api_key:
            st.warning("⚠️ 請先在側邊欄輸入 Groq API Key。")
            st.stop()
        if not upper.strip():
            st.warning("⚠️ 請輸入上聯。")
            st.stop()

        prompt = (
            f"你是一位精通對聯的繁體中文文學大師。\n"
            f"上聯：{upper}\n\n"
            f"請為這副上聯配一個工整的下聯。要求：\n"
            f"1. 字數與上聯相同\n"
            f"2. 詞性對仗工整\n"
            f"3. 平仄盡量協調\n"
            f"4. 意境相呼應或形成對比\n"
            f"5. 使用繁體中文\n\n"
            f"請提供 3 個不同風格的下聯選擇，並簡要說明每個下聯的巧妙之處。\n"
            f"格式：\n下聯一：...\n說明：...\n下聯二：...\n說明：...\n下聯三：...\n說明：..."
        )

        client = Groq(api_key=api_key)
        with st.spinner("✍️ AI 正在思考下聯..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是精通中國對聯藝術的繁體中文文學大師。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.8,
                    max_tokens=1024,
                )
                result = response.choices[0].message.content
                st.divider()
                st.subheader("📜 下聯結果")
                st.markdown(f"**上聯：** {upper}")
                st.markdown(result)
            except Exception as e:
                st.error(f"❌ 發生錯誤：{e}")

else:
    theme = st.text_input("🎉 春聯主題", placeholder="例如：新年快樂、事業有成、闔家平安")
    generate = st.button("🧨 產生春聯", use_container_width=True)

    if generate:
        if not api_key:
            st.warning("⚠️ 請先在側邊欄輸入 Groq API Key。")
            st.stop()
        if not theme.strip():
            st.warning("⚠️ 請輸入主題。")
            st.stop()

        prompt = (
            f"你是一位精通春聯的繁體中文文學大師。\n"
            f"請根據主題「{theme}」創作 2 副完整的春聯。\n\n"
            f"每副春聯包含：上聯、下聯、橫批。\n"
            f"要求：對仗工整、寓意吉祥、繁體中文。\n"
            f"格式：\n【第一副】\n上聯：...\n下聯：...\n橫批：...\n賞析：..."
        )

        client = Groq(api_key=api_key)
        with st.spinner("🧨 AI 正在揮毫..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是精通中國春聯藝術的繁體中文文學大師。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.8,
                    max_tokens=1024,
                )
                result = response.choices[0].message.content
                st.divider()
                st.subheader(f"🧧 主題「{theme}」春聯")
                st.markdown(result)
            except Exception as e:
                st.error(f"❌ 發生錯誤：{e}")
