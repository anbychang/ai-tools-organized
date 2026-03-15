import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 翻譯+解析", page_icon="🌐")
st.title("🌐 AI 翻譯+解析")
st.caption("輸入英文文本，AI 翻譯為中文並解析文法、詞彙與句型結構")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    st.markdown("### 📖 使用說明")
    st.markdown(
        "1. 輸入 Groq API Key\n"
        "2. 在文字區域貼上英文文本\n"
        "3. 選擇解析深度\n"
        "4. 點擊「翻譯並解析」"
    )

# 主介面
english_text = st.text_area(
    "📝 請輸入英文文本",
    height=200,
    placeholder="在此貼上你想翻譯與解析的英文文本..."
)

depth = st.select_slider(
    "🔍 解析深度",
    options=["基礎", "中等", "詳細"],
    value="中等"
)

depth_instructions = {
    "基礎": "提供簡要的翻譯和基本文法說明",
    "中等": "提供完整翻譯、文法重點、詞彙等級分析",
    "詳細": "提供逐句翻譯、詳細文法解析、詞彙等級、句型結構拆解、同義替換建議"
}

if st.button("🚀 翻譯並解析", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key！")
    elif not english_text.strip():
        st.error("請輸入英文文本！")
    else:
        try:
            client = Groq(api_key=api_key)
            prompt = f"""你是一位專業的英文翻譯與語言分析師。請針對以下英文文本進行分析。
解析深度要求：{depth_instructions[depth]}

請使用以下格式回覆（全部使用繁體中文）：

## 📖 中文翻譯
（完整翻譯）

## 📝 文法重點
（標注重要文法結構並解釋）

## 📚 詞彙解析
（列出重要詞彙，標注詞性、難度等級如 CEFR A1-C2，並給出例句）

## 🔗 句型結構分析
（拆解句子結構，說明主詞、動詞、子句等）

## 💡 學習建議
（根據文本難度給出學習建議）

英文文本：
{english_text}"""

            with st.spinner("AI 正在翻譯與解析中..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是專業英文教師與翻譯專家，所有回覆使用繁體中文。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=4096,
                )
            result = response.choices[0].message.content
            st.divider()
            st.markdown(result)

        except Exception as e:
            st.error(f"發生錯誤：{e}")
