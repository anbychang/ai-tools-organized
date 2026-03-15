import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 週報產生器", page_icon="📊")
st.title("📊 AI 週報產生器")
st.subheader("輸入工作重點，AI 幫你產出漂亮的週報")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    department = st.selectbox("🏢 部門", ["工程部", "產品部", "設計部", "行銷部", "業務部", "人資部", "財務部", "客服部", "營運部", "其他"])
    report_style = st.selectbox("📝 週報風格", ["正式詳細", "簡潔扼要", "重點條列"])
    week_date = st.date_input("📅 週報日期")
    st.divider()
    st.markdown("### 使用說明")
    st.markdown("1. 輸入 Groq API Key\n2. 列出本週工作\n3. 產生格式化週報")

# 主要內容
st.markdown("### 📋 本週工作內容")
work_done = st.text_area(
    "列出你本週做了什麼（簡單條列即可）",
    height=200,
    placeholder="例如：\n- 完成首頁改版\n- 修了三個 bug\n- 開了產品需求會議\n- 跟客戶 demo\n- 寫了 API 文件"
)

col1, col2 = st.columns(2)
with col1:
    blockers = st.text_area("🚧 遇到的困難或阻礙（選填）", height=100, placeholder="例如：等後端 API、需求不明確...")
with col2:
    next_week = st.text_area("📅 下週計畫（選填）", height=100, placeholder="例如：上線新功能、準備季度報告...")

col3, col4 = st.columns(2)
with col3:
    achievements = st.text_input("🏆 本週亮點（選填）", placeholder="例如：提前完成專案、客戶好評...")
with col4:
    help_needed = st.text_input("🆘 需要的支援（選填）", placeholder="例如：需要設計支援、需要增加人力...")

if st.button("✨ 產生週報", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key！")
    elif not work_done.strip():
        st.warning("請先列出本週工作內容！")
    else:
        prompt = f"""你是一位擅長撰寫工作週報的專業助手。請根據以下資訊，產生一份格式化的週報。

部門：{department}
週報日期：{week_date}
週報風格：{report_style}

本週工作內容：
{work_done}

遇到的困難：{blockers if blockers.strip() else '無'}
下週計畫：{next_week if next_week.strip() else '未填寫'}
本週亮點：{achievements if achievements else '無'}
需要的支援：{help_needed if help_needed else '無'}

請用繁體中文產生週報，包含以下區塊：

1. **週報標題**（含部門、日期）
2. **本週工作摘要**（一段話總結）
3. **工作項目明細** - 將簡單的條列擴展成完整的工作描述，包含：
   - 項目名稱
   - 進度百分比
   - 完成狀態（已完成/進行中/待處理）
4. **本週亮點與成果**
5. **遭遇問題與解決方案**
6. **下週工作計畫**
7. **需要的資源與支援**

請讓週報看起來專業且有條理，適合直接交給主管。不要過度誇大，但要讓工作成果清楚可見。"""

        try:
            client = Groq(api_key=api_key)
            with st.spinner("正在產生週報..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                    max_tokens=4096,
                )
            st.markdown("---")
            st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"發生錯誤：{e}")
