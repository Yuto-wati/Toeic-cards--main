# Script to generate HAVE guide part1.html from source text
import re

# Read source text
with open(r'c:\Users\yuto\OneDrive\Toeic-cards--main\verbs\have\guide\part1の原文テキスト.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# HTML header
html = '''<!DOCTYPE html>
<html lang="ja">

<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>HAVE 句動詞 完全解説【前編】 - Phrasal Verb Master</title>
	<script src="https://cdn.tailwindcss.com"></script>
	<link rel="preconnect" href="https://fonts.googleapis.com">
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
	<link
		href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&family=Poppins:wght@400;600;700&display=swap"
		rel="stylesheet">
	<style>
		body {
			font-family: 'Noto Sans JP', sans-serif;
			background-color: #f8fafc;
			color: #334155;
			line-height: 1.6;
		}

		.font-poppins {
			font-family: 'Poppins', sans-serif;
		}

		.card {
			background: white;
			border-radius: 12px;
			box-shadow: 0 2px 4px rgba(0, 0, 0, 0.01);
			border: 1px solid #e2e8f0;
			margin-bottom: 24px;
			overflow: hidden;
		}

		.card-header {
			background-color: #f1f5f9;
			padding: 16px 24px;
			border-bottom: 1px solid #e2e8f0;
			display: flex;
			justify-content: space-between;
			align-items: center;
			flex-wrap: wrap;
			gap: 10px;
		}

		.phrase {
			font-family: 'Poppins', sans-serif;
			font-weight: 700;
			font-size: 1.5rem;
			color: #1e293b;
		}

		.translation {
			font-size: 0.9rem;
			font-weight: 700;
			color: #64748b;
			background: white;
			padding: 4px 12px;
			border-radius: 20px;
			border: 1px solid #cbd5e1;
		}

		.card-body {
			padding: 24px;
		}

		.core-box {
			background-color: #ecfeff;
			border: 1px dashed #67e8f9;
			border-radius: 8px;
			padding: 16px;
			margin-bottom: 20px;
			text-align: center;
		}

		.core-title {
			font-weight: 700;
			color: #0891b2;
			font-size: 0.9rem;
			margin-bottom: 8px;
			display: block;
		}

		.visual-text {
			font-family: monospace;
			white-space: pre-wrap;
			color: #475569;
			font-weight: 700;
			line-height: 1.4;
		}

		.meaning-section {
			margin-bottom: 20px;
			padding-bottom: 16px;
			border-bottom: 1px solid #f1f5f9;
		}

		.meaning-section:last-child {
			border-bottom: none;
			margin-bottom: 0;
			padding-bottom: 0;
		}

		.meaning-title {
			font-weight: 700;
			color: #3b82f6;
			margin-bottom: 8px;
			display: flex;
			align-items: center;
			gap: 8px;
		}

		.example-box {
			background-color: #f8fafc;
			border-left: 3px solid #cbd5e1;
			padding: 10px 16px;
			margin-bottom: 8px;
		}

		.en-sent {
			font-family: 'Poppins', sans-serif;
			font-weight: 600;
			color: #0f172a;
		}

		.jp-sent {
			font-size: 0.9rem;
			color: #64748b;
		}

		.explanation {
			font-size: 0.85rem;
			color: #475569;
			margin-top: 4px;
		}

		.point-area {
			background-color: #ecfeff;
			border-radius: 8px;
			padding: 16px;
			margin-top: 20px;
			font-size: 0.9rem;
		}

		.point-label {
			font-weight: 700;
			color: #0891b2;
			margin-bottom: 4px;
			display: block;
		}

		.section-title {
			font-size: 1.5rem;
			font-weight: 900;
			color: #1e293b;
			margin-top: 40px;
			margin-bottom: 20px;
			padding-bottom: 10px;
			border-bottom: 2px solid #06b6d4;
			display: flex;
			align-items: center;
			gap: 12px;
		}

		.section-badge {
			background-color: #06b6d4;
			color: white;
			font-size: 1rem;
			padding: 4px 12px;
			border-radius: 9999px;
			font-family: 'Poppins', sans-serif;
		}

		.link-button {
			display: block;
			width: 100%;
			text-align: center;
			background: #06b6d4;
			color: white;
			padding: 16px;
			border-radius: 8px;
			font-weight: bold;
			margin-top: 40px;
			text-decoration: none;
			transition: background-color 0.3s;
		}

		.link-button:hover {
			background-color: #0891b2;
		}

		@media print {
			.card {
				break-inside: avoid;
				border: 1px solid #ccc;
				box-shadow: none;
				print-color-adjust: exact;
				-webkit-print-color-adjust: exact;
			}

			.nav-container,
			.link-button,
			footer {
				display: none;
			}

			body {
				background: white;
			}
		}
	</style>
</head>

<body class="p-4 md:p-8 max-w-5xl mx-auto">

	<header class="text-center mb-12">
		<div
			class="inline-block px-4 py-1 rounded-full bg-cyan-50 text-cyan-600 font-bold text-sm mb-4 tracking-wider uppercase">
			HAVE PHRASAL VERBS
		</div>
		<h1 class="text-3xl md:text-5xl font-black text-slate-800 mb-4">
			HAVE 句動詞 <span class="text-cyan-600">完全解説</span>
		</h1>
		<p class="text-slate-500 font-bold">基本イメージから日常会話表現まで（Section 1〜2）</p>
	</header>

	<!-- Core Image Section -->
	<div class="card">
		<div class="card-header bg-cyan-50" style="background-color: #ecfeff;">
			<span class="phrase text-cyan-700" style="color: #0e7490;">🎯 HAVEのコアイメージ（基礎）</span>
		</div>
		<div class="card-body">
			<div class="core-box">
				<span class="core-title">本質：「自分の領域に持っている（所有・経験・属性）」</span>
				<div class="visual-text text-xl">[主語] ⊃ [対象] ✨<br>自分のスペースに存在させる</div>
			</div>
			<div class="point-area bg-white border-0 p-0 mt-0">
				<p class="font-bold text-slate-600 mb-4">HAVEの本質は「自分の領域に持っている」という広範な状態を表します。物理的な「所持」、経験としての「保持」、人間関係の「属性」、さらには使役構文のような「状況の維持」まで、すべて「自分のテリトリー内にある」イメージで繋がっています。</p>
			</div>
		</div>
	</div>

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
	<footer class="text-center mt-12 mb-12">
		<a href="./part2.html"
			class="inline-block bg-cyan-600 text-white font-bold py-4 px-8 rounded-full shadow hover:bg-cyan-700 transition">
			HAVE 句動詞【後編】多義語・慣用表現 →
		</a>
	</footer>

</body>

</html>'''

# Write complete HTML
with open(r'c:\Users\yuto\OneDrive\Toeic-cards--main\verbs\have\guide\part1.html', 'w', encoding='utf-8') as f:
    f.write(html + cards_html + footer)

print("Generated part1.html successfully!")
