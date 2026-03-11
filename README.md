<div align="center">

# 🌍 Intel Briefing - 国际时事日报

**每天自动聚合全球新闻，生成中英双语日报。**

覆盖国际政治、经济金融、军事安全、社会人文、亚洲焦点、深度分析六大领域。

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/77AutumN/Intel_Briefing?style=social)](https://github.com/77AutumN/Intel_Briefing)

</div>

---

## 🤔 这是什么？

一个**开箱即用的国际新闻聚合引擎**。从 BBC、Reuters、AP、Al Jazeera、SCMP、Guardian、FT、NHK、Yonhap 等 20+ 免费 RSS 源并行抓取，用 Gemini 翻译英文条目，生成一份中英双语日报。

**适合谁用？**
- 想每天快速了解国际时事的读者
- 做地缘政治、宏观经济研究的分析师
- 关注亚洲动态的研究者和从业者
- 任何想打破信息茧房的人

---

## ✨ 六大板块

| 板块 | 数据源 |
|:--|:--|
| 🏛️ 国际政治与外交 | BBC · Reuters · AP · Al Jazeera · SCMP · NHK · BBC中文 · RFI中文 · VOA中文 |
| 💹 经济与金融 | Reuters · FT · Bloomberg · WSJ · The Economist · SCMP · BBC中文财经 |
| ⚔️ 军事与安全 | Defense News · Reuters · Al Jazeera · Yonhap · BBC · VOA中文 |
| 🌱 社会与人文 | The Guardian · UN News · AP · Al Jazeera · BBC中文 · RFI中文 |
| 🌏 亚洲焦点 | SCMP · NHK · Yonhap · Straits Times · BBC中文 · RFI中文 |
| 📖 深度分析 | Foreign Affairs · The Economist · Guardian Opinion · NYT Opinion · FT Opinion |

中文来源（BBC中文、RFI中文、VOA中文等）直接展示原文，英文来源通过 Gemini 翻译标题和摘要。

---

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/77AutumN/Intel_Briefing.git
cd Intel_Briefing
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API 密钥（可选）

```bash
cp .env.example .env
# 只需填入 GEMINI_API_KEY（用于翻译），不填也能运行
```

### 4. 运行

```bash
# 生成今日日报
python run_mission.py

# 快速测试（每源1条）
python cli.py --test

# 自定义条数
python cli.py --limit 5
```

报告保存在 `reports/daily_briefings/` 目录下。

### 5. 代理配置（可选）

```bash
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890
```

---

## 🔑 API 密钥说明

| 密钥 | 用途 | 是否必需 |
|:--|:--|:--|
| `GEMINI_API_KEY` | 英文条目中文翻译 | 可选，不填则展示英文原文 |

> 所有新闻数据源均为免费公开 RSS，无需任何付费 API。

---

## 📁 项目结构

```
Intel_Briefing/
├── run_mission.py              # 主入口：生成日报
├── cli.py                      # 命令行工具（支持 --test / --limit）
├── src/
│   ├── intel_collector.py      # 并行抓取协调器
│   ├── report_generator.py     # Markdown 报告生成
│   ├── config.py               # 统一配置
│   ├── sensors/                # RSS 传感器
│   │   ├── rss_politics.py     # 国际政治与外交
│   │   ├── rss_economics.py    # 经济与金融
│   │   ├── rss_military.py     # 军事与安全
│   │   ├── rss_society.py      # 社会与人文
│   │   ├── rss_asia.py         # 亚洲焦点
│   │   └── rss_analysis.py     # 深度分析
│   └── utils/
│       ├── gemini_translator.py # Gemini 翻译
│       └── jina_reader.py      # 网页全文提取（备用）
├── tests/
│   └── test_core.py            # 基础测试
├── reports/
│   └── daily_briefings/        # 生成的日报
└── .github/workflows/
    └── daily-report.yml        # 每日自动运行（UTC 23:51）
```

---

## 🤖 GitHub Actions 自动化

项目自带 `.github/workflows/daily-report.yml`，每天北京时间 07:51 自动生成日报并推送到 PWA 展示端。

只需在仓库 Secrets 中配置：
- `GEMINI_API_KEY` — 翻译用（可选）
- `PWA_DEPLOY_TOKEN` — 推送到展示仓库用

---

## 📄 License

MIT — 随便用，改了也不用告诉我。

---

<div align="center">

**如果觉得有用，给个 ⭐ 就是最大的支持。**

</div>
