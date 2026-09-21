# X 自動投稿

`content/queue.jsonl` に積んだ内容を、GitHub Actions が1日5回自動で1件ずつ X (Twitter) に投稿する仕組み。

## 下書き（承認前）と投稿キュー（承認後）の2段階

X API には「下書きとして保存する」エンドポイントが存在しない（Xアプリの下書き機能はアプリ内ローカル保存のみで、外部からは書き込めない）。そのためこのリポジトリでは、代わりに以下の2段階で「下書き→承認→自動投稿」を再現している。

- `content/drafts.jsonl`: 投稿候補の下書き置き場。**ここに入っているだけでは投稿されない。**
- `content/queue.jsonl`: 実際に自動投稿されるキュー。**workflowはこのファイルの先頭だけを読む。**

内容を確認・修正し、OKが出たものだけ `drafts.jsonl` から `queue.jsonl` に移す（このファイルを直接編集するか、Claudeに「これをqueueに移して」と頼む）。

## 仕組み

- `content/drafts.jsonl`: 承認待ちの下書き（1行1JSON）
- `content/queue.jsonl`: 承認済み・投稿待ちの内容（1行1JSON、先頭から順に投稿）
- `.github/workflows/post-to-x.yml`: 1日5回（JST 08:00 / 11:30 / 15:00 / 18:30 / 21:30）実行され、`queue.jsonl` の先頭を1件投稿する
- `scripts/post_to_x.py`: 実際に X API (v2) へ投稿するスクリプト。投稿後、そのエントリを `queue.jsonl` から削除し `content/posted.jsonl` に記録してコミット・push する
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

### 4. 下書きを確認し、投稿キューに移す

1. `content/drafts.jsonl` の内容を確認する
2. 問題なければ、該当行を `content/queue.jsonl` に移す（コピー＋drafts側から削除）
3. 新しく書きたい内容は、まず `content/drafts.jsonl` に追記してから確認する

フォーマットは共通で1行1JSON。

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

`.github/workflows/post-to-x.yml` の `schedule` に並んだ `cron` の値を変更・増減する（[crontab.guru](https://crontab.guru/) 等で確認可能）。UTC基準の点に注意（JSTは+9時間）。1つの`cron`が1回の投稿に対応するので、回数を増やしたければ行を増やす。

## 補充のタイミング

週49本ペース（1日5〜7投稿目安）で下書きを用意した場合、約10日で `queue.jsonl` が枯渇する。`content/posted.jsonl` の件数を見て、残りが少なくなってきたら新しい下書きを `drafts.jsonl` に追加する。
