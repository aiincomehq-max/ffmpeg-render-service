"""Minimal Blotato REST client (stdlib only).

Env: BLOTATO_API_KEY (Blotato > Settings > API). Without it, or with CLIPPER_DRY_RUN=1,
nothing is sent: calls are logged and fake IDs returned.

VERIFY ON FIRST REAL USE against https://help.blotato.com/api (couldn't be reached from the
cloud session that wrote this). Field names match Blotato's own MCP tool schemas
(accountId, platform, text, mediaUrls, title, privacyStatus, shouldNotifySubscribers,
isMadeForKids, privacyLevel, disabledComments/Duet/Stitch, isBrandedContent, isYourBrand,
isAiGenerated, mediaType, scheduledTime). Endpoint paths are constants below if they need fixing.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
import uuid
from pathlib import Path

BASE = os.environ.get("BLOTATO_BASE", "https://backend.blotato.com/v2")
EP_ACCOUNTS = "/users/me/accounts"
EP_UPLOAD = "/media/uploads"       # -> {presignedUrl, publicUrl}
EP_POSTS = "/posts"                # -> {postSubmissionId}
EP_POST_STATUS = "/posts/{id}"


def dry_run() -> bool:
    return os.environ.get("CLIPPER_DRY_RUN") == "1" or not os.environ.get("BLOTATO_API_KEY")


class BlotatoError(RuntimeError):
    pass


def _req(method: str, path: str, body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(BASE + path, data=data, method=method, headers={
        "blotato-api-key": os.environ["BLOTATO_API_KEY"], "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            txt = resp.read().decode() or "{}"
            return json.loads(txt)
    except urllib.error.HTTPError as e:
        raise BlotatoError(f"{method} {path} -> {e.code}: {e.read().decode()[:500]}") from e


def accounts(platform: str | None = None) -> list[dict]:
    if dry_run():
        return []
    j = _req("GET", EP_ACCOUNTS + (f"?platform={platform}" if platform else ""))
    return j.get("items", j if isinstance(j, list) else [])


def upload(path: Path, log: list) -> str:
    """Local file -> public URL Blotato can fetch."""
    if dry_run():
        log.append({"upload": str(path)})
        return f"https://dry-run.invalid/{path.name}"
    j = _req("POST", EP_UPLOAD, {"filename": path.name})
    put = urllib.request.Request(j["presignedUrl"], data=path.read_bytes(), method="PUT",
                                 headers={"Content-Type": "video/mp4"})
    with urllib.request.urlopen(put, timeout=600):
        pass
    return j["publicUrl"]


def target(platform: str, title: str) -> dict:
    """Platform-specific fields (YouTube needs title/privacy/notify; TikTok needs privacy + flags)."""
    if platform == "youtube":
        return {"targetType": "youtube", "title": title[:100], "privacyStatus": "public",
                "shouldNotifySubscribers": True, "isMadeForKids": False, "containsSyntheticMedia": False}
    if platform == "tiktok":
        return {"targetType": "tiktok", "privacyLevel": "PUBLIC_TO_EVERYONE", "disabledComments": False,
                "disabledDuet": False, "disabledStitch": False, "isBrandedContent": False,
                "isYourBrand": False, "isAiGenerated": False, "title": title[:90]}
    if platform == "instagram":
        return {"targetType": "instagram", "mediaType": "reel", "shareToFeed": True}
    raise ValueError(platform)


def create_post(platform: str, account_id: str, text: str, media_url: str, title: str,
                scheduled_iso: str | None, log: list) -> str:
    body = {"post": {"accountId": account_id,
                     "content": {"text": text, "mediaUrls": [media_url], "platform": platform},
                     "target": target(platform, title)}}
    if scheduled_iso:
        body["scheduledTime"] = scheduled_iso
    if dry_run():
        log.append({"post": body})
        return f"dry-{uuid.uuid4().hex[:8]}"
    j = _req("POST", EP_POSTS, body)
    return j.get("postSubmissionId") or j.get("id") or json.dumps(j)


def status(post_id: str) -> dict:
    if dry_run() or post_id.startswith("dry-"):
        return {"status": "dry-run"}
    return _req("GET", EP_POST_STATUS.format(id=post_id))
