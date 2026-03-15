import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 遲到藉口", page_icon="⏰")
st.title("⏰ AI 遲到藉口產生器")
st.subheader("遲到了？讓 AI 幫你想個好理由！")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    st.markdown("### 使用說明")
    st.markdown("1. 輸入 Groq API Key\n2. 選擇遲到情境\n3. 取得完美藉口")
    st.divider()
    st.caption("⚠️ 本工具僅供娛樂，建議還是準時比較好 😉")

# 主要內容
col1, col2 = st.columns(2)
with col1:
    late_level = st.selectbox("⏱️ 遲到程度", ["10 分鐘以內", "10-30 分鐘", "30 分鐘 - 1 小時", "1 小時以上", "整個遲到沒去"])
    occasion = st.selectbox("📍 遲到場合", ["上班", "約會", "上課", "朋友聚會", "家庭聚餐", "面試", "重要會議"])
with col2:
    boss_type = st.selectbox("👤 對象個性", ["嚴格認真", "隨和好說話", "愛開玩笑", "不太熟", "很在意守時"])
    excuse_style = st.selectbox("🎭 藉口風格", ["合理可信", "搞笑誇張", "感人肺腑", "技術性拖延", "半真半假"])

real_reason = st.text_input("🤫 真正遲到的原因（選填，AI 不會告訴別人）", placeholder="例如：睡過頭、打電動...")

if st.button("💡 產生藉口", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key！")
    else:
        prompt = f"""你是一位「藉口創意大師」，擅長想出讓人信服的遲到理由。請根據以下情境產生藉口。

遲到程度：{late_level}
場合：{occasion}
對象個性：{boss_type}
藉口風格：{excuse_style}
真正原因：{real_reason if real_reason else '不明'}

請用繁體中文回答，提供：

1. **🥇 最佳藉口** - 一個完整的遲到說詞（包含表情和語氣建議）
2. **🎭 表演指導** - 說這個藉口時的表情、語氣、肢體語言
3. **❓ 可能被追問的問題** - 對方可能會問什麼，以及你該怎麼回答
4. **🥈 備用藉口 x2** - 再給兩個不同風格的備用方案
5. **💯 可信度評分** - 每個藉口的可信度（1-10分）
6. **⚠️ 注意事項** - 使用這個藉口要注意什麼，避免穿幫

語氣請幽默有趣！"""

        try:
            client = Groq(api_key=api_key)
            with st.spinner("正在編造...不是，正在構思完美理由..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=1.0,
                    max_tokens=3000,
                )
            st.markdown("---")
            st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"發生錯誤：{e}")
