# Claude Updates JP

Anthropic / Claude の公式情報を自動で集めて日本語タイトル付きで一覧する非公式アグリゲーター。

## 運用方針(権利配慮)

本文や要約は表示せず、**タイトルの日本語訳と公式記事へのリンクのみ**を提供します。
読者は必ず公式記事に遷移する設計です。

- ✅ 公式タイトルの日本語訳
- ✅ 公式記事への外部リンク
- ✅ 公開日・カテゴリ・情報源バッジ
- ❌ 記事本文の翻訳・要約・転載
- ❌ description の翻訳掲載
- ❌ 検索エンジンへのインデックス(`noindex,nofollow`)

掲載停止依頼は GitHub Issues で受け付けます。

## 構成

- **ホスティング**: GitHub Pages (無料)
- **定期実行**: GitHub Actions (6時間ごと)
- **翻訳**: MyMemory API (完全無料、APIキー不要、メアド登録で1日10万文字)
- **新規分のみ翻訳**: 既存翻訳結果を再利用

```
.
├── .github/workflows/update.yml   # 6時間ごとに動くワークフロー
├── scripts/
│   ├── sources.py                 # 情報源の定義
│   ├── fetch.py                   # RSS取得 → data.json
│   ├── translate.py               # 未翻訳タイトルのみ DeepL で翻訳
│   └── generate_demo_data.py      # ローカル動作確認用
├── data/data.json                 # 永続データ (Actionsが自動更新)
└── site/                          # GitHub Pages公開ディレクトリ
    ├── index.html
    ├── style.css
    ├── app.js
    └── data.json                  # ビルド時にコピーされる
```

## 情報源

| 名前 | カテゴリ | 元URL |
|---|---|---|
| Anthropic News | News | https://www.anthropic.com/news |
| Anthropic Engineering | Engineering | https://www.anthropic.com/engineering |
| Anthropic Research | Research | https://www.anthropic.com/research |
| Claude Blog | Blog | https://www.claude.com/blog |
| Claude Code Changelog | Release | claude-code リポジトリ |

RSS は [Olshansk/rss-feeds](https://github.com/Olshansk/rss-feeds) のスクレイプ済みフィードを利用。

## セットアップ手順

1. このリポジトリを GitHub に置く
2. **Settings → Pages** で Source を「GitHub Actions」に設定
3. (任意) MyMemory の利用上限を倍にしたい場合、**Settings → Secrets and variables → Actions** で `MYMEMORY_EMAIL` にメアドを登録(登録しなくても動きます)
4. **Actions** タブから `Update feed and deploy` を手動実行(初回データ生成)

以降は自動で 6 時間ごとに更新されます。

## ローカル確認

```bash
pip install feedparser requests
python scripts/fetch.py
python scripts/translate.py    # MYMEMORY_EMAILが無くても動く
cp data/data.json site/data.json
python -m http.server -d site 8000
# → http://localhost:8000
```

## カスタマイズ

- 情報源の追加: `scripts/sources.py` に追記
- 更新間隔: `.github/workflows/update.yml` の cron
- 配色やバッジ色: `scripts/sources.py` の `color` と `site/style.css`

## 免責事項

本サイトは Anthropic とは無関係の非公式プロジェクトです。
タイトルの日本語訳は機械翻訳のため誤訳を含む可能性があります。
正確な情報は必ず公式記事をご確認ください。
著作権は各記事の発行元に帰属します。
