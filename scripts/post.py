#!/usr/bin/env python3
"""Posts the next due item in queue.json to Instagram via the Graph API.

Run on a schedule (see .github/workflows/post.yml). Each run:
  1. Finds the next unposted queue item (wraps around to the top once the
     queue is exhausted, so the account never runs dry).
  2. Creates an Instagram media container from the image's raw GitHub URL.
  3. Publishes the container.
  4. Marks the item posted and commits queue.json back to the repo.

Required environment variables (set as GitHub Actions secrets):
  IG_ACCESS_TOKEN   - Meta Graph API access token with instagram_content_publish
  IG_USER_ID        - Instagram Business Account ID (numeric)
  GITHUB_REPOSITORY - "owner/repo" (set automatically by GitHub Actions)
"""
import json
import os
import sys
import time
import urllib.request
import urllib.parse

GRAPH_VERSION = "v21.0"
GRAPH_BASE = f"https://graph.facebook.com/{GRAPH_VERSION}"
QUEUE_PATH = os.path.join(os.path.dirname(__file__), "..", "queue.json")


def graph_post(path, params):
    url = f"{GRAPH_BASE}/{path}"
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def graph_get(path, params):
    url = f"{GRAPH_BASE}/{path}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read().decode())


def raw_image_url(repo, image_name):
    return f"https://raw.githubusercontent.com/{repo}/main/images/{image_name}"


def main():
    access_token = os.environ["IG_ACCESS_TOKEN"]
    ig_user_id = os.environ["IG_USER_ID"]
    repo = os.environ["GITHUB_REPOSITORY"]

    with open(QUEUE_PATH) as f:
        queue = json.load(f)

    unposted = [item for item in queue if not item["posted"]]
    if not unposted:
        print("Queue exhausted — resetting all items to unposted for another cycle.")
        for item in queue:
            item["posted"] = False
            item["posted_at"] = None
        with open(QUEUE_PATH, "w") as f:
            json.dump(queue, f, indent=2, ensure_ascii=False)
        unposted = queue

    item = unposted[0]
    image_url = raw_image_url(repo, item["image"])
    print(f"Posting {item['id']} ({item['image']}) ...")

    container = graph_post(
        f"{ig_user_id}/media",
        {
            "image_url": image_url,
            "caption": item["caption"],
            "access_token": access_token,
        },
    )
    if "id" not in container:
        print(f"ERROR creating media container: {container}", file=sys.stderr)
        sys.exit(1)
    creation_id = container["id"]

    # Poll until the container has finished processing.
    for _ in range(10):
        status = graph_get(creation_id, {"fields": "status_code", "access_token": access_token})
        code = status.get("status_code")
        if code == "FINISHED":
            break
        if code == "ERROR":
            print(f"ERROR: media container failed processing: {status}", file=sys.stderr)
            sys.exit(1)
        time.sleep(5)

    publish = graph_post(
        f"{ig_user_id}/media_publish",
        {"creation_id": creation_id, "access_token": access_token},
    )
    if "id" not in publish:
        print(f"ERROR publishing media: {publish}", file=sys.stderr)
        sys.exit(1)

    print(f"Published: {publish['id']}")

    item["posted"] = True
    item["posted_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(QUEUE_PATH, "w") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
