import re
import os
from jinja2 import Environment, FileSystemLoader

# ==========================================
# CONFIGURATION
# ==========================================
TARGET_VERB = "template_verb"  # REPLACE THIS with the target verb
# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VERB_BASE_DIR = os.path.join(BASE_DIR, TARGET_VERB, 'phrasal')
OUTPUT_BASE_DIR = os.path.join(BASE_DIR, TARGET_VERB, 'phrasal')
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

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
    if group_id == 1:
        header_description = "最も重要な基本フレーズ。"
    elif group_id == 2:
        header_description = "表現力を広げる日常・学習フレーズ。"
    elif group_id == 3:
        header_description = "ビジネスで必須の表現。"
    elif group_id == 4:
        header_description = "多義語・注意すべき表現。"

    # Prepare next group URL
    next_group_url = f'../{group_id+1:02d}/' if group_id < 4 else ""

    # Render Template
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template('phrasal_list_template.html')
    
    html = template.render(
        verb_title=TARGET_VERB.upper(),
        group_str=group_str,
        subtitle=subtitle,
        description=header_description,
        phrases=phrases,
        next_group_url=next_group_url
    )

    # Write output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated {output_path} with {len(phrases)} phrases using Jinja2.")

if __name__ == "__main__":
    # Run for 01-04
    for i in range(1, 5):
        generate_phrasal_list(i)
