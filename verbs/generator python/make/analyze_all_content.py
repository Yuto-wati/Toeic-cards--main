import re

# Read source text for Part 1
with open('c:/Users/yuto/OneDrive/Toeic-cards--main/verbs/make/guide/guide01の原文テキスト.txt', 'r', encoding='utf-8') as f:
    source_content = f.read()

# Read generated HTML for Part 1
with open('c:/Users/yuto/OneDrive/Toeic-cards--main/verbs/make/guide/part1.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Extract phrasal verbs from source text
# Regular format: ### **phrase - translation**
regular_phrases = re.findall(r'### \*\*([^*]+) - ([^*]+)\*\*', source_content)

# Extract phrases from HTML comments
html_phrases = re.findall(r'<!-- ([^-]+) -->', html_content)

print(f"Source regular: {len(regular_phrases)}")
print(f"HTML cards: {len(html_phrases)}")

# Create sets for comparison
source_set = set([phrase.strip() for phrase, _ in regular_phrases])
html_set = set([phrase.strip() for phrase in html_phrases if phrase.strip() and 'SECTION' not in phrase and 'Footer' not in phrase and 'Core Image' not in phrase])

# Find missing phrases
missing = source_set - html_set

print(f"\nMissing from Part1: {len(missing)}")
if missing:
    with open('missing_phrases_part1.txt', 'w', encoding='utf-8') as f:
        for phrase in sorted(missing):
            f.write(f"{phrase}\n")
            print(f"  - {phrase}")
else:
    print("No missing phrases in Part1!")

# Also check Part2
with open('c:/Users/yuto/OneDrive/Toeic-cards--main/verbs/make/guide/guide02の原文テキスト.txt', 'r', encoding='utf-8') as f:
    source_content2 = f.read()

with open('c:/Users/yuto/OneDrive/Toeic-cards--main/verbs/make/guide/part2.html', 'r', encoding='utf-8') as f:
    html_content2 = f.read()

regular_phrases2 = re.findall(r'### \*\*([^*]+) - ([^*]+)\*\*', source_content2)
polysemy_phrases2 = re.findall(r'### \*\*([^*]+)（多義）\*\*', source_content2)

html_phrases2 = re.findall(r'<!-- ([^-]+) -->', html_content2)

source_set2 = set([phrase.strip() for phrase, _ in regular_phrases2] + [phrase.strip() for phrase in polysemy_phrases2])
html_set2 = set([phrase.strip().replace('（多義）', '') for phrase in html_phrases2 if phrase.strip() and 'SECTION' not in phrase and 'Footer' not in phrase])

missing2 = source_set2 - html_set2

print(f"\nMissing from Part2: {len(missing2)}")
if missing2:
    with open('missing_phrases_part2.txt', 'w', encoding='utf-8') as f:
        for phrase in sorted(missing2):
            f.write(f"{phrase}\n")
            print(f"  - {phrase}")
else:
    print("No missing phrases in Part2!")
