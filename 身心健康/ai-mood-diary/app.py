import streamlit as st
import json
from groq import Groq

st.set_page_config(page_title="AI 心情日記", page_icon="📔")
st.title("📔 AI 心情日記分析")

with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    st.markdown("寫下你的日記，AI 會分析你的情緒狀態並給予支持。")

if "mood_result" not in st.session_state:
    st.session_state.mood_result = None

st.subheader("✏️ 今天過得如何？")
diary_entry = st.text_area("寫下你的日記...", placeholder="今天發生了什麼事？你的感受如何？", height=200)

if st.button("🔍 分析情緒", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key。")
    elif not diary_entry or len(diary_entry) < 10:
        st.warning("請寫多一點內容，讓 AI 更好地理解你的心情。")
    else:
        client = Groq(api_key=api_key)
        prompt = f"""分析以下日記的情緒。請以 JSON 格式回覆，不要有其他文字。

日記內容：
{diary_entry}

回覆格式（百分比總和必須為 100）：
{{
  "emotions": {{
    "喜悅": 數字,
    "悲傷": 數字,
    "憤怒": 數字,
    "焦慮": 數字,
    "平靜": 數字
  }},
  "main_emotion": "主要情緒名稱",
  "summary": "一句話概括今天的心情",
  "feedback": "200字以內的溫暖支持性回饋，像一個好朋友一樣給予鼓勵和建議"
}}"""

        with st.spinner("正在感受你的心情..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=800,
                )
                content = response.choices[0].message.content
                # Extract JSON from response
                start = content.find("{")
                end = content.rfind("}") + 1
                if start != -1 and end > start:
                    st.session_state.mood_result = json.loads(content[start:end])
                else:
                    st.error("AI 回覆格式異常，請重試。")
            except json.JSONDecodeError:
                st.error("情緒分析結果解析失敗，請重試。")
            except Exception as e:
                st.error(f"發生錯誤：{e}")

if st.session_state.mood_result:
    result = st.session_state.mood_result
    st.markdown("---")

    st.subheader(f"🎭 主要情緒：{result.get('main_emotion', '未知')}")
    st.caption(result.get("summary", ""))

    st.markdown("### 📊 情緒分佈")
    emoji_map = {"喜悅": "😊", "悲傷": "😢", "憤怒": "😠", "焦慮": "😰", "平靜": "😌"}
    emotions = result.get("emotions", {})
    for emotion, value in emotions.items():
        emoji = emoji_map.get(emotion, "")
        col1, col2, col3 = st.columns([2, 6, 1])
        with col1:
            st.write(f"{emoji} {emotion}")
        with col2:
            st.progress(min(value, 100) / 100)
        with col3:
            st.write(f"{value}%")

    st.markdown("### 💌 給你的話")
    st.info(result.get("feedback", ""))
