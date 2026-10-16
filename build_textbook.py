#!/usr/bin/env python3
import os
import re
import markdown

WORKSPACE = "/Users/notlimitedguy/Documents/SPbU"
SUPER_DIR = os.path.join(WORKSPACE, "Super_Textbook")

VOLUMES = [
    {
        "id": "algebra1",
        "title": "ОАиТЧ (1 сем)",
        "icon": "📘",
        "file": "01_Основы_алгебры_и_теории_чисел.md",
        "header_title": "Том 1: Основы алгебры и теории чисел (I семестр)",
        "subtitle": "22 экзаменационных билета коллоквиума: от наивной теории множеств до теоремы Эйлера и КТО"
    },
    {
        "id": "analysis1",
        "title": "Матанализ (1 сем)",
        "icon": "📗",
        "file": "02_Математический_анализ_1_семестр.md",
        "header_title": "Том 2: Математический анализ (I семестр)",
        "subtitle": "83 экзаменационных вопроса: супремумы, пределы последовательностей и функций, число e, непрерывность, производные и формула Тейлора"
    },
    {
        "id": "discrete",
        "title": "Дискретная математика",
        "icon": "📙",
        "file": "03_Дискретная_математика.md",
        "header_title": "Том 3: Дискретная математика (Осень 2025)",
        "subtitle": "18 экзаменационных билетов: булеаны, частичные порядки, расписания, теорема Дилуорса, LIS O(n log n), числа Стирлинга/Белла, производящие функции, Монти Холл и Alias-метод Вокера O(1)"
    },
    {
        "id": "linalg2",
        "title": "Линал и поля (2 сем)",
        "icon": "📕",
        "file": "04_Линейная_алгебра_и_поля_2_семестр.md",
        "header_title": "Том 4: Линейная алгебра и теория полей (II семестр)",
        "subtitle": "25 экзаменационных билетов: формула Грассмана, ФСР, операторы, закон инерции Сильвестра, поля Галуа, эндоморфизм Фробениуса и теорема Гамильтона-Кэли"
    },
    {
        "id": "geom",
        "title": "Аффинная геометрия",
        "icon": "📓",
        "file": "05_Аналитическая_и_аффинная_геометрия.md",
        "header_title": "Том 5: Аналитическая и аффинная геометрия",
        "subtitle": "Аксиомы Вейля, аффинные реперы, барицентрические координаты в симплексе и аффинные подпространства"
    },
    {
        "id": "cheat",
        "title": "Шпаргалка и навигатор",
        "icon": "🎯",
        "file": "06_Шпаргалка_и_Экзаменационный_навигатор.md",
        "header_title": "Том 6: Экзаменационный навигатор и супер-шпаргалка",
        "subtitle": "Сводная матрица всех билетов, ключевые идеи, формулы и типичные ловушки на экзамене"
    }
]

def preprocess_markdown(text, vol_id):
    lines = text.split('\n')
    processed_lines = []
    in_proof = False
    proof_lines = []
    
    proof_header_pattern = re.compile(r'^(#{3,5})\s*📝\s*(.*)$')
    
    for line in lines:
        match = proof_header_pattern.match(line)
        if match and not in_proof:
            in_proof = True
            title = match.group(2).strip()
            if not title:
                title = "Строгое доказательство"
            proof_lines = [
                f'<details class="proof-box" open>',
                f'<summary><span class="proof-icon">📜</span> <strong>{title}</strong> <span class="proof-badge">кликните, чтобы скрыть</span></summary>',
                f'<div class="proof-content">'
            ]
            continue
            
        if in_proof:
            if line.startswith('# ') or line.startswith('## ') or line.startswith('### ') or line.startswith('---'):
                proof_lines.append('</div></details>\n')
                processed_lines.extend(proof_lines)
                in_proof = False
                proof_lines = []
                processed_lines.append(line)
                continue
            elif r'\blacksquare' in line:
                proof_lines.append(line)
                proof_lines.append('</div></details>\n')
                processed_lines.extend(proof_lines)
                in_proof = False
                proof_lines = []
                continue
            else:
                proof_lines.append(line)
                continue
                
        processed_lines.append(line)
        
    if in_proof:
        proof_lines.append('</div></details>\n')
        processed_lines.extend(proof_lines)
        
    text = '\n'.join(processed_lines)
    
    # Transform alerts
    lines = text.split('\n')
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        alert_m = re.match(r'^>\s*\[!(NOTE|IMPORTANT|TIP|WARNING|CAUTION)\]\s*$', line)
        if alert_m:
            alert_type = alert_m.group(1)
            i += 1
            body_acc = []
            while i < len(lines) and lines[i].startswith('>'):
                body_acc.append(re.sub(r'^>\s?', '', lines[i]))
                i += 1
            
            css_class = "callout-thm"
            title = "Теорема / Утверждение"
            icon = "⚡"
            if alert_type == "IMPORTANT":
                css_class = "callout-def"
                title = "Определение / Важный принцип"
                icon = "📐"
            elif alert_type == "TIP":
                css_class = "callout-intuition"
                title = "Интуиция / Ментальная модель"
                icon = "💡"
            elif alert_type in ("WARNING", "CAUTION"):
                css_class = "callout-trap"
                title = "Ловушка на экзамене / Внимание!"
                icon = "⚠️"
                
            body_md = '\n'.join(body_acc)
            body_html = markdown.markdown(body_md, extensions=['tables', 'fenced_code'])
            new_lines.append(f'<div class="callout {css_class}"><div class="callout-title">{icon} {title}</div><div class="callout-body">{body_html}</div></div>\n')
        else:
            new_lines.append(line)
            i += 1
            
    return '\n'.join(new_lines)

def build_toc_and_html():
    compiled_volumes = []
    
    for vol in VOLUMES:
        filepath = os.path.join(SUPER_DIR, vol["file"])
        if not os.path.exists(filepath):
            print(f"Warning: {filepath} does not exist!")
            continue
            
        with open(filepath, "r", encoding="utf-8") as f:
            raw_md = f.read()
            
        preprocessed = preprocess_markdown(raw_md, vol["id"])
        
        toc_items = []
        heading_pattern = re.compile(r'^(#{1,4})\s+(.+)$', re.MULTILINE)
        anchor_counter = {}
        
        def replace_heading(m):
            level = len(m.group(1))
            heading_text = m.group(2).strip()
            
            clean_anchor = re.sub(r'[\$\{\}\\\(\)\+\*\?\^\/\|\:\,\.\'\"«»—\[\]]', '', heading_text)
            clean_anchor = re.sub(r'\s+', '-', clean_anchor).strip('-').lower()
            if not clean_anchor:
                clean_anchor = f"sec-{len(toc_items)}"
                
            count = anchor_counter.get(clean_anchor, 0) + 1
            anchor_counter[clean_anchor] = count
            if count > 1:
                anchor_id = f"{vol['id']}-{clean_anchor}-{count}"
            else:
                anchor_id = f"{vol['id']}-{clean_anchor}"
                
            is_ticket = "Билет" in heading_text or "Вопрос" in heading_text
            is_chapter = "Глава" in heading_text or "Модуль" in heading_text
            
            if level <= 3:
                toc_items.append({
                    "id": anchor_id,
                    "title": heading_text,
                    "level": level,
                    "is_ticket": is_ticket,
                    "is_chapter": is_chapter
                })
                
            return f'<h{level} id="{anchor_id}">{heading_text}</h{level}>'
            
        html_with_ids = heading_pattern.sub(replace_heading, preprocessed)
        body_html = markdown.markdown(html_with_ids, extensions=['tables', 'fenced_code'])
        
        compiled_volumes.append({
            "meta": vol,
            "toc": toc_items,
            "html": body_html
        })
        
    return compiled_volumes

def generate_full_html():
    volumes = build_toc_and_html()
    print(f"Generated {len(volumes)} volumes.")
    
    # Build TOC HTML
    toc_html = []
    for vol_idx, v in enumerate(volumes):
        vol_id = v["meta"]["id"]
        vol_title = v["meta"]["title"]
        vol_icon = v["meta"]["icon"]
        
        toc_html.append(f'<div class="toc-group" data-cat="{vol_id}" id="toc-group-{vol_id}">')
        toc_html.append(f'  <div class="toc-group-header" onclick="toggleTocGroup(\'{vol_id}\')">')
        toc_html.append(f'    <span class="toc-group-icon">{vol_icon}</span>')
        toc_html.append(f'    <span class="toc-group-name">{vol_title}</span>')
        toc_html.append(f'    <span class="toc-group-badge">{len(v["toc"])} тем</span>')
        toc_html.append(f'  </div>')
        toc_html.append(f'  <div class="toc-links-wrapper">')
        
        for item in v["toc"]:
            link_class = "toc-link"
            if item["is_ticket"]:
                link_class += " toc-link-ticket"
            elif item["is_chapter"]:
                link_class += " toc-link-chapter"
            elif item["level"] == 1:
                link_class += " toc-link-h1"
            elif item["level"] == 2:
                link_class += " toc-link-h2"
            else:
                link_class += " toc-link-h3"
                
            toc_html.append(f'    <a href="#{item["id"]}" class="{link_class}" onclick="handleNavClick(event, \'{vol_id}\', \'{item["id"]}\')">{item["title"]}</a>')
            
        toc_html.append(f'  </div>')
        toc_html.append(f'</div>')
        
    toc_str = '\n'.join(toc_html)
    
    # Build Sections HTML
    content_html = []
    for idx, v in enumerate(volumes):
        vol_id = v["meta"]["id"]
        vol_title = v["meta"]["header_title"]
        vol_subtitle = v["meta"]["subtitle"]
        vol_icon = v["meta"]["icon"]
        
        # Display the first section by default, others hide until clicked or 'all' is chosen
        initial_style = "display: block;" if idx == 0 else "display: none;"
        
        content_html.append(f'<section class="volume-section" id="section-{vol_id}" data-cat="{vol_id}" style="{initial_style}">')
        content_html.append(f'  <header class="volume-banner">')
        content_html.append(f'    <div class="volume-badge">{vol_icon} {v["meta"]["title"]}</div>')
        content_html.append(f'    <h1 class="volume-main-title">{vol_title}</h1>')
        content_html.append(f'    <p class="volume-desc">{vol_subtitle}</p>')
        content_html.append(f'  </header>')
        content_html.append(f'  <div class="volume-content-body">')
        content_html.append(v["html"])
        content_html.append(f'  </div>')
        content_html.append(f'</section>')
        
    content_str = '\n'.join(content_html)
    
    full_page = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>СПбГУ Матмех | Фундаментальный суперучебник по Высшей математике</title>
  
  <!-- KaTeX for fast Math typesetting -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&family=Inter:wght@300;400;500;600;700;800&family=Merriweather:ital,wght@0,300;0,400;0,700;1,300&display=swap" rel="stylesheet">

  <style>
    :root {{
      --bg-primary: #ffffff;
      --bg-secondary: #f8fafc;
      --bg-tertiary: #f1f5f9;
      --border-color: #e2e8f0;
      --text-main: #0f172a;
      --text-muted: #64748b;
      --accent: #2563eb;
      --accent-hover: #1d4ed8;
      --accent-light: #eff6ff;
      --sidebar-width: 320px;
      
      --callout-def-bg: #f5f3ff;
      --callout-def-border: #8b5cf6;
      --callout-thm-bg: #ecfdf5;
      --callout-thm-border: #10b981;
      --callout-trap-bg: #fff1f2;
      --callout-trap-border: #f43f5e;
      --callout-intuition-bg: #eff6ff;
      --callout-intuition-border: #3b82f6;
    }}

    [data-theme="dark"] {{
      --bg-primary: #0b0f19;
      --bg-secondary: #111827;
      --bg-tertiary: #1f2937;
      --border-color: #374151;
      --text-main: #f9fafb;
      --text-muted: #9ca3af;
      --accent: #3b82f6;
      --accent-hover: #60a5fa;
      --accent-light: #1e293b;
      
      --callout-def-bg: #1e1b4b;
      --callout-def-border: #a78bfa;
      --callout-thm-bg: #064e3b;
      --callout-thm-border: #34d399;
      --callout-trap-bg: #4c0519;
      --callout-trap-border: #fb7185;
      --callout-intuition-bg: #172554;
      --callout-intuition-border: #60a5fa;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    
    html, body {{
      height: 100%;
      background-color: var(--bg-primary);
      color: var(--text-main);
      font-family: 'Inter', system-ui, -apple-system, sans-serif;
      line-height: 1.75;
      font-size: 15.5px;
      overflow: hidden;
      -webkit-font-smoothing: antialiased;
    }}

    /* Global layout */
    #app-layout {{
      display: flex;
      height: 100vh;
      width: 100vw;
      overflow: hidden;
      position: relative;
    }}

    /* Reading Progress Bar */
    #progress-container {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 3px;
      background: transparent;
      z-index: 1000;
      pointer-events: none;
    }}
    #progress-bar {{
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, #3b82f6, #8b5cf6, #10b981);
      transition: width 0.05s linear;
      transform: translateZ(0);
    }}

    /* Mobile drawer backdrop */
    #drawer-backdrop {{
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.5);
      z-index: 800;
      opacity: 0;
      transition: opacity 0.2s ease;
    }}
    #drawer-backdrop.active {{
      display: block;
      opacity: 1;
    }}

    /* Sidebar Navigation */
    #sidebar {{
      width: var(--sidebar-width);
      min-width: var(--sidebar-width);
      height: 100vh;
      background: var(--bg-secondary);
      border-right: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      z-index: 900;
      transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      transform: translateZ(0);
      will-change: transform;
    }}

    .sidebar-header {{
      padding: 16px 18px;
      border-bottom: 1px solid var(--border-color);
      background: var(--bg-secondary);
      flex-shrink: 0;
    }}

    .univ-tag {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--accent);
      background: var(--accent-light);
      padding: 3px 8px;
      border-radius: 6px;
      margin-bottom: 6px;
    }}

    .sidebar-title {{
      font-size: 15px;
      font-weight: 800;
      color: var(--text-main);
      line-height: 1.3;
    }}

    .sidebar-sub {{
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 2px;
    }}

    .search-wrapper {{
      margin-top: 10px;
      position: relative;
    }}

    .search-input {{
      width: 100%;
      padding: 8px 12px 8px 32px;
      border-radius: 8px;
      border: 1px solid var(--border-color);
      background: var(--bg-primary);
      color: var(--text-main);
      font-size: 13px;
      outline: none;
      transition: border-color 0.15s;
    }}
    .search-input:focus {{
      border-color: var(--accent);
    }}
    .search-icon-svg {{
      position: absolute;
      left: 10px;
      top: 9px;
      width: 15px;
      height: 15px;
      stroke: var(--text-muted);
    }}

    .toc-scroll {{
      flex: 1;
      overflow-y: auto;
      padding: 10px 8px 30px 8px;
      -webkit-overflow-scrolling: touch;
      contain: content;
    }}

    .toc-group {{
      margin-bottom: 12px;
      border-radius: 6px;
    }}

    .toc-group-header {{
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 7px 10px;
      font-size: 12.5px;
      font-weight: 700;
      color: var(--text-main);
      background: var(--bg-tertiary);
      border-radius: 6px;
      cursor: pointer;
      user-select: none;
    }}

    .toc-group-name {{
      flex: 1;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .toc-group-badge {{
      font-size: 11px;
      color: var(--text-muted);
      font-weight: 500;
    }}

    .toc-links-wrapper {{
      padding: 3px 0 3px 4px;
    }}

    .toc-link {{
      display: block;
      padding: 4px 8px;
      border-radius: 5px;
      color: var(--text-muted);
      text-decoration: none;
      font-size: 12px;
      line-height: 1.4;
      margin-bottom: 1px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      transition: background 0.1s, color 0.1s;
    }}
    .toc-link:hover {{
      background: var(--bg-tertiary);
      color: var(--accent);
    }}

    .toc-link-ticket {{
      font-weight: 600;
      color: var(--text-main);
    }}
    .toc-link-chapter {{
      font-weight: 700;
      color: var(--accent);
      margin-top: 4px;
      border-left: 2px solid var(--accent);
      border-radius: 0 4px 4px 0;
    }}

    /* =========================================================
       PERFORMANCE ENGINE: 120 FPS BUTTER SMOOTH SCROLLING
       ========================================================= */

    /* Main Content Viewport */
    #main-content {{
      flex: 1;
      height: 100vh;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      position: relative;
      scroll-behavior: smooth;
      -webkit-overflow-scrolling: touch;
      transform: translateZ(0);
      will-change: scroll-position;
    }}

    /* Modern CSS Content-Visibility: Browser completely skips off-screen rendering */
    .volume-section {{
      content-visibility: auto;
      contain-intrinsic-size: 1px 1500px;
      margin-bottom: 40px;
    }}

    .callout, details.proof-box {{
      content-visibility: auto;
      contain-intrinsic-size: 1px 180px;
    }}

    /* Top Sticky Navigation: SOLID background, NO expensive backdrop-filter */
    .top-navbar {{
      height: 56px;
      min-height: 56px;
      background: var(--bg-primary);
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
      position: sticky;
      top: 0;
      z-index: 500;
      gap: 10px;
      transform: translateZ(0);
    }}

    .nav-left {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex: 1;
      overflow: hidden;
    }}

    .mobile-menu-btn {{
      display: none;
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 6px 10px;
      border-radius: 7px;
      font-size: 16px;
      cursor: pointer;
      line-height: 1;
    }}

    /* Horizontal Subject Pills */
    .subject-tabs {{
      display: flex;
      align-items: center;
      gap: 5px;
      overflow-x: auto;
      white-space: nowrap;
      padding: 2px 0;
      -webkit-overflow-scrolling: touch;
      scrollbar-width: none;
    }}
    .subject-tabs::-webkit-scrollbar {{
      display: none;
    }}

    .tab-btn {{
      padding: 5px 11px;
      border-radius: 16px;
      border: 1px solid var(--border-color);
      background: var(--bg-secondary);
      color: var(--text-muted);
      font-size: 12.5px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: background 0.15s, color 0.15s, border-color 0.15s;
      user-select: none;
    }}
    .tab-btn:hover {{
      background: var(--bg-tertiary);
      color: var(--text-main);
    }}
    .tab-btn.active {{
      background: var(--accent);
      color: #ffffff;
      border-color: var(--accent);
    }}

    .nav-actions {{
      display: flex;
      align-items: center;
      gap: 6px;
      flex-shrink: 0;
    }}

    .btn-action {{
      padding: 6px 10px;
      border-radius: 7px;
      border: 1px solid var(--border-color);
      background: var(--bg-secondary);
      color: var(--text-main);
      font-size: 12.5px;
      font-weight: 500;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: background 0.15s;
    }}
    .btn-action:hover {{
      background: var(--bg-tertiary);
    }}
    .btn-action.active {{
      background: #f59e0b;
      color: #000000;
      border-color: #f59e0b;
      font-weight: 700;
    }}

    /* Article Reader Layout */
    .article-container {{
      max-width: 900px;
      width: 100%;
      margin: 0 auto;
      padding: 28px 24px 100px 24px;
      box-sizing: border-box;
    }}

    /* Volume Banner */
    .volume-banner {{
      background: linear-gradient(135deg, #1e293b, #0f172a);
      color: #ffffff;
      border-radius: 14px;
      padding: 26px 24px;
      margin-bottom: 32px;
      border: 1px solid var(--border-color);
    }}
    [data-theme="dark"] .volume-banner {{
      background: linear-gradient(135deg, #111827, #1f2937);
    }}

    .volume-badge {{
      display: inline-block;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      background: rgba(255, 255, 255, 0.16);
      padding: 3px 10px;
      border-radius: 16px;
      margin-bottom: 10px;
    }}

    .volume-main-title {{
      font-size: clamp(20px, 3.2vw, 28px);
      font-weight: 800;
      line-height: 1.25;
      margin: 0 0 8px 0;
      color: #ffffff !important;
    }}

    .volume-desc {{
      font-size: 14px;
      color: #cbd5e1;
      margin: 0;
      line-height: 1.5;
    }}

    /* Typography inside textbook */
    h1, h2, h3, h4 {{
      color: var(--text-main);
      font-weight: 700;
      line-height: 1.35;
      scroll-margin-top: 70px;
    }}
    
    h1 {{
      font-size: 24px;
      margin: 40px 0 18px 0;
      padding-bottom: 8px;
      border-bottom: 2px solid var(--border-color);
    }}

    h2 {{
      font-size: 20px;
      margin: 32px 0 14px 0;
    }}

    h3 {{
      font-size: 17px;
      margin: 24px 0 12px 0;
      color: var(--accent);
    }}

    p {{
      margin-bottom: 12px;
      font-size: 15.5px;
    }}

    ul, ol {{
      margin: 10px 0 14px 22px;
    }}
    li {{
      margin-bottom: 5px;
    }}

    hr {{
      border: 0;
      height: 1px;
      background: var(--border-color);
      margin: 32px 0;
    }}

    /* Tables with Horizontal Scroll Wrapper */
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 18px 0;
      font-size: 13.5px;
    }}
    th, td {{
      padding: 9px 12px;
      border: 1px solid var(--border-color);
      text-align: left;
    }}
    th {{
      background: var(--bg-tertiary);
      font-weight: 700;
    }}

    /* Callouts (Definitions, Theorems, Traps, Intuition) */
    .callout {{
      border-radius: 10px;
      padding: 16px 20px;
      margin: 20px 0;
      border-left: 5px solid;
      background-color: var(--bg-secondary);
    }}
    .callout-title {{
      font-weight: 800;
      font-size: 13.5px;
      margin-bottom: 6px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .callout-body p:last-child {{
      margin-bottom: 0;
    }}

    .callout-thm {{
      background-color: var(--callout-thm-bg);
      border-color: var(--callout-thm-border);
    }}
    .callout-def {{
      background-color: var(--callout-def-bg);
      border-color: var(--callout-def-border);
    }}
    .callout-trap {{
      background-color: var(--callout-trap-bg);
      border-color: var(--callout-trap-border);
    }}
    .callout-intuition {{
      background-color: var(--callout-intuition-bg);
      border-color: var(--callout-intuition-border);
    }}

    /* Interactive Proof Box */
    details.proof-box {{
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      margin: 20px 0;
      overflow: hidden;
    }}

    details.proof-box summary {{
      padding: 11px 16px;
      font-weight: 600;
      font-size: 14px;
      cursor: pointer;
      user-select: none;
      color: var(--accent);
      background: var(--bg-tertiary);
      display: flex;
      align-items: center;
      gap: 7px;
    }}
    details.proof-box summary:hover {{
      background: var(--accent-light);
    }}
    .proof-badge {{
      margin-left: auto;
      font-size: 11px;
      font-weight: 400;
      color: var(--text-muted);
    }}

    .proof-content {{
      padding: 20px 22px;
      border-top: 1px solid var(--border-color);
      font-family: 'Merriweather', Georgia, serif;
      font-size: 14.5px;
      line-height: 1.8;
      background: var(--bg-primary);
    }}

    /* KaTeX responsive formula protection: NEVER BLOW OUT MOBILE */
    .katex-display {{
      overflow-x: auto !important;
      overflow-y: hidden !important;
      padding: 6px 0 !important;
      max-width: 100% !important;
      -webkit-overflow-scrolling: touch !important;
      contain: content;
    }}

    /* Responsive Design for Mobile Devices */
    @media (max-width: 900px) {{
      #sidebar {{
        position: fixed;
        top: 0;
        left: 0;
        height: 100vh;
        transform: translateX(-100%);
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.2);
      }}
      #sidebar.drawer-open {{
        transform: translateX(0);
      }}
      .mobile-menu-btn {{
        display: inline-flex;
      }}
      .top-navbar {{
        padding: 0 12px;
      }}
      .article-container {{
        padding: 18px 14px 70px 14px;
      }}
      .volume-banner {{
        padding: 20px 16px;
      }}
      .proof-content {{
        padding: 14px 12px;
        font-size: 14px;
      }}
      .callout {{
        padding: 12px 14px;
      }}
      .btn-action span.btn-text {{
        display: none;
      }}
    }}
  </style>
</head>
<body>

  <!-- Reading Progress Bar -->
  <div id="progress-container"><div id="progress-bar"></div></div>

  <!-- Mobile Drawer Backdrop -->
  <div id="drawer-backdrop" onclick="closeSidebar()"></div>

  <div id="app-layout">
    
    <!-- Sidebar / TOC Drawer -->
    <aside id="sidebar">
      <div class="sidebar-header">
        <div class="univ-tag">СПбГУ Матмех • AI & DS</div>
        <div class="sidebar-title">Суперучебник</div>
        <div class="sidebar-sub">Все предметы с нуля до экзамена</div>
        
        <div class="search-wrapper">
          <svg class="search-icon-svg" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input type="text" id="searchInput" class="search-input" placeholder="Поиск (теорема, билет)..." onkeyup="filterSearch()">
        </div>
      </div>

      <div class="toc-scroll" id="tocScroll">
        {toc_str}
      </div>
    </aside>

    <!-- Main Reader Viewport -->
    <main id="main-content">
      
      <!-- Top Sticky Navigation -->
      <nav class="top-navbar">
        <div class="nav-left">
          <button class="mobile-menu-btn" onclick="toggleSidebar()" aria-label="Меню">☰</button>
          
          <div class="subject-tabs" id="subjectTabs">
            <button class="tab-btn active" data-cat="algebra1" onclick="switchSubject('algebra1', this)">📘 ОАиТЧ 1 сем</button>
            <button class="tab-btn" data-cat="analysis1" onclick="switchSubject('analysis1', this)">📗 Матанализ</button>
            <button class="tab-btn" data-cat="discrete" onclick="switchSubject('discrete', this)">📙 Дискретка</button>
            <button class="tab-btn" data-cat="linalg2" onclick="switchSubject('linalg2', this)">📕 Линал 2 сем</button>
            <button class="tab-btn" data-cat="geom" onclick="switchSubject('geom', this)">📓 Геометрия</button>
            <button class="tab-btn" data-cat="cheat" onclick="switchSubject('cheat', this)">🎯 Шпаргалка</button>
            <button class="tab-btn" data-cat="all" onclick="switchSubject('all', this)">🌐 Все предметы</button>
          </div>
        </div>

        <div class="nav-actions">
          <button class="btn-action" id="examModeBtn" onclick="toggleExamMode()" title="Скрыть/показать все доказательства">
            <span>🎓</span> <span class="btn-text">Экзамен</span>
          </button>
          <button class="btn-action" onclick="toggleTheme()" title="Переключить тему">
            <span id="themeIcon">🌙</span>
          </button>
        </div>
      </nav>

      <!-- Textbook Content Container -->
      <article class="article-container" id="articleContainer">
        {content_str}
      </article>

    </main>

  </div>

  <script>
    // Progressive / On-Demand KaTeX rendering
    function renderMathIn(element) {{
      if (typeof renderMathInElement !== 'undefined' && element && !element.dataset.mathRendered) {{
        renderMathInElement(element, {{
          delimiters: [
            {{left: '$$', right: '$$', display: true}},
            {{left: '$', right: '$', display: false}}
          ],
          throwOnError: false
        }});
        element.dataset.mathRendered = 'true';
      }}
    }}

    document.addEventListener("DOMContentLoaded", function() {{
      // Render active section immediately
      const activeSection = document.getElementById('section-algebra1');
      if (activeSection) {{
        renderMathIn(activeSection);
      }}

      // Lazy observer for other sections as they approach viewport
      if ('IntersectionObserver' in window) {{
        const observer = new IntersectionObserver((entries) => {{
          entries.forEach(entry => {{
            if (entry.isIntersecting) {{
              renderMathIn(entry.target);
              observer.unobserve(entry.target);
            }}
          }});
        }}, {{ root: document.getElementById('main-content'), rootMargin: '800px 0px' }});

        document.querySelectorAll('.volume-section').forEach(sec => observer.observe(sec));
      }} else {{
        renderMathIn(document.body);
      }}
      wrapTables();
      initProgressScroll();
      
      // Filter TOC initially to algebra1
      filterTocToCat('algebra1');
    }});

    // Wrap tables for responsive horizontal scrolling
    function wrapTables() {{
      const tables = document.querySelectorAll('.volume-content-body table');
      tables.forEach(tbl => {{
        if (!tbl.parentElement.classList.contains('table-scroll-wrapper')) {{
          const wrapper = document.createElement('div');
          wrapper.className = 'table-scroll-wrapper';
          wrapper.style.overflowX = 'auto';
          wrapper.style.maxWidth = '100%';
          wrapper.style.margin = '16px 0';
          wrapper.style.webkitOverflowScrolling = 'touch';
          tbl.parentNode.insertBefore(wrapper, tbl);
          wrapper.appendChild(tbl);
        }}
      }});
    }}

    // High performance passive throttled scroll listener (120 FPS)
    function initProgressScroll() {{
      const mainContent = document.getElementById('main-content');
      const progressBar = document.getElementById('progress-bar');
      let ticking = false;

      mainContent.addEventListener('scroll', function() {{
        if (!ticking) {{
          window.requestAnimationFrame(function() {{
            const top = mainContent.scrollTop;
            const height = mainContent.scrollHeight - mainContent.clientHeight;
            if (height > 0) {{
              progressBar.style.width = (top / height * 100) + '%';
            }}
            ticking = false;
          }});
          ticking = true;
        }}
      }}, {{ passive: true }});
    }}

    // Mobile drawer toggle
    function toggleSidebar() {{
      const sb = document.getElementById('sidebar');
      const bd = document.getElementById('drawer-backdrop');
      sb.classList.toggle('drawer-open');
      bd.classList.toggle('active');
    }}

    function closeSidebar() {{
      const sb = document.getElementById('sidebar');
      const bd = document.getElementById('drawer-backdrop');
      sb.classList.remove('drawer-open');
      bd.classList.remove('active');
    }}

    // Navigation click
    function handleNavClick(e, volId, targetId) {{
      if (window.innerWidth <= 900) {{
        closeSidebar();
      }}
      
      const currentActiveTab = document.querySelector('.tab-btn.active').getAttribute('data-cat');
      if (currentActiveTab !== 'all' && currentActiveTab !== volId) {{
        const targetBtn = document.querySelector(`.tab-btn[data-cat="${{volId}}"]`);
        if (targetBtn) {{
          switchSubject(volId, targetBtn);
        }}
      }}
    }}

    // Filter TOC to active category
    function filterTocToCat(cat) {{
      const tocGroups = document.querySelectorAll('.toc-group');
      tocGroups.forEach(grp => {{
        if (cat === 'all' || grp.getAttribute('data-cat') === cat) {{
          grp.style.display = 'block';
        }} else {{
          grp.style.display = 'none';
        }}
      }});
    }}

    // Switch subject tabs with instant render & math trigger
    function switchSubject(cat, btn) {{
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const sections = document.querySelectorAll('.volume-section');
      sections.forEach(sec => {{
        const secCat = sec.getAttribute('data-cat');
        if (cat === 'all' || secCat === cat) {{
          sec.style.display = 'block';
          renderMathIn(sec);
        }} else {{
          sec.style.display = 'none';
        }}
      }});

      filterTocToCat(cat);
      document.getElementById('main-content').scrollTop = 0;
    }}

    // Toggle specific TOC group collapse
    function toggleTocGroup(volId) {{
      const grp = document.getElementById('toc-group-' + volId);
      const wrapper = grp.querySelector('.toc-links-wrapper');
      if (wrapper.style.display === 'none') {{
        wrapper.style.display = 'block';
      }} else {{
        wrapper.style.display = 'none';
      }}
    }}

    // Exam Mode: Collapse/expand all proofs
    let examMode = false;
    function toggleExamMode() {{
      examMode = !examMode;
      const btn = document.getElementById('examModeBtn');
      const proofs = document.querySelectorAll('details.proof-box');

      if (examMode) {{
        btn.classList.add('active');
        btn.innerHTML = '<span>⚡</span> <span class="btn-text">Режим экзамена (скрыты)</span>';
        proofs.forEach(p => p.removeAttribute('open'));
      }} else {{
        btn.classList.remove('active');
        btn.innerHTML = '<span>🎓</span> <span class="btn-text">Экзамен</span>';
        proofs.forEach(p => p.setAttribute('open', 'true'));
      }}
    }}

    // Theme toggle (Dark/Light)
    function toggleTheme() {{
      const html = document.documentElement;
      const current = html.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      document.getElementById('themeIcon').textContent = next === 'dark' ? '☀️' : '🌙';
      localStorage.setItem('theme', next);
    }}
    if (localStorage.getItem('theme') === 'dark' || (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {{
      document.documentElement.setAttribute('data-theme', 'dark');
      const ti = document.getElementById('themeIcon');
      if (ti) ti.textContent = '☀️';
    }}

    // Real-time search across TOC
    function filterSearch() {{
      const query = document.getElementById('searchInput').value.toLowerCase().trim();
      const links = document.querySelectorAll('.toc-link');
      const groups = document.querySelectorAll('.toc-group');

      if (!query) {{
        links.forEach(l => l.style.display = 'block');
        const activeCat = document.querySelector('.tab-btn.active').getAttribute('data-cat');
        filterTocToCat(activeCat);
        return;
      }}

      groups.forEach(g => {{
        let hasMatch = false;
        const gLinks = g.querySelectorAll('.toc-link');
        gLinks.forEach(l => {{
          const text = l.textContent.toLowerCase();
          if (text.includes(query)) {{
            l.style.display = 'block';
            hasMatch = true;
          }} else {{
            l.style.display = 'none';
          }}
        }});
        g.style.display = hasMatch ? 'block' : 'none';
        g.querySelector('.toc-links-wrapper').style.display = hasMatch ? 'block' : 'none';
      }});
    }}
  </script>
</body>
</html>
"""
    output_path = os.path.join(WORKSPACE, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_page)
    print(f"Successfully wrote {output_path} ({len(full_page)} bytes)")

    dup_path = os.path.join(WORKSPACE, "Super_SPbU_Textbook.html")
    with open(dup_path, "w", encoding="utf-8") as f:
        f.write(full_page)
    print(f"Successfully duplicated to {dup_path}")

if __name__ == "__main__":
    generate_full_html()
