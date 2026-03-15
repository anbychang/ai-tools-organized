import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 期末猜題", page_icon="🎯")

# --- 側邊欄 ---
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    st.markdown("輸入課程資訊，AI 預測可能的考題")

st.title("🎯 AI 期末猜題")
st.markdown("輸入課程名稱與大綱，AI 預測可能的期末考題並提供建議答案。")

# --- 課程資訊 ---
course_name = st.text_input("課程名稱", placeholder="例如：普通物理學（一）")

syllabus = st.text_area(
    "課程大綱 / 章節內容",
    height=200,
    placeholder="例如：\n第1章 運動學\n第2章 牛頓運動定律\n第3章 功與能量\n第4章 動量與碰撞\n或貼上課程大綱...",
)

col1, col2 = st.columns(2)
with col1:
    exam_type = st.selectbox("考試類型", ["期中考", "期末考", "小考", "模擬考"])
with col2:
    question_count = st.selectbox("預測題數", ["5題", "10題", "15題", "20題"])

question_types = st.multiselect(
    "題目類型",
    ["選擇題", "填充題", "簡答題", "計算題", "申論題", "名詞解釋"],
    default=["選擇題", "簡答題"],
)

extra_info = st.text_area(
    "額外資訊（選填）",
    height=80,
    placeholder="例如：老師上課強調過的重點、往年考題方向、老師風格等",
)

def predict_exam(api_key: str, course_name: str, syllabus: str, exam_type: str,
                 question_count: str, question_types: list, extra_info: str) -> str:
    client = Groq(api_key=api_key)
    types_str = "、".join(question_types) if question_types else "混合題型"

    prompt = f"""你是一位資深大學教授，擅長出考題。請根據以下課程資訊，預測最可能出現的{exam_type}題目。

## 課程資訊
- 課程名稱：{course_name}
- 考試類型：{exam_type}
- 課程大綱：
{syllabus}
- 額外資訊：{extra_info if extra_info.strip() else '無'}

## 要求
- 預測 {question_count}
- 題目類型：{types_str}
- 每題都要附上建議答案和解題思路

## 回覆格式

### 考前重點提醒
（列出最可能考的核心概念）

### 預測考題

**第 N 題**（題型：XXX）
題目：...
建議答案：...
解題思路：...
考點分析：為什麼這題可能會考？

---

### 讀書建議
（針對這些預測考題，給出讀書優先順序建議）

請用繁體中文回覆。"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "你是資深大學教授，擅長分析考試方向並預測考題，請用繁體中文回覆。"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=4096,
    )
    return response.choices[0].message.content

# --- 猜題按鈕 ---
if st.button("開始猜題", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not course_name.strip():
        st.warning("請輸入課程名稱。")
    elif not syllabus.strip():
        st.warning("請輸入課程大綱或章節內容。")
    else:
        with st.spinner("AI 正在分析課程內容並預測考題..."):
            try:
                result = predict_exam(
                    api_key, course_name, syllabus, exam_type,
                    question_count, question_types, extra_info,
                )
                st.markdown("---")
                st.subheader(f"《{course_name}》{exam_type}預測")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
