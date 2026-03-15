import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 報告產生器", page_icon="📑")

# --- 側邊欄 ---
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    st.markdown("輸入報告題目，AI 自動產生大綱與重點")

st.title("📑 AI 報告產生器")
st.markdown("輸入報告相關資訊，AI 幫你產生完整大綱與各段重點。")

# --- 輸入區 ---
topic = st.text_input("報告題目", placeholder="例如：人工智慧對教育的影響")

col1, col2 = st.columns(2)
with col1:
    subject = st.text_input("所屬科目", placeholder="例如：資訊科技概論")
with col2:
    word_count = st.selectbox("字數要求", ["500字", "1000字", "1500字", "2000字", "3000字", "5000字"])

report_type = st.selectbox("報告類型", ["課堂報告", "期末報告", "專題研究", "文獻探討", "實驗報告"])

extra_notes = st.text_area("額外要求或備註（選填）", height=80, placeholder="例如：需要引用至少3篇參考文獻")

def generate_outline(api_key: str, topic: str, subject: str, word_count: str, report_type: str, extra_notes: str) -> str:
    client = Groq(api_key=api_key)
    prompt = f"""你是一位學術報告寫作專家。請根據以下資訊產生報告大綱與各段落重點。

## 報告資訊
- 題目：{topic}
- 科目：{subject}
- 類型：{report_type}
- 字數要求：{word_count}
- 額外要求：{extra_notes if extra_notes.strip() else '無'}

## 請提供以下內容

### 一、報告大綱
列出完整的章節結構（含子標題）

### 二、各段落重點
每個章節/段落的：
- 核心論點
- 建議涵蓋的內容
- 建議引用的資料方向

### 三、寫作建議
- 開頭破題技巧
- 論述邏輯建議
- 結尾收束方式

### 四、建議參考關鍵字
列出可用於搜尋文獻的中英文關鍵字

請用繁體中文回覆，格式清楚易讀。"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "你是學術報告寫作專家，擅長規劃報告架構，請用繁體中文回覆。"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=3072,
    )
    return response.choices[0].message.content

# --- 產生按鈕 ---
if st.button("產生報告大綱", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not topic.strip():
        st.warning("請輸入報告題目。")
    else:
        with st.spinner("AI 正在規劃報告大綱..."):
            try:
                result = generate_outline(api_key, topic, subject, word_count, report_type, extra_notes)
                st.markdown("---")
                st.subheader(f"《{topic}》報告大綱")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
