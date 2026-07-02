from pathlib import Path
import zipfile, tarfile, gzip, bz2, lzma, shutil

def _safe_target(base, member_name):
    target = (base / member_name).resolve()
    base = base.resolve()
    if not str(target).startswith(str(base)):
        raise ValueError(f"Unsafe archive member path: {member_name}")
    return target

def _safe_extract_zip(archive, target):
    with zipfile.ZipFile(archive, "r") as zf:
        for member in zf.namelist():
            _safe_target(target, member)
        zf.extractall(target)

def _safe_extract_tar(archive, target):
    with tarfile.open(archive, "r:*") as tf:
        for member in tf.getmembers():
            _safe_target(target, member.name)
        tf.extractall(target)

def _tar_target(archive):
    name = archive.name.lower()
    if name.endswith(".tar.gz"):
        return archive.parent / archive.name[:-7]
    if name.endswith(".tar.bz2"):
        return archive.parent / archive.name[:-8]
    if name.endswith(".tar.xz"):
        return archive.parent / archive.name[:-7]
    if name.endswith(".tgz"):
        return archive.parent / archive.name[:-4]
    if name.endswith(".tar"):
        return archive.parent / archive.name[:-4]
    return archive.with_suffix("")

def extract_archives_recursive(data_dir="data", overwrite=False, max_rounds=20):
    data_dir = Path(data_dir)
    extracted = []

    for _ in range(max_rounds):
        found = False

        for archive in sorted(data_dir.rglob("*")):
            if not archive.is_file():
                continue

            name = archive.name.lower()

            if name.endswith(".zip"):
                target = archive.with_suffix("")
                if target.exists() and not overwrite:
                    continue
                print(f"Extracting ZIP: {archive} -> {target}")
                target.mkdir(parents=True, exist_ok=True)
                _safe_extract_zip(archive, target)
                extracted.append(target)
                found = True

            elif name.endswith((".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tar.xz")):
                target = _tar_target(archive)
                if target.exists() and not overwrite:
                    continue
                print(f"Extracting TAR: {archive} -> {target}")
                target.mkdir(parents=True, exist_ok=True)
                _safe_extract_tar(archive, target)
                extracted.append(target)
                found = True

            elif name.endswith(".gz") and not name.endswith(".tar.gz"):
                target = archive.with_suffix("")
                if target.exists() and not overwrite:
                    continue
                print(f"Decompressing GZ: {archive} -> {target}")
                with gzip.open(archive, "rb") as src, open(target, "wb") as dst:
                    shutil.copyfileobj(src, dst)
                extracted.append(target)
                found = True

            elif name.endswith(".bz2") and not name.endswith(".tar.bz2"):
                target = archive.with_suffix("")
                if target.exists() and not overwrite:
                    continue
                print(f"Decompressing BZ2: {archive} -> {target}")
                with bz2.open(archive, "rb") as src, open(target, "wb") as dst:
                    shutil.copyfileobj(src, dst)
                extracted.append(target)
                found = True

            elif name.endswith(".xz") and not name.endswith(".tar.xz"):
                target = archive.with_suffix("")
                if target.exists() and not overwrite:
                    continue
                print(f"Decompressing XZ: {archive} -> {target}")
                with lzma.open(archive, "rb") as src, open(target, "wb") as dst:
                    shutil.copyfileobj(src, dst)
                extracted.append(target)
                found = True

        if not found:
            break

    return extracted
