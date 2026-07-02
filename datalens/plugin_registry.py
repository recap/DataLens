from pathlib import Path

def load_plugins():
    from .plugins.tabular import CSVPlugin, TSVPlugin, ExcelPlugin, ParquetPlugin
    from .plugins.text import TextPlugin, JSONPlugin
    from .plugins.gis import VectorGISPlugin, RasterPlugin
    from .plugins.netcdf import NetCDFPlugin
    from .plugins.image import ImagePlugin
    from .plugins.pdf import PDFPlugin

    return [
        CSVPlugin(), TSVPlugin(), ExcelPlugin(), ParquetPlugin(),
        TextPlugin(), JSONPlugin(),
        VectorGISPlugin(), RasterPlugin(),
        NetCDFPlugin(), ImagePlugin(), PDFPlugin(),
    ]

def matching_plugins(path, plugins):
    return [plugin for plugin in plugins if plugin.supports(path)]

def analyse_inventory(inventory, plugins, max_files_per_type=3):
    results = []
    counts = {}

    for _, row in inventory.iterrows():
        path = Path(row["path"])

        for plugin in matching_plugins(path, plugins):
            count = counts.get(plugin.name, 0)
            if count >= max_files_per_type:
                continue

            try:
                result = plugin.analyse(path)
                result["plugin"] = plugin.name
                result["path"] = row["relative_path"]
                result["renderable"] = plugin.renderable
                results.append(result)
                counts[plugin.name] = count + 1
            except Exception as exc:
                results.append({
                    "plugin": plugin.name,
                    "path": row["relative_path"],
                    "renderable": plugin.renderable,
                    "error": str(exc),
                })

    return results

def render_inventory(inventory, plugins, max_files_per_type=2):
    from IPython.display import display, Markdown

    counts = {}

    for _, row in inventory.iterrows():
        path = Path(row["path"])

        for plugin in matching_plugins(path, plugins):
            if not plugin.renderable:
                continue

            count = counts.get(plugin.name, 0)
            if count >= max_files_per_type:
                continue

            print('=' * 100)

            display(Markdown(f"### {plugin.name}: `{row['relative_path']}`"))

            try:
                plugin.render(path)
                counts[plugin.name] = count + 1
            except Exception as exc:
                display(Markdown(f"**Render error:** `{exc}`"))
