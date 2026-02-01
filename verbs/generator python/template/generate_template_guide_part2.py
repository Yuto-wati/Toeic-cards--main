import re
import os
from jinja2 import Environment, FileSystemLoader

# ==========================================
# CONFIGURATION
# ==========================================
TARGET_VERB = "do" # REPLACE THIS
VERB_TITLE = TARGET_VERB.upper()
JAPANESE_TITLE = f"{VERB_TITLE} 句動詞 完全解説【後編】 - Phrasal Verb Master"

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VERB_DIR = os.path.join(BASE_DIR, TARGET_VERB)
GUIDE_SOURCE_PATH = os.path.join(VERB_DIR, 'guide', 'guide02の原文テキスト.txt')
OUTPUT_PATH = os.path.join(VERB_DIR, 'guide', 'part2.html')
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')

# Phrasal List Source Paths (used as Master List)
PHRASAL_LIST_PATHS = [
    ("03", "ビジネス・上級", os.path.join(VERB_DIR, 'phrasal', '03', 'phrasal03の原文テキスト.txt')),
    ("04", "多義語・注意", os.path.join(VERB_DIR, 'phrasal', '04', 'phrasal04の原文テキスト.txt'))
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
        'point': "",
        'is_stats': False 
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
        # Polysemy Logic for Guide 02 (Global Code Block + Headers)
        
        # 1. Extract Global Code Block (Core Visuals)
        core_map = {}
        global_code_match = re.search(r'```\n(.*?)\n```', existing_content, re.DOTALL)
        if global_code_match:
            code_content = global_code_match.group(1)
            # Split by "意味x:" lines
            parts = re.split(r'(\s*意味\d+[:：].*?)(?=\n\s*意味|[\r\n]+$)', code_content)
            current_num = None
            for part in parts:
                num_match = re.search(r'意味(\d+)[:：]', part)
                if num_match:
                    current_num = num_match.group(1)
                elif current_num and part.strip():
                    # This is the visual text for the current num
                    # If logical line below title
                    clean_core = part.strip()
                    # Remove "意味1: Title" line if it was captured in previous part logic?
                    # Actually split usually keeps separators. 
                    # Let's try simpler regex on the whole block.
                    pass
            
            # Simpler approach: find all "意味N: ... \n Visual..."
            visual_matches = re.findall(r'意味(\d+)[:：]\s*([^\n]+)\n(.*?)(?=\n\s*意味\d+[:：]|$)', code_content, re.DOTALL)
            for v_num, v_title, v_visual in visual_matches:
               core_map[v_num] = v_visual.strip().replace(chr(10), "<br>")

        # 2. Extract Intro Text
        # Text before the first "#### 意味" or "**意味"
        intro_match = re.search(r'^(.*?)(?=(?:####|\*\*)\s*意味\d+)', existing_content, re.DOTALL)
        if intro_match:
            intro_text = intro_match.group(1)
            # Remove the global code block from intro text if it was captured
            intro_text = re.sub(r'```.*?```', '', intro_text, flags=re.DOTALL).strip()
            intro_text = re.sub(r'^---+\s*$', '', intro_text, flags=re.MULTILINE).strip()
            if intro_text:
                card_data['intro_text'] = intro_text

        # 3. Parse Meaning Sections
        # Support both '#### 意味N：Title' and '**意味N：Title**'
        # Note: Guide 02 uses ####.
        
        # Find all sections sections
        sections = re.findall(r'(?:####|\*\*)\s*意味(\d+)[:：]\s*(.*?)(?:\*\*|\n)(.*?)(?=(?:####|\*\*)\s*意味\d+[:：]|(?:💡\s*)?\*\*ポイント：|$)', existing_content, re.DOTALL)
        

        

        
        # print(f"  Found {len(sections)} sections")
        if len(sections) == 0:
             print(f"Warning: No sections found for polysemy phrase '{phrase}'")
             # print(f"Content start: {existing_content[:200]}")
        
        for m_num, m_title, m_content in sections:
            m_title = m_title.strip()
            m_ex_list = []
            
            # Parse Examples in this section
            ex_matches = re.findall(r'- (.+?)\n\s+(?:→\s*)?(.+?)(?=\n\n|- |$)', m_content, re.DOTALL)
            for en, jp in ex_matches:
                 m_ex_list.append({'en': en.strip(), 'jp': jp.strip()})
            
            # Get core visual from map
            m_core = core_map.get(m_num, "")
            
            card_data['meanings'].append({
                'num': m_num,
                'title': m_title,
                'core': m_core,
                'examples': m_ex_list
            })
            
    else:
        # Normal Logic
        core_match = re.search(r'```\n(.*?)\n```', existing_content, re.DOTALL)
        if core_match:
            card_data['core_visual'] = core_match.group(1).strip().replace('\n', '<br>')
            
        examples_match = re.search(r'\*\*例文：\*\*\s*\n+(.*?)\n+(?:💡\s*)?\*\*ポイント：\*\*', existing_content, re.DOTALL)
        if examples_match:
            examples_text = examples_match.group(1)
            examples = re.findall(r'- (.+?)\n\s+(?:→\s*)?(.+?)(?=\n\n|- |$)', examples_text, re.DOTALL)
            for en, jp in examples:
                card_data['examples'].append({'en': en.strip(), 'jp': jp.strip()})
        


    # Point Extraction
    if point_match:
        card_data['point'] = point_match.group(1).replace("**🎯 TOEIC超頻出**", "").replace("**🎯 TOEIC頻出**", "").strip()

    return card_data

def prepare_stats_card(stats_lines):
    items = []
    for sline in stats_lines:
        sline = sline.strip()
        if not sline or "📊 統計情報" in sline: continue
        
        if "合計フレーズ数" in sline:
            items.append({'type': 'total', 'text': sline})
        elif "レベル別内訳" in sline:
            items.append({'type': 'breakdown', 'text': sline})
        elif "💡" in sline or "コアイメージ" in sline:
            items.append({'type': 'core_title'})
        elif "HAVE =" in sline or ("=" in sline and "HAVE" not in sline): # Check simple visual assignment
            items.append({'type': 'visual_text', 'text': sline})
        else:
            items.append({'type': 'text', 'text': sline})
            
    return {
        'phrase': '📊 統計情報',
        'is_stats': True,
        'stats_items': items
    }

def main():
    # PATHS TO BOTH SOURCES
    GUIDE01_PATH = os.path.join(VERB_DIR, 'guide', 'guide01の原文テキスト.txt')
    GUIDE02_PATH = os.path.join(VERB_DIR, 'guide', 'guide02の原文テキスト.txt')

    content_map = {}

    # 1. Parse GUIDE 01 (Standard Format)
    if os.path.exists(GUIDE01_PATH):
        with open(GUIDE01_PATH, 'r', encoding='utf-8') as f:
            content1 = f.read()
        
        # Standard Regex for Guide 01
        matches1 = list(re.finditer(r'### \*\*([^*]+?)(?: - ([^*]+?)|\（多義\）)\*\*(.*?)(?=###|\Z)', content1, re.DOTALL))
        print(f"Guide 01: Found {len(matches1)} items (Standard format).")
        for match in matches1:
            phrase = match.group(1).strip()
            translation = match.group(2).strip() if match.group(2) else "多義語"
            card_content = match.group(3).strip()
            content_map[phrase] = {
                'translation': translation,
                'content': card_content,
                'is_polysemy': "多義" in match.group(0)
            }
    else:
        print(f"Warning: Guide 01 not found at {GUIDE01_PATH}")

    # 2. Parse GUIDE 02 (Numbered Format)
    if os.path.exists(GUIDE02_PATH):
        with open(GUIDE02_PATH, 'r', encoding='utf-8') as f:
            content2 = f.read()

        # Numbered Regex for Guide 02
        # Lookahead must target the specific header pattern to avoid stopping at #### subsections
        matches2 = list(re.finditer(r'### \d+\.\s+([^「\n]+)(?:「([^」]+)」)?(.*?)(?=### \d+\.|\Z)', content2, re.DOTALL))
        print(f"Guide 02: Found {len(matches2)} items (Numbered format).")
        for match in matches2:
            phrase_raw = match.group(1).strip()
            
            # Handle different parentheses formats:
            # - "do in（多義語：2つの意味）" → phrase="do in", translation="多義語", is_polysemy=True
            # - "do by（意味：扱う、処遇する）" → phrase="do by", translation="扱う、処遇する", is_polysemy=False
            # - "do with vs do without（対比：...）" → phrase="do with vs do without", translation="...", is_polysemy=False
            
            # Check if it's polysemy format
            polysemy_match = re.search(r'[（(]多義語[:：]([^）)]+)[）)]', phrase_raw)
            meaning_match = re.search(r'[（(]意味[:：]([^）)]+)[）)]', phrase_raw)
            contrast_match = re.search(r'[（(]対比[:：]([^）)]+)[）)]', phrase_raw)
            
            if polysemy_match:
                # Polysemy format: remove parentheses, use "多義語" as translation
                phrase = re.sub(r'[（(]多義語[:：][^）)]+[）)]', '', phrase_raw).strip()
                translation = match.group(2).strip() if match.group(2) else "多義語"
                is_polysemy = True
            elif meaning_match or contrast_match:
                # Non-polysemy with meaning/contrast in parentheses
                # Extract translation from parentheses
                paren_match = meaning_match or contrast_match
                phrase = re.sub(r'[（(][^）)]+[）)]', '', phrase_raw).strip()
                translation = paren_match.group(1).strip()
                is_polysemy = False
            else:
                # No special parentheses, use bracket translation if available
                phrase = re.sub(r'[（(][^）)]+[）)]', '', phrase_raw).strip()
                translation = match.group(2).strip() if match.group(2) else "多義語"
                is_polysemy = False
            
            card_content = match.group(3).strip()
            
            # Add to map (merging/overwriting if exists)
            content_map[phrase] = {
                'translation': translation,
                'content': card_content,
                'is_polysemy': is_polysemy
            }

        # Also try Standard Regex on Guide 02 just in case
        matches2b = list(re.finditer(r'### \*\*([^*]+?)(?: - ([^*]+?)|\（多義\）)\*\*(.*?)(?=###|\Z)', content2, re.DOTALL))
        if matches2b:
             print(f"Guide 02: Found {len(matches2b)} items (Standard format).")
             for match in matches2b:
                phrase = match.group(1).strip()
                translation = match.group(2).strip() if match.group(2) else "多義語"
                card_content = match.group(3).strip()
                content_map[phrase] = {
                    'translation': translation,
                    'content': card_content,
                    'is_polysemy': "多義" in match.group(0)
                }
    else:
        print(f"Warning: Guide 02 not found at {GUIDE02_PATH}")

    sections_data = []

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
        
        stats_card = None
        if stats_start_idx != -1:
             # Generate stats data
             stats_lines = phr_lines[stats_start_idx:]
             phr_lines = phr_lines[:stats_start_idx] # Remove from phrase parsing
             stats_card = prepare_stats_card(stats_lines)

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
            cards = []
            
            # Phrases Cards
            for phrase, translation in phrases_in_section:
                # Check for direct match or alias
                target_phrase = phrase
                
                # Aliases for known mismatches
                # Aliases for known mismatches
                ALIASES = {
                    'do duty': 'do duty as',
                    'do with / do without': 'do with vs do without',
                    # Add others if strictly necessary
                }
                
                if phrase in ALIASES:
                    target_phrase = ALIASES[phrase]
                    
                if target_phrase in content_map:
                    data = content_map[target_phrase]
                    # Pass the ORIGINAL phrase name for the card title, but use the ALISED content
                    cards.append(prepare_card_data(phrase, data['translation'], data['content'], data['is_polysemy']))
                else:
                    cards.append(prepare_card_data(phrase, translation))
            
            sections_data.append({
                'num': sec_num,
                'name': sec_name,
                'phrases': phrases_in_section,
                'cards': cards
            })

            # Append stats card separately if belongs to this file/section context?
            # Originally stats were appended at the end. We'll append it as a separate "section" or just last card of last section?
            # current logic appends it to output. Let's add it as a separate section data with no header if needed.
        
        if stats_card:
            sections_data.append({
                'num': "",
                'name': "",
                'phrases': [],
                'cards': [stats_card]
            })

    # Render
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template('guide_part2_template.html')
    
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
