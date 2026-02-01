import re
import os
from jinja2 import Environment, FileSystemLoader

# ==========================================
# CONFIGURATION
# ==========================================
TARGET_VERB = "template_verb"  # REPLACE THIS
VERB_TITLE = TARGET_VERB.upper()
JAPANESE_TITLE = f"{VERB_TITLE} 完全解説｜全レベル網羅"

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VERB_DIR = os.path.join(BASE_DIR, TARGET_VERB)
SOURCE_PATH = os.path.join(VERB_DIR, 'core', 'coreの原文テキスト.txt')
OUTPUT_PATH = os.path.join(VERB_DIR, 'core', 'index.html')
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

def parse_phrasal_block(block):
    header_match = re.search(r'### \*\*(.*?) - (.*?)\*\*', block)
    if not header_match:
        return None
    phrase = header_match.group(1).strip()
    translation = header_match.group(2).strip()
    
    # Core Image (optional)
    core_match = re.search(r'```\n(.*?)\n```', block, re.DOTALL)
    visual = core_match.group(1).strip() if core_match else ""
    
    rest_block = block[header_match.end():]
    description = ""
    
    # Description logic
    if visual:
        desc_match = re.search(r'```\n.*?\n```\s*\n\n(.*?)\n\n\*\*例文：\*\*', rest_block, re.DOTALL)
        if desc_match:
            description = desc_match.group(1).strip()
    else:
        desc_match = re.search(r'^\s*(.*?)\n\n\*\*例文：\*\*', rest_block, re.DOTALL)
        if desc_match:
            description = desc_match.group(1).strip()
            
    core_snippet = "..."
    if '「' in description and '」' in description:
        core_snippet = description.split('「')[1].split('」')[0]

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
        'core_snippet': core_snippet,
        'examples': examples,
        'point': point,
        'first_en': examples[0]['en'] if examples else "",
        'first_jp': examples[0]['jp'] if examples else ""
    }

def main():
    if not os.path.exists(SOURCE_PATH):
        print(f"Error: Source file not found: {SOURCE_PATH}")
        return

    with open(SOURCE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. CORE IMAGE SECTION
    core_image_data = None
    core_match = re.search(rf'## 🎯 {VERB_TITLE}のコアイメージ\n\n```\n(.*?)\n```\n\n(.*?)\n\n---', content, re.DOTALL)
    if core_match:
        visual_text = core_match.group(1).strip()
        explanation = re.search(r'本質：「(.*?)」', core_match.group(2)).group(1) if '本質：' in core_match.group(2) else ""
        core_image_data = {
            'visual_text': visual_text,
            'explanation': explanation
        }

    # 2. SECTIONS
    sections_data = []
    raw_sections = re.split(r'\n## ', content)
    
    for section in raw_sections:
        section_data = None
        
        if section.startswith('📚 中学生レベル'):
             blocks = re.split(r'\n(?=### )', section)
             items = [parse_phrasal_block(b) for b in blocks if b.strip() and b.startswith('###')]
             items = [i for i in items if i] # Filter Nones
             
             section_data = {
                 'title': '📚 中学生レベルの語法',
                 'type': 'level1',
                 'badge': '<span class="level-badge bg-orange-100 text-orange-700">Level 1</span>',
                 'delay_class': 'delay-200',
                 'grid_class': 'md:grid-cols-2 lg:grid-cols-3',
                 'h3_color': 'text-orange-700',
                 'point_label_color': 'text-orange-600',
                 'items': items
             }
             
        elif section.startswith('🎓 高校生レベル'):
             blocks = re.split(r'\n(?=### )', section)
             items = [parse_phrasal_block(b) for b in blocks if b.strip() and b.startswith('###')]
             items = [i for i in items if i]
             
             section_data = {
                 'title': '🎓 高校生レベルの語法',
                 'type': 'level2',
                 'badge': '<span class="level-badge bg-indigo-100 text-indigo-700">Level 2</span>',
                 'delay_class': 'delay-300',
                 'grid_class': 'md:grid-cols-2',
                 'h3_color': 'text-indigo-700',
                 'point_label_color': 'text-indigo-600',
                 'items': items
             }

        elif section.startswith('🏆 難関大学合格レベル'):
             blocks = re.split(r'\n(?=### )', section)
             items = [parse_phrasal_block(b) for b in blocks if b.strip() and b.startswith('###')]
             items = [i for i in items if i]
             
             section_data = {
                 'title': '🏆 難関大学合格レベルの語法',
                 'type': 'level3',
                 'badge': '<span class="level-badge bg-amber-100 text-amber-700">Level 3</span>',
                 'delay_class': 'delay-400',
                 'grid_class': 'md:grid-cols-2 lg:grid-cols-4',
                 'items': items
             }
             
        elif section.startswith('💼 TOEIC頻出ビジネス英語'):
             blocks = re.split(r'\n(?=### )', section)
             items = [parse_phrasal_block(b) for b in blocks if b.strip() and b.startswith('###')]
             items = [i for i in items if i]
             
             section_data = {
                 'title': '💼 TOEIC頻出ビジネス英語の語法',
                 'type': 'business',
                 'badge': '<span class="level-badge bg-purple-100 text-purple-700">TOEIC</span>',
                 'delay_class': 'delay-500',
                 'grid_class': 'md:grid-cols-2 lg:grid-cols-4',
                 'items': items
             }
        
        if section_data:
            sections_data.append(section_data)

    # Render
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template('core_template.html')
    
    html_output = template.render(
        title=JAPANESE_TITLE,
        verb_title=VERB_TITLE,
        core_image=core_image_data,
        sections=sections_data
    )
    
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(html_output)

    print(f"Generated {OUTPUT_PATH} successfully using Jinja2!")

if __name__ == "__main__":
    main()
