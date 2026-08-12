#!/usr/bin/env python3
"""Build a Chinese-over-Japanese package with English fallback text."""

import argparse
import hashlib
import json
import tempfile
import zipfile
from pathlib import Path, PurePosixPath


PACKAGE_ROOT = PurePosixPath("LocalizeTemp_jp")
MANIFEST_ROOT = "Assets/Resources_moved/Localize/jp"
UI_OVERRIDES = {
    "loginui_sign_in_with_google": "Google登入",
    "loginui_sign_in_with_apple": "Apple登入",
    "loginui_sign_in_with_steam": "Steam登入",
    "loginui_sign_in_with_guest": "游客登入",
    "loginui_loading_battlehint": "玩法提示",
}


def source_path(relative: PurePosixPath) -> PurePosixPath:
    if ".." in relative.parts or not relative.name.startswith("JP_"):
        raise ValueError(f"unexpected Japanese filename: {relative}")
    return relative.with_name(relative.name[3:])


def apply_ui_overrides(relative: PurePosixPath, data: bytes) -> tuple[bytes, int]:
    if relative.as_posix() != "LoginUIText.json":
        return data, 0

    document = json.loads(data.decode("utf-8-sig"))
    rows = document.get("dataList")
    if not isinstance(rows, list):
        raise ValueError("LoginUIText.json must contain a dataList array")

    changed = 0
    found: set[str] = set()
    for row in rows:
        row_id = row.get("id")
        if row_id in UI_OVERRIDES:
            found.add(row_id)
            if row.get("content") != UI_OVERRIDES[row_id]:
                row["content"] = UI_OVERRIDES[row_id]
                changed += 1

    missing = set(UI_OVERRIDES) - found
    if missing:
        raise ValueError(f"LoginUIText.json is missing override IDs: {sorted(missing)}")
    if not changed:
        return data, 0
    return (
        (json.dumps(document, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
        changed,
    )


def build(
    package: Path, manifest_path: Path, llc_root: Path, output_dir: Path
) -> tuple[int, int, int]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = manifest.get("Files")
    if not isinstance(files, dict):
        raise ValueError("manifest must contain a Files object")

    chinese_root = llc_root / "LLC_zh-CN"
    english_root = llc_root / "EN"
    if not chinese_root.is_dir() or not english_root.is_dir():
        raise ValueError("LLC root must contain LLC_zh-CN and EN directories")

    output_dir.mkdir(parents=True, exist_ok=True)
    package_output = output_dir / "localize_jp.zip"
    manifest_output = output_dir / "manifest.json"
    package_temp = package_output.with_suffix(".zip.tmp")
    manifest_temp = manifest_output.with_suffix(".json.tmp")
    written = fallback_files = overridden_strings = 0

    try:
        with zipfile.ZipFile(package) as source, zipfile.ZipFile(
            package_temp, "w", zipfile.ZIP_DEFLATED, compresslevel=9
        ) as target:
            for entry in source.infolist():
                if entry.is_dir():
                    continue

                path = PurePosixPath(entry.filename)
                try:
                    package_relative = path.relative_to(PACKAGE_ROOT)
                except ValueError as error:
                    raise ValueError(f"unexpected package path: {path}") from error

                relative = source_path(package_relative)
                original = source.read(entry)
                data = original
                chinese = chinese_root.joinpath(*relative.parts)
                english = english_root.joinpath(*relative.parts)
                if not chinese.is_file() and english.is_file():
                    data = english.read_bytes()
                    fallback_files += 1

                data, override_count = apply_ui_overrides(relative, data)
                overridden_strings += override_count

                manifest_key = f"{MANIFEST_ROOT}/{package_relative.as_posix()}"
                if manifest_key not in files:
                    raise ValueError(f"manifest entry is missing: {manifest_key}")
                files[manifest_key]["Size"] = len(data)
                if data != original:
                    # The game uses this value as a cache-busting content version.
                    files[manifest_key]["Hash"] = hashlib.md5(data).hexdigest()
                    files[manifest_key]["Crc"] = 0

                target.writestr(entry, data)
                written += 1

        if not written:
            raise ValueError("package contains no localization files")
        manifest_temp.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=4) + "\n",
            encoding="utf-8",
        )
        package_temp.replace(package_output)
        manifest_temp.replace(manifest_output)
    finally:
        package_temp.unlink(missing_ok=True)
        manifest_temp.unlink(missing_ok=True)

    return written, fallback_files, overridden_strings


def self_test() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        package = root / "localize_jp.zip"
        manifest = root / "source-manifest.json"
        llc = root / "llc"
        output = root / "dist"
        (llc / "LLC_zh-CN").mkdir(parents=True)
        (llc / "EN").mkdir()

        login = {
            "dataList": [
                {"id": row_id, "content": "old"} for row_id in UI_OVERRIDES
            ]
        }
        login_data = json.dumps(login).encode()
        japanese_data = b'{"dataList":[{"id":"x","content":"Japanese"}]}'
        english_data = b'{"dataList":[{"id":"x","content":"English"}]}'
        with zipfile.ZipFile(package, "w") as archive:
            archive.writestr("LocalizeTemp_jp/JP_LoginUIText.json", login_data)
            archive.writestr("LocalizeTemp_jp/JP_Missing.json", japanese_data)
        (llc / "LLC_zh-CN" / "LoginUIText.json").write_text("{}")
        (llc / "EN" / "Missing.json").write_bytes(english_data)

        entries = {}
        for name, size in [
            ("JP_LoginUIText.json", len(login_data)),
            ("JP_Missing.json", len(japanese_data)),
        ]:
            entries[f"{MANIFEST_ROOT}/{name}"] = {
                "Hash": "old",
                "Size": size,
                "Crc": 0,
            }
        manifest.write_text(json.dumps({"Files": entries}), encoding="utf-8")

        assert build(package, manifest, llc, output) == (2, 1, 5)
        with zipfile.ZipFile(output / "localize_jp.zip") as archive:
            assert archive.read("LocalizeTemp_jp/JP_Missing.json") == english_data
            result = json.loads(
                archive.read("LocalizeTemp_jp/JP_LoginUIText.json").decode()
            )
            assert {row["id"]: row["content"] for row in result["dataList"]} == UI_OVERRIDES
        result_manifest = json.loads(
            (output / "manifest.json").read_text(encoding="utf-8")
        )
        assert result_manifest["Files"][f"{MANIFEST_ROOT}/JP_Missing.json"] == {
            "Hash": hashlib.md5(english_data).hexdigest(),
            "Size": len(english_data),
            "Crc": 0,
        }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build localize_jp.zip with Chinese text and English fallback."
    )
    parser.add_argument("package", type=Path, nargs="?")
    parser.add_argument("manifest", type=Path, nargs="?")
    parser.add_argument("llc_root", type=Path, nargs="?")
    parser.add_argument("--output-dir", type=Path, default=Path("dist"))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        print("self-test passed")
        return
    if args.package is None or args.manifest is None or args.llc_root is None:
        parser.error("package, manifest and llc_root are required unless --self-test is used")

    written, fallback_files, overridden_strings = build(
        args.package, args.manifest, args.llc_root, args.output_dir
    )
    print(
        f"wrote {written} files; used English fallback for {fallback_files}; "
        f"overrode {overridden_strings} UI strings"
    )


if __name__ == "__main__":
    main()
