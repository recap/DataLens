from ..plugin_base import DataLensPlugin

class ImagePlugin(DataLensPlugin):
    name = "image"
    suffixes = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
    renderable = True

    def analyse(self, path, max_rows=5):
        from PIL import Image
        with Image.open(path) as img:
            return {
                "kind": "Image",
                "format": img.format,
                "width": img.width,
                "height": img.height,
                "mode": img.mode,
            }

    def render(self, path, max_rows=5):
        from IPython.display import Image as IPyImage, display
        display(IPyImage(filename=str(path)))
