import re

# Read source text
with open('c:/Users/yuto/OneDrive/Toeic-cards--main/verbs/make/guide/guide02の原文テキスト.txt', 'r', encoding='utf-8') as f:
    source_content = f.read()

# Read generated HTML
with open('c:/Users/yuto/OneDrive/Toeic-cards--main/verbs/make/guide/part2.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Extract phrasal verbs from source text
# Regular format: ### **phrase - translation**
regular_phrases = re.findall(r'### \*\*([^*]+) - ([^*]+)\*\*', source_content)
# Polysemous format: ### **phrase（多義）**
polysemy_phrases = re.findall(r'### \*\*([^*]+)（多義）\*\*', source_content)

# Extract phrases from HTML comments
html_phrases = re.findall(r'<!-- ([^-]+) -->', html_content)

print(f"Source regular: {len(regular_phrases)}")
print(f"Source polysemy: {len(polysemy_phrases)}")
print(f"HTML cards: {len(html_phrases)}")

# Create sets for comparison
source_set = set([phrase.strip() for phrase, _ in regular_phrases] + [phrase.strip() for phrase in polysemy_phrases])
html_set = set([phrase.strip().replace('（多義）', '') for phrase in html_phrases if phrase.strip() and 'SECTION' not in phrase and 'Footer' not in phrase])

# Find missing phrases
missing = source_set - html_set

print(f"\nMissing: {len(missing)}")
with open('missing_phrases.txt', 'w', encoding='utf-8') as f:
    for phrase in sorted(missing):
        f.write(f"{phrase}\n")
        
print("Missing phrases written to missing_phrases.txt")
