import streamlit as st
from groq import Groq

# --- 頁面設定 ---
st.set_page_config(page_title="AI 垃圾話產生器", page_icon="🗑️", layout="centered")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("使用 **Llama 3.3 70B** 模型")
    st.markdown("🗑️ 垃圾話也是一種藝術！")

# --- 主頁面 ---
st.title("🗑️ AI 垃圾話產生器")
st.markdown("選擇對象和程度，AI 幫你產生有趣的垃圾話！")

st.warning("⚠️ 免責聲明：本工具純屬娛樂搞笑，請勿用於霸凌或傷害他人！")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    target = st.selectbox("🎯 對象", [
        "朋友（互嘴用）",
        "自己（自嘲用）",
        "人生（感嘆用）",
        "星期一（上班族共鳴）",
        "天氣（抱怨用）",
        "塞車（通勤族必備）",
    ])
with col2:
    level = st.selectbox("🌶️ 辛辣程度", [
        "溫和（小打小鬧）",
        "中等（有點嗆）",
        "毒舌（高能預警）",
    ])

style = st.selectbox("🎨 風格", [
    "台灣日常", "文言文風", "詩意優美", "冷笑話風", "哲學深度", "網路迷因風"
])

topic = st.text_input("📝 指定主題（選填）", placeholder="例如：總是遲到、愛放鴿子、每天都在減肥...")
count = st.slider("📊 產生數量", min_value=3, max_value=10, value=5)

if st.button("🔥 產生垃圾話", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key！")
    else:
        try:
            client = Groq(api_key=api_key)
            prompt = f"""你是垃圾話藝術大師，專門產生有趣、搞笑但不會真正傷人的垃圾話。

對象：{target}
辛辣程度：{level}
風格：{style}
指定主題：{topic if topic.strip() else "不限"}
數量：{count} 句

規則：
1. 每句垃圾話要簡短有力（一兩句話）
2. 要搞笑、有創意、有梗
3. 絕對不能涉及外貌歧視、種族歧視、性別歧視等敏感議題
4. 如果是「自己」或「人生」，要帶有自嘲的幽默感
5. 根據風格調整用詞和語氣

請產生 {count} 句垃圾話，每句前面加上編號和合適的 emoji。
最後附上一句「今日最佳垃圾話」精選。
繁體中文回答。"""

            with st.spinner("🗑️ AI 正在醞釀垃圾話..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是幽默的垃圾話大師，產生搞笑但不傷人的垃圾話，繁體中文。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=1.0,
                    max_tokens=1024,
                )
            result = response.choices[0].message.content
            st.markdown("---")
            st.subheader("🔥 垃圾話出爐")
            st.markdown(result)
            st.markdown("---")
            st.info("💡 小提示：好的垃圾話讓人笑，壞的垃圾話讓人哭。請善用！")

        except Exception as e:
            st.error(f"發生錯誤：{e}")

# --- 頁尾 ---
st.markdown("---")
st.caption("🗑️ AI 垃圾話產生器 — 純屬娛樂，友情提醒：說垃圾話要看對象！")
