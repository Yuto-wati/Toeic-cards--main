/**
 * Convert all HTML slides to PNG images
 * Usage: node convert_to_png.js
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const OUT_DIR = path.join(__dirname, 'out');
const PNG_DIR = path.join(__dirname, 'png_output');

// Ensure PNG output directory exists
if (!fs.existsSync(PNG_DIR)) {
    fs.mkdirSync(PNG_DIR, { recursive: true });
}

async function convertHtmlToPng(htmlPath, pngPath) {
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();

    // Set viewport to match canvas size (1080x1920)
    await page.setViewport({
        width: 1080,
        height: 1920,
        deviceScaleFactor: 1
    });

    // Load HTML file
    await page.goto(`file://${htmlPath}`, {
        waitUntil: 'networkidle0'
    });

    // Take screenshot
    await page.screenshot({
        path: pngPath,
        type: 'png',
        fullPage: false
    });

    await browser.close();
    console.log(`✓ Created: ${path.basename(pngPath)}`);
}

async function processAllSlides() {
    console.log('Starting PNG conversion...\n');

    // Get all subdirectories in out/
    const cardDirs = fs.readdirSync(OUT_DIR).filter(name => {
        const fullPath = path.join(OUT_DIR, name);
        return fs.statSync(fullPath).isDirectory();
    });

    let totalConverted = 0;

    for (const cardDir of cardDirs) {
        const cardPath = path.join(OUT_DIR, cardDir);
        const pngCardDir = path.join(PNG_DIR, cardDir);

        // Create PNG subdirectory
        if (!fs.existsSync(pngCardDir)) {
            fs.mkdirSync(pngCardDir, { recursive: true });
        }

        console.log(`Processing ${cardDir}...`);

        // Get all HTML files in this card directory
        const htmlFiles = fs.readdirSync(cardPath).filter(name => name.endsWith('.html'));

        for (const htmlFile of htmlFiles) {
            const htmlPath = path.join(cardPath, htmlFile);
            const pngFile = htmlFile.replace('.html', '.png');
            const pngPath = path.join(pngCardDir, pngFile);

            await convertHtmlToPng(htmlPath, pngPath);
            totalConverted++;
        }

        console.log('');
    }

    console.log(`\n✅ Conversion complete!`);
    console.log(`Total slides converted: ${totalConverted}`);
    console.log(`Output directory: ${PNG_DIR}`);
}

// Run the conversion
processAllSlides().catch(err => {
    console.error('Error:', err);
    process.exit(1);
});
