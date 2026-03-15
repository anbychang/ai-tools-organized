import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 論文摘要", page_icon="📄")

# --- 側邊欄 ---
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    st.markdown("貼上論文內容，AI 產生結構化中文摘要")

st.title("📄 AI 論文摘要")
st.markdown("貼上論文全文或部分段落，AI 幫你產生結構化的中文摘要。")

# --- 論文語言 ---
paper_lang = st.selectbox("論文語言", ["英文", "中文", "其他"])

# --- 論文輸入 ---
paper_text = st.text_area(
    "貼上論文內容",
    height=350,
    placeholder="將論文的摘要、方法、結果等章節貼在此處...",
)

# --- 摘要選項 ---
col1, col2 = st.columns(2)
with col1:
    summary_length = st.selectbox("摘要長度", ["簡短（200字）", "標準（500字）", "詳細（1000字）"])
with col2:
    audience = st.selectbox("目標讀者", ["一般大眾", "大學生", "研究生", "專業研究者"])

def summarize_paper(api_key: str, paper_text: str, paper_lang: str, summary_length: str, audience: str) -> str:
    client = Groq(api_key=api_key)
    prompt = f"""你是一位學術論文分析專家。請閱讀以下{paper_lang}論文內容，並產生結構化的繁體中文摘要。

目標讀者：{audience}
摘要長度：{summary_length}

請用以下結構回覆：

## 📌 論文基本資訊
（如能從文本判斷，列出標題、作者、年份等）

## 🎯 研究目的
本研究旨在解決什麼問題？為什麼這個問題重要？

## 📐 研究方法
使用了什麼研究方法？資料如何收集與分析？

## 📊 主要結果
最重要的研究發現是什麼？（列點說明）

## 💡 結論與貢獻
研究的主要結論是什麼？對該領域有什麼貢獻？

## ⚠️ 研究限制
（如能判斷）研究有什麼限制或不足？

## 🔑 關鍵字
列出 5-8 個關鍵字（中英文）

---

論文內容：
{paper_text}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "你是學術論文摘要專家，擅長提煉論文重點並用清楚的繁體中文呈現。"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=3072,
    )
    return response.choices[0].message.content

# --- 產生摘要 ---
if st.button("產生摘要", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not paper_text.strip():
        st.warning("請貼上論文內容。")
    elif len(paper_text.strip()) < 100:
        st.warning("論文內容太短，請貼上更多文字以獲得更好的摘要。")
    else:
        st.info(f"論文字數：約 {len(paper_text)} 字")
        with st.spinner("AI 正在閱讀與分析論文..."):
            try:
                result = summarize_paper(api_key, paper_text, paper_lang, summary_length, audience)
                st.markdown("---")
                st.subheader("論文摘要")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
