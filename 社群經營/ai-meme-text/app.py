import streamlit as st
from groq import Groq

# --- 頁面設定 ---
st.set_page_config(page_title="AI 迷因文字產生器", page_icon="😂", layout="centered")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("使用 **Llama 3.3 70B** 模型")
    st.markdown("輸入情境，AI 幫你產生迷因上下文字！")

# --- 主頁面 ---
st.title("😂 AI 迷因文字產生器")
st.markdown("輸入一個情境描述，AI 會幫你產生適合各種迷因模板的上下文字！")

# --- 迷因模板選擇 ---
meme_templates = {
    "Drake 偏好梗": "Drake 左邊不要、右邊要的格式",
    "分心男友": "男友回頭看路人，女友不爽的三人格式",
    "災難女孩": "前面微笑、後面著火的格式",
    "兩個按鈕": "面對兩個按鈕猶豫不決的格式",
    "腦袋越來越大": "從小腦到大腦，想法越來越荒謬的格式",
    "改變我的想法": "坐在桌前說『改變我的想法』的格式",
    "This is fine 狗": "房間著火但狗說沒事的格式",
    "蜘蛛人指對方": "兩個蜘蛛人互指的格式",
}

template = st.selectbox("🎭 選擇迷因模板", list(meme_templates.keys()))
situation = st.text_area(
    "📝 描述你的情境",
    placeholder="例如：期末考前一天還在追劇、老闆說今天可以準時下班結果...",
    height=100,
)

if st.button("🚀 產生迷因文字", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key！")
    elif not situation.strip():
        st.error("請輸入情境描述！")
    else:
        try:
            client = Groq(api_key=api_key)
            prompt = f"""你是一個迷因文字產生器專家。請根據以下資訊產生迷因文字。

迷因模板：{template}（{meme_templates[template]}）
情境描述：{situation}

請產生適合這個迷因模板的文字，包含：
1. 上方文字（Top Text）
2. 下方文字（Bottom Text）
3. 如果模板有多個面板，請為每個面板產生對應文字

請提供 3 個不同版本的迷因文字，從溫和到爆笑。
用繁體中文回答，文字要簡短有力、有梗。
每個版本請標示版本編號和搞笑程度（⭐ 到 ⭐⭐⭐）。"""

            with st.spinner("🧠 AI 正在想梗中..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是一個專業的迷因文字創作者，擅長用繁體中文創作有趣的迷因。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.9,
                    max_tokens=1024,
                )
            result = response.choices[0].message.content
            st.markdown("---")
            st.subheader(f"🎉 {template} 迷因文字")
            st.markdown(result)

            st.markdown("---")
            st.info("💡 小提示：複製文字後，到迷因產生器網站貼上即可製作迷因圖片！")

        except Exception as e:
            st.error(f"發生錯誤：{e}")

# --- 頁尾 ---
st.markdown("---")
st.caption("AI 迷因文字產生器 — 用 AI 讓你的迷因更有梗 😂")
