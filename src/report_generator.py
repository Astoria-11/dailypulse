#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Report Generator - 国际时事日报报告生成模块
"""

import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

try:
    from config import GEMINI_RATE_LIMIT_DELAY
except ImportError:
    try:
        from src.config import GEMINI_RATE_LIMIT_DELAY
    except ImportError:
        GEMINI_RATE_LIMIT_DELAY = 1.5

try:
    from utils.gemini_translator import translate_to_chinese
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

if not GEMINI_AVAILABLE:
    logger.info("Gemini translator not available, using original text.")
    def translate_to_chinese(text, max_chars=100):
        return text[:max_chars] + "..." if len(text) > max_chars else text


def _render_section(items, limit, section_label):
    """Render a news section. zh items shown as-is; en items translated if Gemini available."""
    lines = []
    if not items:
        lines.append("*暂无数据*\n")
        return lines

    for i, item in enumerate(items[:limit], 1):
        title = item.get("title", "Untitled")
        url = item.get("url", "#")
        source = item.get("source", "")
        pub_date = item.get("pub_date", "")
        summary = item.get("summary", "")
        lang = item.get("lang", "en")

        if lang == "zh":
            display_title = title
            display_summary = summary
        elif GEMINI_AVAILABLE:
            display_title = translate_to_chinese(title, max_chars=100)
            time.sleep(GEMINI_RATE_LIMIT_DELAY)
            display_summary = translate_to_chinese(summary, max_chars=300) if summary else ""
            if display_summary:
                time.sleep(GEMINI_RATE_LIMIT_DELAY)
        else:
            display_title = title
            display_summary = summary

        lines.append(f"### {i}. [{display_title}]({url})")
        if lang == "en" and display_title != title:
            lines.append(f"*{title}*")
        meta = f"📰 {source}"
        if pub_date:
            meta += f" | 📅 {pub_date}"
        lines.append(meta)
        if display_summary:
            lines.append(f"> {display_summary[:200]}")
        lines.append("")

    return lines


def generate_report(intel: dict, date_str: str) -> str:
    """Generate international news daily briefing in Markdown."""
    lines = [
        "# 🌍 国际时事日报 (World Affairs Daily Briefing)",
        f"**日期:** {date_str}",
        f"**生成时间:** {datetime.now().strftime('%H:%M')}",
        "**数据源:** BBC · Reuters · AP · SCMP · Guardian · FT · NHK · Yonhap · Al Jazeera · VOA中文 · RFI中文 · BBC中文",
        "",
        "---",
        "",
    ]

    sections = [
        ("politics",  "🏛️ 国际政治与外交 (International Politics & Diplomacy)", 10),
        ("economics", "💹 经济与金融 (Economics & Markets)",                     8),
        ("military",  "⚔️ 军事与安全 (Military & Security)",                    8),
        ("society",   "🌱 社会与人文 (Society & Humanitarian)",                  8),
        ("asia",      "🌏 亚洲焦点 (Asia Focus)",                               10),
        ("analysis",  "📖 深度分析 (Analysis & Opinion)",                        5),
    ]

    for key, heading, limit in sections:
        lines.append(f"## {heading}")
        lines.append("")
        lines.extend(_render_section(intel.get(key, []), limit, heading))

    lines.append("---")
    lines.append("*报告由 DailyPulse 自动生成*")

    return "\n".join(lines)


__all__ = ['generate_report']
