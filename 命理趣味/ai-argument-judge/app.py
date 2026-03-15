import streamlit as st
from groq import Groq

# --- 頁面設定 ---
st.set_page_config(page_title="AI 吵架裁判", page_icon="⚖️", layout="centered")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("使用 **Llama 3.3 70B** 模型")
    st.markdown("⚖️ 公正客觀的 AI 裁判！")

# --- 主頁面 ---
st.title("⚖️ AI 吵架裁判")
st.markdown("把雙方的說法都貼上來，讓 AI 公正裁決誰有道理！")

st.markdown("---")

# --- 吵架類型 ---
argument_type = st.selectbox(
    "🏷️ 吵架類型",
    ["情侶吵架", "朋友糾紛", "家人爭執", "同事衝突", "網路筆戰", "室友問題", "其他"]
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 A 方")
    name_a = st.text_input("A 方稱呼", value="A", key="name_a")
    argument_a = st.text_area(
        f"{name_a} 的說法",
        placeholder="請輸入 A 方的立場和論點...",
        height=200,
        key="arg_a",
    )

with col2:
    st.subheader("👤 B 方")
    name_b = st.text_input("B 方稱呼", value="B", key="name_b")
    argument_b = st.text_area(
        f"{name_b} 的說法",
        placeholder="請輸入 B 方的立場和論點...",
        height=200,
        key="arg_b",
    )

context = st.text_input("📍 背景補充（選填）", placeholder="例如：交往三年、同住半年...")

if st.button("⚖️ 開始裁決", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key！")
    elif not argument_a.strip() or not argument_b.strip():
        st.error("請輸入雙方的說法！")
    else:
        try:
            client = Groq(api_key=api_key)
            prompt = f"""你是一位公正、幽默又有智慧的吵架裁判。請根據雙方說法做出裁決。

吵架類型：{argument_type}
背景：{context if context.strip() else "無額外背景"}

【{name_a} 的說法】
{argument_a}

【{name_b} 的說法】
{argument_b}

請提供：
1. 📊 裁決比例：{name_a} 有理 X% vs {name_b} 有理 Y%（數字需加總 100%）
2. ⚖️ 最終裁決：判定誰比較有道理
3. 🧠 裁決理由：分析雙方各自的道理和不足之處
4. 💡 給 {name_a} 的建議
5. 💡 給 {name_b} 的建議
6. 🤝 和解方案：建議雙方如何化解爭議
7. 😂 裁判金句：用一句幽默的話總結

語調要公正但帶點幽默。繁體中文回答。"""

            with st.spinner("⚖️ AI 裁判正在審理案件..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是公正幽默的吵架裁判，用繁體中文做出合理裁決。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.8,
                    max_tokens=1500,
                )
            result = response.choices[0].message.content
            st.markdown("---")
            st.subheader("⚖️ 裁決結果")
            st.markdown(result)

        except Exception as e:
            st.error(f"發生錯誤：{e}")

# --- 頁尾 ---
st.markdown("---")
st.caption("⚖️ AI 吵架裁判 — 純屬娛樂參考，真正的問題需要好好溝通")
