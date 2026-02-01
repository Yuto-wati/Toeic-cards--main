import re
import os

# ==========================================
# CONFIGURATION
# ==========================================
TARGET_VERB = "template_verb"  # REPLACE THIS with the target verb
# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VERB_BASE_DIR = os.path.join(BASE_DIR, TARGET_VERB, 'phrasal')
OUTPUT_BASE_DIR = os.path.join(BASE_DIR, TARGET_VERB, 'phrasal')

# ==========================================
# TEMPLATE
# ==========================================

def generate_phrasal_list(group_id):
    group_str = f"{group_id:02d}"
    source_path = os.path.join(VERB_BASE_DIR, f"{group_str}", f'phrasal{group_str}の原文テキスト.txt')
    output_path = os.path.join(OUTPUT_BASE_DIR, group_str, 'index.html')
    
    if not os.path.exists(source_path):
        print(f"Skipping {group_str}: Source not found at {source_path}")
        return

    with open(source_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Parse content
    title_line = ""
    phrases = []
    
    # Check for Statistics section delimiter
    stats_start_idx = -1
    for i, line in enumerate(lines):
        if "📊 統計情報" in line:
            stats_start_idx = i
            break
    
    # Look only at lines before stats for phrase parsing
    parse_lines = lines[:stats_start_idx] if stats_start_idx != -1 else lines

    for line in parse_lines:
        line = line.strip()
        if not line: continue
        
        # Line 2 typically contains the group title "01｜基本・最優先"
        if line.startswith(f"{group_str}｜"):
            title_line = line
            continue
            
        # Parse phrases: phrase - translation
        # Use regex to be flexible about spaces
        match = re.match(r'^(.*?)\s+-\s+(.*)$', line)
        if match:
            phrases.append({
                'phrase': match.group(1).strip(),
                'trans': match.group(2).strip()
            })
            
    # Extract subtitle from title line
    subtitle = title_line.split('｜')[1] if '｜' in title_line else "Phrases"
    
    # Define Description text - Customize this per verb if needed
    header_description = "Essential phrases." 
    # Example logic, customize as needed
    if group_id == 1:
        header_description = "最も重要な基本フレーズ。"
    elif group_id == 2:
        header_description = "表現力を広げる日常・学習フレーズ。"
    elif group_id == 3:
        header_description = "ビジネスで必須の表現。"
    elif group_id == 4:
        header_description = "多義語・注意すべき表現。"

    # HTML Template
    html = f'''<!doctype html>
<html lang="ja">

<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>{TARGET_VERB} 句動詞 {group_str}｜{subtitle}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@500;700;900&family=Poppins:wght@600;700&display=swap"
        rel="stylesheet">
    <style>
        body {{
            font-family: 'Noto Sans JP', sans-serif;
            background-color: #f8fafc;
            color: #334155;
        }}

        .font-poppins {{
            font-family: 'Poppins', sans-serif;
        }}

        .hover-card {{
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .hover-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, .1);
        }}
    </style>
</head>

<body class="p-6 md:p-12">
    <div class="max-w-4xl mx-auto space-y-12">

        <!-- Header -->
        <header class="space-y-4 border-b border-orange-100 pb-6">
            <a href="../"
                class="inline-flex items-center text-xs font-bold text-slate-400 hover:text-orange-600 transition-colors">
                ◀ INDEXに戻る
            </a>
            <div class="space-y-2">
                <div
                    class="inline-block bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-xs font-black tracking-widest font-poppins">
                    GROUP {group_str}</div>
                <h1 class="text-3xl md:text-4xl font-black text-slate-900">{TARGET_VERB} 句動詞 {group_str}｜{subtitle}</h1>
                <p class="text-orange-600 font-bold">{header_description}</p>
            </div>
        </header>

        <!-- List -->
        <main class="grid md:grid-cols-2 gap-4">
'''

    # Generate Cards
    for i, p in enumerate(phrases, 1):
        html += f'''            <div class="bg-white border border-slate-200 border-l-[6px] border-l-orange-400 rounded-2xl p-5 hover-card">
                <h3 class="text-lg font-bold font-poppins text-slate-800 mb-1"><span
                        class="text-orange-500 mr-2">{i}.</span>{p['phrase']}</h3>
                <p class="text-sm text-slate-700 font-bold">{p['trans']}</p>
            </div>
'''

    html += f'''        </main>

        <!-- Navigation Footer -->
        <footer
            class="flex flex-col md:flex-row justify-between items-center gap-6 py-10 mt-12 border-t border-slate-200">
            <div class="w-full md:w-auto"><span></span></div>

            <a href="../" class="text-sm font-black text-slate-500 hover:text-orange-600 transition-colors">
                ← 一覧に戻る
            </a>

            <div class="w-full md:w-auto text-right">
                {'<a href="../' + f"{group_id+1:02d}" + '/" class="text-sm font-black text-slate-700 hover:text-orange-600 transition-colors">次へ →</a>' if group_id < 4 else ''}
            </div>
        </footer>

    </div>
</body>

</html>'''

    # Write output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated {output_path} with {len(phrases)} phrases.")

if __name__ == "__main__":
    # Run for 01-04
    for i in range(1, 5):
        generate_phrasal_list(i)
