# X 自動投稿

`content/queue.jsonl` に積んだ内容を、GitHub Actions が毎日自動で1件ずつ X (Twitter) に投稿する仕組み。

## 仕組み

- `content/queue.jsonl`: 投稿待ちの内容（1行1JSON、先頭から順に投稿）
- `.github/workflows/post-to-x.yml`: 毎日 09:00 JST（`0 0 * * *` UTC）に実行され、キューの先頭を1件投稿する
- `scripts/post_to_x.py`: 実際に X API (v2) へ投稿するスクリプト。投稿後、そのエントリをキューから削除し `content/posted.jsonl` に記録してコミット・push する
- `content/queue.example.jsonl`: フォーマットの見本（単発ツイート／スレッド）

## セットアップ

### 1. X Developer App を作成し、認証情報を取得する

1. https://developer.x.com/ でアプリを作成（Free枠で可）
2. アプリの権限を **Read and write** に設定
3. 投稿したいアカウントで認証し、以下4つを取得する
   - API Key（Consumer Key）
   - API Secret（Consumer Secret）
   - Access Token
   - Access Token Secret

   ※ Access Token は「投稿するアカウント自身」で発行すること（OAuth 1.0a, User context）。

### 2. GitHub リポジトリに Secrets を登録する

このリポジトリの Settings → Secrets and variables → Actions で、以下を登録する。

| Secret名 | 値 |
|---|---|
| `X_API_KEY` | API Key |
| `X_API_SECRET` | API Secret |
| `X_ACCESS_TOKEN` | Access Token |
| `X_ACCESS_TOKEN_SECRET` | Access Token Secret |

### 3. ワークフローを有効化する

`.github/workflows/post-to-x.yml` は **default branch にマージされて初めて** スケジュール実行される（GitHub Actions の仕様）。このブランチをデフォルトブランチにマージ（PRをマージ）してから有効になる。

### 4. 投稿内容をキューに追加する

`content/queue.jsonl` に1行1JSONで追記する。

```jsonl
{"text": "単発ツイートの例文"}
{"text": ["スレッド1件目", "スレッド2件目", "スレッド3件目"]}
```

`text` を配列にすると、先頭からリプライ形式で連投（スレッド）になる。

## 手動実行・動作確認

- GitHub の Actions タブから `Post to X` ワークフローを開き、`Run workflow` で即時実行できる（`workflow_dispatch`）。
- ローカルで試す場合は環境変数を設定してから実行する。

```bash
pip install -r requirements.txt
export X_API_KEY=...
export X_API_SECRET=...
export X_ACCESS_TOKEN=...
export X_ACCESS_TOKEN_SECRET=...
python scripts/post_to_x.py
```

## 頻度・時刻の変更

`.github/workflows/post-to-x.yml` の `cron` の値を変更する（[crontab.guru](https://crontab.guru/) 等で確認可能）。UTC基準の点に注意（JSTは+9時間）。
