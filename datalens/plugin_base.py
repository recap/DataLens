class DataLensPlugin:
    name = "base"
    suffixes = set()
    renderable = False

    def supports(self, path):
        return path.suffix.lower() in self.suffixes

    def analyse(self, path, max_rows=5):
        raise NotImplementedError

    def render(self, path, max_rows=5):
        raise NotImplementedError(f"{self.name} does not support rendering")
