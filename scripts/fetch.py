"""
RSSフィードを取得し、共通フォーマットのJSONに統合する。
- 保存するのはタイトル/リンク/カテゴリ/日付のみ
- description (本文の要約) は権利配慮のため保存しない
- 既存のdata.jsonとマージし、翻訳済みエントリの結果を保持
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import feedparser

sys.path.insert(0, os.path.dirname(__file__))
from sources import SOURCES

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "data.json"


def load_existing():
    if DATA_FILE.exists():
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {"items": [], "updated_at": None}


def parse_date(entry):
    for key in ("published_parsed", "updated_parsed"):
        if entry.get(key):
            return datetime(*entry[key][:6], tzinfo=timezone.utc).isoformat()
    return None


def fetch_source(source):
    print(f"  Fetching {source['name']}...", flush=True)
    try:
        feed = feedparser.parse(source["url"])
    except Exception as e:
        print(f"  ERROR: {e}", flush=True)
        return []

    items = []
    for entry in feed.entries:
        guid = entry.get("id") or entry.get("link")
        items.append({
            "id": f"{source['id']}::{guid}",
            "source_id": source["id"],
            "source_name": source["name"],
            "category": source["category"],
            "color": source["color"],
            "title_en": entry.get("title", "").strip(),
            "title_ja": None,
            "link": entry.get("link", ""),
            "published": parse_date(entry),
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "translated": False,
        })
    return items


def merge(existing_items, new_items):
    by_id = {it["id"]: it for it in existing_items}
    added = 0
    for it in new_items:
        if it["id"] not in by_id:
            by_id[it["id"]] = it
            added += 1
        else:
            old = by_id[it["id"]]
            old["fetched_at"] = it["fetched_at"]
            old["title_en"] = it["title_en"]
            old["link"] = it["link"]
            old["category"] = it["category"]
            old["color"] = it["color"]
            old["source_name"] = it["source_name"]

    merged = list(by_id.values())
    merged.sort(key=lambda x: x.get("published") or "", reverse=True)
    return merged, added


def main():
    print(f"Fetch start: {datetime.now(timezone.utc).isoformat()}")
    existing = load_existing()
    all_new = []
    for src in SOURCES:
        all_new.extend(fetch_source(src))

    merged, added = merge(existing["items"], all_new)
    payload = {
        "items": merged,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "source_count": len(SOURCES),
        "item_count": len(merged),
    }

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"Done. total={len(merged)} new={added}")


if __name__ == "__main__":
    main()
