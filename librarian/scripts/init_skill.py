#!/usr/bin/env python3
"""Create a minimal Agent Skill scaffold."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VALID_RESOURCES = {"references", "scripts", "assets", "agents"}


def validate_name(name: str) -> None:
    if not name or len(name) > 64 or not NAME_RE.fullmatch(name):
        raise SystemExit(
            "skill name must be <=64 characters and contain only lowercase letters, "
            "digits, and single hyphens between segments"
        )


def parse_resources(raw: str) -> list[str]:
    if not raw.strip():
        return []
    values = [item.strip() for item in raw.split(",") if item.strip()]
    unknown = sorted(set(values) - VALID_RESOURCES)
    if unknown:
        raise SystemExit(f"unknown resource directories: {', '.join(unknown)}")
    return list(dict.fromkeys(values))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="hyphen-case skill name")
    parser.add_argument("--path", required=True, help="parent directory for the new skill")
    parser.add_argument("--description", required=True, help="discovery description: what + when")
    parser.add_argument(
        "--resources",
        default="",
        help="comma-separated optional directories: references,scripts,assets,agents",
    )
    args = parser.parse_args()

    validate_name(args.name)
    description = args.description.strip()
    if not description:
        raise SystemExit("description must not be empty")

    root = Path(args.path).expanduser().resolve() / args.name
    if root.exists():
        raise SystemExit(f"refusing to overwrite existing path: {root}")
    root.mkdir(parents=True)

    body = f"""---\nname: {args.name}\ndescription: {description}\n---\n\n# {args.name}\n\n[Replace this scaffold text with concise procedural instructions.]\n"""
    (root / "SKILL.md").write_text(body, encoding="utf-8")

    for resource in parse_resources(args.resources):
        (root / resource).mkdir()

    print(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
