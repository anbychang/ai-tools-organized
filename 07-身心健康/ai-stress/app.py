import streamlit as st
import json
from groq import Groq

st.set_page_config(page_title="AI 壓力分析", page_icon="🧠")
st.title("🧠 AI 壓力分析師")

with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    st.markdown("描述你的煩惱，AI 會分析壓力來源並提供具體的應對策略。")

if "stress_result" not in st.session_state:
    st.session_state.stress_result = None

st.subheader("💭 說說你的煩惱")
worries = st.text_area(
    "描述讓你感到壓力的事情...",
    placeholder="可以寫工作、人際關係、學業、健康、經濟等任何讓你煩心的事...",
    height=180,
)

if st.button("🔍 分析壓力", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key。")
    elif not worries or len(worries) < 10:
        st.warning("請多描述一些，讓 AI 更了解你的情況。")
    else:
        client = Groq(api_key=api_key)
        prompt = f"""分析以下壓力描述，以 JSON 格式回覆，不要有其他文字。

壓力描述：
{worries}

回覆格式：
{{
  "sources": [
    {{
      "category": "壓力類別（如：工作、人際、學業、健康、經濟、家庭等）",
      "description": "具體壓力描述",
      "severity": 1到10的數字,
      "coping": "針對此壓力的具體應對策略（50字以內）"
    }}
  ],
  "overall_severity": 1到10的數字,
  "overall_assessment": "整體壓力評估（50字以內）",
  "immediate_action": "現在馬上可以做的一件事",
  "long_term_advice": "長期建議（100字以內）",
  "encouragement": "一段溫暖的鼓勵話語（80字以內）"
}}"""

        with st.spinner("正在分析你的壓力狀況..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=1500,
                )
                content = response.choices[0].message.content
                start = content.find("{")
                end = content.rfind("}") + 1
                if start != -1 and end > start:
                    st.session_state.stress_result = json.loads(content[start:end])
                else:
                    st.error("分析結果格式異常，請重試。")
            except json.JSONDecodeError:
                st.error("結果解析失敗，請重試。")
            except Exception as e:
                st.error(f"發生錯誤：{e}")

if st.session_state.stress_result:
    r = st.session_state.stress_result
    st.markdown("---")

    # Overall severity
    severity = r.get("overall_severity", 5)
    color = "🟢" if severity <= 3 else "🟡" if severity <= 6 else "🔴"
    st.subheader(f"{color} 整體壓力指數：{severity}/10")
    st.progress(severity / 10)
    st.caption(r.get("overall_assessment", ""))

    # Stress sources
    st.markdown("### 📋 壓力來源分析")
    for i, src in enumerate(r.get("sources", []), 1):
        with st.expander(f"{'🔴' if src['severity'] > 6 else '🟡' if src['severity'] > 3 else '🟢'} {src['category']}（嚴重度：{src['severity']}/10）"):
            st.write(f"**描述：** {src['description']}")
            st.progress(src["severity"] / 10)
            st.success(f"**應對策略：** {src['coping']}")

    # Actions
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ⚡ 立即行動")
        st.info(r.get("immediate_action", ""))
    with col2:
        st.markdown("### 🌱 長期建議")
        st.info(r.get("long_term_advice", ""))

    st.markdown("### 💪 給你的鼓勵")
    st.success(r.get("encouragement", ""))
