# Script to generate MAKE guide part1.html from source text
import re

# Read source text
with open(r'c:\Users\yuto\OneDrive\Toeic-cards--main\verbs\make\guide\guide01の原文テキスト.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# HTML header
html = '''<!DOCTYPE html>
<html lang="ja">

<head>
\t<meta charset="UTF-8">
\t<meta name="viewport" content="width=device-width, initial-scale=1.0">
\t<title>MAKE 句動詞 完全解説【前編】 - Phrasal Verb Master</title>
\t<script src="https://cdn.tailwindcss.com"></script>
\t<link rel="preconnect" href="https://fonts.googleapis.com">
\t<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
\t<link
\t\thref="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&family=Poppins:wght@400;600;700&display=swap"
\t\trel="stylesheet">
\t<style>
\t\tbody {
\t\t\tfont-family: 'Noto Sans JP', sans-serif;
\t\t\tbackground-color: #f8fafc;
\t\t\tcolor: #334155;
\t\t\tline-height: 1.6;
\t\t}

\t\t.font-poppins {
\t\t\tfont-family: 'Poppins', sans-serif;
\t\t}

\t\t.card {
\t\t\tbackground: white;
\t\t\tborder-radius: 12px;
\t\t\tbox-shadow: 0 2px 4px rgba(0, 0, 0, 0.01);
\t\t\tborder: 1px solid #e2e8f0;
\t\t\tmargin-bottom: 24px;
\t\t\toverflow: hidden;
\t\t}

\t\t.card-header {
\t\t\tbackground-color: #f1f5f9;
\t\t\tpadding: 16px 24px;
\t\t\tborder-bottom: 1px solid #e2e8f0;
\t\t\tdisplay: flex;
\t\t\tjustify-content: space-between;
\t\t\talign-items: center;
\t\t\tflex-wrap: wrap;
\t\t\tgap: 10px;
\t\t}

\t\t.phrase {
\t\t\tfont-family: 'Poppins', sans-serif;
\t\t\tfont-weight: 700;
\t\t\tfont-size: 1.5rem;
\t\t\tcolor: #1e293b;
\t\t}

\t\t.translation {
\t\t\tfont-size: 0.9rem;
\t\t\tfont-weight: 700;
\t\t\tcolor: #64748b;
\t\t\tbackground: white;
\t\t\tpadding: 4px 12px;
\t\t\tborder-radius: 20px;
\t\t\tborder: 1px solid #cbd5e1;
\t\t}

\t\t.card-body {
\t\t\tpadding: 24px;
\t\t}

\t\t.core-box {
\t\t\tbackground-color: #fff7ed;
\t\t\tborder: 1px dashed #fdba74;
\t\t\tborder-radius: 8px;
\t\t\tpadding: 16px;
\t\t\tmargin-bottom: 20px;
\t\t\ttext-align: center;
\t\t}

\t\t.core-title {
\t\t\tfont-weight: 700;
\t\t\tcolor: #ea580c;
\t\t\tfont-size: 0.9rem;
\t\t\tmargin-bottom: 8px;
\t\t\tdisplay: block;
\t\t}

\t\t.visual-text {
\t\t\tfont-family: monospace;
\t\t\twhite-space: pre-wrap;
\t\t\tcolor: #475569;
\t\t\tfont-weight: 700;
\t\t\tline-height: 1.4;
\t\t}

\t\t.meaning-section {
\t\t\tmargin-bottom: 20px;
\t\t\tpadding-bottom: 16px;
\t\t\tborder-bottom: 1px solid #f1f5f9;
\t\t}

\t\t.meaning-section:last-child {
\t\t\tborder-bottom: none;
\t\t\tmargin-bottom: 0;
\t\t\tpadding-bottom: 0;
\t\t}

\t\t.meaning-title {
\t\t\tfont-weight: 700;
\t\t\tcolor: #3b82f6;
\t\t\tmargin-bottom: 8px;
\t\t\tdisplay: flex;
\t\t\talign-items: center;
\t\t\tgap: 8px;
\t\t}

\t\t.example-box {
\t\t\tbackground-color: #f8fafc;
\t\t\tborder-left: 3px solid #cbd5e1;
\t\t\tpadding: 10px 16px;
\t\t\tmargin-bottom: 8px;
\t\t}

\t\t.en-sent {
\t\t\tfont-family: 'Poppins', sans-serif;
\t\t\tfont-weight: 600;
\t\t\tcolor: #0f172a;
\t\t}

\t\t.jp-sent {
\t\t\tfont-size: 0.9rem;
\t\t\tcolor: #64748b;
\t\t}

\t\t.explanation {
\t\t\tfont-size: 0.85rem;
\t\t\tcolor: #475569;
\t\t\tmargin-top: 4px;
\t\t}

\t\t.point-area {
\t\t\tbackground-color: #fff7ed;
\t\t\tborder-radius: 8px;
\t\t\tpadding: 16px;
\t\t\tmargin-top: 20px;
\t\t\tfont-size: 0.9rem;
\t\t}

\t\t.point-label {
\t\t\tfont-weight: 700;
\t\t\tcolor: #ea580c;
\t\t\tmargin-bottom: 4px;
\t\t\tdisplay: block;
\t\t}

\t\t.section-title {
\t\t\tfont-size: 1.5rem;
\t\t\tfont-weight: 900;
\t\t\tcolor: #1e293b;
\t\t\tmargin-top: 40px;
\t\t\tmargin-bottom: 20px;
\t\t\tpadding-bottom: 10px;
\t\t\tborder-bottom: 2px solid #f97316;
\t\t\tdisplay: flex;
\t\t\talign-items: center;
\t\t\tgap: 12px;
\t\t}

\t\t.section-badge {
\t\t\tbackground-color: #f97316;
\t\t\tcolor: white;
\t\t\tfont-size: 1rem;
\t\t\tpadding: 4px 12px;
\t\t\tborder-radius: 9999px;
\t\t\tfont-family: 'Poppins', sans-serif;
\t\t}

\t\t.link-button {
\t\t\tdisplay: block;
\t\t\twidth: 100%;
\t\t\ttext-align: center;
\t\t\tbackground: #f97316;
\t\t\tcolor: white;
\t\t\tpadding: 16px;
\t\t\tborder-radius: 8px;
\t\t\tfont-weight: bold;
\t\t\tmargin-top: 40px;
\t\t\ttext-decoration: none;
\t\t\ttransition: background-color 0.3s;
\t\t}

\t\t.link-button:hover {
\t\t\tbackground-color: #ea580c;
\t\t}

\t\t@media print {
\t\t\t.card {
\t\t\t\tbreak-inside: avoid;
\t\t\t\tborder: 1px solid #ccc;
\t\t\t\tbox-shadow: none;
\t\t\t\tprint-color-adjust: exact;
\t\t\t\t-webkit-print-color-adjust: exact;
\t\t\t}

\t\t\t.nav-container,
\t\t\t.link-button,
\t\t\tfooter {
\t\t\t\tdisplay: none;
\t\t\t}

\t\t\tbody {
\t\t\t\tbackground: white;
\t\t\t}
\t\t}
\t</style>
</head>

<body class="p-4 md:p-8 max-w-5xl mx-auto">

\t<header class="text-center mb-12">
\t\t<div
\t\t\tclass="inline-block px-4 py-1 rounded-full bg-orange-50 text-orange-600 font-bold text-sm mb-4 tracking-wider uppercase">
\t\t\tMAKE PHRASAL VERBS
\t\t</div>
\t\t<h1 class="text-3xl md:text-5xl font-black text-slate-800 mb-4">
\t\t\tMAKE 句動詞 <span class="text-orange-600">完全解説</span>
\t\t</h1>
\t\t<p class="text-slate-500 font-bold">基本イメージから日常会話表現まで（Section 1〜2）</p>
\t</header>

\t<!-- Core Image Section -->
\t<div class="card">
\t\t<div class="card-header bg-amber-50" style="background-color: #fff7ed;">
\t\t\t<span class="phrase text-amber-700" style="color: #ea580c;">🎯 MAKEのコアイメージ（基礎）</span>
\t\t</div>
\t\t<div class="card-body">
\t\t\t<div class="core-box">
\t\t\t\t<span class="core-title">本質：「存在しなかったものを生み出す」「変化を引き起こす」</span>
\t\t\t\t<div class="visual-text text-xl">[材料] + [行動] = [新しいもの] ✨<br>   💡 → 🛠️ → 📦 MAKE</div>
\t\t\t</div>
\t\t\t<div class="point-area bg-white border-0 p-0 mt-0">
\t\t\t\t<p class="font-bold text-slate-600 mb-4">MAKEの本質は「何かを生み出す・変化させる力」です。物理的なものを作るだけでなく、状況や関係性を「作り出す」、決定を「成立させる」など、「無→有」「A→B」の変化を引き起こすイメージが全ての意味に共通しています。</p>
\t\t\t</div>
\t\t</div>
\t</div>

'''

# Parse sections
sections = re.split(r'## (\d+)｜([^\r\n]+)', content)

cards_html = ""
section_num = 0

for i in range(1, len(sections), 3):
    section_num_str = sections[i]
    section_title = sections[i+1]
    section_content = sections[i+2]
    
    # Add section header
    cards_html += f'\t<!-- SECTION {section_num_str} -->\n'
    cards_html += f'\t<div class="section-title">\n'
    cards_html += f'\t\t<span class="section-badge">{section_num_str}</span>\n'
    cards_html += f'\t\t{section_title}\n'
    cards_html += f'\t</div>\n\n'
    
    # Extract section description (text between section header and first phrasal verb)
    desc_match = re.match(r'^(.*?)(?=###|\Z)', section_content, re.DOTALL)
    if desc_match:
        desc_text = desc_match.group(1).strip()
        # Remove --- separators and clean up
        desc_text = re.sub(r'^---+\s*$', '', desc_text, flags=re.MULTILINE).strip()
        if desc_text:
            cards_html += f'\t<p class="text-slate-600 mb-8 text-center">{desc_text}</p>\n\n'
    
    # Parse phrasal verbs in this section
    phrases = re.split(r'### \*\*([^*]+) - ([^*]+)\*\*', section_content)
    
    for j in range(1, len(phrases), 3):
        phrase = phrases[j].strip()
        translation = phrases[j+1].strip()
        phrase_content = phrases[j+2]
        
        # Extract core image
        core_match = re.search(r'```\n(.*?)\n```', phrase_content, re.DOTALL)
        core_text = core_match.group(1) if core_match else ""
        
        # Extract explanation
        expl_match = re.search(r'```.*?```\s*\n\n(.*?)\n\n\*\*例文：\*\*', phrase_content, re.DOTALL)
        explanation = expl_match.group(1).strip() if expl_match else ""
        
        # Extract examples
        examples_match = re.search(r'\*\*例文：\*\*\s*\n\n(.*?)\n\n\*\*ポイント：\*\*', phrase_content, re.DOTALL)
        examples_text = examples_match.group(1) if examples_match else ""
        examples = re.findall(r'- (.+?)\n  → (.+?)(?=\n\n|- |$)', examples_text, re.DOTALL)
        
        # Extract point
        point_match = re.search(r'\*\*ポイント：\*\* (.+?)(?=\n\n---|$)', phrase_content, re.DOTALL)
        point = point_match.group(1).strip() if point_match else ""
        
        # Check for TOEIC badge
        toeic_badge = ""
        if "🎯 TOEIC" in point:
            toeic_badge = '<span class="bg-amber-100 text-amber-700 text-xs font-bold px-2 py-1 rounded-full border border-amber-200 ml-2">TOEIC頻出</span>'
            point = point.replace("**🎯 TOEIC超頻出**", "").replace("**🎯 TOEIC頻出**", "").strip()
        
        # Build card HTML
        cards_html += f'\t<!-- {phrase} -->\n'
        cards_html += f'\t<div class="card">\n'
        cards_html += f'\t\t<div class="card-header"><span class="phrase">{phrase}</span><span class="translation">{translation}</span>{toeic_badge}</div>\n'
        cards_html += f'\t\t<div class="card-body">\n'
        
        # Core box
        if core_text:
            core_lines = core_text.split('\n')
            core_visual = '<br>'.join(core_lines)
            cards_html += f'\t\t\t<div class="core-box"><span class="core-title">コアイメージ</span>\n'
            cards_html += f'\t\t\t\t<div class="visual-text">{core_visual}</div>\n'
            cards_html += f'\t\t\t</div>\n'
        
        # Examples
        if examples:
            cards_html += f'\t\t\t<div class="meaning-section">\n'
            for en, jp in examples:
                cards_html += f'\t\t\t\t<div class="example-box">\n'
                cards_html += f'\t\t\t\t\t<p class="en-sent">{en.strip()}</p>\n'
                cards_html += f'\t\t\t\t\t<p class="jp-sent">{jp.strip()}</p>\n'
                cards_html += f'\t\t\t\t</div>\n'
            cards_html += f'\t\t\t</div>\n'
        
        # Point
        if point:
            cards_html += f'\t\t\t<div class="point-area"><span class="point-label">Point：</span>\n'
            cards_html += f'\t\t\t\t<p>{point}</p>\n'
            cards_html += f'\t\t\t</div>\n'
        
        cards_html += f'\t\t</div>\n'
        cards_html += f'\t</div>\n\n'

# Footer
footer = '''\t<!-- Footer -->
\t<footer class="text-center mt-12 mb-12">
\t\t<a href="./part2.html"
\t\t\tclass="inline-block bg-orange-600 text-white font-bold py-4 px-8 rounded-full shadow hover:bg-orange-700 transition">
\t\t\tMAKE 句動詞【後編】多義語・慣用表現 →
\t\t</a>
\t</footer>

</body>

</html>'''

# Write complete HTML
with open(r'c:\Users\yuto\OneDrive\Toeic-cards--main\verbs\make\guide\part1.html', 'w', encoding='utf-8') as f:
    f.write(html + cards_html + footer)

print("Generated part1.html successfully!")
