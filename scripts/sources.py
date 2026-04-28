"""
Anthropic / Claude 関連の情報源定義
- name: 表示名
- url: RSS / Atom フィードURL
- category: バッジ表示用カテゴリ
- color: バッジ色 (Tailwind系)
"""

SOURCES = [
    {
        "id": "anthropic_news",
        "name": "Anthropic News",
        "url": "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_news.xml",
        "category": "News",
        "color": "#3b82f6",  # blue
    },
    {
        "id": "anthropic_engineering",
        "name": "Engineering",
        "url": "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_engineering.xml",
        "category": "Engineering",
        "color": "#8b5cf6",  # purple
    },
    {
        "id": "anthropic_research",
        "name": "Research",
        "url": "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_research.xml",
        "category": "Research",
        "color": "#10b981",  # green
    },
    {
        "id": "claude_blog",
        "name": "Claude Blog",
        "url": "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_claude.xml",
        "category": "Blog",
        "color": "#f59e0b",  # amber
    },
    {
        "id": "claude_code_changelog",
        "name": "Claude Code",
        "url": "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_changelog_claude_code.xml",
        "category": "Release",
        "color": "#ef4444",  # red
    },
]
