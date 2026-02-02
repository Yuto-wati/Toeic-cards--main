"""
Convert all HTML slides to PNG images using Playwright
Usage: python convert_to_png.py
"""
from pathlib import Path
import asyncio
from playwright.async_api import async_playwright

PROJECT_DIR = Path(__file__).resolve().parent
OUT_DIR = PROJECT_DIR / "out"
PNG_DIR = PROJECT_DIR / "png_output"

# Ensure PNG output directory exists
PNG_DIR.mkdir(exist_ok=True)


async def convert_html_to_png(html_path: Path, png_path: Path):
    """Convert a single HTML file to PNG"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1080, 'height': 1920})
        
        # Load HTML file
        await page.goto(f'file://{html_path.as_posix()}')
        
        # Wait for any animations/fonts to load
        await page.wait_for_timeout(500)
        
        # Take screenshot
        await page.screenshot(path=str(png_path), type='png', full_page=False)
        
        await browser.close()
    
    print(f"✓ Created: {png_path.name}")


async def process_all_slides():
    """Process all HTML slides in the out directory"""
    print("Starting PNG conversion...\n")
    
    # Get all subdirectories in out/
    card_dirs = [d for d in OUT_DIR.iterdir() if d.is_dir()]
    
    total_converted = 0
    
    for card_dir in sorted(card_dirs):
        png_card_dir = PNG_DIR / card_dir.name
        png_card_dir.mkdir(exist_ok=True)
        
        print(f"Processing {card_dir.name}...")
        
        # Get all HTML files in this card directory
        html_files = sorted(card_dir.glob("*.html"))
        
        for html_file in html_files:
            png_file = html_file.stem + ".png"
            png_path = png_card_dir / png_file
            
            await convert_html_to_png(html_file, png_path)
            total_converted += 1
        
        print()
    
    print(f"\n✅ Conversion complete!")
    print(f"Total slides converted: {total_converted}")
    print(f"Output directory: {PNG_DIR}")


if __name__ == "__main__":
    asyncio.run(process_all_slides())
