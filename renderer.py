import os

from playwright.sync_api import sync_playwright


def download_and_render_pages(
    doc_id: str, doc_index: int = 1, output_dir: str = "output"
) -> list:
    """Downloads SVGs using Playwright and saves them as single-page PDFs."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    temp_files = []
    print("Starting Playwright (headless browser) to render perfect SVGs...")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page_context = browser.new_page()

        page = 1
        while True:
            page_url = f"https://svg.issuu.com/{doc_id}/page_{page}.svg"
            print(f"Downloading & rendering page {page} from {page_url} ...")

            try:
                response = page_context.goto(page_url, wait_until="networkidle")

                if response and not response.ok:
                    print(
                        f"End of document reached at page {page} (HTTP {response.status})."
                    )
                    break

                dimensions = page_context.evaluate("""() => { 
                    const svg = document.querySelector('svg'); 
                    if (!svg) return null;
                    return { width: svg.viewBox.baseVal.width, height: svg.viewBox.baseVal.height }; 
                }""")

                if not dimensions:
                    print("Could not find SVG dimensions. Stopping.")
                    break

                temp_pdf = os.path.join(
                    output_dir, f"temp_doc{doc_index:03d}_page_{page:04d}.pdf"
                )

                # Force Chromium to print exactly that size
                page_context.pdf(
                    path=temp_pdf,
                    width=f"{dimensions['width']}px",
                    height=f"{dimensions['height']}px",
                    print_background=True,
                    page_ranges="1",
                    margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
                )

                temp_files.append(temp_pdf)
                page += 1

            except Exception as e:
                print(f"Failed to download/render page {page}: {e}. Stopping.")
                break

        browser.close()

    return temp_files
