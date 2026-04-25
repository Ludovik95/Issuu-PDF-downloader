import urllib.request
import json
import os
from playwright.sync_api import sync_playwright
from pypdf import PdfWriter

def main():
    input_url = input("Enter the document URL: ")
    n_pages = int(input("Enter the number of pages to download: "))
    
    # Fetch the JSON data from Issuu
    doc_infos_url = f"https://issuu.com/oembed?url={input_url}&format=json"
    req_info = urllib.request.Request(doc_infos_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req_info) as response:
        doc_infos = json.loads(response.read().decode())

    thumbnail_url = doc_infos["thumbnail_url"]
    doc_id = thumbnail_url.split('/')[3]

    merger = PdfWriter()
    temp_files = []

    print("Starting Playwright (headless browser) to render perfect SVGs...")
    
    with sync_playwright() as p:
        # Launch Chromium headless
        browser = p.chromium.launch()
        page_context = browser.new_page()

        for page in range(1, n_pages + 1):
            page_url = f"https://svg.issuu.com/{doc_id}/page_{page}.svg"
            print(f"Downloading & rendering page {page} from {page_url} ...")
            
            try:
                # Load the raw SVG page directly into Chromium
                page_context.goto(page_url, wait_until="networkidle")
                
                # Ask the browser how big the original SVG canvas is
                dimensions = page_context.evaluate("""() => { 
                    const svg = document.querySelector('svg'); 
                    return { width: svg.viewBox.baseVal.width, height: svg.viewBox.baseVal.height }; 
                }""")
                
                temp_pdf = f"output/temp_page_{page}.pdf"
                
                # Force Chromium to print exactly that size, generating a perfect vector PDF
                page_context.pdf(
                    path=temp_pdf,
                    width=f"{dimensions['width']}px",
                    height=f"{dimensions['height']}px",
                    print_background=True,
                    page_ranges="1",
                    margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}
                )
                
                # Add this page to our merger list
                merger.append(temp_pdf)
                temp_files.append(temp_pdf)
                
            except Exception as e:
                print(f"Failed to download/render page {page}: {e}")

        browser.close()

    # Save the combined final PDF
    if temp_files:
        output_filename = f"output/{doc_id}.pdf"
        print(f"Saving all pages into final {output_filename}...")
        
        merger.write(output_filename)
        merger.close()
        
        # Clean up temporary page PDFs
        for temp_pdf in temp_files:
            try:
                os.remove(temp_pdf)
            except OSError:
                pass
                
        print("Completed successfully!")
    else:
        print("No pages were downloaded.")

if __name__ == "__main__":
    main()