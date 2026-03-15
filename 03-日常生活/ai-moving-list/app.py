import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 搬家清單", page_icon="📦")
st.title("📦 AI 搬家清單產生器")
st.subheader("根據房型自動產生完整搬家清單與時間規劃")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    st.markdown("### 使用說明")
    st.markdown("1. 輸入 Groq API Key\n2. 選擇房型\n3. 填寫額外資訊\n4. 點擊產生清單")

# 主要內容
room_type = st.selectbox("🏠 選擇房型", ["套房", "兩房一廳", "三房兩廳", "四房以上"])

col1, col2 = st.columns(2)
with col1:
    has_pets = st.checkbox("有寵物")
    has_kids = st.checkbox("有小孩")
with col2:
    has_piano = st.checkbox("有鋼琴/大型家具")
    has_plants = st.checkbox("有植物")

move_date = st.date_input("📅 預計搬家日期")
special_notes = st.text_area("📝 其他特殊需求（選填）", placeholder="例如：有易碎品、需要搬到五樓無電梯...")

if st.button("🚚 產生搬家清單", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key！")
    else:
        extras = []
        if has_pets:
            extras.append("有寵物")
        if has_kids:
            extras.append("有小孩")
        if has_piano:
            extras.append("有鋼琴或大型家具")
        if has_plants:
            extras.append("有植物")
        extra_str = "、".join(extras) if extras else "無"

        prompt = f"""你是一位專業的搬家規劃師。請根據以下資訊，產生一份完整的搬家清單與時間規劃。

房型：{room_type}
搬家日期：{move_date}
特殊條件：{extra_str}
其他需求：{special_notes if special_notes else '無'}

請用繁體中文回答，包含：
1. **搬家前兩週** - 準備工作清單
2. **搬家前一週** - 打包計畫（按房間分類）
3. **搬家前一天** - 最後確認事項
4. **搬家當天** - 流程與注意事項
5. **搬家後一週** - 整理與設定清單
6. **必備物品採購清單** - 紙箱、膠帶等耗材數量建議
7. **預估費用範圍**

請條列式整理，清楚明瞭。"""

        try:
            client = Groq(api_key=api_key)
            with st.spinner("正在產生搬家清單..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=4096,
                )
            st.markdown("---")
            st.markdown("### 📋 你的搬家清單")
            st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"發生錯誤：{e}")
