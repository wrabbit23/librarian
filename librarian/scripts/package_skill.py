#!/usr/bin/env python3
"""Validate and package one Agent Skill as a deterministic ZIP."""

from __future__ import annotations

import argparse
import importlib.util
import os
from pathlib import Path
import stat
import zipfile

EXCLUDE_PARTS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".venv", "venv", "node_modules"}
EXCLUDE_NAMES = {".DS_Store", "Thumbs.db"}
FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def load_validator(script_dir: Path):
    path = script_dir / "validate_skill.py"
    spec = importlib.util.spec_from_file_location("validate_skill", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load validate_skill.py")
    module = importlib.util.module_from_spec(spec)
    # dataclasses expects the module to be visible while class decorators execute.
    import sys
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def should_include(path: Path, root: Path, output: Path) -> bool:
    rel = path.relative_to(root)
    if any(part in EXCLUDE_PARTS for part in rel.parts):
        return False
    if path.name in EXCLUDE_NAMES:
        return False
    if path.resolve() == output.resolve():
        return False
    return True


def write_file(zf: zipfile.ZipFile, source: Path, arcname: str) -> None:
    data = source.read_bytes()
    info = zipfile.ZipInfo(arcname, FIXED_TIME)
    mode = source.stat().st_mode
    perms = 0o755 if (mode & stat.S_IXUSR) else 0o644
    info.external_attr = (stat.S_IFREG | perms) << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    zf.writestr(info, data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_directory")
    parser.add_argument("--output", help="output ZIP path; defaults beside the skill directory")
    args = parser.parse_args()

    root = Path(args.skill_directory).expanduser().resolve()
    output = Path(args.output).expanduser().resolve() if args.output else root.parent / f"{root.name}.zip"

    try:
        output.relative_to(root)
    except ValueError:
        pass
    else:
        raise SystemExit("output ZIP must be outside the skill directory")

    validator = load_validator(Path(__file__).resolve().parent)
    metadata, _ = validator.parse_simple_frontmatter((root / "SKILL.md").read_text(encoding="utf-8"))
    skill_name = metadata.get("name", root.name)
    findings = validator.validate(root)
    errors = [f for f in findings if f.level == "ERROR"]
    warnings = [f for f in findings if f.level == "WARN"]
    for finding in findings:
        print(f"{finding.level}: {finding.message}")
    if errors:
        raise SystemExit(f"refusing to package invalid skill ({len(errors)} error(s))")
    if warnings:
        print(f"Packaging with {len(warnings)} warning(s).")

    output.parent.mkdir(parents=True, exist_ok=True)
    temp = output.with_suffix(output.suffix + ".tmp")
    if temp.exists():
        temp.unlink()

    with zipfile.ZipFile(temp, "w") as zf:
        for path in sorted(root.rglob("*"), key=lambda p: p.as_posix()):
            if path.is_symlink():
                raise SystemExit(f"refusing symlink: {path}")
            if not path.is_file() or not should_include(path, root, output):
                continue
            arcname = f"{skill_name}/{path.relative_to(root).as_posix()}"
            write_file(zf, path, arcname)

    os.replace(temp, output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
