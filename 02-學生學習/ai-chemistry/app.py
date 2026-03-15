import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 化學方程式", page_icon="🧪")

# --- 側邊欄 ---
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    st.markdown("輸入反應物，AI 幫你配平方程式並解說")

st.title("🧪 AI 化學方程式")
st.markdown("輸入化學反應物，AI 幫你配平方程式、說明反應類型與生成物。")

# --- 輸入模式 ---
input_mode = st.radio(
    "輸入方式",
    ["輸入反應物", "輸入完整方程式（待配平）", "描述反應情境"],
    horizontal=True,
)

if input_mode == "輸入反應物":
    col1, col2 = st.columns(2)
    with col1:
        reactant1 = st.text_input("反應物 1", placeholder="例如：Fe")
    with col2:
        reactant2 = st.text_input("反應物 2", placeholder="例如：O2")
    extra_reactants = st.text_input("其他反應物（選填，用逗號分隔）", placeholder="例如：H2O, HCl")
    query = f"反應物：{reactant1} + {reactant2}"
    if extra_reactants.strip():
        query += f" + {extra_reactants}"
elif input_mode == "輸入完整方程式（待配平）":
    query = st.text_input("輸入未配平的方程式", placeholder="例如：Fe + O2 -> Fe2O3")
else:
    query = st.text_area("描述反應情境", height=100, placeholder="例如：鐵在空氣中生鏽的過程")

# --- 解說深度 ---
depth = st.selectbox("解說深度", ["基礎（國中）", "進階（高中）", "詳細（大學）"])

def analyze_reaction(api_key: str, query: str, input_mode: str, depth: str) -> str:
    client = Groq(api_key=api_key)
    prompt = f"""你是一位化學老師。學生提供了以下化學反應資訊：

輸入方式：{input_mode}
內容：{query}
希望的解說深度：{depth}

請提供以下內容：

## ⚖️ 配平後的化學方程式
（用正確的化學式和係數表示）

## 🔬 反應類型
說明這是什麼類型的反應（化合、分解、置換、複分解、氧化還原等）

## 📋 反應物與生成物
| 物質 | 化學式 | 角色 | 狀態 |
|------|--------|------|------|

## 💡 反應原理說明
解釋為什麼這個反應會發生，涉及什麼化學原理

## 🔥 反應條件
說明此反應需要什麼條件（溫度、催化劑、壓力等）

## 🌍 生活應用
這個反應在日常生活中的應用或例子

## ⚠️ 注意事項
安全注意事項或常見錯誤

請用繁體中文回覆。"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "你是化學教學專家，擅長配平方程式和解說化學反應，請用繁體中文回覆。"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=3072,
    )
    return response.choices[0].message.content

# --- 分析按鈕 ---
if st.button("分析反應", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not query.strip() or query.strip() == "反應物： +":
        st.warning("請輸入反應資訊。")
    else:
        with st.spinner("AI 正在分析化學反應..."):
            try:
                result = analyze_reaction(api_key, query, input_mode, depth)
                st.markdown("---")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
