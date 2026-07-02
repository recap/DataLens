from ..plugin_base import DataLensPlugin

class NetCDFPlugin(DataLensPlugin):
    name = "netcdf"
    suffixes = {".nc", ".netcdf"}
    renderable = True

    def analyse(self, path, max_rows=5):
        import xarray as xr
        ds = xr.open_dataset(path)
        return {
            "kind": "NetCDF",
            "dimensions": {k: int(v) for k, v in ds.sizes.items()},
            "data_variables": list(ds.data_vars),
            "coordinates": list(ds.coords),
            "attributes": dict(ds.attrs),
        }

    def render(self, path, max_rows=5):
        import xarray as xr
        from IPython.display import display
        ds = xr.open_dataset(path)
        display(ds)

        for name in list(ds.data_vars)[:3]:
            da = ds[name]
            try:
                if len(da.dims) >= 2:
                    da.isel({dim: 0 for dim in da.dims[:-2]}).plot()
                elif len(da.dims) == 1:
                    da.plot()
            except Exception as exc:
                print(f"Could not plot {name}: {exc}")
