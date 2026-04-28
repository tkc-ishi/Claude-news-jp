"""
未翻訳エントリの「タイトルだけ」を DeepL で日本語化する。
本文や description は翻訳しない (権利配慮 + 翻訳量削減)。

- 環境変数 DEEPL_API_KEY が必要
- キーが無い場合は dummy 翻訳でフォールバック (動作確認用)
- すでに translated=True のエントリはスキップ (再翻訳しない)
"""
import json
import os
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "data.json"

DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY", "").strip()
DEEPL_ENDPOINT = "https://api-free.deepl.com/v2/translate"


def deepl_translate(texts):
    """テキスト配列を一括翻訳。50件ずつバッチ。"""
    if not texts:
        return []
    out = []
    BATCH = 50
    for i in range(0, len(texts), BATCH):
        chunk = texts[i:i + BATCH]
        data = [("auth_key", DEEPL_API_KEY), ("target_lang", "JA"), ("source_lang", "EN")]
        for t in chunk:
            data.append(("text", t))
        r = requests.post(DEEPL_ENDPOINT, data=data, timeout=60)
        r.raise_for_status()
        out.extend([x["text"] for x in r.json()["translations"]])
        time.sleep(0.5)
    return out


def dummy_translate(texts):
    return [f"【ダミー訳】{t}" for t in texts]


def main():
    if not DATA_FILE.exists():
        print("data.json not found. Run fetch.py first.")
        return

    with DATA_FILE.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    items = payload["items"]
    pending = [it for it in items if not it.get("translated")]
    print(f"Pending translations: {len(pending)}")

    if not pending:
        print("Nothing to translate.")
        return

    use_real = bool(DEEPL_API_KEY)
    print(f"Mode: {'DeepL API' if use_real else 'DUMMY (no DEEPL_API_KEY set)'}")

    titles = [it["title_en"] for it in pending]
    translator = deepl_translate if use_real else dummy_translate
    titles_ja = translator(titles)

    for it, t_ja in zip(pending, titles_ja):
        it["title_ja"] = t_ja
        it["translated"] = True

    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"Done. translated={len(pending)} titles")


if __name__ == "__main__":
    main()
