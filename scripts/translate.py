"""
未翻訳エントリのタイトルだけを MyMemory 翻訳 API で日本語化する。

MyMemory: https://mymemory.translated.net/
- 完全無料、APIキー不要
- 匿名で1日5万文字、メアド登録で1日10万文字
- タイトル翻訳には十分

環境変数:
- MYMEMORY_EMAIL: 登録不要だが、メアドを送ると上限が倍になる (任意)
"""
import json
import os
import time
from pathlib import Path
from urllib.parse import urlencode

import requests

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "data.json"

EMAIL = os.environ.get("MYMEMORY_EMAIL", "").strip()
ENDPOINT = "https://api.mymemory.translated.net/get"


def mymemory_translate(text):
    """1件翻訳する。失敗時は原文を返す。"""
    params = {
        "q": text,
        "langpair": "en|ja",
    }
    if EMAIL:
        params["de"] = EMAIL

    try:
        url = f"{ENDPOINT}?{urlencode(params)}"
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        data = r.json()
        # MyMemory のレスポンス形式
        # {"responseData": {"translatedText": "...", "match": 1.0}, ...}
        translated = data.get("responseData", {}).get("translatedText", "")
        if not translated:
            return text  # 失敗時はそのまま
        return translated
    except Exception as e:
        print(f"  Translation error for '{text[:40]}...': {e}", flush=True)
        return text


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

    print(f"Mode: MyMemory API ({'with email' if EMAIL else 'anonymous'})")

    for i, it in enumerate(pending, 1):
        original = it["title_en"]
        ja = mymemory_translate(original)
        it["title_ja"] = ja
        it["translated"] = True
        print(f"  [{i}/{len(pending)}] {original[:50]}... -> {ja[:50]}...", flush=True)
        time.sleep(0.5)  # API側に優しく

        # 進捗を逐次保存(途中で止まっても再開可能)
        if i % 10 == 0:
            with DATA_FILE.open("w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)

    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"Done. translated={len(pending)} titles")


if __name__ == "__main__":
    main()
