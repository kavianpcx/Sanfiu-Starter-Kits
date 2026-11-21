from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
KITS = {
    "sanfiu-market": ROOT / "templates/ecommerce/sanfiu-market",
    "sanfiu-live": ROOT / "templates/events/sanfiu-live",
    "sanfiu-marketplace": ROOT / "templates/marketplace/sanfiu-marketplace",
    "sanfiu-academy": ROOT / "templates/education/sanfiu-academy",
    "sanfiu-tickets": ROOT / "templates/ticketing/sanfiu-tickets",
    "sanfiu-devices": ROOT / "templates/showcase/sanfiu-devices",
    "sanfiu-weather": ROOT / "templates/utilities/sanfiu-weather",
    "sanfiu-world-clock": ROOT / "templates/utilities/sanfiu-world-clock",
}
EXCLUDED_PARTS = {".venv", "__pycache__", "staticfiles"}
EXCLUDED_NAMES = {".env", "db.sqlite3"}


def should_include(path: Path) -> bool:
    return not any(part in EXCLUDED_PARTS for part in path.parts) and path.name not in EXCLUDED_NAMES and not path.name.endswith(".pyc")


def main() -> None:
    output_dir = ROOT / "downloads"
    output_dir.mkdir(exist_ok=True)
    for name, source_dir in KITS.items():
        archive = output_dir / f"{name}.zip"
        with ZipFile(archive, "w", compression=ZIP_DEFLATED) as zipped:
            for source in sorted(source_dir.rglob("*")):
                if source.is_file() and should_include(source):
                    relative = source.relative_to(source_dir.parent)
                    zipped.write(source, relative.as_posix())
        print(f"Created {archive.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
