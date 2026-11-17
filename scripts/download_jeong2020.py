import urllib.request
import zipfile
import re
import shutil

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dataset" / "jeong2020"

URL = "https://zenodo.org/records/{record}/files/sub{subject}.zip?download=1"

RECORDS = {
    **{s: "19021436" for s in range(1, 6)},
    **{s: "19021439" for s in range(6, 11)},
    **{s: "19021438" for s in range(11, 16)},
    **{s: "19021435" for s in range(16, 21)},
    **{s: "19021437" for s in range(21, 26)},
}

def download(subject):
    sub_dir = OUT / f"sub{subject}"
    zip_path = OUT / f"sub{subject}.zip"
    sub_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading sub{subject} ...")
    urllib.request.urlretrieve(URL.format(record=RECORDS[subject], subject=subject), zip_path)

    # Extract only the multigrasp recordings into sub{N}/session{K}/
    with zipfile.ZipFile(zip_path) as z:
        for name in z.namelist():
            file_name = Path(name).name
            if "multigrasp" not in file_name:
                continue
            session = re.search(r"session(\d+)", file_name).group(1)
            target = sub_dir / f"session{session}" / file_name
            target.parent.mkdir(parents=True, exist_ok=True)
            with z.open(name) as src, open(target, "wb") as dst:
                shutil.copyfileobj(src, dst)

    # Delete the zip to save space
    zip_path.unlink()

download(2)

# for subject in range(1, 26):
#     download(subject)
