import streamlit as st
from groq import Groq

# --- 頁面設定 ---
st.set_page_config(page_title="AI 藉口百科", page_icon="🤥", layout="centered")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("使用 **Llama 3.3 70B** 模型")
    st.markdown("🤥 千萬個理由，只為了你的自由！")

# --- 主頁面 ---
st.title("🤥 AI 藉口百科")
st.markdown("選擇你的窘境，AI 幫你量身打造完美藉口！")

st.markdown("---")

# --- 情境選擇 ---
situations = {
    "不想出門 🏠": "朋友/同事邀約出門，但你只想在家耍廢",
    "不想加班 💼": "老闆/主管要求加班，但你想準時下班",
    "不想借錢 💰": "朋友/親戚來借錢，你不想借",
    "忘記紀念日 💔": "忘了重要的紀念日或生日",
    "遲到 ⏰": "上班、上課或約會遲到",
    "不想參加聚餐 🍽️": "不想參加公司聚餐或家族聚餐",
    "不想回訊息 📱": "已讀不回被抓包",
    "不想做家事 🧹": "被催著做家事但不想動",
    "請假 🤒": "想請假但沒有正當理由",
    "拒絕告白 💌": "不想傷人但要拒絕",
}

situation = st.selectbox("😰 選擇你的窘境", list(situations.keys()))
st.caption(f"情境說明：{situations[situation]}")

credibility = st.select_slider(
    "📊 藉口可信度",
    options=["低（搞笑優先）", "中（半信半疑）", "高（天衣無縫）"],
    value="中（半信半疑）",
)

target = st.text_input("👤 要騙的對象（選填）", placeholder="例如：老闆、媽媽、女朋友、同事...")
extra = st.text_input("📝 額外條件（選填）", placeholder="例如：對方很精明、之前用過太多藉口...")

if st.button("🎲 產生藉口", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key！")
    else:
        try:
            client = Groq(api_key=api_key)
            prompt = f"""你是藉口百科全書，專門產生各種創意藉口。

窘境：{situation}
可信度要求：{credibility}
對象：{target if target.strip() else "一般人"}
額外條件：{extra if extra.strip() else "無"}

請提供 5 個不同的藉口，每個包含：
1. 🎭 藉口內容（具體的說法，可以直接照唸）
2. 📊 可信度評分（1-10 分）
3. ⚠️ 風險評估（被拆穿的可能性）
4. 💡 配套措施（如何讓藉口更可信）

從最保守到最大膽排列。
繁體中文回答，語調幽默有趣。
最後附上一個「大絕招」— 最荒謬但最有創意的藉口。"""

            with st.spinner("🧠 AI 正在翻閱藉口百科全書..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是幽默的藉口大師，用繁體中文產生各種創意藉口。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.95,
                    max_tokens=1500,
                )
            result = response.choices[0].message.content
            st.markdown("---")
            st.subheader("📖 藉口清單")
            st.markdown(result)
            st.warning("⚠️ 免責聲明：本工具純屬娛樂，使用藉口的後果請自行負責！")

        except Exception as e:
            st.error(f"發生錯誤：{e}")

# --- 頁尾 ---
st.markdown("---")
st.caption("🤥 AI 藉口百科 — 純屬娛樂，誠實還是最好的策略！")
