"""
Intel Briefing - 基础测试
测试核心模块的基本功能，不依赖外部 API。
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestConfig:
    def test_config_imports(self):
        from src.config import setup_logging, GEMINI_API_URL, JINA_READER_URL
        assert GEMINI_API_URL.startswith("https://")
        assert JINA_READER_URL.startswith("https://")

    def test_rss_limits_defined(self):
        from src.config import (
            RSS_FETCH_TIMEOUT, RSS_MAX_PER_FEED,
            RSS_POLITICS_LIMIT, RSS_ECONOMICS_LIMIT,
            RSS_MILITARY_LIMIT, RSS_SOCIETY_LIMIT,
            RSS_ASIA_LIMIT, RSS_ANALYSIS_LIMIT,
        )
        assert RSS_FETCH_TIMEOUT > 0
        assert RSS_POLITICS_LIMIT > 0


class TestDedup:
    def test_dedup_removes_duplicates(self):
        from src.intel_collector import _dedup_items
        items = [
            {"title": "Hello World", "url": "a"},
            {"title": "hello world", "url": "b"},
            {"title": "Different", "url": "c"},
        ]
        result = _dedup_items(items)
        assert len(result) == 2

    def test_dedup_keeps_empty_titles(self):
        from src.intel_collector import _dedup_items
        items = [{"title": "", "url": "a"}, {"title": "", "url": "b"}]
        result = _dedup_items(items)
        assert len(result) == 2

    def test_dedup_empty_list(self):
        from src.intel_collector import _dedup_items
        assert _dedup_items([]) == []


class TestReportGenerator:
    def test_generate_empty_report(self):
        from src.report_generator import generate_report
        intel = {k: [] for k in ["politics", "economics", "military", "society", "asia", "analysis"]}
        report = generate_report(intel, "2026-01-01")
        assert "国际时事日报" in report
        assert "2026-01-01" in report
        assert "暂无数据" in report

    def test_generate_report_with_data(self):
        from src.report_generator import generate_report
        intel = {
            "politics": [
                {"title": "UN Summit", "url": "https://example.com", "source": "Reuters",
                 "pub_date": "2026-01-01", "summary": "World leaders meet.", "lang": "en"}
            ],
            "economics": [], "military": [], "society": [], "asia": [], "analysis": [],
        }
        report = generate_report(intel, "2026-01-01")
        assert "UN Summit" in report
        assert "https://example.com" in report

    def test_zh_articles_not_translated(self):
        from src.report_generator import generate_report
        intel = {
            "politics": [
                {"title": "联合国峰会", "url": "https://example.com", "source": "BBC中文",
                 "pub_date": "2026-01-01", "summary": "各国领导人会面。", "lang": "zh"}
            ],
            "economics": [], "military": [], "society": [], "asia": [], "analysis": [],
        }
        report = generate_report(intel, "2026-01-01")
        assert "联合国峰会" in report

    def test_all_six_sections_present(self):
        from src.report_generator import generate_report
        intel = {k: [] for k in ["politics", "economics", "military", "society", "asia", "analysis"]}
        report = generate_report(intel, "2026-01-01")
        for heading in ["国际政治与外交", "经济与金融", "军事与安全", "社会与人文", "亚洲焦点", "深度分析"]:
            assert heading in report


class TestSensorDataclasses:
    def test_news_article_defaults(self):
        from src.sensors.rss_politics import NewsArticle
        a = NewsArticle(title="Test", url="https://example.com", source="BBC")
        assert a.lang == "en"
        assert a.summary == ""

    def test_zh_article(self):
        from src.sensors.rss_politics import NewsArticle
        a = NewsArticle(title="标题", url="https://example.com", source="BBC中文", lang="zh")
        assert a.lang == "zh"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
