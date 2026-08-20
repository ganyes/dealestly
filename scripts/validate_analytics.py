#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GA4_ID = "G-1BEC3BTBVG"


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.shop_links: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        attr = {key: value or "" for key, value in attrs}
        classes = set(attr.get("class", "").split())
        if "shop-deal-link" in classes or attr.get("data-analytics") == "shop-deal":
            self.shop_links.append(attr)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_ga(path: Path, text: str, errors: list[str]) -> None:
    if GA4_ID not in text:
        errors.append(f"{path.name}: missing GA4 ID {GA4_ID}")
    tag_count = len(re.findall(r"googletagmanager\.com/gtag/js\?id=G-1BEC3BTBVG", text))
    if tag_count != 1:
        errors.append(f"{path.name}: expected exactly one GA4 script tag, found {tag_count}")
    config_count = len(re.findall(r"gtag\('config', 'G-1BEC3BTBVG'\)", text))
    if config_count != 1:
        errors.append(f"{path.name}: expected exactly one GA4 config call, found {config_count}")


def check_today(text: str, errors: list[str]) -> None:
    if "shop_deal_click" not in text or "gtag('event', 'shop_deal_click'" not in text:
        errors.append("today.html: missing shared shop_deal_click handler")
    if "a.shop-deal-link" not in text:
        errors.append("today.html: shared handler should target a.shop-deal-link")

    parser = LinkParser()
    parser.feed(text)
    if not parser.shop_links:
        errors.append("today.html: no SHOP DEAL tracking links found")

    required = [
        "data-product-name",
        "data-retailer",
        "data-current-price",
        "data-product-url",
        "data-deal-section",
    ]
    for index, link in enumerate(parser.shop_links, start=1):
        classes = set(link.get("class", "").split())
        if "shop-deal-link" not in classes:
            errors.append(f"SHOP DEAL link {index}: missing class shop-deal-link")
        for key in required:
            if not link.get(key):
                errors.append(f"SHOP DEAL link {index}: missing {key}")
        section = link.get("data-deal-section")
        if section == "featured" and not link.get("data-deal-number"):
            errors.append(f"SHOP DEAL link {index}: featured link missing data-deal-number")
        if section == "additional" and link.get("data-deal-number"):
            errors.append(f"SHOP DEAL link {index}: additional link should not have data-deal-number")
        if section not in {"featured", "additional"}:
            errors.append(f"SHOP DEAL link {index}: invalid data-deal-section {section!r}")


def main() -> int:
    errors: list[str] = []
    index = ROOT / "index.html"
    today = ROOT / "today.html"

    for path in (index, today):
        if not path.exists():
            errors.append(f"{path.name}: file not found")
            continue
        check_ga(path, read(path), errors)

    if today.exists():
        check_today(read(today), errors)

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS")
    print("GA4 and shop_deal_click tracking are configured.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
