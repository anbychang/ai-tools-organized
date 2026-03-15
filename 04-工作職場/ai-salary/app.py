import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 薪水談判", page_icon="💰")
st.title("💰 AI 薪水談判教練")
st.subheader("用 AI 準備你的薪資談判策略與話術")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    st.markdown("### 使用說明")
    st.markdown("1. 輸入 Groq API Key\n2. 填寫薪資與職位資訊\n3. 取得談判策略")

# 主要內容
st.markdown("### 📊 基本資訊")
col1, col2 = st.columns(2)
with col1:
    current_salary = st.number_input("目前月薪（萬元）", min_value=0.0, max_value=100.0, value=4.0, step=0.5)
    expected_salary = st.number_input("期望月薪（萬元）", min_value=0.0, max_value=100.0, value=5.0, step=0.5)
    experience_years = st.selectbox("工作年資", ["應屆畢業", "1-2 年", "3-5 年", "5-8 年", "8-12 年", "12 年以上"])
with col2:
    position = st.text_input("職位名稱", placeholder="例如：資深前端工程師")
    industry = st.selectbox("產業", ["科技業", "金融業", "製造業", "零售業", "醫療業", "顧問業", "新創", "其他"])
    scenario = st.selectbox("談判情境", ["新工作 Offer", "年度調薪", "升職加薪", "跳槽談判", "試用期轉正"])

st.markdown("### 💪 你的優勢")
strengths = st.text_area(
    "列出你的優勢與成就",
    placeholder="例如：\n- 帶領團隊完成重要專案\n- 擁有 AWS 證照\n- 年度績效 A+\n- 有其他公司 Offer",
    height=120
)

has_other_offer = st.checkbox("手上有其他公司的 Offer")
if has_other_offer:
    other_offer = st.text_input("其他 Offer 的薪資與公司（選填）", placeholder="例如：某科技公司月薪 5.5 萬")
else:
    other_offer = ""

if st.button("🎯 產生談判策略", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key！")
    elif not position:
        st.warning("請輸入職位名稱！")
    else:
        increase_pct = ((expected_salary - current_salary) / current_salary * 100) if current_salary > 0 else 0

        prompt = f"""你是一位資深的薪資談判教練與人力資源專家。請根據以下資訊，提供完整的薪資談判策略。

目前月薪：{current_salary} 萬元
期望月薪：{expected_salary} 萬元（漲幅約 {increase_pct:.0f}%）
職位：{position}
產業：{industry}
年資：{experience_years}
談判情境：{scenario}
個人優勢：{strengths if strengths else '未提供'}
其他 Offer：{other_offer if other_offer else '無'}

請用繁體中文回答，提供：

1. **📊 市場行情分析** - 這個職位在台灣的薪資範圍參考
2. **🎯 談判策略** - 整體談判方針與節奏建議
3. **💬 開場話術** - 具體的開口方式（給 2-3 種版本）
4. **🔄 應對話術** - 當對方說「預算不夠」「你經驗不足」等常見回應的反駁話術
5. **📈 加碼技巧** - 除了底薪，還能談什麼（年終、股票、福利等）
6. **⚠️ 地雷提醒** - 談判中絕對不能說的話
7. **📝 談判劇本** - 模擬一段完整的談判對話
8. **🏆 最佳/最差結果** - 設定你的 BATNA（最佳替代方案）

請給出實用、具體、可直接使用的建議。"""

        try:
            client = Groq(api_key=api_key)
            with st.spinner("正在制定談判策略..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=4096,
                )
            st.markdown("---")
            st.markdown("### 🎯 你的薪資談判策略")
            st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"發生錯誤：{e}")
