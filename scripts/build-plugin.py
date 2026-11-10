#!/usr/bin/env python3
"""Build a deterministic skills-only Codex plugin ZIP without publishing it."""

import json
from pathlib import Path
import runpy
import stat
import zipfile

ROOT = Path(__file__).resolve().parents[1]
POLICY = runpy.run_path(str(ROOT / "scripts/validate-distribution.py"))


def denied_path(path: Path) -> bool:
    return (bool(POLICY["DENIED_PARTS"].intersection(path.parts))
            or any(part.startswith(".") for part in path.parts[1:]))


def payload_files() -> list[Path]:
    roots = [ROOT / ".codex-plugin/plugin.json", ROOT / "LICENSE",
             ROOT / "skills", ROOT / "shared"]
    files = []
    for root in roots:
        if not root.exists():
            raise ValueError(f"missing payload: {root.relative_to(ROOT)}")
        for path in [root, *sorted(root.rglob("*"))]:
            relative = path.relative_to(ROOT)
            if path.is_symlink():
                target = path.resolve()
                try:
                    resolved = target.relative_to(ROOT)
                except ValueError as error:
                    raise ValueError(f"external symlink in payload: {relative}") from error
                if (not target.is_file()
                        or resolved.parts[0] not in {"skills", "shared"}
                        or denied_path(resolved)):
                    raise ValueError(f"unsafe symlink in payload: {relative}")
            if denied_path(relative):
                raise ValueError(f"denied path in payload: {relative}")
            if relative.parts[0] not in (
                    POLICY["ALLOWED_DIRS"] | POLICY["ALLOWED_ROOT_FILES"]):
                raise ValueError(f"denied payload root: {relative}")
            if path.is_file():
                files.append(path)
            elif not path.is_dir():
                raise ValueError(f"unsupported payload file: {relative}")
    return sorted(files)


def main() -> None:
    files = payload_files()
    manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
    version = manifest["version"]
    if not isinstance(version, str) or any(c not in "0123456789." for c in version):
        raise ValueError("invalid plugin version")
    output = ROOT / "dist" / f"groundcrew-seo-{version}.zip"
    output.parent.mkdir(exist_ok=True)
    temporary = output.with_suffix(".zip.tmp")
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_STORED) as archive:
            for path in files:
                info = zipfile.ZipInfo(path.relative_to(ROOT).as_posix(),
                                       date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = (stat.S_IFREG | 0o644) << 16
                archive.writestr(info, path.read_bytes())
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    print(f"Built {output.relative_to(ROOT)}: {len(files)} allowlisted files")


if __name__ == "__main__":
    main()
