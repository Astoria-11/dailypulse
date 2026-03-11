#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RSS Military Sensor - 军事与安全
"""

import logging
import feedparser
from dataclasses import dataclass
from typing import List

logger = logging.getLogger(__name__)

FEEDS = [
    {"title": "Defense News",   "url": "https://www.defensenews.com/arc/outboundfeeds/rss/?outputType=xml"},
    {"title": "Reuters World",  "url": "https://feeds.reuters.com/reuters/worldNews"},
    {"title": "Al Jazeera",     "url": "https://www.aljazeera.com/xml/rss/all.xml"},
    {"title": "Yonhap",         "url": "https://en.yna.co.kr/RSS/national.xml"},
    {"title": "BBC World News", "url": "https://feeds.bbci.co.uk/news/world/rss.xml"},
    {"title": "VOA中文",        "url": "https://www.voachinese.com/api/zqkotmveiq", "lang": "zh"},
]

MAX_PER_FEED = 5


@dataclass
class NewsArticle:
    title: str
    url: str
    source: str
    pub_date: str = ""
    summary: str = ""
    lang: str = "en"


def fetch_military_news(limit: int = 8) -> List[NewsArticle]:
    articles = []
    seen_titles = set()

    for feed_cfg in FEEDS:
        try:
            parsed = feedparser.parse(feed_cfg["url"])
            lang = feed_cfg.get("lang", "en")
            count = 0
            for entry in parsed.entries:
                if count >= MAX_PER_FEED:
                    break
                title = (entry.get("title") or "").strip()
                url = entry.get("link") or entry.get("url") or ""
                if not title or not url:
                    continue
                key = title.lower()
                if key in seen_titles:
                    continue
                seen_titles.add(key)
                summary = entry.get("summary") or entry.get("description") or ""
                pub_date = entry.get("published") or entry.get("updated") or ""
                articles.append(NewsArticle(
                    title=title, url=url, source=feed_cfg["title"],
                    pub_date=pub_date[:16], summary=summary[:300], lang=lang,
                ))
                count += 1
        except Exception as e:
            logger.warning(f"[rss_military] {feed_cfg['title']} failed: {e}")

    return articles[:limit]
