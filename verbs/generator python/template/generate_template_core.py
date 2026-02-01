import re
import os

# ==========================================
# CONFIGURATION
# ==========================================
TARGET_VERB = "template_verb"  # REPLACE THIS with the target verb (e.g., "have", "make")
VERB_TITLE = TARGET_VERB.upper() # Main title verb
JAPANESE_TITLE = f"{VERB_TITLE} 完全解説｜全レベル網羅"

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VERB_DIR = os.path.join(BASE_DIR, TARGET_VERB)
SOURCE_PATH = os.path.join(VERB_DIR, 'core', 'coreの原文テキスト.txt')
OUTPUT_PATH = os.path.join(VERB_DIR, 'core', 'index.html')

# ==========================================
# TEMPLATE
# ==========================================

html_header = f'''<!doctype html>
<html lang="ja">

<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>{JAPANESE_TITLE}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@500;700;900&family=Poppins:wght@600;700&display=swap"
        rel="stylesheet">
    <style>
        body {{
            font-family: 'Noto Sans JP', system-ui, sans-serif;
            background-color: #f1f5f9;
            color: #334155;
            line-height: 1.6;
        }}

        .font-poppins {{
            font-family: 'Poppins', system-ui, sans-serif;
        }}

        /* Animations */
        .fade-in-up {{
            animation: fadeInUp 0.8s ease-out forwards;
            opacity: 0;
            transform: translateY(20px);
        }}

        @keyframes fadeInUp {{
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .delay-100 {{
            animation-delay: 0.1s;
        }}

        .delay-200 {{
            animation-delay: 0.2s;
        }}

        .delay-300 {{
            animation-delay: 0.3s;
        }}

        .delay-400 {{
            animation-delay: 0.4s;
        }}

        .delay-500 {{
            animation-delay: 0.5s;
        }}

        /* Card Hover */
        .hover-card {{
            transition: all 0.3s ease;
        }}

        .hover-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }}

        /* Visual Text */
        .core-box {{
            background-color: #fff7ed;
            /* Orange-50 */
            border: 1px dashed #fdba74;
            /* Orange-300 */
            padding: 1rem;
            border-radius: 0.75rem;
            text-align: center;
            margin-bottom: 1rem;
        }}

        .visual-text {{
            display: block;
            font-family: monospace;
            color: #c2410c;
            font-weight: 700;
            margin-top: 0.5rem;
            white-space: pre-wrap;
        }}

        /* Badges */
        .level-badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 900;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}
    </style>
</head>

<body class="p-6 md:p-12">
    <div class="max-w-6xl mx-auto space-y-16">

        <!-- Header -->
        <header class="text-center space-y-6 fade-in-up">
            <div
                class="inline-block bg-slate-800 text-white px-5 py-2 rounded-full text-xs font-black tracking-widest border border-slate-700">
                VERB SERIES: {VERB_TITLE}
            </div>
            <h1 class="text-3xl md:text-5xl font-black text-slate-900 leading-tight">
                {VERB_TITLE} のレベル別完全解説
            </h1>
            <p class="text-lg font-bold text-slate-500">
                コアイメージから難関大・ビジネスレベルまで全網羅
            </p>
        </header>
'''

html_footer = '''        <!-- Footer -->
        <footer
            class="text-center text-xs text-slate-400 font-bold py-10 border-t border-slate-200 mt-12 fade-in-up delay-500">
            <a href="../" class="inline-flex items-center gap-2 hover:text-orange-600 transition-colors">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                </svg>
                トップへ戻る
            </a>
        </footer>

    </div>
</body>

</html>'''

# Helper to parse phrasal verb block
def parse_phrasal_block(block):
    # Header: ### **phrase - translation**
    header_match = re.search(r'### \*\*(.*?) - (.*?)\*\*', block)
    if not header_match:
        return None
    phrase = header_match.group(1).strip()
    translation = header_match.group(2).strip()
    
    # Core Image (optional)
    core_match = re.search(r'```\n(.*?)\n```', block, re.DOTALL)
    visual = core_match.group(1).strip() if core_match else ""
    
    # Description: text between core block and "**例文：**"
    # Or if no core block, text between header and "**例文：**"
    rest_block = block[header_match.end():]
    
    description = ""
    if visual:
        # Look for text after code block
        desc_match = re.search(r'```\n.*?\n```\s*\n\n(.*?)\n\n\*\*例文：\*\*', rest_block, re.DOTALL)
        if desc_match:
            description = desc_match.group(1).strip()
    else:
        # Look for text before examples
        desc_match = re.search(r'^\s*(.*?)\n\n\*\*例文：\*\*', rest_block, re.DOTALL)
        if desc_match:
            description = desc_match.group(1).strip()
    
    # Examples
    examples = []
    ex_matches = re.findall(r'- (.*?)\n  → (.*?)(?=\n|$)', block)
    for en, jp in ex_matches:
        examples.append({'en': en.strip(), 'jp': jp.strip()})
        
    # Point
    point_match = re.search(r'\*\*ポイント：\*\* (.*)', block)
    point = point_match.group(1).strip() if point_match else ""
    
    return {
        'phrase': phrase,
        'translation': translation,
        'visual': visual,
        'description': description,
        'examples': examples,
        'point': point
    }

def main():
    if not os.path.exists(SOURCE_PATH):
        print(f"Error: Source file not found: {SOURCE_PATH}")
        return

    with open(SOURCE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    generated_content = ""

    # 1. CORE IMAGE SECTION
    core_match = re.search(rf'## 🎯 {VERB_TITLE}のコアイメージ\n\n```\n(.*?)\n```\n\n(.*?)\n\n---', content, re.DOTALL)
    if core_match:
        visual_text = core_match.group(1).strip()
        explanation = re.search(r'本質：「(.*?)」', core_match.group(2)).group(1) if '本質：' in core_match.group(2) else ""
        
        generated_content += f'''        <!-- CORE IMAGE SECTION -->
        <section
            class="bg-white border border-slate-200 rounded-3xl p-8 shadow-sm fade-in-up delay-100 border-t-4 border-t-orange-500">
            <div class="text-center space-y-4">
                <h2 class="text-2xl font-black text-orange-600">🎯 {VERB_TITLE}のコアイメージ（基礎）</h2>
                <p class="font-bold text-slate-700">本質：「{explanation}」</p>

                <div class="core-box max-w-md mx-auto">
                    <span class="visual-text">{visual_text}</span>
                </div>
            </div>
        </section>
'''

    # Parse sections
    sections = re.split(r'\n## ', content)

    for section in sections:
        if section.startswith('📚 中学生レベル'):
            # LEVEL 1
            section_badge = '<span class="level-badge bg-orange-100 text-orange-700">Level 1</span>'
            generated_content += f'''
            <!-- LEVEL 1: MIDDLE SCHOOL -->
            <section class="space-y-6 fade-in-up delay-200">
                <div class="flex items-center gap-3 border-b border-slate-200 pb-3 mt-8">
                    {section_badge}
                    <h2 class="text-2xl font-black text-slate-800">📚 中学生レベルの語法</h2>
                </div>
                <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
    '''
            blocks = re.split(r'\n(?=### )', section)
            idx = 1
            for block in blocks:
                if not block.strip() or not block.startswith('###'): continue
                data = parse_phrasal_block(block)
                if not data: continue
                
                core_snippet = "..."
                if '「' in data['description'] and '」' in data['description']:
                    core_snippet = data['description'].split('「')[1].split('」')[0]
                
                generated_content += f'''
                    <!-- {idx} -->
                    <div class="bg-white border border-slate-200 rounded-2xl p-6 hover-card">
                        <h3 class="text-lg font-black text-orange-700 mb-2">{idx}. {data['phrase']}</h3>
                        <p class="text-xs font-bold text-slate-400 mb-4">コアイメージ：{core_snippet}</p>
                        <ul class="space-y-4 text-sm text-slate-700">
    '''
                for ex in data['examples']:
                    generated_content += f'''                        <li>
                                <p class="font-bold font-poppins">{ex['en']}</p>
                                <p class="text-xs text-slate-500">{ex['jp']}</p>
                            </li>
    '''
                generated_content += f'''                    </ul>
                        <div class="mt-4 pt-4 border-t border-slate-100 text-xs text-slate-500 bg-orange-50 p-3 rounded">
                            <span class="font-bold text-orange-600 block mb-1">ポイント：</span>
                            {data['point']}
                        </div>
                    </div>
    '''
                idx += 1
            generated_content += '''            </div>
            </section>
    '''

        elif section.startswith('🎓 高校生レベル'):
            # LEVEL 2
            section_badge = '<span class="level-badge bg-indigo-100 text-indigo-700">Level 2</span>'
            generated_content += f'''
            <!-- LEVEL 2: HIGH SCHOOL -->
            <section class="space-y-6 fade-in-up delay-300">
                <div class="flex items-center gap-3 border-b border-slate-200 pb-3 mt-8">
                    {section_badge}
                    <h2 class="text-2xl font-black text-slate-800">🎓 高校生レベルの語法</h2>
                </div>
                <div class="grid md:grid-cols-2 gap-6">
    '''
            blocks = re.split(r'\n(?=### )', section)
            idx = 1
            for block in blocks:
                if not block.strip() or not block.startswith('###'): continue
                data = parse_phrasal_block(block)
                if not data: continue
                
                core_snippet = "..."
                if '「' in data['description'] and '」' in data['description']:
                    core_snippet = data['description'].split('「')[1].split('」')[0]
                
                generated_content += f'''
                    <!-- {idx} -->
                    <div class="bg-white border border-slate-200 rounded-2xl p-6 hover-card">
                        <h3 class="text-lg font-black text-indigo-700 mb-2">{idx}. {data['phrase']}</h3>
                        <p class="text-xs font-bold text-slate-400 mb-4">コアイメージ：{core_snippet}</p>
                        <div class="space-y-4">
    '''
                for ex in data['examples']:
                    generated_content += f'''                        <div>
                                <p class="text-sm font-bold font-poppins text-slate-700">{ex['en']}</p>
                                <p class="text-xs text-slate-500">{ex['jp']}</p>
                            </div>
    '''
                generated_content += f'''                    </div>
                        <p class="mt-4 pt-4 border-t border-slate-100 text-xs text-slate-500">
                            <span class="font-bold text-indigo-600">ポイント：</span>{data['point']}
                        </p>
                    </div>
    '''
                idx += 1
            generated_content += '''            </div>
            </section>
    '''

        elif section.startswith('🏆 難関大学合格レベル'):
            # LEVEL 3
            section_badge = '<span class="level-badge bg-amber-100 text-amber-700">Level 3</span>'
            generated_content += f'''
            <!-- LEVEL 3: UNIVERSITY -->
            <section class="space-y-6 fade-in-up delay-400">
                <div class="flex items-center gap-3 border-b border-slate-200 pb-3 mt-8">
                    {section_badge}
                    <h2 class="text-2xl font-black text-slate-800">🏆 難関大学合格レベルの語法</h2>
                </div>
                <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
    '''
            blocks = re.split(r'\n(?=### )', section)
            idx = 1
            for block in blocks:
                if not block.strip() or not block.startswith('###'): continue
                data = parse_phrasal_block(block)
                if not data: continue
                
                first_ex = data['examples'][0] if data['examples'] else {'en': '', 'jp': ''}
                
                generated_content += f'''
                    <div class="bg-white border border-slate-200 rounded-2xl p-6 hover-card">
                        <h3 class="text-lg font-black text-amber-700 mb-2">{idx}. {data['phrase']}</h3>
                        <p class="text-xs font-bold text-slate-400 mb-4">{data['translation']}</p>
                        <p class="text-sm font-bold font-poppins text-slate-700">{first_ex['en']}</p>
                        <p class="text-xs text-slate-500 mt-2">{first_ex['jp']}</p>
                    </div>
    '''
                idx += 1
            generated_content += '''            </div>
            </section>
    '''

        elif section.startswith('💼 TOEIC頻出ビジネス英語'):
            # BUSINESS
            section_badge = '<span class="level-badge bg-purple-100 text-purple-700">TOEIC</span>'
            generated_content += f'''
            <!-- BUSINESS: TOEIC -->
            <section class="space-y-6 fade-in-up delay-500">
                <div class="flex items-center gap-3 border-b border-slate-200 pb-3 mt-8">
                    {section_badge}
                    <h2 class="text-2xl font-black text-slate-800">💼 TOEIC頻出ビジネス英語の語法</h2>
                </div>
                <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
    '''
            blocks = re.split(r'\n(?=### )', section)
            idx = 1
            for block in blocks:
                if not block.strip() or not block.startswith('###'): continue
                data = parse_phrasal_block(block)
                if not data: continue
                
                first_ex = data['examples'][0]['en'] if data['examples'] else ""
                
                generated_content += f'''
                    <div class="bg-white p-5 rounded-xl border border-slate-200 hover:shadow-md transition">
                        <h4 class="font-black text-purple-700 mb-1">{idx}. {data['phrase']}</h4>
                        <p class="text-xs font-bold text-slate-500 mb-2">{data['translation']}</p>
                        <p class="text-sm text-slate-700">{first_ex}</p>
                    </div>
    '''
                idx += 1
            generated_content += '''            </div>
            </section>
    '''
    
    # Write complete HTML
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(html_header + generated_content + html_footer)

    print(f"Generated {OUTPUT_PATH} successfully!")

if __name__ == "__main__":
    main()
