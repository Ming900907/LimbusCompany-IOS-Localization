#!/usr/bin/env python3
"""Move an existing Chinese-over-Japanese package to the English locale slot."""

import argparse
import json
import tempfile
import zipfile
from pathlib import Path, PurePosixPath


JP_ROOT = PurePosixPath("LocalizeTemp_jp")
EN_ROOT = PurePosixPath("LocalizeTemp_en")
EN_MANIFEST_ROOT = "Assets/Resources_moved/Localize/en"
JP_MANIFEST_ROOT = "Assets/Resources_moved/Localize/jp"


def migrate(package: Path, manifest_path: Path, output_dir: Path) -> tuple[int, int]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = manifest.get("Files")
    if not isinstance(files, dict):
        raise ValueError("manifest must contain a Files object")

    output_dir.mkdir(parents=True, exist_ok=True)
    package_output = output_dir / "localize_en.zip"
    manifest_output = output_dir / "manifest.json"
    package_temp = package_output.with_suffix(".zip.tmp")
    manifest_temp = manifest_output.with_suffix(".json.tmp")
    written = 0
    skipped = 0
    targets: set[str] = set()

    try:
        with zipfile.ZipFile(package) as source, zipfile.ZipFile(
            package_temp, "w", zipfile.ZIP_DEFLATED, compresslevel=9
        ) as target:
            for entry in source.infolist():
                if entry.is_dir():
                    continue

                path = PurePosixPath(entry.filename)
                try:
                    relative = path.relative_to(JP_ROOT)
                except ValueError as error:
                    raise ValueError(f"unexpected package path: {path}") from error
                if ".." in relative.parts or not relative.name.startswith("JP_"):
                    raise ValueError(f"unexpected Japanese filename: {path}")

                english_relative = relative.with_name(f"EN_{relative.name[3:]}")
                manifest_key = f"{EN_MANIFEST_ROOT}/{english_relative.as_posix()}"
                if manifest_key not in files:
                    skipped += 1
                    continue

                source_manifest_key = f"{JP_MANIFEST_ROOT}/{relative.as_posix()}"
                if source_manifest_key not in files:
                    raise ValueError(f"Japanese manifest entry is missing: {source_manifest_key}")

                data = source.read(entry)
                files[manifest_key]["Hash"] = files[source_manifest_key]["Hash"]
                files[manifest_key]["Crc"] = files[source_manifest_key].get("Crc", 0)
                files[manifest_key]["Size"] = len(data)
                target_name = (EN_ROOT / english_relative).as_posix()
                if target_name in targets:
                    raise ValueError(f"duplicate package path: {target_name}")
                targets.add(target_name)
                target.writestr(target_name, data)
                written += 1

        if not written:
            raise ValueError("package contains no files present in the English manifest")

        manifest_temp.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=4) + "\n",
            encoding="utf-8",
        )
        package_temp.replace(package_output)
        manifest_temp.replace(manifest_output)
    finally:
        package_temp.unlink(missing_ok=True)
        manifest_temp.unlink(missing_ok=True)

    return written, skipped


def self_test() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        package = root / "localize_jp.zip"
        manifest = root / "source-manifest.json"
        output = root / "dist"
        content = b'{"dataList":[{"id":1,"name":"Chinese"}]}'

        with zipfile.ZipFile(package, "w") as archive:
            archive.writestr("LocalizeTemp_jp/JP_Main.json", content)
            archive.writestr("LocalizeTemp_jp/JP_NotInEnglish.json", b"[]")
        manifest.write_text(
            json.dumps(
                {
                    "Files": {
                        f"{EN_MANIFEST_ROOT}/EN_Main.json": {
                            "Hash": "english",
                            "Size": 1,
                            "Crc": 0,
                        },
                        f"{JP_MANIFEST_ROOT}/JP_Main.json": {
                            "Hash": "chinese-package-version",
                            "Size": len(content),
                            "Crc": 7,
                        }
                    }
                }
            ),
            encoding="utf-8",
        )

        assert migrate(package, manifest, output) == (1, 1)
        with zipfile.ZipFile(output / "localize_en.zip") as archive:
            assert archive.namelist() == ["LocalizeTemp_en/EN_Main.json"]
            assert archive.read("LocalizeTemp_en/EN_Main.json") == content
        result = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
        entry = result["Files"][f"{EN_MANIFEST_ROOT}/EN_Main.json"]
        assert entry == {
            "Hash": "chinese-package-version",
            "Size": len(content),
            "Crc": 7,
        }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build localize_en.zip and manifest.json from the current JP-slot package."
    )
    parser.add_argument("package", type=Path, nargs="?")
    parser.add_argument("manifest", type=Path, nargs="?")
    parser.add_argument("--output-dir", type=Path, default=Path("dist"))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        print("self-test passed")
        return
    if args.package is None or args.manifest is None:
        parser.error("package and manifest are required unless --self-test is used")

    written, skipped = migrate(args.package, args.manifest, args.output_dir)
    print(f"wrote {written} files; skipped {skipped} files missing from the English manifest")


if __name__ == "__main__":
    main()
