import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 取名字", page_icon="👶")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("使用 Llama 3.3 70B 模型")


def generate_names(surname, gender, expectations, name_type):
    """呼叫 Groq API 產生名字建議"""
    client = Groq(api_key=api_key)

    if name_type == "中文名字":
        prompt = f"""你是一位專業的命名顧問。請根據以下條件，產生 5 個中文名字建議：
- 姓氏：{surname}
- 性別：{gender}
- 期望/特質：{expectations}

請為每個名字提供：
1. 完整姓名
2. 名字的含義解釋
3. 為什麼適合這個期望

請用繁體中文回答，格式清晰美觀。"""
    else:
        prompt = f"""你是一位專業的命名顧問。請根據以下條件，產生 5 個英文名字建議：
- 姓氏：{surname}
- 性別：{gender}
- 期望/特質：{expectations}

請為每個名字提供：
1. 英文名 + 姓氏
2. 名字的起源與含義
3. 為什麼適合這個期望

請用繁體中文回答，格式清晰美觀。"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=2000,
    )
    return response.choices[0].message.content


# 主頁面
st.title("👶 AI 取名字")
st.markdown("讓 AI 幫你取一個有意義的好名字！")

st.markdown("---")

name_type = st.radio("名字類型", ["中文名字", "英文名字"], horizontal=True)

col1, col2 = st.columns(2)
with col1:
    surname = st.text_input("姓氏", placeholder="例如：王、林、陳")
with col2:
    gender = st.selectbox("性別", ["男", "女", "中性"])

expectations = st.text_area(
    "期望與特質",
    placeholder="例如：希望孩子聰明、善良、有領導力...",
    height=100,
)

if st.button("✨ 產生名字建議", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key！")
    elif not surname:
        st.warning("請輸入姓氏！")
    elif not expectations:
        st.warning("請輸入期望與特質！")
    else:
        with st.spinner("AI 正在為你取名字..."):
            try:
                result = generate_names(surname, gender, expectations, name_type)
                st.markdown("### 🎯 名字建議")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
