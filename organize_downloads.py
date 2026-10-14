"""Sort files in the Downloads folder into category subfolders.

This script is scheduled by Windows Task Scheduler to run every two days.
"""

from __future__ import annotations

import shutil
from pathlib import Path


CATEGORIES: dict[str, set[str]] = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".svg", ".heic"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".webm", ".m4v"},
    "Music": {".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg", ".wma"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"},
    "Programs": {".exe", ".msi", ".msix", ".appx", ".bat", ".cmd"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".json", ".xml", ".java", ".cpp", ".c", ".cs"},
}


def category_for(file: Path) -> str:
    for category, extensions in CATEGORIES.items():
        if file.suffix.lower() in extensions:
            return category
    return "Other"


def unused_destination(destination: Path) -> Path:
    if not destination.exists():
        return destination
    number = 1
    while True:
        candidate = destination.with_name(f"{destination.stem} ({number}){destination.suffix}")
        if not candidate.exists():
            return candidate
        number += 1


def main() -> None:
    downloads = Path.home() / "Downloads"
    for item in downloads.iterdir():
        if not item.is_file():
            continue
        destination = unused_destination(downloads / category_for(item) / item.name)
        destination.parent.mkdir(exist_ok=True)
        shutil.move(str(item), str(destination))


if __name__ == "__main__":
    main()
