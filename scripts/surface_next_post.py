#!/usr/bin/env python3
"""Surface the next queued item as a GitHub Issue for manual posting to X.

No X API is involved (and no cost). This just pops the front entry off
content/queue.jsonl, opens a GitHub Issue containing the text so the
user gets notified and can copy it into X by hand, then archives the
entry to content/delivered.jsonl.

Requires GITHUB_TOKEN and GITHUB_REPOSITORY, both provided automatically
by GitHub Actions (no secrets need to be registered manually).
"""
import datetime
import json
import os
import pathlib

import requests

QUEUE_PATH = pathlib.Path("content/queue.jsonl")
DELIVERED_PATH = pathlib.Path("content/delivered.jsonl")


def load_queue() -> list[str]:
    if not QUEUE_PATH.exists():
        return []
    return [line for line in QUEUE_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]


def save_queue(lines: list[str]) -> None:
    content = "\n".join(lines)
    QUEUE_PATH.write_text(content + ("\n" if content else ""), encoding="utf-8")


def append_delivered(entry: dict) -> None:
    DELIVERED_PATH.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "delivered_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "entry": entry,
    }
    with DELIVERED_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def create_issue(texts: list[str]) -> None:
    token = os.environ["GITHUB_TOKEN"]
    repo = os.environ["GITHUB_REPOSITORY"]
    now = datetime.datetime.now(datetime.timezone.utc).astimezone()
    title = f"X投稿ドラフト: {now.strftime('%Y-%m-%d %H:%M')}"

    if len(texts) == 1:
        body = texts[0]
    else:
        body = "\n\n---\n\n".join(f"{i + 1}件目:\n{t}" for i, t in enumerate(texts))
    body += "\n\n---\nこの内容をコピーしてXに手動で投稿してください。"

    response = requests.post(
        f"https://api.github.com/repos/{repo}/issues",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
        json={"title": title, "body": body, "labels": ["x-draft"]},
        timeout=30,
    )
    if response.status_code >= 300:
        raise SystemExit(f"GitHub API error {response.status_code}: {response.text}")


def main() -> None:
    lines = load_queue()
    if not lines:
        print("queue is empty; nothing to surface")
        return

    raw, remaining = lines[0], lines[1:]
    entry = json.loads(raw)
    texts = entry["text"] if isinstance(entry["text"], list) else [entry["text"]]

    create_issue(texts)
    save_queue(remaining)
    append_delivered(entry)
    print(f"opened an issue with {len(texts)} text(s)")


if __name__ == "__main__":
    main()
