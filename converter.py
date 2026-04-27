import os

from docling.document_converter import DocumentConverter


def convert_pdf_to_markdown(pdf_path: str, md_path: str):
    # Converts a PDF file to a Markdown file using Docling.
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return

    print("Generating Markdown using Docling...")
    converter = DocumentConverter()
    result = converter.convert(source=pdf_path)
    md_text = result.document.export_to_markdown()

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_text)

    print(f"Saved Markdown file to {md_path}")
