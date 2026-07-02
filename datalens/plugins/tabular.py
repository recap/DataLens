from ..plugin_base import DataLensPlugin

def _summarise_dataframe(df, max_rows=5):
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns),
        "dtypes": {str(k): str(v) for k, v in df.dtypes.items()},
        "missing_cells": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "preview": df.head(max_rows),
    }

class CSVPlugin(DataLensPlugin):
    name = "csv"
    suffixes = {".csv"}
    renderable = True

    def analyse(self, path, max_rows=5):
        import pandas as pd
        df = pd.read_csv(path)
        return {"kind": "CSV table", **_summarise_dataframe(df, max_rows)}

    def render(self, path, max_rows=20):
        import pandas as pd
        from IPython.display import display
        display(pd.read_csv(path, nrows=max_rows))

class TSVPlugin(DataLensPlugin):
    name = "tsv"
    suffixes = {".tsv", ".tab"}
    renderable = True

    def analyse(self, path, max_rows=5):
        import pandas as pd
        df = pd.read_csv(path, sep="\t")
        return {"kind": "TSV table", **_summarise_dataframe(df, max_rows)}

    def render(self, path, max_rows=20):
        import pandas as pd
        from IPython.display import display
        display(pd.read_csv(path, sep="\t", nrows=max_rows))

class ExcelPlugin(DataLensPlugin):
    name = "excel"
    suffixes = {".xls", ".xlsx"}
    renderable = True

    def analyse(self, path, max_rows=5):
        import pandas as pd
        sheets = pd.read_excel(path, sheet_name=None, nrows=1000)
        return {
            "kind": "Excel workbook",
            "sheets": {
                name: _summarise_dataframe(df, max_rows)
                for name, df in sheets.items()
            },
        }

    def render(self, path, max_rows=20):
        import pandas as pd
        from IPython.display import display, Markdown
        sheets = pd.read_excel(path, sheet_name=None, nrows=max_rows)
        for name, df in sheets.items():
            display(Markdown(f"#### Sheet: `{name}`"))
            display(df)

class ParquetPlugin(DataLensPlugin):
    name = "parquet"
    suffixes = {".parquet"}
    renderable = True

    def analyse(self, path, max_rows=5):
        import pandas as pd
        df = pd.read_parquet(path)
        return {"kind": "Parquet table", **_summarise_dataframe(df, max_rows)}

    def render(self, path, max_rows=20):
        import pandas as pd
        from IPython.display import display
        display(pd.read_parquet(path).head(max_rows))
