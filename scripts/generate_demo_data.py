"""
プレビュー用 data.json 生成。本番では fetch.py + translate.py を使う。
"""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "data.json"

sample = [
    {
        "source_id": "anthropic_news", "source_name": "Anthropic News",
        "category": "News", "color": "#3b82f6",
        "title_en": "Introducing Claude Design by Anthropic Labs",
        "title_ja": "Anthropic LabsのClaude Designを発表",
        "link": "https://www.anthropic.com/news/claude-design-anthropic-labs",
        "published": "2026-04-17T00:00:00+00:00",
    },
    {
        "source_id": "anthropic_news", "source_name": "Anthropic News",
        "category": "News", "color": "#3b82f6",
        "title_en": "Introducing Claude Opus 4.7",
        "title_ja": "Claude Opus 4.7を発表",
        "link": "https://www.anthropic.com/news/claude-opus-4-7",
        "published": "2026-04-16T00:00:00+00:00",
    },
    {
        "source_id": "anthropic_news", "source_name": "Anthropic News",
        "category": "News", "color": "#3b82f6",
        "title_en": "Anthropic's Long-Term Benefit Trust appoints Vas Narasimhan to Board of Directors",
        "title_ja": "AnthropicのLong-Term Benefit Trust、Vas Narasimhan氏を取締役に任命",
        "link": "https://www.anthropic.com/news/narasimhan-board",
        "published": "2026-04-14T00:00:00+00:00",
    },
    {
        "source_id": "anthropic_engineering", "source_name": "Engineering",
        "category": "Engineering", "color": "#8b5cf6",
        "title_en": "Building effective tool calling for agents",
        "title_ja": "エージェント向け効果的なツール呼び出しの構築",
        "link": "https://www.anthropic.com/engineering/building-effective-tool-calling",
        "published": "2026-04-10T00:00:00+00:00",
    },
    {
        "source_id": "anthropic_research", "source_name": "Research",
        "category": "Research", "color": "#10b981",
        "title_en": "Sparse autoencoders for interpretability",
        "title_ja": "解釈可能性のためのスパースオートエンコーダー",
        "link": "https://www.anthropic.com/research/sparse-autoencoders",
        "published": "2026-04-08T00:00:00+00:00",
    },
    {
        "source_id": "anthropic_news", "source_name": "Anthropic News",
        "category": "News", "color": "#3b82f6",
        "title_en": "Anthropic expands partnership with Google and Broadcom for multiple gigawatts of next-generation compute",
        "title_ja": "AnthropicがGoogleおよびBroadcomとの提携を拡大、次世代計算基盤で数ギガワット規模に",
        "link": "https://www.anthropic.com/news/google-broadcom-partnership-compute",
        "published": "2026-04-06T00:00:00+00:00",
    },
    {
        "source_id": "claude_code_changelog", "source_name": "Claude Code",
        "category": "Release", "color": "#ef4444",
        "title_en": "Claude Code v1.8.0 — Improved MCP server discovery",
        "title_ja": "Claude Code v1.8.0 — MCPサーバー検出の改善",
        "link": "https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md",
        "published": "2026-04-05T00:00:00+00:00",
    },
    {
        "source_id": "claude_blog", "source_name": "Claude Blog",
        "category": "Blog", "color": "#f59e0b",
        "title_en": "How teams are using Claude in production",
        "title_ja": "Claudeをプロダクションで活用するチーム事例",
        "link": "https://www.claude.com/blog/teams-using-claude-production",
        "published": "2026-04-02T00:00:00+00:00",
    },
    {
        "source_id": "anthropic_news", "source_name": "Anthropic News",
        "category": "News", "color": "#3b82f6",
        "title_en": "Australian government and Anthropic sign MOU for AI safety and research",
        "title_ja": "オーストラリア政府とAnthropic、AI安全性と研究に関する覚書を締結",
        "link": "https://www.anthropic.com/news/australia-MOU",
        "published": "2026-03-31T00:00:00+00:00",
    },
    {
        "source_id": "anthropic_news", "source_name": "Anthropic News",
        "category": "News", "color": "#3b82f6",
        "title_en": "Introducing Claude Sonnet 4.6",
        "title_ja": "Claude Sonnet 4.6を発表",
        "link": "https://www.anthropic.com/news/claude-sonnet-4-6",
        "published": "2026-02-17T00:00:00+00:00",
    },
    {
        "source_id": "anthropic_news", "source_name": "Anthropic News",
        "category": "News", "color": "#3b82f6",
        "title_en": "Claude's new constitution",
        "title_ja": "Claudeの新しい憲法",
        "link": "https://www.anthropic.com/news/claude-new-constitution",
        "published": "2026-01-22T00:00:00+00:00",
    },
    {
        "source_id": "claude_code_changelog", "source_name": "Claude Code",
        "category": "Release", "color": "#ef4444",
        "title_en": "Claude Code v1.7.2 — Skills GA, performance improvements",
        "title_ja": "Claude Code v1.7.2 — Skills正式公開、パフォーマンス向上",
        "link": "https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md",
        "published": "2026-01-20T00:00:00+00:00",
    },
]

items = []
for s in sample:
    s["id"] = f"{s['source_id']}::{s['link']}"
    s["translated"] = True
    s["fetched_at"] = datetime.now(timezone.utc).isoformat()
    items.append(s)

items.sort(key=lambda x: x["published"], reverse=True)

payload = {
    "items": items,
    "updated_at": datetime.now(timezone.utc).isoformat(),
    "source_count": 5,
    "item_count": len(items),
}

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

print(f"Wrote {OUT} with {len(items)} items")
