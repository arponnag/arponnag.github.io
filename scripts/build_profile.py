#!/usr/bin/env python3
"""Regenerate marked HTML sections in index.html from data/profile.json."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "data" / "profile.json"
INDEX_PATH = ROOT / "index.html"


def load_profile() -> dict:
    with PROFILE_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def render_experience(profile: dict) -> str:
    blocks = []
    for item in profile["experience"]:
        upcoming_class = " experience-upcoming" if item.get("upcoming") else ""
        badge = (
            '<span class="experience-badge">Upcoming</span>'
            if item.get("upcoming")
            else ""
        )
        bullets = "\n".join(
            f"              <li>{bullet}</li>" for bullet in item["bullets"]
        )
        blocks.append(
            f"""          <div class="col-md-12 mt-4 mt-md-0 icon-box{upcoming_class}" data-aos="fade-up" data-aos-delay="100">
            <h4 style="text-align:left;">{badge}<a href="{item["url"]}" target="_blank" rel="noopener noreferrer" style="color:#12d640">{item["company"]}</a></h4>
            <h5 style="text-align:left;">{item["dates"]}</h5>
            <p style="text-align:left;color:#fff"><em>{item["role"]}</em></p>
            <ul style="text-align:left;">
{bullets}
            </ul>
          </div>"""
        )
    return "\n".join(blocks)


def render_education(profile: dict) -> str:
    blocks = []
    for item in profile["education"]:
        bullets = []
        for highlight in item["highlights"]:
            if "Uppsala University" in highlight:
                bullets.append(
                    '              <li>Semester Exchange at <a href="https://www.uu.se/en" target="_blank" rel="noopener noreferrer" style="color:#12d640">Uppsala University, Sweden</a>: Machine Learning, Cyber Security, and Statistical Risk Analysis</li>'
                )
            else:
                bullets.append(f"              <li>{highlight}</li>")
        bullet_html = "\n".join(bullets)
        blocks.append(
            f"""          <div class="col-md-12 mt-4 mt-md-0 icon-box" data-aos="fade-up" data-aos-delay="100">
            <h4 style="text-align:left;"><a href="{item["url"]}" target="_blank" rel="noopener noreferrer" style="color:#12d640">{item["school"]}</a></h4>
            <h5 style="text-align:left;">{item["dates"]}</h5>
            <p style="text-align:left;color:#fff"><em>{item["degree"]}</em></p>
            <ul style="text-align:left;color:#fff;">
{bullet_html}
            </ul>
          </div>"""
        )
    return "\n".join(blocks)


def replace_section(html: str, name: str, content: str) -> str:
    pattern = (
        rf"(<!-- PROFILE:{name}:START -->)\s*.*?\s*(<!-- PROFILE:{name}:END -->)"
    )
    replacement = rf"\1\n{content}\n        \2"
    updated, count = re.subn(pattern, replacement, html, count=1, flags=re.DOTALL)
    if count != 1:
        raise RuntimeError(f"Could not update PROFILE:{name} section in index.html")
    return updated


def main() -> None:
    profile = load_profile()
    html = INDEX_PATH.read_text(encoding="utf-8")
    html = replace_section(html, "EXPERIENCE", render_experience(profile))
    html = replace_section(html, "EDUCATION", render_education(profile))
    INDEX_PATH.write_text(html, encoding="utf-8")
    print("Updated index.html from data/profile.json")


if __name__ == "__main__":
    main()
