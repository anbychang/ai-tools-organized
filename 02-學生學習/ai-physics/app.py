import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 物理教室", page_icon="⚡")

# --- 側邊欄 ---
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    st.markdown("用生活比喻理解物理原理")

st.title("⚡ AI 物理教室")
st.markdown("描述一個物理情境或問題，AI 用簡單的比喻幫你理解物理原理。")

# --- 物理領域 ---
field = st.selectbox(
    "物理領域（選填，幫助 AI 更精準）",
    ["自動判斷", "力學", "熱學", "光學", "電磁學", "波動", "近代物理", "流體力學"],
)

# --- 問題輸入 ---
question = st.text_area(
    "輸入物理情境或問題",
    height=150,
    placeholder="例如：\n為什麼溜冰選手收手後旋轉會變快？\n或：如果在電梯裡量體重會怎樣？",
)

level = st.radio("希望的解說程度", ["國中程度", "高中程度", "大學程度"], horizontal=True)

def explain_physics(api_key: str, question: str, field: str, level: str) -> str:
    client = Groq(api_key=api_key)
    field_hint = f"（此問題可能涉及{field}）" if field != "自動判斷" else ""

    prompt = f"""你是一位擅長用生活比喻的物理老師。{field_hint}

學生的問題：{question}

解說程度：{level}

請用以下架構回答：

## 🔍 這個現象涉及什麼原理？
簡要說明涉及的物理原理名稱

## 🎯 生活化比喻
用一個貼近日常生活的比喻來解釋這個原理

## 📐 原理詳解
用{level}的程度解釋物理原理，包含：
- 核心概念
- 相關公式（如適用）
- 邏輯推導

## 🌍 生活中的其他例子
列出 2-3 個同樣原理的生活實例

## 💡 常見迷思
指出學生對此概念常見的錯誤理解

請用繁體中文回覆。"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "你是物理教學專家，擅長用生活比喻讓抽象概念變得具體易懂，請用繁體中文回覆。"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=3072,
    )
    return response.choices[0].message.content

# --- 解題按鈕 ---
if st.button("開始解說", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not question.strip():
        st.warning("請輸入物理問題或情境。")
    else:
        with st.spinner("物理老師正在準備精彩的比喻..."):
            try:
                result = explain_physics(api_key, question, field, level)
                st.markdown("---")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
