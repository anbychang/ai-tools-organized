"""GitHub 專案爬蟲 — 自動搜尋有潛力但未完成的專案

用法：
    python github_crawler.py

輸出：results/github_projects.json + results/report.txt

不需要 API token（用 GitHub 公開 API，有速率限制但夠用）
如果有 GitHub token 可以設環境變數 GITHUB_TOKEN 提高速率限制
"""

import json
import os
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path

# ── 設定 ──
RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

GITHUB_API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

# 搜尋關鍵字組合
SEARCH_QUERIES = [
    # 有潛力但被放棄的 AI 專案
    ("abandoned AI tool python", "stars", "desc"),
    ("unmaintained AI project python", "stars", "desc"),
    ("archived AI assistant python", "stars", "desc"),
    ("deprecated AI bot python", "stars", "desc"),
    # WIP / 未完成
    ("WIP machine learning tool", "stars", "desc"),
    ("unfinished python project AI", "stars", "desc"),
    ("incomplete python automation", "stars", "desc"),
    # 有趣但停更的工具
    ("python tool archived NOT fork", "stars", "desc"),
    ("python bot abandoned NOT fork", "stars", "desc"),
    ("python scraper unmaintained", "stars", "desc"),
    ("python game AI abandoned", "stars", "desc"),
    ("python cli tool archived", "stars", "desc"),
    # 特定有趣領域
    ("python music generator abandoned", "stars", "desc"),
    ("python image tool unmaintained", "stars", "desc"),
    ("python chat bot archived", "stars", "desc"),
    ("python productivity tool unmaintained", "stars", "desc"),
    ("python fun project abandoned", "stars", "desc"),
    ("python creative coding archived", "stars", "desc"),
    # 台灣/中文相關
    ("taiwan python tool", "stars", "desc"),
    ("chinese NLP tool python archived", "stars", "desc"),
]

# 額外：按星星數搜尋停更超過 1 年的
STAR_RANGE_QUERIES = [
    "language:python stars:50..300 pushed:<{cutoff}",
    "language:python stars:300..1000 pushed:<{cutoff} topic:ai",
    "language:python stars:100..500 pushed:<{cutoff} topic:tool",
    "language:python stars:50..500 pushed:<{cutoff} topic:bot",
    "language:python stars:50..500 pushed:<{cutoff} topic:game",
    "language:python stars:50..500 pushed:<{cutoff} topic:automation",
    "language:python stars:100..1000 pushed:<{cutoff} topic:nlp",
    "language:python stars:50..300 pushed:<{cutoff} topic:scraper",
    "language:python stars:50..500 pushed:<{cutoff} topic:cli",
    "language:python stars:50..500 pushed:<{cutoff} topic:productivity",
]


def api_request(url: str) -> dict | list | None:
    """發送 GitHub API 請求"""
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitHub-Project-Crawler/1.0",
    }
    if TOKEN:
        headers["Authorization"] = f"token {TOKEN}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 403:
            # 速率限制，等待後重試
            reset_time = e.headers.get("X-RateLimit-Reset")
            if reset_time:
                wait = max(int(reset_time) - int(time.time()), 1)
                print(f"  [速率限制] 等待 {wait} 秒...")
                time.sleep(min(wait + 1, 60))
                return api_request(url)  # 重試
            print(f"  [403] 被限制，等 60 秒...")
            time.sleep(60)
            return api_request(url)
        elif e.code == 422:
            print(f"  [422] 搜尋語法錯誤，跳過")
            return None
        else:
            print(f"  [HTTP {e.code}] {url[:80]}")
            return None
    except Exception as e:
        print(f"  [錯誤] {e}")
        return None


def search_repos(query: str, sort: str = "stars", order: str = "desc", per_page: int = 30) -> list:
    """搜尋 GitHub repos"""
    encoded = urllib.parse.quote(query)
    url = f"{GITHUB_API}/search/repositories?q={encoded}&sort={sort}&order={order}&per_page={per_page}"
    data = api_request(url)
    if data and "items" in data:
        return data["items"]
    return []


def get_repo_details(full_name: str) -> dict | None:
    """取得 repo 詳細資訊"""
    url = f"{GITHUB_API}/repos/{full_name}"
    return api_request(url)


def get_repo_readme(full_name: str) -> str:
    """取得 README 內容（前 500 字）"""
    url = f"{GITHUB_API}/repos/{full_name}/readme"
    data = api_request(url)
    if data and "content" in data:
        import base64
        try:
            content = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
            return content[:1000]
        except Exception:
            pass
    return ""


def is_interesting(repo: dict) -> bool:
    """判斷 repo 是否有趣"""
    stars = repo.get("stargazers_count", 0)
    if stars < 10:
        return False

    # 排除太大的專案（不是我們能完成的）
    size = repo.get("size", 0)
    if size > 100000:  # > 100MB
        return False

    # 排除 fork
    if repo.get("fork", False):
        return False

    # 必須是 Python
    lang = repo.get("language", "")
    if lang and lang.lower() not in ("python", "jupyter notebook"):
        return False

    return True


def calculate_potential_score(repo: dict) -> float:
    """計算專案潛力分數"""
    score = 0.0

    # 星星數（越多越好，但太多的不適合我們完成）
    stars = repo.get("stargazers_count", 0)
    if 50 <= stars <= 200:
        score += 30
    elif 200 < stars <= 500:
        score += 25
    elif 10 <= stars < 50:
        score += 15
    elif stars > 500:
        score += 10

    # 有 issues 代表有人關注
    issues = repo.get("open_issues_count", 0)
    if 1 <= issues <= 20:
        score += 15
    elif issues > 20:
        score += 5

    # 停更時間（6個月-2年最好，代表有做一部分但放棄了）
    pushed = repo.get("pushed_at", "")
    if pushed:
        try:
            last_push = datetime.strptime(pushed[:10], "%Y-%m-%d")
            days_inactive = (datetime.now() - last_push).days
            if 180 <= days_inactive <= 730:
                score += 20
            elif 730 < days_inactive <= 1460:
                score += 10
            elif days_inactive < 180:
                score += 5  # 還算活躍，不太需要我們
        except ValueError:
            pass

    # 有 description 代表作者有想法
    desc = repo.get("description", "") or ""
    if len(desc) > 30:
        score += 10

    # 有 topics 代表有整理
    topics = repo.get("topics", [])
    if topics:
        score += 5

    # Forks（有人嘗試過）
    forks = repo.get("forks_count", 0)
    if 1 <= forks <= 20:
        score += 10
    elif forks > 20:
        score += 5

    # 大小適中
    size = repo.get("size", 0)
    if 10 <= size <= 5000:
        score += 10
    elif 5000 < size <= 50000:
        score += 5

    return score


def main():
    print("=" * 60)
    print("GitHub 專案爬蟲 — 搜尋有潛力的未完成專案")
    print("=" * 60)

    if TOKEN:
        print(f"使用 GitHub Token（速率限制：5000/小時）")
    else:
        print(f"未設定 Token（速率限制：10/分鐘，會比較慢）")
        print(f"設定方式：set GITHUB_TOKEN=你的token")

    all_repos = {}  # full_name -> repo data

    # 1. 關鍵字搜尋
    print(f"\n[階段 1] 關鍵字搜尋（{len(SEARCH_QUERIES)} 組）")
    for i, (query, sort, order) in enumerate(SEARCH_QUERIES):
        print(f"  ({i+1}/{len(SEARCH_QUERIES)}) 搜尋: {query[:50]}...")
        repos = search_repos(query, sort, order, per_page=20)
        for repo in repos:
            if is_interesting(repo):
                all_repos[repo["full_name"]] = repo
        print(f"    找到 {len(repos)} 個，累計有趣的: {len(all_repos)}")

        # 避免觸發速率限制
        if not TOKEN:
            time.sleep(8)
        else:
            time.sleep(1)

    # 2. 按星星數+停更時間搜尋
    cutoff = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    print(f"\n[階段 2] 搜尋停更超過 1 年的專案（截止日: {cutoff}）")
    for i, query_template in enumerate(STAR_RANGE_QUERIES):
        query = query_template.format(cutoff=cutoff)
        print(f"  ({i+1}/{len(STAR_RANGE_QUERIES)}) 搜尋: {query[:60]}...")
        repos = search_repos(query, "stars", "desc", per_page=20)
        for repo in repos:
            if is_interesting(repo):
                all_repos[repo["full_name"]] = repo
        print(f"    找到 {len(repos)} 個，累計有趣的: {len(all_repos)}")

        if not TOKEN:
            time.sleep(8)
        else:
            time.sleep(1)

    # 3. 計算分數並排序
    print(f"\n[階段 3] 分析 {len(all_repos)} 個專案...")
    scored_repos = []
    for full_name, repo in all_repos.items():
        score = calculate_potential_score(repo)
        scored_repos.append({
            "name": repo.get("name", ""),
            "full_name": full_name,
            "url": repo.get("html_url", ""),
            "description": repo.get("description", "") or "",
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "open_issues": repo.get("open_issues_count", 0),
            "language": repo.get("language", ""),
            "topics": repo.get("topics", []),
            "created_at": repo.get("created_at", "")[:10],
            "last_push": repo.get("pushed_at", "")[:10],
            "size_kb": repo.get("size", 0),
            "archived": repo.get("archived", False),
            "potential_score": score,
        })

    # 按分數排序
    scored_repos.sort(key=lambda x: x["potential_score"], reverse=True)

    # 4. 取前 50 名的 README
    top_n = min(50, len(scored_repos))
    print(f"\n[階段 4] 取得前 {top_n} 名的 README...")
    for i in range(top_n):
        repo = scored_repos[i]
        print(f"  ({i+1}/{top_n}) {repo['full_name']}...")
        readme = get_repo_readme(repo["full_name"])
        repo["readme_preview"] = readme
        if not TOKEN:
            time.sleep(3)
        else:
            time.sleep(0.5)

    # 5. 儲存結果
    output_json = RESULTS_DIR / "github_projects.json"
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(scored_repos, f, ensure_ascii=False, indent=2)

    # 6. 生成報告
    output_report = RESULTS_DIR / "report.txt"
    with open(output_report, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("GitHub 未完成專案搜尋報告\n")
        f.write(f"搜尋時間: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"總共找到: {len(scored_repos)} 個專案\n")
        f.write("=" * 70 + "\n\n")

        for i, repo in enumerate(scored_repos[:50]):
            f.write(f"{'─' * 70}\n")
            f.write(f"#{i+1} | 潛力分數: {repo['potential_score']:.0f}\n")
            f.write(f"名稱: {repo['name']}\n")
            f.write(f"網址: {repo['url']}\n")
            f.write(f"說明: {repo['description'][:100]}\n")
            f.write(f"星星: {repo['stars']} | Fork: {repo['forks']} | Issues: {repo['open_issues']}\n")
            f.write(f"語言: {repo['language']} | 大小: {repo['size_kb']}KB\n")
            f.write(f"建立: {repo['created_at']} | 最後更新: {repo['last_push']}\n")
            f.write(f"標籤: {', '.join(repo['topics'][:5]) if repo['topics'] else '無'}\n")
            f.write(f"已封存: {'是' if repo['archived'] else '否'}\n")
            if repo.get("readme_preview"):
                preview = repo["readme_preview"][:300].replace("\n", " ")
                f.write(f"README: {preview}...\n")
            f.write("\n")

    print(f"\n{'=' * 60}")
    print(f"完成！")
    print(f"  JSON: {output_json}")
    print(f"  報告: {output_report}")
    print(f"  共 {len(scored_repos)} 個專案，前 50 名附有 README")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
