import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 信用卡推薦", page_icon="💳", layout="centered")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("取得 API Key：[Groq Console](https://console.groq.com/)")

st.title("💳 AI 信用卡推薦助手")
st.caption("根據您的消費習慣，推薦最適合的信用卡")

# --- 消費類型與金額 ---
st.subheader("📊 每月消費分布")

col1, col2 = st.columns(2)
with col1:
    dining = st.number_input("🍽️ 餐飲（元/月）", min_value=0, value=3000, step=500)
    transport = st.number_input("🚗 交通（元/月）", min_value=0, value=2000, step=500)
    online = st.number_input("🛒 網購（元/月）", min_value=0, value=2000, step=500)
with col2:
    travel = st.number_input("✈️ 旅遊（元/月）", min_value=0, value=1000, step=500)
    grocery = st.number_input("🛍️ 超市/量販（元/月）", min_value=0, value=2000, step=500)
    other = st.number_input("📦 其他（元/月）", min_value=0, value=1000, step=500)

total = dining + transport + online + travel + grocery + other
st.metric("💰 每月總消費", f"NT$ {total:,}")

# --- 偏好 ---
st.subheader("🎯 回饋偏好")
col3, col4 = st.columns(2)
with col3:
    reward_type = st.selectbox("偏好回饋類型", ["現金回饋", "點數/哩程", "都可以"])
with col4:
    annual_fee = st.selectbox("年費接受度", ["免年費", "可接受年費（有好回饋）", "不在意"])

extra = st.multiselect(
    "其他需求",
    ["機場貴賓室", "旅遊險", "高鐵/台鐵優惠", "電影優惠", "行動支付加碼", "海外消費回饋"],
)

if st.button("🔍 推薦信用卡", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    else:
        extra_str = "、".join(extra) if extra else "無"
        prompt = (
            f"你是台灣信用卡理財專家。根據以下消費習慣推薦最適合的信用卡：\n\n"
            f"每月消費：\n"
            f"- 餐飲：NT${dining:,}\n- 交通：NT${transport:,}\n- 網購：NT${online:,}\n"
            f"- 旅遊：NT${travel:,}\n- 超市/量販：NT${grocery:,}\n- 其他：NT${other:,}\n"
            f"- 總計：NT${total:,}\n\n"
            f"偏好回饋：{reward_type}\n年費接受度：{annual_fee}\n其他需求：{extra_str}\n\n"
            "請推薦 3-5 張最適合的台灣信用卡，每張卡請說明：\n"
            "1. **卡片名稱**（銀行+卡名）\n"
            "2. **核心回饋**：主要的回饋機制\n"
            "3. **適合原因**：為什麼適合這個消費模式\n"
            "4. **預估每月回饋金額**\n"
            "5. **注意事項**：回饋上限、排除項目等\n\n"
            "最後請給一個綜合建議，說明如何搭配使用這些卡片來最大化回饋。"
        )

        try:
            client = Groq(api_key=api_key)
            with st.spinner("AI 正在分析最佳信用卡組合..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是台灣信用卡理財專家，熟悉各家銀行信用卡的回饋方案。請用繁體中文提供實用建議。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.5,
                    max_tokens=2048,
                )
            result = response.choices[0].message.content
            st.markdown("---")
            st.subheader("💳 推薦信用卡方案")
            st.markdown(result)
            st.info("💡 信用卡優惠方案可能隨時異動，申辦前請至各銀行官網確認最新資訊。")
        except Exception as e:
            st.error(f"發生錯誤：{e}")
