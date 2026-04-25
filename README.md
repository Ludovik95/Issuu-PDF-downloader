# Issuu PDF Downloader

A Python script that downloads documents from Issuu and converts them into high-quality, single-file PDFs.

Unlike simple image scrapers, this tool uses Playwright (headless Chromium) to render the original SVG pages. This ensures that the generated PDFs retain perfect visual fidelity while keeping the text fully selectable and searchable.

## Features
- **Selectable Text**: Preserves the vector text layers and layout.
- **High Quality**: Renders the exact SVG/JPEG composites used by Issuu's reader.
- **Multi-page PDF**: Automatically merges all downloaded pages into a single `.pdf` document.

## Prerequisites
- Python 3.x
- Linux, macOS, or Windows

## Installation

It is recommended to use a Python virtual environment to avoid installing packages globally.

1. **Clone the repository & enter the directory:**
   ```bash
   git clone https://github.com/ludovik95/issuu-pdf-downloader.git
   cd issuu-pdf-downloader
   ```

2. **Create and activate a virtual environment:**
   - On Linux/macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - On Windows:
     ```cmd
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the required Playwright browser:**
   ```bash
   playwright install chromium
   ```

## Usage

1. Activate your virtual environment (if not already activated):
   ```bash
   source venv/bin/activate
   ```

2. Run the script:
   ```bash
   python main.py
   ```

3. Enter the requested information:
   - **Document URL**: The full URL of the Issuu document (e.g., `https://issuu.com/username/docs/document_name`)
   - **Number of pages**: How many pages you want to download.

The script will download each page, render it perfectly in the background, and output a single `{document_id}.pdf` file in the same directory.

## Disclaimer
This tool is provided for educational and personal use only. Please respect the copyright of the authors and platforms. Do not distribute downloaded works without permission from the copyright holder.