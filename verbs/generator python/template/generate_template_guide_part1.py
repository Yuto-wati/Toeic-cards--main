import re
import os
from jinja2 import Environment, FileSystemLoader

# ==========================================
# CONFIGURATION
# ==========================================
TARGET_VERB = "template_verb" # REPLACE THIS
VERB_TITLE = TARGET_VERB.upper()
JAPANESE_TITLE = f"{VERB_TITLE} 句動詞 完全解説【前編】 - Phrasal Verb Master"

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VERB_DIR = os.path.join(BASE_DIR, TARGET_VERB)
GUIDE_SOURCE_PATH = os.path.join(VERB_DIR, 'guide', 'part1の原文テキスト.txt')
OUTPUT_PATH = os.path.join(VERB_DIR, 'guide', 'part1.html')
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

# Phrasal List Source Paths (used as Master List)
PHRASAL_LIST_PATHS = [
    ("01", "基本・最優先", os.path.join(VERB_DIR, 'phrasal', '01', 'phrasal01の原文テキスト.txt')),
    ("02", "日常・TOEIC", os.path.join(VERB_DIR, 'phrasal', '02', 'phrasal02の原文テキスト.txt'))
]

def prepare_card_data(phrase, translation, existing_content=None, is_polysemy=False):
    card_data = {
        'phrase': phrase,
        'translation': translation,
        'existing_content': False,
        'toeic_badge': False,
        'is_polysemy': is_polysemy,
        'intro_text': "",
        'meanings': [],
        'core_visual': "",
        'examples': [],
        'point': ""
    }

    if not existing_content:
        return card_data
    
    card_data['existing_content'] = True
    
    # Check TOEIC Badge
    point_match = re.search(r'\*\*ポイント：\*\* (.+?)(?=\n\n---|$)', existing_content, re.DOTALL)
    if point_match:
        point_text = point_match.group(1).strip()
        if "🎯 TOEIC" in point_text:
            card_data['toeic_badge'] = True

    if is_polysemy:
        # Polysemy Logic
        intro_match = re.search(r'^(.*?)(?=\*\*意味\d+：)', existing_content, re.DOTALL)
        if intro_match:
            intro_text = intro_match.group(1).strip()
            intro_text = re.sub(r'^---+\s*$', '', intro_text, flags=re.MULTILINE).strip()
            if intro_text:
                card_data['intro_text'] = intro_text
        
        meanings = re.findall(r'\*\*意味(\d+)：([^*]+)\*\*\s*```\n(.*?)\n```\s*\n(.*?)(?=\*\*意味\d+：|\*\*ポイント：|$)', existing_content, re.DOTALL)
        for m_num, m_title, m_core, m_examples in meanings:
            m_ex_list = []
            examples = re.findall(r'- (.+?)\n  → (.+?)(?=\n\n|- |$)', m_examples, re.DOTALL)
            for en, jp in examples:
                m_ex_list.append({'en': en.strip(), 'jp': jp.strip()})
            
            card_data['meanings'].append({
                'num': m_num,
                'title': m_title,
                'core': m_core.strip().replace(chr(10), "<br>") if m_core.strip() else "",
                'examples': m_ex_list
            })
            
    else:
        # Normal Logic
        core_match = re.search(r'```\n(.*?)\n```', existing_content, re.DOTALL)
        if core_match:
            card_data['core_visual'] = core_match.group(1).strip().replace('\n', '<br>')
        
        examples_match = re.search(r'\*\*例文：\*\*\s*\n\n(.*?)\n\n\*\*ポイント：\*\*', existing_content, re.DOTALL)
        if examples_match:
            examples_text = examples_match.group(1)
            examples = re.findall(r'- (.+?)\n  → (.+?)(?=\n\n|- |$)', examples_text, re.DOTALL)
            for en, jp in examples:
                card_data['examples'].append({'en': en.strip(), 'jp': jp.strip()})

    # Point Extraction
    point_match = re.search(r'\*\*ポイント：\*\* (.+?)(?=\n\n---|$)', existing_content, re.DOTALL)
    if point_match:
        card_data['point'] = point_match.group(1).replace("**🎯 TOEIC超頻出**", "").replace("**🎯 TOEIC頻出**", "").strip()

    return card_data

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

    # Prepare Sections Data
    sections_data = []
    
    for sec_num, sec_name, phr_path in PHRASAL_LIST_PATHS:
        if not os.path.exists(phr_path):
            print(f"Warning: Phrasal list missing: {phr_path}")
            continue

        with open(phr_path, 'r', encoding='utf-8') as f:
            phr_lines = f.readlines()
            
        phrases_in_section = []
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
            cards = []
            for phrase, translation in phrases_in_section:
                if phrase in content_map:
                    data = content_map[phrase]
                    cards.append(prepare_card_data(phrase, data['translation'], data['content'], data['is_polysemy']))
                else:
                    cards.append(prepare_card_data(phrase, translation))
            
            sections_data.append({
                'num': sec_num,
                'name': sec_name,
                'phrases': phrases_in_section,
                'cards': cards
            })

    # Render Template
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template('guide_part1_template.html')
    
    html_output = template.render(
        title=JAPANESE_TITLE,
        verb_title=VERB_TITLE,
        sections=sections_data
    )

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(html_output)
    print(f"Generated {OUTPUT_PATH} using Jinja2")

if __name__ == "__main__":
    main()
