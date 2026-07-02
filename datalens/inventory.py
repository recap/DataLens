from pathlib import Path
import pandas as pd

def scan_data_folder(data_dir="/data"):
    data_dir = Path(data_dir)
    if not data_dir.exists():
        raise FileNotFoundError(f"Data folder does not exist: {data_dir}")

    rows = []
    for path in sorted(data_dir.rglob("*")):
        if path.is_file():
            stat = path.stat()
            rows.append({
                "path": path,
                "relative_path": path.relative_to(data_dir).as_posix(),
                "name": path.name,
                "suffix": path.suffix.lower(),
                "size_bytes": stat.st_size,
                "size_mb": round(stat.st_size / 1024 / 1024, 3),
            })
    return pd.DataFrame(rows)

def file_type_summary(inventory):
    if inventory.empty:
        return pd.DataFrame(columns=["suffix", "count", "total_size_mb"])

    return (
        inventory.groupby("suffix", dropna=False)
        .agg(count=("path", "count"), total_size_mb=("size_mb", "sum"))
        .reset_index()
        .sort_values(["count", "total_size_mb"], ascending=False)
    )

def print_inventory_summary(inventory):
    print(f"Files: {len(inventory)}")
    if len(inventory) > 0:
        print(f"Total size: {inventory['size_mb'].sum():.2f} MB")
        print(file_type_summary(inventory).to_string(index=False))
