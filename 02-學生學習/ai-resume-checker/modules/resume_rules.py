"""
Rule-based pre-checks for resume content.
Detects common issues before sending to AI.
"""

import re
from dataclasses import dataclass, field


@dataclass
class RuleCheckResult:
    """Result of rule-based resume pre-check."""
    issues: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    passed: list[str] = field(default_factory=list)
    score_penalty: int = 0  # total penalty points to subtract


def check_length(text: str) -> tuple[list[str], list[str], list[str], int]:
    issues, warnings, passed = [], [], []
    char_count = len(text.strip())
    if char_count < 100:
        issues.append(f"履歷內容過短（僅 {char_count} 字），建議至少 300 字以上")
        return issues, warnings, passed, 20
    if char_count < 300:
        warnings.append(f"履歷內容偏短（{char_count} 字），建議補充更多細節")
        return issues, warnings, passed, 10
    if char_count >= 500:
        passed.append(f"履歷長度充足（{char_count} 字）")
    return issues, warnings, passed, 0


def check_metrics(text: str) -> tuple[list[str], list[str], list[str], int]:
    """Check if resume contains quantifiable metrics / numbers."""
    issues, warnings, passed = [], [], []
    number_pattern = re.compile(r'\d+[%％萬億千百]|\d+\s*(?:人|位|個|件|次|年|月|專案|項)')
    matches = number_pattern.findall(text)
    if len(matches) == 0:
        issues.append("未偵測到任何量化數據（如百分比、人數、金額），建議加入具體成果數字")
        return issues, warnings, passed, 15
    if len(matches) < 3:
        warnings.append(f"量化數據偏少（僅找到 {len(matches)} 處），建議多用數字展示成果")
        return issues, warnings, passed, 5
    passed.append(f"包含充足的量化數據（{len(matches)} 處）")
    return issues, warnings, passed, 0


def check_contact_info(text: str) -> tuple[list[str], list[str], list[str], int]:
    """Check for contact information (email, phone)."""
    issues, warnings, passed = [], [], []
    has_email = bool(re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text))
    has_phone = bool(re.search(r'09\d{2}[-\s]?\d{3}[-\s]?\d{3}|\+?\d{1,3}[-\s]?\d{3,4}[-\s]?\d{3,4}[-\s]?\d{0,4}', text))

    if not has_email and not has_phone:
        issues.append("未偵測到聯絡資訊（Email 或電話），請確認是否已附上")
        return issues, warnings, passed, 10
    found = []
    if has_email:
        found.append("Email")
    if has_phone:
        found.append("電話")
    if not has_email or not has_phone:
        missing = "Email" if not has_email else "電話"
        warnings.append(f"僅偵測到 {', '.join(found)}，建議同時附上{missing}")
        return issues, warnings, passed, 3
    passed.append("聯絡資訊完整（Email + 電話）")
    return issues, warnings, passed, 0


def check_section_keywords(text: str) -> tuple[list[str], list[str], list[str], int]:
    """Check for common resume section keywords."""
    issues, warnings, passed = [], [], []
    sections = {
        "工作經歷": ["工作經歷", "工作經驗", "經歷", "任職", "職務"],
        "學歷": ["學歷", "教育", "畢業", "大學", "碩士", "博士", "學士"],
        "技能": ["技能", "專長", "能力", "技術", "工具"],
    }
    found_sections = []
    missing_sections = []
    for section_name, keywords in sections.items():
        if any(kw in text for kw in keywords):
            found_sections.append(section_name)
        else:
            missing_sections.append(section_name)

    if len(missing_sections) >= 3:
        issues.append(f"缺少關鍵段落：{', '.join(missing_sections)}")
        return issues, warnings, passed, 15
    if missing_sections:
        warnings.append(f"可能缺少段落：{', '.join(missing_sections)}（建議補充）")
        return issues, warnings, passed, 5
    passed.append(f"段落結構完整（{', '.join(found_sections)}）")
    return issues, warnings, passed, 0


def check_typo_patterns(text: str) -> tuple[list[str], list[str], list[str], int]:
    """Check for common typo patterns in Chinese resumes."""
    issues, warnings, passed = [], [], []
    typo_map = {
        "的的": "重複「的」字",
        "了了": "重複「了」字",
        "是是": "重複「是」字",
        "我我": "重複「我」字",
        "在在": "重複「在」字",
        "負責人負責": "疑似重複文字",
    }
    found_typos = []
    penalty = 0
    for pattern, desc in typo_map.items():
        if pattern in text:
            found_typos.append(desc)

    # Check for excessive use of first person
    first_person_count = text.count("我")
    if first_person_count > 10:
        warnings.append(f"「我」字出現 {first_person_count} 次，建議減少第一人稱，改用更專業的敘述方式")
        penalty += 2

    if found_typos:
        warnings.append(f"偵測到可能的筆誤：{', '.join(found_typos)}")
        penalty += 3
    else:
        passed.append("未偵測到明顯筆誤")
    return issues, warnings, passed, penalty


def check_action_verbs(text: str) -> tuple[list[str], list[str], list[str], int]:
    """Check for strong action verbs."""
    issues, warnings, passed = [], [], []
    strong_verbs = [
        "主導", "帶領", "建立", "開發", "設計", "優化", "提升", "推動",
        "執行", "規劃", "管理", "分析", "導入", "整合", "達成", "創建",
        "改善", "實現", "負責", "協調", "策劃", "統籌",
    ]
    found_verbs = [v for v in strong_verbs if v in text]
    if len(found_verbs) == 0:
        warnings.append("缺少強力動詞（如「主導」「優化」「提升」），建議使用行動導向的敘述")
        return issues, warnings, passed, 5
    if len(found_verbs) >= 3:
        passed.append(f"使用了良好的行動動詞（如：{', '.join(found_verbs[:5])}）")
    return issues, warnings, passed, 0


def run_all_checks(text: str) -> RuleCheckResult:
    """Run all rule-based checks and aggregate results."""
    result = RuleCheckResult()
    checks = [
        check_length,
        check_metrics,
        check_contact_info,
        check_section_keywords,
        check_typo_patterns,
        check_action_verbs,
    ]
    for check_fn in checks:
        issues, warnings, passed, penalty = check_fn(text)
        result.issues.extend(issues)
        result.warnings.extend(warnings)
        result.passed.extend(passed)
        result.score_penalty += penalty
    return result
