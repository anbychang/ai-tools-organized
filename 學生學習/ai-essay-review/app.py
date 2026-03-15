import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 作文批改", page_icon="📝")

# --- 側邊欄 ---
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    st.markdown("使用 Groq LLM 進行作文批改與評分")

st.title("📝 AI 作文批改")
st.markdown("貼上你的作文，AI 將為你評分並提供修改建議。")

# --- 文體選擇 ---
genre = st.selectbox("選擇文體", ["記敘文", "論說文", "抒情文"])

# --- 作文輸入 ---
essay = st.text_area("請貼上你的作文", height=300, placeholder="在此輸入作文內容...")

def review_essay(api_key: str, essay: str, genre: str) -> str:
    client = Groq(api_key=api_key)
    prompt = f"""你是一位專業的中文作文老師。請針對以下「{genre}」進行批改。

請依照以下格式回覆：

## 評分（每項滿分 10 分）

| 評分項目 | 分數 | 說明 |
|---------|------|------|
| 內容立意 | X/10 | ... |
| 文章結構 | X/10 | ... |
| 文字表達 | X/10 | ... |
| 總分 | X/30 | ... |

## 優點分析
（列出作文的優點）

## 改進建議
（具體指出可以改進的地方，並給出修改範例）

## 修改後範例段落
（選擇一段進行改寫示範）

以下是學生的作文：

{essay}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "你是專業的中文作文批改老師，請用繁體中文回覆。"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=2048,
    )
    return response.choices[0].message.content

# --- 批改按鈕 ---
if st.button("開始批改", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not essay.strip():
        st.warning("請先輸入作文內容。")
    else:
        with st.spinner("AI 老師正在批改中..."):
            try:
                result = review_essay(api_key, essay, genre)
                st.markdown("---")
                st.subheader("批改結果")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
