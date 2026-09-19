#!/usr/bin/env python3
"""Post the next queued item to X (Twitter) using the v2 API.

Reads content/queue.jsonl (one JSON object per line, oldest first),
posts it, removes it from the queue, and appends the result to
content/posted.jsonl. Each queue entry is:

    {"text": "single tweet text"}
    {"text": ["tweet 1", "tweet 2", "..."]}   # posted as a reply-chain thread

Requires these environment variables (X Developer App, OAuth 1.0a,
"Read and write" permission, tied to the account that should post):
    X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET
"""
import datetime
import json
import os
import pathlib

import requests
from requests_oauthlib import OAuth1

API_URL = "https://api.twitter.com/2/tweets"
QUEUE_PATH = pathlib.Path("content/queue.jsonl")
POSTED_PATH = pathlib.Path("content/posted.jsonl")

REQUIRED_ENV_VARS = (
    "X_API_KEY",
    "X_API_SECRET",
    "X_ACCESS_TOKEN",
    "X_ACCESS_TOKEN_SECRET",
)


def load_queue() -> list[str]:
    if not QUEUE_PATH.exists():
        return []
    return [line for line in QUEUE_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]


def save_queue(lines: list[str]) -> None:
    content = "\n".join(lines)
    QUEUE_PATH.write_text(content + ("\n" if content else ""), encoding="utf-8")


def append_posted(entry: dict, tweet_ids: list[str]) -> None:
    POSTED_PATH.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "posted_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "tweet_ids": tweet_ids,
        "entry": entry,
    }
    with POSTED_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def build_auth() -> OAuth1:
    missing = [name for name in REQUIRED_ENV_VARS if not os.environ.get(name)]
    if missing:
        raise SystemExit(f"missing required environment variable(s): {', '.join(missing)}")
    return OAuth1(
        os.environ["X_API_KEY"],
        os.environ["X_API_SECRET"],
        os.environ["X_ACCESS_TOKEN"],
        os.environ["X_ACCESS_TOKEN_SECRET"],
    )


def post_tweet(oauth: OAuth1, text: str, reply_to: str | None = None) -> str:
    payload = {"text": text}
    if reply_to:
        payload["reply"] = {"in_reply_to_tweet_id": reply_to}
    response = requests.post(API_URL, auth=oauth, json=payload, timeout=30)
    if response.status_code >= 300:
        raise SystemExit(f"X API error {response.status_code}: {response.text}")
    return response.json()["data"]["id"]


def main() -> None:
    lines = load_queue()
    if not lines:
        print("queue is empty; nothing to post")
        return

    raw, remaining = lines[0], lines[1:]
    entry = json.loads(raw)
    texts = entry["text"] if isinstance(entry["text"], list) else [entry["text"]]

    oauth = build_auth()
    tweet_ids: list[str] = []
    reply_to = None
    for text in texts:
        tweet_id = post_tweet(oauth, text, reply_to=reply_to)
        tweet_ids.append(tweet_id)
        reply_to = tweet_id

    save_queue(remaining)
    append_posted(entry, tweet_ids)
    print(f"posted {len(tweet_ids)} tweet(s): {tweet_ids}")


if __name__ == "__main__":
    main()
