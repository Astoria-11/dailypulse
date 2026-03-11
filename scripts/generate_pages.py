#!/usr/bin/env python3
"""Convert today's daily report Markdown to a fancy index.html with Tab-based mobile UX."""
import sys
import datetime
import markdown

# --- 1. Setup ---
date = datetime.date.today().strftime("%Y-%m-%d")
date_display = datetime.date.today().strftime("%Y年%m月%d日")
report_path = f"reports/daily_briefings/Morning_Report_{date}.md"

try:
    with open(report_path, encoding="utf-8") as f:
        content = f.read()
except FileNotFoundError:
    print(f"Report not found: {report_path}", file=sys.stderr)
    sys.exit(1)

html_body = markdown.markdown(content, extensions=["tables", "fenced_code"])

# --- 2. Enhanced HTML Template ---
page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>DailyPulse · {date_display}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@500;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">

<style>
  :root {{
    --bg-body: #F3F4F6;
    --bg-card: #FFFFFF;
    --text-primary: #1F2937;
    --text-summary: #4B5563;
    --text-meta: #6B7280;
    --accent: #2563EB;
    --border-color: #E5E7EB;
    
    /* 头部深色背景 */
    --header-bg: #1e1b4b;
    --header-gradient: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
    
    --shadow-card: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    --shadow-hover: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    
    --font-serif: "Noto Serif SC", serif;
    --font-sans: "Inter", -apple-system, sans-serif;
  }}

  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg-body: #111827;
      --bg-card: #1F2937;
      --text-primary: #F9FAFB;
      --text-summary: #9CA3AF;
      --text-meta: #9CA3AF;
      --accent: #60A5FA;
      --border-color: #374151;
      --header-bg: #0f172a;
      --header-gradient: linear-gradient(to right, #0f172a, #1e293b);
      --shadow-card: none;
      --shadow-hover: 0 0 0 1px var(--accent);
    }}
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }}
  
  body {{
    background: var(--bg-body);
    color: var(--text-primary);
    font-family: var(--font-sans);
    line-height: 1.6;
    font-size: 15px;
    padding-bottom: 40px;
  }}

  /* --- Header --- */
  .site-header {{
    background: var(--header-gradient);
    color: #fff;
    padding: 2.5rem 1rem 5rem; /* 增加底部padding，为负margin留空间 */
    text-align: center;
    /* 桌面端稍微有点切角设计 */
    clip-path: ellipse(120% 100% at 50% 0%); 
    margin-bottom: 0;
  }}
  .site-header .brand {{ 
    font-size: 0.75rem; 
    letter-spacing: 0.15em; 
    text-transform: uppercase; 
    opacity: 0.7; 
    margin-bottom: 0.5rem; 
  }}
  .site-header h1 {{ 
    font-family: var(--font-serif);
    font-size: 2.2rem; 
    margin-bottom: 0.8rem;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
  }}
  .date-badge {{
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(4px);
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.85rem;
    display: inline-block;
  }}

  /* --- Layout Wrapper --- */
  .layout-container {{
    max-width: 1000px;
    margin: -50px auto 0; /* 负margin，让内容向上浮动覆盖Header */
    padding: 0 20px;
    display: grid;
    grid-template-columns: 220px 1fr;
    gap: 30px;
    position: relative;
    z-index: 10;
  }}

  /* --- Sidebar (Desktop) --- */
  .sidebar {{
    position: sticky;
    top: 20px;
    align-self: start;
    background: var(--bg-card);
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    border: 1px solid var(--border-color);
  }}
  .sidebar-title {{
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--text-meta);
    margin-bottom: 12px;
    padding-left: 8px;
    text-transform: uppercase;
  }}
  .nav-link {{
    display: flex;
    align-items: center;
    padding: 10px 12px;
    color: var(--text-summary);
    text-decoration: none;
    font-size: 0.95rem;
    border-radius: 8px;
    margin-bottom: 4px;
    transition: background 0.2s, color 0.2s;
    cursor: pointer;
  }}
  .nav-link:hover {{ background: var(--bg-body); color: var(--text-primary); }}
  
  /* 桌面端激活状态：左侧粗边框 + 背景色 */
  .layout-container:not(.mobile-mode) .nav-link.active {{
    background: #eff6ff; 
    color: var(--accent); 
    font-weight: 600;
  }}
  @media (prefers-color-scheme: dark) {{
    .layout-container:not(.mobile-mode) .nav-link.active {{ background: #1e293b; }}
  }}

  /* --- Main Content Area --- */
  #main-content {{
    min-width: 0;
    padding-top: 60px; /* 补偿负margin，让第一个h2不落在深色header上 */
  }}
  
  /* 桌面端：所有 Section 默认显示，通过滚动定位 */
  .section {{
    background: transparent; /* 桌面端Section本身不带背景，卡片带 */
    margin-bottom: 50px;
    scroll-margin-top: 20px; /* 防止锚点定位被遮挡 */
  }}
  
  .section-header h2 {{
    font-family: var(--font-serif);
    font-size: 1.5rem;
    color: var(--text-primary); /* 确保标题是深色，不被Header遮挡 */
    padding-bottom: 15px;
    margin-bottom: 20px;
    border-bottom: 2px solid var(--border-color);
    line-height: 1.3;
  }}

  /* --- Article Cards --- */
  .article-card {{
    background: var(--bg-card);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: var(--shadow-card);
    border: 1px solid var(--border-color);
    transition: transform 0.2s;
  }}
  .article-card:hover {{
    transform: translateY(-2px);
    box-shadow: var(--shadow-hover);
    border-color: var(--accent);
  }}

  .article-title {{
    font-family: var(--font-serif);
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 10px;
    line-height: 1.4;
    color: var(--text-primary);
  }}
  .article-title a {{ text-decoration: none; color: inherit; }}
  
  .article-summary {{
    font-size: 0.95rem;
    color: var(--text-summary);
    margin-bottom: 12px;
    line-height: 1.5;
  }}

  .article-meta {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 16px;
    font-size: 0.75rem;
  }}
  .meta-pill {{
    background: var(--bg-body);
    color: var(--text-meta);
    padding: 2px 8px;
    border-radius: 4px;
    border: 1px solid var(--border-color);
  }}

  .article-content {{
    border-left: 3px solid var(--accent);
    padding-left: 14px;
    margin-top: 12px;
    font-size: 1rem;
    color: var(--text-primary);
    line-height: 1.7;
  }}
  
  footer {{
    text-align: center;
    font-size: 0.8rem;
    color: var(--text-meta);
    margin-top: 40px;
  }}

  /* --- MOBILE OPTIMIZATION (Tab Switcher Mode) --- */
  @media (max-width: 768px) {{
    .layout-container {{
      display: block; /* 取消 Grid */
      margin-top: -30px; /* 上移幅度减小 */
      padding: 0;
    }}
    
    .site-header {{
        padding-bottom: 4rem; /* 减小留白 */
        clip-path: none; /* 手机上去除圆弧，节省空间 */
    }}
    
    /* 1. 顶部固定导航栏 (Sticky Tabs) */
    .sidebar {{
        position: sticky;
        top: 0;
        z-index: 100;
        border-radius: 0;
        border: none;
        border-bottom: 1px solid var(--border-color);
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(10px);
        margin: 0;
        padding: 0;
        overflow-x: auto;
        white-space: nowrap;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        
        /* 隐藏滚动条 */
        -ms-overflow-style: none;
        scrollbar-width: none;
    }}
    @media (prefers-color-scheme: dark) {{
        .sidebar {{ background: rgba(31, 41, 55, 0.98); }}
    }}
    .sidebar::-webkit-scrollbar {{ display: none; }}

    .sidebar-title {{ display: none; }}

    .sidebar nav {{
        display: flex;
        padding: 0 16px;
    }}

    .nav-link {{
        display: inline-block;
        padding: 14px 16px;
        margin: 0;
        font-size: 0.9rem;
        background: transparent !important;
        border-radius: 0;
        color: var(--text-summary);
        border-bottom: 2px solid transparent;
        flex-shrink: 0;
    }}
    
    /* 手机端激活状态：下划线 */
    .nav-link.active {{
        color: var(--accent) !important;
        border-bottom-color: var(--accent);
        font-weight: 600;
        background: transparent !important;
    }}

    /* 2. 内容区域：Tab 切换模式 */
    #main-content {{
        padding: 20px 16px;
        background: var(--bg-body);
        min-height: 60vh;
    }}
    
    /* 手机端只显示激活的 section，其他的 display: none */
    .section {{
        display: none; 
        animation: fadeIn 0.3s ease;
    }}
    .section.active-tab {{
        display: block;
    }}
    
    /* 手机端标题调整 */
    .section-header h2 {{
        font-size: 1.3rem;
        margin-top: 0;
        padding-top: 0;
    }}
    
    .article-card {{
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(5px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
  }}
</style>
</head>
<body>

<header class="site-header">
  <div class="brand">DailyPulse</div>
  <h1>🌍 国际时事日报</h1>
  <div class="date-badge">📅 {date_display}</div>
</header>

<div class="layout-container" id="layout-container">
  <aside class="sidebar">
    <div class="sidebar-title">板块导航</div>
    <nav id="sidebar-nav"></nav>
  </aside>

  <main id="main-content"></main>
</div>

<footer>
  Generated by DailyPulse AI · {date}
</footer>

<div id="raw-content" style="display:none">{html_body}</div>

<script>
(function() {{
  const raw = document.getElementById('raw-content');
  const main = document.getElementById('main-content');
  const nav = document.getElementById('sidebar-nav');
  const layout = document.getElementById('layout-container');
  
  // 判断是否是移动端
  const isMobile = window.innerWidth <= 768;
  if(isMobile) {{
      layout.classList.add('mobile-mode');
  }}

  const labelMap = {{
    '🏛': '政治外交', '💹': '经济金融', '⚔': '军事安全',
    '🌱': '社会人文', '🌏': '亚洲焦点', '📖': '深度分析'
  }};
  
  function getShortLabel(text) {{
    for (const [emoji, label] of Object.entries(labelMap)) {{
      if (text.includes(emoji)) return emoji + ' ' + label;
    }}
    return text.replace(/<[^>]+>/g, '').trim().slice(0, 8);
  }}

  // 1. Parsing
  const nodes = Array.from(raw.childNodes);
  let currentSection = null;
  const sections = [];

  nodes.forEach(node => {{
    if (node.nodeType !== 1) return;
    if (node.tagName === 'H2') {{
      currentSection = {{ title: node.innerHTML, articles: [] }};
      sections.push(currentSection);
    }} else if (node.tagName === 'H3' && currentSection) {{
      currentSection.articles.push({{ title: node, elements: [] }});
    }} else if (currentSection && currentSection.articles.length > 0) {{
      currentSection.articles[currentSection.articles.length - 1].elements.push(node);
    }}
  }});

  // 2. Building DOM
  sections.forEach((sec, idx) => {{
    const secID = 'sec-' + idx;
    
    // Section Container
    const sectionEl = document.createElement('div');
    sectionEl.className = 'section';
    sectionEl.id = secID;
    
    // Header
    const headerEl = document.createElement('div');
    headerEl.className = 'section-header';
    headerEl.innerHTML = `<h2>${{sec.title}}</h2>`;
    sectionEl.appendChild(headerEl);
    
    // Articles
    sec.articles.forEach(art => {{
      const card = document.createElement('div');
      card.className = 'article-card';
      
      const titleDiv = document.createElement('div');
      titleDiv.className = 'article-title';
      titleDiv.innerHTML = art.title.innerHTML;
      card.appendChild(titleDiv);
      
      art.elements.forEach(el => {{
        const text = el.textContent.trim();
        // A. Content (Blockquote)
        if (el.tagName === 'BLOCKQUOTE') {{
          const contentDiv = document.createElement('div');
          contentDiv.className = 'article-content';
          contentDiv.innerHTML = el.innerHTML;
          card.appendChild(contentDiv);
        }} 
        // B. Meta (BBC/Date) - Check for icons or keywords
        else if (text.includes('BBC') || text.includes('📅') || text.includes('📰')) {{
          const metaDiv = document.createElement('div');
          metaDiv.className = 'article-meta';
          const parts = text.split('|');
          parts.forEach(p => {{
            const pill = document.createElement('span');
            pill.className = 'meta-pill';
            pill.innerHTML = p.trim();
            metaDiv.appendChild(pill);
          }});
          card.appendChild(metaDiv);
        }}
        // C. English Summary (Subtitle)
        else if (text.length > 0) {{
          const summaryDiv = document.createElement('div');
          summaryDiv.className = 'article-summary';
          summaryDiv.innerHTML = el.innerHTML;
          card.appendChild(summaryDiv);
        }}
      }});
      sectionEl.appendChild(card);
    }});
    
    main.appendChild(sectionEl);
    
    // Nav Link
    const link = document.createElement('a');
    // Mobile uses data-target only, desktop uses href anchor
    link.href = isMobile ? 'javascript:void(0)' : '#' + secID;
    link.className = 'nav-link';
    link.innerHTML = getShortLabel(sec.title);
    link.dataset.target = secID;
    
    link.onclick = (e) => {{
        if(isMobile) {{
            e.preventDefault();
            switchTab(secID);
        }} else {{
            // Desktop: default anchor behavior works fine, but we can smooth scroll
            e.preventDefault();
            document.getElementById(secID).scrollIntoView({{ behavior: 'smooth' }});
        }}
    }};
    nav.appendChild(link);
  }});

  // 3. Logic for Tab Switching vs Scrolling
  const navLinks = Array.from(document.querySelectorAll('.nav-link'));
  const sectionEls = Array.from(document.querySelectorAll('.section'));

  function switchTab(targetId) {{
      // Update Nav
      navLinks.forEach(l => l.classList.remove('active'));
      const activeLink = navLinks.find(l => l.dataset.target === targetId);
      if(activeLink) {{
          activeLink.classList.add('active');
          activeLink.scrollIntoView({{ behavior: 'smooth', block: 'nearest', inline: 'center' }});
      }}

      // Update Content (Mobile Only)
      sectionEls.forEach(el => {{
          if (el.id === targetId) {{
              el.classList.add('active-tab');
          }} else {{
              el.classList.remove('active-tab');
          }}
      }});
      
      // Scroll to top of content
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
  }}

  if (isMobile) {{
      // Initialize first tab
      if(sectionEls.length > 0) {{
          switchTab(sectionEls[0].id);
      }}
  }} else {{
      // Desktop Scroll Spy
      const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
          if (entry.isIntersecting) {{
            navLinks.forEach(l => l.classList.remove('active'));
            const activeLink = navLinks.find(l => l.dataset.target === entry.target.id);
            if (activeLink) activeLink.classList.add('active');
          }}
        }});
      }}, {{ rootMargin: '-10% 0px -80% 0px' }});
      sectionEls.forEach(el => observer.observe(el));
      if(navLinks.length > 0) navLinks[0].classList.add('active');
  }}

}})();
</script>

</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(page)
print(f"Index.html generated for {date}")
