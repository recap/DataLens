from ..plugin_base import DataLensPlugin

class VectorGISPlugin(DataLensPlugin):
    name = "vector_gis"
    suffixes = {".gpkg", ".geojson", ".shp"}
    renderable = True

    def analyse(self, path, max_rows=5):
        import geopandas as gpd

        result = {"kind": "Vector GIS"}

        if path.suffix.lower() == ".gpkg":
            try:
                import fiona
                layers = fiona.listlayers(path)
                result["layers"] = layers
                if not layers:
                    return result
                gdf = gpd.read_file(path, layer=layers[0])
                result["analysed_layer"] = layers[0]
            except Exception:
                gdf = gpd.read_file(path)
        else:
            gdf = gpd.read_file(path)

        result.update({
            "features": int(len(gdf)),
            "columns": list(gdf.columns),
            "crs": str(gdf.crs),
            "geometry_types": list(gdf.geometry.geom_type.dropna().unique()),
            "bounds": list(gdf.total_bounds),
            "preview": gdf.head(max_rows),
        })
        return result

    def render(self, path, max_rows=5):
        import geopandas as gpd
        import matplotlib.pyplot as plt
        from IPython.display import display, Markdown

        if path.suffix.lower() == ".gpkg":
            try:
                import fiona
                layers = fiona.listlayers(path)
            except Exception:
                layers = [None]
        else:
            layers = [None]

        for layer in layers[:3]:
            if layer:
                gdf = gpd.read_file(path, layer=layer)
                display(Markdown(f"#### Layer: `{layer}`"))
            else:
                gdf = gpd.read_file(path)

            display(gdf.head(max_rows))

            if gdf.empty:
                print("No features to render.")
                continue

            fig, ax = plt.subplots(figsize=(8, 8))
            gdf.plot(ax=ax)
            ax.set_title(path.name if layer is None else f"{path.name} :: {layer}")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            plt.show()

class RasterPlugin(DataLensPlugin):
    name = "raster"
    suffixes = {".tif", ".tiff"}
    renderable = True

    def analyse(self, path, max_rows=5):
        import rasterio
        with rasterio.open(path) as src:
            return {
                "kind": "Raster",
                "width": src.width,
                "height": src.height,
                "bands": src.count,
                "crs": str(src.crs),
                "bounds": list(src.bounds),
                "dtype": src.dtypes[0] if src.dtypes else None,
                "nodata": src.nodata,
            }

    def render(self, path, max_rows=5):
        import rasterio
        from rasterio.plot import show
        import matplotlib.pyplot as plt

        with rasterio.open(path) as src:
            fig, ax = plt.subplots(figsize=(8, 8))
            show(src, ax=ax)
            ax.set_title(path.name)
            plt.show()
