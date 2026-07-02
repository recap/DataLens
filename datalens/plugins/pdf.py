from ..plugin_base import DataLensPlugin

class PDFPlugin(DataLensPlugin):
    name = "pdf"
    suffixes = {".pdf"}
    renderable = True

    def analyse(self, path, max_rows=5):
        from pypdf import PdfReader
        reader = PdfReader(str(path))
        metadata = reader.metadata or {}
        text = reader.pages[0].extract_text() if reader.pages else ""
        return {
            "kind": "PDF",
            "pages": len(reader.pages),
            "metadata": {str(k): str(v) for k, v in metadata.items()},
            "first_page_preview": (text or "")[:1500],
        }

    def render(self, path, max_rows=5):
        from IPython.display import display, Markdown
        from pypdf import PdfReader
        reader = PdfReader(str(path))
        display(Markdown(f"PDF pages: **{len(reader.pages)}**"))
        if reader.pages:
            text = reader.pages[0].extract_text() or ""
            display(Markdown("#### First page text preview"))
            display(Markdown("```text\n" + text[:2000] + "\n```"))
