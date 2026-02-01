# Script to generate HAVE guide part2.html from source text
import re

# Read source text
with open(r'c:\Users\yuto\OneDrive\Toeic-cards--main\verbs\have\guide\part2の原文テキスト.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# HTML header
html = '''<!DOCTYPE html>
<html lang="ja">

<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>HAVE 句動詞 完全解説【後編】 - Phrasal Verb Master</title>
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
			HAVE 句動詞 <span class="text-cyan-600">完全解説【後編】</span>
		</h1>
		<p class="text-slate-500 font-bold">多義語・慣用表現（Section 3〜4）</p>
	</header>

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
    
    # Extract section description (text before first ###)
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
    
    # Parse polysemous phrasal verbs (多義語) - special format
    polysemy_phrases = re.split(r'### \*\*([^*]+)（多義）\*\*', section_content)
    
    for j in range(1, len(polysemy_phrases), 2):
        phrase = polysemy_phrases[j].strip()
        phrase_content = polysemy_phrases[j+1]
        
        # Extract intro text
        intro_match = re.search(r'^(.*?)(?=\*\*意味\d+：)', phrase_content, re.DOTALL)
        intro_text = intro_match.group(1).strip() if intro_match else ""
        intro_text = re.sub(r'^---+\s*$', '', intro_text, flags=re.MULTILINE).strip()
        
        # Extract all meanings
        meanings = re.findall(r'\*\*意味(\d+)：([^*]+)\*\*\s*```\n(.*?)\n```\s*\n(.*?)(?=\*\*意味\d+：|\*\*ポイント：|$)', phrase_content, re.DOTALL)
        
        # Extract point
        point_match = re.search(r'\*\*ポイント：\*\* (.+?)(?=\n\n---|$)', phrase_content, re.DOTALL)
        point = point_match.group(1).strip() if point_match else ""
        
        # Check for TOEIC badge
        toeic_badge = ""
        if "🎯 TOEIC" in point:
            toeic_badge = '<span class="bg-amber-100 text-amber-700 text-xs font-bold px-2 py-1 rounded-full border border-amber-200 ml-2">TOEIC頻出</span>'
            point = point.replace("**🎯 TOEIC超頻出**", "").replace("**🎯 TOEIC頻出**", "").strip()
        
        # Build polysemy card HTML
        cards_html += f'\t<!-- {phrase}（多義） -->\n'
        cards_html += f'\t<div class="card">\n'
        cards_html += f'\t\t<div class="card-header"><span class="phrase">{phrase}</span><span class="translation">多義語</span>{toeic_badge}</div>\n'
        cards_html += f'\t\t<div class="card-body">\n'
        
        # Intro text
        if intro_text:
            cards_html += f'\t\t\t<p class="text-slate-600 mb-4">{intro_text}</p>\n'
        
        # Each meaning
        for meaning_num, meaning_title, core_text, examples_text in meanings:
            cards_html += f'\t\t\t<div class="meaning-section">\n'
            cards_html += f'\t\t\t\t<div class="meaning-title">意味{meaning_num}：{meaning_title}</div>\n'
            
            # Core image for this meaning
            if core_text.strip():
                core_lines = core_text.strip().split('\n')
                core_visual = '<br>'.join(core_lines)
                cards_html += f'\t\t\t\t<div class="core-box"><span class="core-title">コアイメージ</span>\n'
                cards_html += f'\t\t\t\t\t<div class="visual-text">{core_visual}</div>\n'
                cards_html += f'\t\t\t\t</div>\n'
            
            # Examples for this meaning
            examples = re.findall(r'- (.+?)\n  → (.+?)(?=\n\n|- |$)', examples_text, re.DOTALL)
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

# Extract summary section (## まとめ)
summary_html = ""
summary_match = re.search(r'## まとめ\s*\n\n(.*?)(?=\n---\n\n\*\*HAVE句動詞大全|$)', content, re.DOTALL)
if summary_match:
    summary_content = summary_match.group(1).strip()
    
    # Build summary HTML
    summary_html += '\t<!-- Summary Section -->\n'
    summary_html += '\t<div class="card" style="background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%); border: none; margin-top: 48px;">\n'
    summary_html += '\t\t<div class="card-header" style="background: rgba(255,255,255,0.1); border-bottom: 1px solid rgba(255,255,255,0.2);">\n'
    summary_html += '\t\t\t<span class="phrase" style="color: white; font-size: 2rem;">📚 まとめ</span>\n'
    summary_html += '\t\t</div>\n'
    summary_html += '\t\t<div class="card-body" style="color: white;">\n'
    
    # Split by sections (marked by **)
    lines = summary_content.split('\n')
    current_section = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if it's a section header (starts with **)
        if line.startswith('**') and line.endswith('**'):
            # Output previous section if exists
            if current_section:
                summary_html += '\t\t\t<div class="mb-6">\n'
                for item in current_section:
                    summary_html += f'\t\t\t\t<p class="ml-4">{item}</p>\n'
                summary_html += '\t\t\t</div>\n'
                current_section = []
            
            # Add section header
            section_title = line.replace('**', '').replace('：', ':')
            summary_html += f'\t\t\t<h3 class="text-xl font-bold mb-3 mt-6" style="color: #67e8f9;">{section_title}</h3>\n'
        elif line.startswith('-'):
            # List item
            item_text = line[1:].strip()
            current_section.append(f'• {item_text}')
        else:
            # Regular paragraph
            if current_section:
                summary_html += '\t\t\t<div class="mb-6">\n'
                for item in current_section:
                    summary_html += f'\t\t\t\t<p class="ml-4">{item}</p>\n'
                summary_html += '\t\t\t</div>\n'
                current_section = []
            summary_html += f'\t\t\t<p class="mb-4 text-lg leading-relaxed">{line}</p>\n'
    
    # Output remaining items
    if current_section:
        summary_html += '\t\t\t<div class="mb-6">\n'
        for item in current_section:
            summary_html += f'\t\t\t\t<p class="ml-4">{item}</p>\n'
        summary_html += '\t\t\t</div>\n'
    
    summary_html += '\t\t</div>\n'
    summary_html += '\t</div>\n\n'
    
    # Add completion message
    summary_html += '\t<div class="text-center mt-8 mb-8">\n'
    summary_html += '\t\t<p class="text-2xl font-black text-slate-800">🎉 HAVE句動詞大全（全編）完 🎉</p>\n'
    summary_html += '\t</div>\n\n'

# Footer
footer = '''\t<!-- Footer -->
	<footer class="text-center mt-12 mb-12">
		<a href="./part1.html"
			class="inline-block bg-slate-600 text-white font-bold py-4 px-8 rounded-full shadow hover:bg-slate-700 transition">
			← HAVE 句動詞【前編】に戻る
		</a>
	</footer>

</body>

</html>'''

# Write complete HTML
with open(r'c:\Users\yuto\OneDrive\Toeic-cards--main\verbs\have\guide\part2.html', 'w', encoding='utf-8') as f:
    f.write(html + cards_html + summary_html + footer)

print("Generated part2.html successfully!")
