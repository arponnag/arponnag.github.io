#!/usr/bin/env python3
"""
Optional LinkedIn sync helper.

LinkedIn does not provide a free public profile API. This script supports
Proxycurl (https://nubela.co/proxycurl/) when PROXYCURL_API_KEY is set.

Without an API key, update data/profile.json manually or replace the CV PDF.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "data" / "profile.json"
LINKEDIN_URL = "https://www.linkedin.com/in/arpon-nag/"


def fetch_linkedin_profile(api_key: str) -> dict:
    url = (
        "https://nubela.co/proxycurl/api/v2/linkedin?url="
        + urllib.parse.quote(LINKEDIN_URL, safe="")
    )
    request = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {api_key}"},
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def main() -> int:
    api_key = os.environ.get("PROXYCURL_API_KEY", "").strip()
    if not api_key:
        print(
            "LinkedIn auto-sync skipped: set PROXYCURL_API_KEY to enable optional sync.",
            file=sys.stderr,
        )
        return 0

    try:
        payload = fetch_linkedin_profile(api_key)
    except urllib.error.URLError as error:
        print(f"LinkedIn sync failed: {error}", file=sys.stderr)
        return 1

    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    if payload.get("headline"):
        profile["tagline"] = payload["headline"]
    if payload.get("summary"):
        profile["about"] = payload["summary"]

    PROFILE_PATH.write_text(
        json.dumps(profile, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print("Updated profile.json headline/summary from LinkedIn.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
