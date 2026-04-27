import os
import re

from converter import convert_pdf_to_markdown
from merger import merge_pdfs
from metadata import get_document_info
from renderer import download_and_render_pages


def clean_filename(title: str) -> str:
    # Sanitize the document title to create a valid filename.
    return re.sub(r'[\\/*?:"<>|]', "", title)


def main():
    print("Enter the URLs of the Issuu documents you want to download.")
    print("Press Enter on a blank line when you are finished adding URLs.")

    urls = []
    while True:
        url = input("URL: ").strip()
        if not url:
            break
        urls.append(url)

    if not urls:
        print("No URLs were provided. Exiting.")
        return

    print("\nSelect the format you want to download:")
    print("  1. PDF")
    print("  2. Markdown (using Docling)")
    print("  3. Both (PDF & Markdown)")

    while True:
        choice = input("Enter your choice (1/2/3) [default: 1]: ").strip()
        if not choice or choice == "1":
            format_choice = "pdf"
            break
        elif choice == "2":
            format_choice = "markdown"
            break
        elif choice == "3":
            format_choice = "both"
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    download_pdf = format_choice in ["pdf", "both"]
    download_md = format_choice in ["markdown", "both"]

    merge_choice = "n"
    if len(urls) > 1 and download_pdf:
        merge_choice = (
            input(
                "\nDo you want to merge all these documents into ONE single PDF? (y/n): "
            )
            .strip()
            .lower()
        )

    merge_all = merge_choice == "y"
    all_temp_files = []

    for idx, input_url in enumerate(urls, start=1):
        print(f"\n--- Processing Document {idx}/{len(urls)} ---")
        try:
            # 1. Fetch document data
            doc_info = get_document_info(input_url)
            doc_id = doc_info["doc_id"]
            safe_title = clean_filename(doc_info["title"])

            # 2. Download and render individual pages
            temp_files = download_and_render_pages(
                doc_id=doc_id, doc_index=idx, output_dir="output"
            )

            if not temp_files:
                print(f"Skipping '{safe_title}' because no pages were downloaded.")
                continue

            # 3. Handle PDF grouping or singular output
            if merge_all:
                all_temp_files.extend(temp_files)
            else:
                final_output = f"output/{safe_title}.pdf"
                merge_pdfs(temp_files, final_output)

                # Process the PDF using Docling if Markdown is requested
                if download_md:
                    md_output = f"output/{safe_title}.md"
                    convert_pdf_to_markdown(final_output, md_output)

                # Clean up intermediate PDF if only Markdown was requested
                if not download_pdf:
                    print(
                        f"Removing intermediate PDF {final_output} (only Mardskdown requested)..."
                    )
                    if os.path.exists(final_output):
                        os.remove(final_output)

        except Exception as e:
            print(f"An error occurred while processing {input_url}: {e}")

    # 4. Final merge step if user wanted them combined
    if merge_all and all_temp_files:
        final_output = "output/Merged_Documents.pdf"
        print(f"\n--- Merging ALL documents into {final_output} ---")
        merge_pdfs(all_temp_files, final_output)

        if download_md:
            md_output = "output/Merged_Documents.md"
            convert_pdf_to_markdown(final_output, md_output)

        if not download_pdf:
            print(
                f"Removing intermediate PDF {final_output} (only Markdown requested)..."
            )
            if os.path.exists(final_output):
                os.remove(final_output)


if __name__ == "__main__":
    main()
