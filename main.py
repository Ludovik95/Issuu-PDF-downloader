import os
import re

from metadata import get_document_info
from merger import merge_pdfs
from renderer import download_and_render_pages


def clean_filename(title: str) -> str:
    # Sanitize the document title to create a valid filename.
    return re.sub(r'[\\/*?:"<>|]', "", title)


def main():
    input_url = input("Enter the document URL: ")

    try:
        # 1. Fetch document data
        doc_info = get_document_info(input_url)
        doc_id = doc_info["doc_id"]
        safe_title = clean_filename(doc_info["title"])

        # 2. Download and render individual pages
        temp_files = download_and_render_pages(doc_id, output_dir="output")

        # 3. Merge pages into the final PDF
        if temp_files:
            final_output = f"output/{safe_title}.pdf"
            merge_pdfs(temp_files, final_output)
        else:
            print("No pages were downloaded.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
