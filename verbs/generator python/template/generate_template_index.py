import os
from jinja2 import Environment, FileSystemLoader

# ==========================================
# CONFIGURATION
# ==========================================
TARGET_VERB = "do"
VERB_TITLE = TARGET_VERB

# Custom Blurbs for DO
VERB_DESCRIPTION = "「行動」「完遂」イメージで、日常会話からビジネスまで攻略する。"
CORE_BLURB = "意味の核から、全用法を一本で理解。<br>なぜ「〜する」も「間に合う」も do なのか？"
PHRASAL_BLURB = "do up / over / without… を地図化。<br>「実行・完了」イメージで熟語を攻略する。"

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VERB_DIR = os.path.join(BASE_DIR, TARGET_VERB)
OUTPUT_PATH = os.path.join(VERB_DIR, 'index.html')
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')

def main():
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template('verb_index_template.html')
    
    html_output = template.render(
        verb_title=VERB_TITLE,
        verb_description=VERB_DESCRIPTION,
        core_blurb=CORE_BLURB,
        phrasal_blurb=PHRASAL_BLURB
    )
    
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(html_output)

    print(f"Generated {OUTPUT_PATH} successfully!")

if __name__ == "__main__":
    main()
