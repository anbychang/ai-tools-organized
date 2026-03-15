"""
AI 履歷健檢 - Streamlit App
Paste your resume text, AI scores it and gives improvement suggestions.
"""

import json
import re
import streamlit as st
from groq import Groq

from modules.resume_rules import run_all_checks

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI 履歷健檢",
    page_icon="📄",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    .score-gauge {
        text-align: center;
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
    }
    .score-number {
        font-size: 4rem;
        font-weight: 800;
        line-height: 1;
    }
    .score-label {
        font-size: 1.1rem;
        margin-top: 0.3rem;
    }
    .section-card {
        padding: 1rem 1.2rem;
        border-radius: 0.6rem;
        margin-bottom: 0.6rem;
        border-left: 5px solid;
    }
    .section-green  { background: #e8f5e9; border-color: #43a047; }
    .section-yellow { background: #fff8e1; border-color: #f9a825; }
    .section-red    { background: #ffebee; border-color: #e53935; }
    .section-score  { font-size: 1.4rem; font-weight: 700; }
    .rule-issue   { color: #c62828; }
    .rule-warning { color: #e65100; }
    .rule-pass    { color: #2e7d32; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", help="請前往 https://console.groq.com 取得 API Key")
    job_type = st.selectbox("目標職位類型", ["軟體工程師", "行銷企劃", "設計師", "業務", "通用"])
    st.divider()
    st.caption("模型：llama-3.3-70b-versatile（Groq）")
    st.caption("此工具僅供參考，不取代專業人資意見。")

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("📄 AI 履歷健檢")
st.markdown("貼上你的履歷內容，AI 幫你評分並提供改善建議。")

# ---------------------------------------------------------------------------
# Main input
# ---------------------------------------------------------------------------
resume_text = st.text_area(
    "請貼上履歷內容",
    height=300,
    placeholder="將你的履歷文字內容貼在這裡...",
)

analyze_btn = st.button("🔍 開始分析", type="primary", use_container_width=True)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def score_color(score: int) -> str:
    if score >= 70:
        return "green"
    if score >= 40:
        return "yellow"
    return "red"


def score_bg(score: int) -> str:
    if score >= 70:
        return "#e8f5e9"
    if score >= 40:
        return "#fff8e1"
    return "#ffebee"


def score_fg(score: int) -> str:
    if score >= 70:
        return "#2e7d32"
    if score >= 40:
        return "#e65100"
    return "#c62828"


def score_label(score: int) -> str:
    if score >= 90:
        return "優秀"
    if score >= 70:
        return "良好"
    if score >= 50:
        return "普通"
    if score >= 30:
        return "待加強"
    return "需大幅改善"


def render_score_gauge(score: int):
    bg = score_bg(score)
    fg = score_fg(score)
    label = score_label(score)
    st.markdown(
        f"""
        <div class="score-gauge" style="background:{bg};">
            <div class="score-number" style="color:{fg};">{score}</div>
            <div class="score-label" style="color:{fg};">總分（滿分 100） — {label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_score(name: str, score: int):
    css_class = f"section-{score_color(score)}"
    fg = score_fg(score)
    st.markdown(
        f"""
        <div class="section-card {css_class}">
            <span class="section-score" style="color:{fg};">{score}</span>
            <span style="margin-left:0.6rem;font-weight:600;">{name}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_prompt(resume: str, job: str) -> str:
    return f"""你是一位專業的履歷顧問，專精繁體中文履歷撰寫與優化。
請針對以下履歷內容進行深度分析，目標職位類型為「{job}」。

請以 **JSON 格式** 回覆，結構如下（請嚴格遵守此格式，不要加任何 markdown 或額外文字）：
{{
  "overall_score": 75,
  "section_scores": {{
    "工作經歷": 70,
    "技能": 80,
    "學歷": 60,
    "排版建議": 65
  }},
  "strengths": [
    "優點一",
    "優點二"
  ],
  "weaknesses": [
    "缺點一",
    "缺點二"
  ],
  "improvement_suggestions": [
    "具體建議一",
    "具體建議二",
    "具體建議三"
  ],
  "rewritten_examples": [
    {{
      "original": "原句",
      "improved": "改寫後的句子",
      "reason": "改寫原因"
    }}
  ]
}}

評分標準：
- 工作經歷（0-100）：是否有量化成果、行動動詞、與目標職位的相關性
- 技能（0-100）：技能清單是否完整、是否與職位匹配
- 學歷（0-100）：是否清楚列出、是否有相關補充（證照/課程）
- 排版建議（0-100）：結構是否清晰、段落是否合理、有無多餘資訊

請提供至少 3 條優點、3 條缺點、5 條具體改善建議、3 組改寫範例。

以下是待分析的履歷內容：
---
{resume}
---"""


def call_groq(api_key: str, prompt: str) -> dict | None:
    """Call Groq API and parse the JSON response."""
    client = Groq(api_key=api_key)
    chat_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "你是專業履歷顧問。請只回覆純 JSON，不要加 markdown code block 或任何其他文字。",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=4096,
    )
    raw = chat_completion.choices[0].message.content.strip()
    # Strip markdown code fences if present
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)


# ---------------------------------------------------------------------------
# Analysis flow
# ---------------------------------------------------------------------------
if analyze_btn:
    if not resume_text.strip():
        st.warning("請先貼上履歷內容。")
        st.stop()

    # ---- Rule-based pre-check (no API key needed) ----------------------------
    st.subheader("📋 基本檢查（規則偵測）")
    rule_result = run_all_checks(resume_text)

    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        if rule_result.issues:
            for item in rule_result.issues:
                st.markdown(f"<p class='rule-issue'>❌ {item}</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p class='rule-pass'>✅ 未發現嚴重問題</p>", unsafe_allow_html=True)
    with col_r2:
        if rule_result.warnings:
            for item in rule_result.warnings:
                st.markdown(f"<p class='rule-warning'>⚠️ {item}</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p class='rule-pass'>✅ 無警告</p>", unsafe_allow_html=True)
    with col_r3:
        if rule_result.passed:
            for item in rule_result.passed:
                st.markdown(f"<p class='rule-pass'>✅ {item}</p>", unsafe_allow_html=True)

    if rule_result.score_penalty:
        st.info(f"規則檢查扣分：-{rule_result.score_penalty} 分（將反映在 AI 總分建議中供參考）")

    st.divider()

    # ---- AI Analysis (requires API key) --------------------------------------
    if not api_key.strip():
        st.warning("請在左側欄輸入 Groq API Key 以啟用 AI 深度分析。")
        st.stop()

    st.subheader("🤖 AI 深度分析")
    with st.spinner("AI 正在分析你的履歷，請稍候..."):
        try:
            prompt = build_prompt(resume_text, job_type)
            data = call_groq(api_key, prompt)
        except json.JSONDecodeError:
            st.error("AI 回傳格式異常，請重新嘗試。")
            st.stop()
        except Exception as e:
            st.error(f"呼叫 Groq API 失敗：{e}")
            st.stop()

    if not data:
        st.error("未取得分析結果。")
        st.stop()

    # ---- Overall score -------------------------------------------------------
    overall = max(0, min(100, data.get("overall_score", 0)))
    render_score_gauge(overall)

    # ---- Section scores ------------------------------------------------------
    st.markdown("#### 各項評分")
    section_scores = data.get("section_scores", {})
    cols = st.columns(len(section_scores) if section_scores else 1)
    for idx, (sec_name, sec_score) in enumerate(section_scores.items()):
        with cols[idx % len(cols)]:
            render_section_score(sec_name, sec_score)

    st.divider()

    # ---- Strengths & Weaknesses side by side ---------------------------------
    col_s, col_w = st.columns(2)
    with col_s:
        st.markdown("#### 💪 優點")
        for s in data.get("strengths", []):
            st.markdown(f"- {s}")
    with col_w:
        st.markdown("#### 🔍 待改善")
        for w in data.get("weaknesses", []):
            st.markdown(f"- {w}")

    st.divider()

    # ---- Improvement suggestions ---------------------------------------------
    st.markdown("#### 💡 具體改善建議")
    for i, suggestion in enumerate(data.get("improvement_suggestions", []), 1):
        st.markdown(f"**{i}.** {suggestion}")

    st.divider()

    # ---- Rewritten examples --------------------------------------------------
    st.markdown("#### ✏️ 改寫範例")
    for ex in data.get("rewritten_examples", []):
        original = ex.get("original", "")
        improved = ex.get("improved", "")
        reason = ex.get("reason", "")
        with st.expander(f"原句：{original[:50]}{'...' if len(original) > 50 else ''}"):
            st.markdown(f"**原句：** {original}")
            st.markdown(f"**改寫：** {improved}")
            st.markdown(f"**原因：** {reason}")
