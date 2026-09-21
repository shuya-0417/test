# X 投稿ドラフトの自動配信

X APIは使わない。GitHub Actionsが1日5回、`content/queue.jsonl` の先頭の投稿文を **GitHub Issueとして自動で作成**し、それを見た人が手動でXにコピペ投稿する仕組み。X APIの登録も料金も一切不要。

## 仕組み

- `content/drafts.jsonl`: 投稿候補の下書き置き場。**ここに入っているだけでは何も起きない。**
- `content/queue.jsonl`: 配信待ちの内容（1行1JSON、先頭から順にIssue化される）
- `.github/workflows/surface-x-draft.yml`: 1日5回（JST 08:00 / 11:30 / 15:00 / 18:30 / 21:30）実行され、`queue.jsonl` の先頭を1件、GitHub Issueとして作成する
- `scripts/surface_next_post.py`: Issue作成後、そのエントリを `queue.jsonl` から削除し `content/delivered.jsonl` に記録してコミット・push する
- `content/queue.example.jsonl`: フォーマットの見本（単発ツイート／スレッド）

## Issueが来たらやること

1. GitHubの通知（メール or GitHubアプリ）でIssueが来る
2. Issue本文に書いてある投稿文をコピー
3. Xを開いて手動でそのまま投稿する

以上。X側の認証やAPIキーは一切不要。

## セットアップ

### 1. ワークフローを有効化する

`.github/workflows/surface-x-draft.yml` は **default branch にマージされて初めて** スケジュール実行される（GitHub Actions の仕様）。このブランチをデフォルトブランチにマージ（PRをマージ）すれば、それだけで動き出す。追加の登録作業（APIキーなど）は無い。

### 2. Issueの通知を受け取れるようにする

GitHubの Settings → Notifications で、Issueの通知（メール推奨）がオンになっているか確認する。

### 3. 下書きを確認し、配信キューに移す

1. `content/drafts.jsonl` の内容を確認する
2. 問題なければ、該当行を `content/queue.jsonl` に移す（コピー＋drafts側から削除）
3. 新しく書きたい内容は、まず `content/drafts.jsonl` に追記してから確認する

フォーマットは共通で1行1JSON。

```jsonl
{"text": "単発ツイートの例文"}
{"text": ["スレッド1件目", "スレッド2件目", "スレッド3件目"]}
```

`text` を配列にすると、Issue本文に「1件目」「2件目」と番号付きで並ぶ（スレッドとして手動投稿する想定）。

## 手動実行・動作確認

GitHub の Actions タブから `Surface X draft` ワークフローを開き、`Run workflow` で即時実行できる（`workflow_dispatch`）。実行後、Issuesタブに新しいIssueができているか確認する。

## 頻度・時刻の変更

`.github/workflows/surface-x-draft.yml` の `schedule` に並んだ `cron` の値を変更・増減する（[crontab.guru](https://crontab.guru/) 等で確認可能）。UTC基準の点に注意（JSTは+9時間）。1つの`cron`が1回の配信に対応するので、回数を増やしたければ行を増やす。

## 補充のタイミング

週49本ペース（1日5投稿目安）で下書きを用意した場合、約10日で `queue.jsonl` が枯渇する。`content/delivered.jsonl` の件数を見て、残りが少なくなってきたら新しい下書きを `drafts.jsonl` に追加する。
