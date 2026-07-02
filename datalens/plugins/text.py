from ..plugin_base import DataLensPlugin
import json

class TextPlugin(DataLensPlugin):
    name = "text"
    suffixes = {".txt", ".md", ".rst"}
    renderable = True

    def analyse(self, path, max_rows=5):
        text = path.read_text(errors="replace")
        return {
            "kind": "Text",
            "characters": len(text),
            "lines": len(text.splitlines()),
            "preview": text[:2000],
        }

    def render(self, path, max_rows=5):
        from IPython.display import display, Markdown
        text = path.read_text(errors="replace")
        display(Markdown("```text\n" + text[:3000] + "\n```"))

class JSONPlugin(DataLensPlugin):
    name = "json"
    suffixes = {".json", ".jsonld"}
    renderable = True

    def analyse(self, path, max_rows=5):
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            data = json.load(f)

        if isinstance(data, dict):
            root_type = "object"
            keys = list(data.keys())
        elif isinstance(data, list):
            root_type = "array"
            keys = []
        else:
            root_type = type(data).__name__
            keys = []

        return {
            "kind": "JSON",
            "root_type": root_type,
            "top_level_keys": keys[:50],
        }

    def render(self, path, max_rows=5):
        from IPython.display import display, JSON
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            data = json.load(f)
        display(JSON(data))
