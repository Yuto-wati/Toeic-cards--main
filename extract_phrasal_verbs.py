"""
Extract phrasal verbs from all verb part1.html files and generate cards.csv
"""
from __future__ import annotations

import json
import csv
import re
from pathlib import Path
from typing import Dict, List, Optional
from bs4 import BeautifulSoup

# Configuration
PROJECT_DIR = Path(__file__).resolve().parent
VERBS_DIR = PROJECT_DIR / "verbs"
INDEX_FILE = PROJECT_DIR / "index.json"
OUTPUT_CSV = PROJECT_DIR / "cards.csv"

VERBS = ["get", "take", "go", "put", "run", "make", "have", "do"]


def load_index() -> Dict[str, int]:
    """Load the current index for each verb from index.json"""
    if INDEX_FILE.exists():
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # Initialize with index 0 for all verbs
        return {verb: 0 for verb in VERBS}


def save_index(index_data: Dict[str, int]) -> None:
    """Save the updated index to index.json"""
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)


def extract_card_at_index(html_path: Path, index: int) -> Optional[Dict[str, str]]:
    """Extract the phrasal verb card at the specified index from HTML"""
    if not html_path.exists():
        print(f"Warning: {html_path} not found")
        return None
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all card elements
    cards = soup.find_all('div', class_='card')
    
    # Filter out the core image card (first card with special header)
    phrasal_cards = []
    for card in cards:
        header = card.find('div', class_='card-header')
        if header:
            phrase_elem = header.find('span', class_='phrase')
            if phrase_elem and '🎯' not in phrase_elem.get_text():
                phrasal_cards.append(card)
    
    if index >= len(phrasal_cards):
        print(f"Warning: Index {index} out of range for {html_path} (only {len(phrasal_cards)} cards)")
        return None
    
    card = phrasal_cards[index]
    
    # Extract phrase
    phrase_elem = card.find('span', class_='phrase')
    phrase = phrase_elem.get_text(strip=True) if phrase_elem else ""
    
    # Extract meaning (translation)
    meaning_elem = card.find('span', class_='translation')
    meaning = meaning_elem.get_text(strip=True) if meaning_elem else ""
    
    # Extract core image
    core_visual_elem = card.find('div', class_='visual-text')
    core_image = ""
    if core_visual_elem:
        # Get text and replace <br> with newlines
        core_text = core_visual_elem.decode_contents()
        core_text = re.sub(r'<br\s*/?>', '\n', core_text)
        core_text = BeautifulSoup(core_text, 'html.parser').get_text()
        # Clean up extra whitespace
        core_image = '\n'.join(line.strip() for line in core_text.split('\n') if line.strip())
    
    # Extract first example
    example_boxes = card.find_all('div', class_='example-box')
    example_en = ""
    example_jp = ""
    if example_boxes:
        first_example = example_boxes[0]
        en_elem = first_example.find('p', class_='en-sent')
        jp_elem = first_example.find('p', class_='jp-sent')
        example_en = en_elem.get_text(strip=True) if en_elem else ""
        example_jp = jp_elem.get_text(strip=True) if jp_elem else ""
    
    # Extract usage points from point area
    point_area = card.find('div', class_='point-area')
    usage_points = ""
    if point_area:
        point_text = point_area.get_text(strip=True)
        # Remove "Point：" or "ポイント：" prefix
        point_text = re.sub(r'^(Point|ポイント)[:：]\s*', '', point_text)
        # Remove emoji and TOEIC markers
        point_text = re.sub(r'🎯\s*TOEIC(超)?頻出(表現)?[。．]?\s*', '', point_text)
        # Take first sentence or first 50 chars as usage point
        sentences = re.split(r'[。．]', point_text)
        if sentences:
            usage_points = sentences[0].strip()
    
    return {
        'phrase': phrase,
        'meaning': meaning,
        'core_image': core_image,
        'usage_points': usage_points,
        'example_en': example_en,
        'example_jp': example_jp,
    }


def generate_csv(cards_data: List[Dict[str, str]], output_path: Path) -> None:
    """Generate cards.csv from extracted data"""
    fieldnames = ['id', 'phrase', 'meaning', 'core_image', 'usage_points', 'example_en', 'example_jp', 'cta']
    
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for card in cards_data:
            writer.writerow(card)
    
    print(f"Generated {output_path} with {len(cards_data)} cards")


def main():
    # Load current index
    index_data = load_index()
    
    cards_data = []
    
    for verb in VERBS:
        current_index = index_data.get(verb, 0)
        html_path = VERBS_DIR / verb / "guide" / "part1.html"
        
        print(f"Processing {verb} (index {current_index})...")
        
        card_data = extract_card_at_index(html_path, current_index)
        
        if card_data:
            # Add ID and CTA
            card_id = f"{verb}_{current_index + 1:03d}"
            card_data['id'] = card_id
            card_data['cta'] = "保存して復習"
            
            cards_data.append(card_data)
            
            # Increment index for next run
            index_data[verb] = current_index + 1
            
            print(f"  ✓ Extracted: {card_data['phrase']}")
        else:
            print(f"  ✗ Failed to extract card at index {current_index}")
    
    # Generate CSV
    if cards_data:
        generate_csv(cards_data, OUTPUT_CSV)
        
        # Save updated index
        save_index(index_data)
        print(f"\nUpdated index.json - next run will extract:")
        for verb, idx in index_data.items():
            print(f"  {verb}: index {idx}")
    else:
        print("No cards extracted!")


if __name__ == "__main__":
    main()
