#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RSS Politics Sensor - 国际政治与外交
"""

import logging
import feedparser
from dataclasses import dataclass, field
from typing import List

logger = logging.getLogger(__name__)

FEEDS = [
    {"title": "BBC World News",  "url": "https://feeds.bbci.co.uk/news/world/rss.xml"},
    {"title": "Reuters World",   "url": "https://feeds.reuters.com/reuters/worldNews"},
    {"title": "AP Top News",     "url": "https://rsshub.app/apnews/topics/apf-topnews"},
    {"title": "Al Jazeera",      "url": "https://www.aljazeera.com/xml/rss/all.xml"},
    {"title": "SCMP World",      "url": "https://www.scmp.com/rss/2/feed"},
    {"title": "NHK World",       "url": "https://www3.nhk.or.jp/rss/news/cat0.xml"},
    {"title": "BBC中文",         "url": "https://feeds.bbci.co.uk/zhongwen/simp/world/rss.xml", "lang": "zh"},
    {"title": "RFI中文",         "url": "https://www.rfi.fr/cn/rss",                            "lang": "zh"},
    {"title": "VOA中文",         "url": "https://www.voachinese.com/api/zqkotmveiq",            "lang": "zh"},
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


def fetch_politics_news(limit: int = 10) -> List[NewsArticle]:
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
            logger.warning(f"[rss_politics] {feed_cfg['title']} failed: {e}")

    return articles[:limit]
