import re
import os

TARGET_VERB = "do"
VERB_TITLE = TARGET_VERB.upper()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VERB_DIR = os.path.join(BASE_DIR, TARGET_VERB)
SOURCE_PATH = os.path.join(VERB_DIR, 'core', 'coreの原文テキスト.txt')

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
    print(f"Reading {SOURCE_PATH}")
    with open(SOURCE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    print("Parsing sections...")
    raw_sections = re.split(r'\n## ', content)
    print(f"Found {len(raw_sections)} raw split sections")
    
    print(f"Type: {type(raw_sections)}")
    
    for i in range(len(raw_sections)):
        section = raw_sections[i]
        print(f"  Section {i}: {section[:20]}...")
        if '中学生' in section:
            blocks = re.split(r'\n(?=### )', section)
            print(f"    Blocks: {len(blocks)}")
            items = [parse_phrasal_block(b) for b in blocks if b.strip() and b.startswith('###')]
            items = [i for i in items if i]
            print(f"    Parsed {len(items)} items")

if __name__ == "__main__":
    main()
