import re
import os

# ==========================================
# CONFIGURATION
# ==========================================
TARGET_VERB = "template_verb" # REPLACE THIS
VERB_TITLE = TARGET_VERB.upper()
JAPANESE_TITLE = f"{VERB_TITLE} 句動詞 完全解説【後編】 - Phrasal Verb Master"

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VERB_DIR = os.path.join(BASE_DIR, TARGET_VERB)
GUIDE_SOURCE_PATH = os.path.join(VERB_DIR, 'guide', 'part2の原文テキスト.txt')
OUTPUT_PATH = os.path.join(VERB_DIR, 'guide', 'part2.html')
# Phrasal List Source Paths (used as Master List)
PHRASAL_LIST_PATHS = [
    ("03", "ビジネス・上級", os.path.join(VERB_DIR, 'phrasal', '03', 'phrasal03の原文テキスト.txt')),
    ("04", "多義語・注意", os.path.join(VERB_DIR, 'phrasal', '04', 'phrasal04の原文テキスト.txt'))
]

# ==========================================
# TEMPLATE
# ==========================================

def generate_card(phrase, translation, existing_content=None, is_polysemy=False):
    # Same standard card generation as Part 1
    # For Part 2, standardizing to same card design + logic
    html = ""
    toeic_badge = ""
    
    if existing_content:
        point_match = re.search(r'\*\*ポイント：\*\* (.+?)(?=\n\n---|$)`, existing_content, re.DOTALL)
        if point_match:
            point_text = point_match.group(1).strip()
            if "🎯 TOEIC" in point_text:
                toeic_badge = '<span class="bg-amber-100 text-amber-700 text-xs font-bold px-2 py-1 rounded-full border border-amber-200 ml-2">TOEIC頻出</span>'

    html += f'\t<!-- {phrase} -->\n'
    html += f'\t<div class="card">\n'
    html += f'\t\t<div class="card-header"><span class="phrase">{phrase}</span><span class="translation">{translation}</span>{toeic_badge}</div>\n'
    html += f'\t\t<div class="card-body">\n'

    if existing_content:
        # Check standard vs polysemy format
        # For simplicity in template, we reuse same logic
        if is_polysemy:
            intro_match = re.search(r'^(.*?)(?=\*\*意味\d+：)', existing_content, re.DOTALL)
            if intro_match:
                 html += f'\t\t\t<p class="text-slate-600 mb-4">{intro_match.group(1).strip()}</p>\n'
            
            meanings = re.findall(r'\*\*意味(\d+)：([^*]+)\*\*\s*```\n(.*?)\n```\s*\n(.*?)(?=\*\*意味\d+：|\*\*ポイント：|$)', existing_content, re.DOTALL)
            for m_num, m_title, m_core, m_examples in meanings:
                html += f'\t\t\t<div class="meaning-section">\n'
                html += f'\t\t\t\t<div class="meaning-title">意味{m_num}：{m_title}</div>\n'
                if m_core.strip():
                     html += f'\t\t\t\t<div class="core-box"><span class="core-title">コアイメージ</span><div class="visual-text">{m_core.strip().replace(chr(10), "<br>")}</div></div>\n'
                examples = re.findall(r'- (.+?)\n  → (.+?)(?=\n\n|- |$)', m_examples, re.DOTALL)
                for en, jp in examples:
                    html += f'\t\t\t\t<div class="example-box"><p class="en-sent">{en.strip()}</p><p class="jp-sent">{jp.strip()}</p></div>\n'
                html += f'\t\t\t</div>\n'
        else:
             # Normal
            core_match = re.search(r'```\n(.*?)\n```', existing_content, re.DOTALL)
            if core_match:
                html += f'\t\t\t<div class="core-box"><span class="core-title">コアイメージ</span><div class="visual-text">{core_match.group(1).strip().replace(chr(10), "<br>")}</div></div>\n'
            
            examples_match = re.search(r'\*\*例文：\*\*\s*\n\n(.*?)\n\n\*\*ポイント：\*\*', existing_content, re.DOTALL)
            if examples_match:
                examples = re.findall(r'- (.+?)\n  → (.+?)(?=\n\n|- |$)', examples_match.group(1), re.DOTALL)
                if examples:
                    html += f'\t\t\t<div class="meaning-section">\n'
                    for en, jp in examples:
                         html += f'\t\t\t\t<div class="example-box"><p class="en-sent">{en.strip()}</p><p class="jp-sent">{jp.strip()}</p></div>\n'
                    html += f'\t\t\t</div>\n'

        point_match = re.search(r'\*\*ポイント：\*\* (.+?)(?=\n\n---|$)', existing_content, re.DOTALL)
        if point_match:
            point = point_match.group(1).replace("**🎯 TOEIC超頻出**", "").replace("**🎯 TOEIC頻出**", "").strip()
            html += f'\t\t\t<div class="point-area"><span class="point-label">Point：</span><p>{point}</p></div>\n'
    else:
        html += f'\t\t\t<div class="point-area"><span class="point-label">Note：</span><p>詳細な解説は準備中です。</p></div>\n'

    html += f'\t\t</div>\n'
    html += f'\t</div>\n\n'
    return html

def main():
    if not os.path.exists(GUIDE_SOURCE_PATH):
        print(f"Error: Guide source not found at {GUIDE_SOURCE_PATH}")
        return

    with open(GUIDE_SOURCE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Build Content Map
    content_map = {}
    pattern = re.compile(r'### \*\*([^*]+?)(?: - ([^*]+?)|\（多義\）)\*\*(.*?)(?=###|\Z)', re.DOTALL)
    for match in pattern.finditer(content):
        phrase = match.group(1).strip()
        translation = match.group(2).strip() if match.group(2) else "多義語"
        card_content = match.group(3).strip()
        content_map[phrase] = {
            'translation': translation,
            'content': card_content,
            'is_polysemy': "多義" in match.group(0)
        }

    # Generate HTML Header
    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{JAPANESE_TITLE}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans JP', sans-serif; background-color: #f8fafc; color: #334155; line-height: 1.6; }}
        .font-poppins {{ font-family: 'Poppins', sans-serif; }}
        .card {{ background: white; border-radius: 12px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.01); border: 1px solid #e2e8f0; margin-bottom: 24px; overflow: hidden; break-inside: avoid; }}
        .card-header {{ background-color: #f1f5f9; padding: 16px 24px; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; }}
        .phrase {{ font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1.5rem; color: #1e293b; }}
        .translation {{ font-size: 0.9rem; font-weight: 700; color: #64748b; background: white; padding: 4px 12px; border-radius: 20px; border: 1px solid #cbd5e1; }}
        .card-body {{ padding: 24px; }}
        .core-box {{ background-color: #ecfeff; border: 1px dashed #67e8f9; border-radius: 8px; padding: 16px; margin-bottom: 20px; text-align: center; }}
        .core-title {{ font-weight: 700; color: #0891b2; font-size: 0.9rem; margin-bottom: 8px; display: block; }}
        .visual-text {{ font-family: monospace; white-space: pre-wrap; color: #475569; font-weight: 700; line-height: 1.4; }}
        .meaning-section {{ margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid #f1f5f9; }}
        .meaning-section:last-child {{ border-bottom: none; margin-bottom: 0; padding-bottom: 0; }}
        .meaning-title {{ font-weight: 700; color: #3b82f6; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }}
        .example-box {{ background-color: #f8fafc; border-left: 3px solid #cbd5e1; padding: 10px 16px; margin-bottom: 8px; }}
        .en-sent {{ font-family: 'Poppins', sans-serif; font-weight: 600; color: #0f172a; }}
        .jp-sent {{ font-size: 0.9rem; color: #64748b; }}
        .point-area {{ background-color: #ecfeff; border-radius: 8px; padding: 16px; margin-top: 20px; font-size: 0.9rem; }}
        .point-label {{ font-weight: 700; color: #0891b2; margin-bottom: 4px; display: block; }}
        .section-title {{ font-size: 1.5rem; font-weight: 900; color: #1e293b; margin-top: 40px; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 2px solid #06b6d4; display: flex; align-items: center; gap: 12px; }}
        .section-badge {{ background-color: #06b6d4; color: white; font-size: 1rem; padding: 4px 12px; border-radius: 9999px; font-family: 'Poppins', sans-serif; }}
        /* Print Styles */
        @media print {{
            .card {{ break-inside: avoid; border: 1px solid #ccc; box-shadow: none; print-color-adjust: exact; -webkit-print-color-adjust: exact; }}
            .nav-container, footer {{ display: none; }}
            body {{ background: white; }}
        }}
    </style>
</head>
<body class="p-4 md:p-8 max-w-5xl mx-auto">
    <header class="text-center mb-12">
        <div class="inline-block px-4 py-1 rounded-full bg-cyan-50 text-cyan-600 font-bold text-sm mb-4 tracking-wider uppercase">
            {VERB_TITLE} PHRASAL VERBS
        </div>
        <h1 class="text-3xl md:text-5xl font-black text-slate-800 mb-4">
            {VERB_TITLE} 句動詞 <span class="text-cyan-600">完全解説【後編】</span>
        </h1>
        <p class="text-slate-500 font-bold">多義語・慣用表現（Section 3〜4）</p>
    </header>
'''

    cards_html = ""
    statistics_html = ""
    
    for sec_num, sec_name, phr_path in PHRASAL_LIST_PATHS:
        # Check source
        if not os.path.exists(phr_path):
            print(f"Warning: Phrasal list missing: {phr_path}")
            continue

        with open(phr_path, 'r', encoding='utf-8') as f:
            phr_lines = f.readlines()
            
        phrases_in_section = []
        
        # -----------------------------------------------
        # LOGIC: SEPARATE STATISTICS SECTION
        # -----------------------------------------------
        stats_start_idx = -1
        for i, line in enumerate(phr_lines):
            if "📊 統計情報" in line:
                stats_start_idx = i
                break
        
        if stats_start_idx != -1:
             # Generate stats immediately
             stats_lines = phr_lines[stats_start_idx:]
             phr_lines = phr_lines[:stats_start_idx] # Remove from phrase parsing
             
             statistics_html += '\t<!-- Statistics Section -->\n'
             statistics_html += '\t<div class="card">\n'
             statistics_html += '\t\t<div class="card-header"><span class="phrase">📊 統計情報</span></div>\n'
             statistics_html += '\t\t<div class="card-body">\n'
             for sline in stats_lines:
                 sline = sline.strip()
                 if not sline or "📊 統計情報" in sline: continue
                 if "合計フレーズ数" in sline:
                     statistics_html += f'\t\t\t<div class="mb-4 font-bold text-lg">{sline}</div>\n'
                 elif "レベル別内訳" in sline:
                     statistics_html += f'\t\t\t<div class="mb-2 font-bold text-slate-700 mt-6">{sline}</div>\n'
                 elif "💡" in sline or "コアイメージ" in sline:
                      statistics_html += f'\t\t\t<div class="core-box mt-8"><span class="core-title">💡 コアイメージ</span>'
                 elif "HAVE =" in sline or ("=" in sline and "HAVE" not in sline): # Check simple visual assignment
                      statistics_html += f'<div class="visual-text mt-4 text-cyan-700">{sline}</div></div>'
                 else:
                      statistics_html += f'\t\t\t<p class="ml-4">{sline}</p>\n'
             statistics_html += '\t\t</div>\n\t</div>\n\n'

        # Parse phrases
        for line in phr_lines:
            line = line.strip()
            if not line or "｜" in line or "合計" in line or "レベル" in line or "目安" in line:
                continue
            
            parts = line.split(' - ')
            if len(parts) >= 2:
                phrase = parts[0].strip()
                translation = parts[1].strip()
                phrases_in_section.append((phrase, translation))
        
        if phrases_in_section:
            cards_html += f'\t<!-- SECTION {sec_num} -->\n'
            cards_html += f'\t<div class="section-title">\n'
            cards_html += f'\t\t<span class="section-badge">{sec_num}</span>\n'
            cards_html += f'\t\t{sec_name}（{len(phrases_in_section)}表現）\n'
            cards_html += f'\t</div>\n\n'
            
            for phrase, translation in phrases_in_section:
                if phrase in content_map:
                    data = content_map[phrase]
                    cards_html += generate_card(phrase, data['translation'], data['content'], data['is_polysemy'])
                else:
                    cards_html += generate_card(phrase, translation)

    # Footer
    footer = '''	<footer class="text-center mt-12 mb-12">
		<a href="./part1.html"
			class="inline-block bg-slate-600 text-white font-bold py-4 px-8 rounded-full shadow hover:bg-slate-700 transition">
			← {VERB_TITLE} 句動詞【前編】に戻る
		</a>
	</footer>
</body>
</html>'''

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        # Note: Summary section is not robustly templated here as it varies widely, 
        # but statistics_html is included
        f.write(html + cards_html + statistics_html + footer)
    print(f"Generated {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
