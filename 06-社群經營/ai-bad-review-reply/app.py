import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 負評回覆助手", page_icon="⭐", layout="centered")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("取得 API Key：[Groq Console](https://console.groq.com/)")

st.title("⭐ AI 負評回覆助手")
st.caption("專業回覆負面評價，化危機為轉機")

# --- 負評內容 ---
review = st.text_area(
    "📩 負評內容",
    height=150,
    placeholder="貼上您收到的負面評價...",
)

# --- 商家設定 ---
col1, col2 = st.columns(2)
with col1:
    biz_type = st.selectbox(
        "🏪 商家類型",
        ["餐廳/餐飲", "民宿/旅館", "網路商店", "美容/美髮", "診所/醫療", "教育/補習班", "其他服務業"],
    )
    biz_name = st.text_input("🏷️ 商家名稱（選填）", placeholder="例如：小確幸咖啡廳")
with col2:
    platform = st.selectbox(
        "📱 評價平台",
        ["Google 評論", "Facebook", "Foodpanda", "UberEats", "Booking.com", "蝦皮", "其他"],
    )
    star_rating = st.selectbox("⭐ 評分", ["1 星", "2 星", "3 星"])

# --- 回覆偏好 ---
st.subheader("🎯 回覆策略")
is_valid = st.radio(
    "這則負評的情況是？",
    ["客人說的有道理，我們確實有疏失", "部分屬實但有誇大", "不實指控/惡意負評"],
    horizontal=True,
)

compensation = st.checkbox("願意提供補償方案（折扣/退款/招待）", value=False)

if st.button("✍️ 產生專業回覆", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not review.strip():
        st.error("請輸入負評內容。")
    else:
        comp_note = "商家願意提供適當補償（如折扣、退款或招待），請在回覆中自然帶入。" if compensation else "暫不提供補償方案。"
        prompt = (
            f"你是專業的商家公關顧問，擅長處理負面評價。\n\n"
            f"負評內容：\n「{review}」\n\n"
            f"商家類型：{biz_type}\n"
            f"商家名稱：{biz_name if biz_name else '未提供'}\n"
            f"評價平台：{platform}\n"
            f"評分：{star_rating}\n"
            f"情況判斷：{is_valid}\n"
            f"補償意願：{comp_note}\n\n"
            "請產生 2 則不同風格的專業回覆，遵循以下原則：\n"
            "1. **先表達感謝與歉意**：感謝顧客的回饋\n"
            "2. **正面回應問題**：針對具體問題說明改善方式\n"
            "3. **展現誠意**：讓其他潛在顧客看到商家的態度\n"
            "4. **邀請再次光臨**：適當邀請對方給予再次體驗的機會\n"
            "5. **不要攻擊或反駁**：即使負評不合理也要保持風度\n"
            "6. **長度適中**：不要太長（3-5 段為宜）\n\n"
            "每則回覆請標註風格（例如：誠懇型、積極改善型等）。\n"
            "請用繁體中文撰寫。"
        )

        try:
            client = Groq(api_key=api_key)
            with st.spinner("AI 正在撰寫專業回覆..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是專業的商家公關顧問，擅長處理負面評價。請用繁體中文撰寫有溫度又專業的回覆。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.6,
                    max_tokens=1536,
                )
            result = response.choices[0].message.content
            st.markdown("---")
            st.subheader("✍️ 專業回覆建議")
            st.markdown(result)

            st.markdown("---")
            st.info(
                "💡 **回覆負評小技巧**\n"
                "- 盡量在 24 小時內回覆\n"
                "- 回覆是給所有潛在顧客看的，展現專業態度很重要\n"
                "- 避免制式化回覆，針對具體問題回應更有誠意"
            )
        except Exception as e:
            st.error(f"發生錯誤：{e}")
