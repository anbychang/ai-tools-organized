import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 選課建議", page_icon="🎓")
st.title("🎓 AI 選課建議")
st.caption("輸入你的興趣、未來方向與成績，AI 為你推薦最適合的課程")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    st.markdown("### 📖 使用說明")
    st.markdown(
        "1. 輸入 Groq API Key\n"
        "2. 填寫個人資料\n"
        "3. 點擊「取得選課建議」"
    )

# 主介面
st.markdown("### 📋 個人資料")

col1, col2 = st.columns(2)
with col1:
    edu_level = st.selectbox("🏫 教育階段", ["大學", "碩士", "高中", "社會人士進修"])
    year = st.selectbox("📅 年級", ["一年級", "二年級", "三年級", "四年級", "不適用"])
with col2:
    department = st.text_input("🏛️ 科系/領域", placeholder="例如：資訊工程系")
    gpa = st.text_input("📊 目前成績概況", placeholder="例如：GPA 3.5 / 班排前 30%")

st.markdown("### 🎯 興趣與方向")

interests = st.text_area(
    "💡 你的興趣（可多項）",
    placeholder="例如：對人工智慧和資料分析很有興趣，也喜歡網頁開發，平常會寫 Python 小專案",
    height=100
)

future_goal = st.text_area(
    "🚀 未來方向/職涯規劃",
    placeholder="例如：希望畢業後當資料科學家，或是到科技公司做後端工程師",
    height=100
)

constraints = st.text_area(
    "⚠️ 限制條件（選填）",
    placeholder="例如：每週最多修 18 學分、不想上太早的課、已修過微積分和線性代數",
    height=80
)

num_courses = st.slider("📚 希望推薦幾門課", min_value=3, max_value=10, value=5)

if st.button("🚀 取得選課建議", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key！")
    elif not interests.strip() or not future_goal.strip():
        st.error("請至少填寫興趣與未來方向！")
    else:
        try:
            client = Groq(api_key=api_key)
            prompt = f"""你是一位經驗豐富的大學選課顧問。請根據以下學生資料，推薦 {num_courses} 門課程。

學生資料：
- 教育階段：{edu_level} {year}
- 科系/領域：{department if department else '未填寫'}
- 成績概況：{gpa if gpa else '未填寫'}
- 興趣：{interests}
- 未來方向：{future_goal}
- 限制條件：{constraints if constraints else '無特殊限制'}

請使用繁體中文，按以下格式推薦：

## 📚 推薦課程清單

每門課程請包含：
1. **課程名稱**
2. **推薦原因**（為什麼適合這位學生）
3. **課程內容簡介**
4. **與未來目標的關聯**
5. **難度評估**（⭐ 1-5 顆星）
6. **修課建議**（先修課程、學習策略等）

## 🗺️ 建議修課順序
（排出建議的修課先後順序與時程規劃）

## 💡 額外建議
（課外學習資源、證照建議等）"""

            with st.spinner("AI 正在分析你的需求並推薦課程..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是專業選課顧問，熟悉各大學課程規劃，回覆使用繁體中文。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,
                    max_tokens=4096,
                )
            result = response.choices[0].message.content
            st.divider()
            st.markdown(result)

        except Exception as e:
            st.error(f"發生錯誤：{e}")
