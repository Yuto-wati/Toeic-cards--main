# Script to generate HAVE guide part1.html from source text
import re

# Read source text
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

# Parse sections from current guide text to build a Content Map
# We ignore the section structure of the guide text and treat it as a flat database of cards
content_map = {}

# Regex to find all phrase blocks
# Matches: ### **phrase - translation** (Normal) OR ### **phrase（多義）** (Polysemy)
# We capture the full block until the next ### or End of File
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

# Helper function to generate card HTML
def generate_card(phrase, translation, existing_content=None, is_polysemy=False):
    html = ""
    # Check for TOEIC badge in existing content
    toeic_badge = ""
    point_text = ""
    
    if existing_content:
        # Extract point to check for badge
        point_match = re.search(r'\*\*ポイント：\*\* (.+?)(?=\n\n---|$)', existing_content, re.DOTALL)
        if point_match:
            point_text = point_match.group(1).strip()
            if "🎯 TOEIC" in point_text:
                toeic_badge = '<span class="bg-amber-100 text-amber-700 text-xs font-bold px-2 py-1 rounded-full border border-amber-200 ml-2">TOEIC頻出</span>'

    html += f'\t<!-- {phrase} -->\n'
    html += f'\t<div class="card">\n'
    html += f'\t\t<div class="card-header"><span class="phrase">{phrase}</span><span class="translation">{translation}</span>{toeic_badge}</div>\n'
    html += f'\t\t<div class="card-body">\n'

    if existing_content:
        if is_polysemy:
             # Parse polysemy content
             # Intro
            intro_match = re.search(r'^(.*?)(?=\*\*意味\d+：)', existing_content, re.DOTALL)
            if intro_match:
                intro_text = intro_match.group(1).strip()
                intro_text = re.sub(r'^---+\s*$', '', intro_text, flags=re.MULTILINE).strip()
                if intro_text:
                    html += f'\t\t\t<p class="text-slate-600 mb-4">{intro_text}</p>\n'
            
            # Meanings
            meanings = re.findall(r'\*\*意味(\d+)：([^*]+)\*\*\s*```\n(.*?)\n```\s*\n(.*?)(?=\*\*意味\d+：|\*\*ポイント：|$)', existing_content, re.DOTALL)
            for m_num, m_title, m_core, m_examples in meanings:
                html += f'\t\t\t<div class="meaning-section">\n'
                html += f'\t\t\t\t<div class="meaning-title">意味{m_num}：{m_title}</div>\n'
                
                if m_core.strip():
                     html += f'\t\t\t\t<div class="core-box"><span class="core-title">コアイメージ</span>\n'
                     html += f'\t\t\t\t\t<div class="visual-text">{m_core.strip().replace(chr(10), "<br>")}</div>\n'
                     html += f'\t\t\t\t</div>\n'
                
                examples = re.findall(r'- (.+?)\n  → (.+?)(?=\n\n|- |$)', m_examples, re.DOTALL)
                for en, jp in examples:
                    html += f'\t\t\t\t<div class="example-box">\n'
                    html += f'\t\t\t\t\t<p class="en-sent">{en.strip()}</p>\n'
                    html += f'\t\t\t\t\t<p class="jp-sent">{jp.strip()}</p>\n'
                    html += f'\t\t\t\t</div>\n'
                html += f'\t\t\t</div>\n'

        else:
            # Normal content
            # Core image
            core_match = re.search(r'```\n(.*?)\n```', existing_content, re.DOTALL)
            if core_match:
                core_visual = core_match.group(1).strip().replace('\n', '<br>')
                html += f'\t\t\t<div class="core-box"><span class="core-title">コアイメージ</span>\n'
                html += f'\t\t\t\t<div class="visual-text">{core_visual}</div>\n'
                html += f'\t\t\t</div>\n'
            
            # Examples
            examples_match = re.search(r'\*\*例文：\*\*\s*\n\n(.*?)\n\n\*\*ポイント：\*\*', existing_content, re.DOTALL)
            if examples_match:
                examples_text = examples_match.group(1)
                examples = re.findall(r'- (.+?)\n  → (.+?)(?=\n\n|- |$)', examples_text, re.DOTALL)
                if examples:
                    html += f'\t\t\t<div class="meaning-section">\n'
                    for en, jp in examples:
                        html += f'\t\t\t\t<div class="example-box">\n'
                        html += f'\t\t\t\t\t<p class="en-sent">{en.strip()}</p>\n'
                        html += f'\t\t\t\t\t<p class="jp-sent">{jp.strip()}</p>\n'
                        html += f'\t\t\t\t</div>\n'
                    html += f'\t\t\t</div>\n'

        # Point (Common for both)
        point_match = re.search(r'\*\*ポイント：\*\* (.+?)(?=\n\n---|$)', existing_content, re.DOTALL)
        if point_match:
            point = point_match.group(1).replace("**🎯 TOEIC超頻出**", "").replace("**🎯 TOEIC頻出**", "").strip()
            html += f'\t\t\t<div class="point-area"><span class="point-label">Point：</span>\n'
            html += f'\t\t\t\t<p>{point}</p>\n'
            html += f'\t\t\t</div>\n'

    else:
        # Placeholder content for missing cards
        html += f'\t\t\t<div class="point-area"><span class="point-label">Note：</span>\n'
        html += f'\t\t\t\t<p>詳細な解説は準備中です。</p>\n'
        html += f'\t\t\t</div>\n'

    html += f'\t\t</div>\n'
    html += f'\t</div>\n\n'
    return html

cards_html = ""

# Define Sections to process
# Format: (Section Number, Phrasal List Title, Path to Phrasal List)
sections_config = [
    ("01", "基本・最優先（18表現）", r'c:\Users\yuto\OneDrive\Toeic-cards--main\verbs\have\phrasal\01\phrasal01の原文テキスト.txt'),
    ("02", "日常・TOEIC（36表現）", r'c:\Users\yuto\OneDrive\Toeic-cards--main\verbs\have\phrasal\02\phrasal02の原文テキスト.txt')
]

for sec_num, sec_title, phr_path in sections_config:
    # Add Section details
    cards_html += f'\t<!-- SECTION {sec_num} -->\n'
    cards_html += f'\t<div class="section-title">\n'
    cards_html += f'\t\t<span class="section-badge">{sec_num}</span>\n'
    cards_html += f'\t\t{sec_title}\n'
    cards_html += f'\t</div>\n\n'
    
    # Read Phrasal List
    try:
        with open(phr_path, 'r', encoding='utf-8') as f:
            phr_lines = f.readlines()
    except FileNotFoundError:
        print(f"Warning: Phrasal list {phr_path} not found.")
        continue

    # Parse phrases from list
    # Format: phrase - translation
    for line in phr_lines:
        line = line.strip()
        if not line or "｜" in line or "合計フレーズ数" in line or "目安" in line or "レベル" in line:
            continue
            
        parts = line.split(' - ')
        if len(parts) >= 2:
            phrase = parts[0].strip()
            translation = parts[1].strip()
            
            # Lookup in content map
            if phrase in content_map:
                # Use data from content map (prefer translation from map if available, or list)
                data = content_map[phrase]
                cards_html += generate_card(phrase, data['translation'], data['content'], data['is_polysemy'])
            else:
                # Generate simple card
                cards_html += generate_card(phrase, translation)



# Footer
footer = '''	<!-- Footer -->
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
