import os

from pypdf import PdfWriter


def merge_pdfs(pdf_list: list, output_filename: str):
    """Merges a list of PDF files into a single PDF and deletes the individual files."""
    if not pdf_list:
        print("No pages to merge.")
        return

    merger = PdfWriter()
    print(f"Saving all pages into final {output_filename}...")

    for pdf_file in pdf_list:
        merger.append(pdf_file)

    merger.write(output_filename)
    merger.close()

    # Clean up temporary page PDFs
    print("Cleaning up temporary files...")
    for pdf_file in pdf_list:
        try:
            os.remove(pdf_file)
        except OSError:
            pass

    print("Completed successfully!")
