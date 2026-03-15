import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 筆記整理", page_icon="📒")
st.title("📒 AI 筆記整理")
st.caption("貼上雜亂的筆記，AI 幫你整理成結構化的清晰筆記")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    st.markdown("### 📖 使用說明")
    st.markdown(
        "1. 輸入 Groq API Key\n"
        "2. 貼上你的雜亂筆記\n"
        "3. 選擇整理格式\n"
        "4. 點擊「整理筆記」"
    )

# 主介面
notes_input = st.text_area(
    "📝 貼上你的雜亂筆記",
    height=250,
    placeholder="把你的筆記、隨手記、上課重點等貼在這裡...\n例如：\nML 就是機器學習 supervised unsupervised\n監督式有標籤 非監督式沒有\nSVM 決策樹 隨機森林\n深度學習是ML的子集 神經網路\nCNN影像 RNN序列 transformer注意力機制"
)

col1, col2 = st.columns(2)
with col1:
    format_type = st.selectbox(
        "📋 整理格式",
        ["重點條列", "心智圖文字版", "表格", "康乃爾筆記法", "大綱式"]
    )
with col2:
    subject = st.text_input("📚 科目/主題（選填）", placeholder="例如：機器學習")

add_summary = st.checkbox("📌 附加摘要總結", value=True)
add_quiz = st.checkbox("❓ 附加自我測驗題", value=False)

format_instructions = {
    "重點條列": "使用清晰的條列式（bullet points），分主題歸類，有層次結構",
    "心智圖文字版": "用縮排和符號呈現心智圖的樹狀結構，中心主題在最上方，分支向下展開",
    "表格": "使用 Markdown 表格整理，欄位包含：主題、重點、說明、備註",
    "康乃爾筆記法": "分為三區：左欄（關鍵字/問題）、右欄（筆記內容）、底部（摘要）",
    "大綱式": "使用編號大綱（I, A, 1, a）的階層結構整理"
}

if st.button("🚀 整理筆記", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key！")
    elif not notes_input.strip():
        st.error("請貼上你的筆記內容！")
    else:
        try:
            client = Groq(api_key=api_key)
            subject_hint = f"這是關於「{subject}」的筆記。" if subject else ""
            extra = ""
            if add_summary:
                extra += "\n\n## 📌 摘要總結\n（用 3-5 句話總結所有重點）"
            if add_quiz:
                extra += "\n\n## ❓ 自我測驗\n（根據筆記內容出 3-5 題測驗題，附答案）"

            prompt = f"""你是一位專業的筆記整理專家。請將以下雜亂的筆記整理成結構化的格式。
{subject_hint}
使用繁體中文回覆。

整理格式要求：{format_instructions[format_type]}

原始筆記：
{notes_input}

請整理成清晰、有組織的筆記。補充必要的連接詞和說明，但不要加入原始筆記沒有提到的新知識。{extra}"""

            with st.spinner("AI 正在整理你的筆記..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是筆記整理專家，擅長將雜亂資訊結構化，回覆使用繁體中文。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=4096,
                )
            result = response.choices[0].message.content
            st.divider()
            st.markdown("### ✨ 整理後的筆記")
            st.markdown(result)

        except Exception as e:
            st.error(f"發生錯誤：{e}")
