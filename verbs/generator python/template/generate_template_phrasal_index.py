import os
from jinja2 import Environment, FileSystemLoader

# ==========================================
# CONFIGURATION
# ==========================================
TARGET_VERB = "do"
VERB_TITLE = TARGET_VERB

# Custom Blurbs for DO Phrasal Index
PHRASAL_DESCRIPTION = "「実行・完了」コアイメージで、具体的な行為から抽象的な処理まで攻略する。"
CORE_MEANING = "実行・完了" # For "まずはここから「X」感覚を掴みましょう"

# Examples and Descriptions
EXAMPLES_01 = "do up / over / without..."
EXAMPLES_01_DESC = "物理的な「実行・処理」を表す必須語。"

EXAMPLES_02 = "do with / for / in..."
EXAMPLES_02_DESC = "会話や試験で頻出の表現。"

EXAMPLES_03 = "do justice to / credit to..."
EXAMPLES_03_DESC = "硬めの表現やイディオム。"

EXAMPLES_04 = "do business / work..." # Group 4 seems to include Business in Core text, though organized differently.
EXAMPLES_04_DESC = "ビジネス・専門的な場面で使う表現。"

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VERB_DIR = os.path.join(BASE_DIR, TARGET_VERB)
OUTPUT_PATH = os.path.join(VERB_DIR, 'phrasal', 'index.html')
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')

def main():
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template('phrasal_index_template.html')
    
    html_output = template.render(
        verb_title=VERB_TITLE,
        phrasal_description=PHRASAL_DESCRIPTION,
        core_meaning=CORE_MEANING,
        examples_01=EXAMPLES_01,
        examples_01_desc=EXAMPLES_01_DESC,
        examples_02=EXAMPLES_02,
        examples_02_desc=EXAMPLES_02_DESC,
        examples_03=EXAMPLES_03,
        examples_03_desc=EXAMPLES_03_DESC,
        examples_04=EXAMPLES_04,
        examples_04_desc=EXAMPLES_04_DESC
    )
    
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(html_output)

    print(f"Generated {OUTPUT_PATH} successfully!")

if __name__ == "__main__":
    main()
