#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RSS Analysis Sensor - 深度分析与评论
"""

import logging
import feedparser
from dataclasses import dataclass
from typing import List

logger = logging.getLogger(__name__)

FEEDS = [
    {"title": "Foreign Affairs",  "url": "https://www.foreignaffairs.com/rss.xml"},
    {"title": "The Economist",    "url": "https://www.economist.com/international/rss.xml"},
    {"title": "Guardian Opinion", "url": "https://www.theguardian.com/commentisfree/rss"},
    {"title": "NYT Opinion",      "url": "https://rss.nytimes.com/services/xml/rss/nyt/Opinion.xml"},
    {"title": "FT Opinion",       "url": "https://www.ft.com/opinion?format=rss"},
    {"title": "BBC中文评论",      "url": "https://feeds.bbci.co.uk/zhongwen/simp/world/rss.xml", "lang": "zh"},
]

MAX_PER_FEED = 3


@dataclass
class NewsArticle:
    title: str
    url: str
    source: str
    pub_date: str = ""
    summary: str = ""
    lang: str = "en"


def fetch_analysis_news(limit: int = 6) -> List[NewsArticle]:
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
            logger.warning(f"[rss_analysis] {feed_cfg['title']} failed: {e}")

    return articles[:limit]
