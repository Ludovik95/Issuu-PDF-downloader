import json
import urllib.request


def get_document_info(input_url: str) -> dict:
    """Fetch document metadata from Issuu."""
    doc_infos_url = f"https://issuu.com/oembed?url={input_url}&format=json"
    req_info = urllib.request.Request(
        doc_infos_url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    )
    with urllib.request.urlopen(req_info) as response:
        doc_infos = json.loads(response.read().decode())

    thumbnail_url = doc_infos["thumbnail_url"]
    return {
        "title": doc_infos.get("title", "document"),
        "doc_id": thumbnail_url.split("/")[3],
    }
