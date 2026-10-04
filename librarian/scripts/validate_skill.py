#!/usr/bin/env python3
"""Validate a portable SKILL.md-centered Agent Skill."""

from __future__ import annotations

import argparse
import ast
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
PLACEHOLDER_PATTERNS = (
    "[Replace this scaffold text",
    "YOUR_SKILL",
)
AUX_DOCS = {"README.md", "INSTALLATION_GUIDE.md", "QUICK_REFERENCE.md", "CHANGELOG.md"}
ALLOWED_TOP_LEVEL = {"SKILL.md", "agents", "references", "scripts", "assets"}
IGNORED_NAMES = {".DS_Store", "Thumbs.db", "__pycache__"}


@dataclass
class Finding:
    level: str
    message: str


def parse_simple_frontmatter(text: str) -> tuple[dict[str, str], list[Finding]]:
    findings: list[Finding] = []
    match = FRONTMATTER_RE.search(text)
    if not match:
        return {}, [Finding("ERROR", "SKILL.md is missing valid YAML frontmatter delimiters")]

    result: dict[str, str] = {}
    for lineno, raw in enumerate(match.group(1).splitlines(), start=2):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith((" ", "\t")):
            findings.append(Finding("WARN", f"frontmatter line {lineno} uses nested/multiline YAML; validator only checks simple top-level scalars"))
            continue
        if ":" not in raw:
            findings.append(Finding("ERROR", f"frontmatter line {lineno} is not key: value syntax"))
            continue
        key, value = raw.split(":", 1)
        key, value = key.strip(), value.strip()
        if not key:
            findings.append(Finding("ERROR", f"frontmatter line {lineno} has an empty key"))
            continue
        if value[:1] in {'"', "'"} and value[-1:] == value[:1] and len(value) >= 2:
            value = value[1:-1]
        result[key] = value.strip()
    return result, findings


def iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.name in IGNORED_NAMES:
            continue
        yield path


def validate(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    if not root.exists() or not root.is_dir():
        return [Finding("ERROR", f"not a directory: {root}")]

    skill_md = root / "SKILL.md"
    if not skill_md.is_file():
        return [Finding("ERROR", "SKILL.md not found at skill root")]

    nested = [p for p in root.rglob("SKILL.md") if p != skill_md]
    if nested:
        findings.append(Finding("ERROR", "nested SKILL.md found; package one skill per directory: " + ", ".join(str(p.relative_to(root)) for p in nested)))

    for path in iter_files(root):
        if path.is_symlink():
            findings.append(Finding("ERROR", f"symlink is not portable/safe to package: {path.relative_to(root)}"))

    text = skill_md.read_text(encoding="utf-8")
    meta, meta_findings = parse_simple_frontmatter(text)
    findings.extend(meta_findings)

    name = meta.get("name", "").strip()
    description = meta.get("description", "").strip()
    if not name:
        findings.append(Finding("ERROR", "frontmatter name is missing or empty"))
    else:
        if len(name) > 64 or not NAME_RE.fullmatch(name):
            findings.append(Finding("ERROR", "name must be <=64 characters and hyphen-case using lowercase letters/digits"))
        if root.name != name and not re.fullmatch(r"skill-[0-9a-f]{32}", root.name):
            findings.append(Finding("ERROR", f"folder name '{root.name}' does not match skill name '{name}'"))
    if not description:
        findings.append(Finding("ERROR", "frontmatter description is missing or empty"))
    elif len(description) > 1200:
        findings.append(Finding("WARN", "description is unusually long; discovery metadata should be concise and discriminating"))

    extras = sorted(set(meta) - {"name", "description"})
    if extras:
        findings.append(Finding("WARN", "extra frontmatter keys reduce portability unless the target platform supports them: " + ", ".join(extras)))

    for token in PLACEHOLDER_PATTERNS:
        if token.lower() in text.lower():
            findings.append(Finding("ERROR", f"unfinished scaffold marker found in SKILL.md: {token}"))

    # Standalone TODO/TBD markers are useful signals, but do not flag prose that discusses them.
    if re.search(r"(?im)^\s*(?:[-*]\s*)?(?:TODO|TBD)(?:\s*:|\s*$)", text):
        findings.append(Finding("ERROR", "unfinished TODO/TBD marker found in SKILL.md"))

    for doc in AUX_DOCS:
        if (root / doc).exists():
            findings.append(Finding("WARN", f"auxiliary documentation is usually unnecessary in a skill: {doc}"))

    for child in root.iterdir():
        if child.name not in ALLOWED_TOP_LEVEL and child.name not in IGNORED_NAMES:
            findings.append(Finding("WARN", f"unusual top-level entry; verify it is required: {child.name}"))

    # Check relative Markdown links from SKILL.md.
    linked: set[Path] = set()
    for target in LINK_RE.findall(text):
        target = target.strip().split("#", 1)[0].strip()
        if not target or "://" in target or target.startswith(("mailto:", "#")):
            continue
        target_path = (root / target).resolve()
        try:
            target_path.relative_to(root.resolve())
        except ValueError:
            findings.append(Finding("ERROR", f"Markdown link escapes the skill directory: {target}"))
            continue
        linked.add(target_path)
        if not target_path.exists():
            findings.append(Finding("ERROR", f"broken local Markdown link in SKILL.md: {target}"))

    references = root / "references"
    if references.is_dir():
        for ref in references.rglob("*"):
            if ref.is_dir():
                if ref != references:
                    findings.append(Finding("WARN", f"nested reference directory makes discovery harder: {ref.relative_to(root)}"))
                continue
            if ref.resolve() not in linked:
                findings.append(Finding("WARN", f"reference is not linked directly from SKILL.md: {ref.relative_to(root)}"))
            try:
                lines = ref.read_text(encoding="utf-8").splitlines()
            except UnicodeDecodeError:
                continue
            if len(lines) > 100:
                first_40 = "\n".join(lines[:40]).lower()
                if "table of contents" not in first_40 and "## contents" not in first_40:
                    findings.append(Finding("WARN", f"long reference may benefit from a table of contents: {ref.relative_to(root)}"))

    scripts = root / "scripts"
    if scripts.is_dir():
        for script in scripts.rglob("*.py"):
            try:
                ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
            except (SyntaxError, UnicodeDecodeError) as exc:
                findings.append(Finding("ERROR", f"Python syntax/read error in {script.relative_to(root)}: {exc}"))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_directory")
    args = parser.parse_args()

    root = Path(args.skill_directory).expanduser().resolve()
    findings = validate(root)
    for finding in findings:
        print(f"{finding.level}: {finding.message}")

    errors = sum(f.level == "ERROR" for f in findings)
    warnings = sum(f.level == "WARN" for f in findings)
    if errors:
        print(f"INVALID: {errors} error(s), {warnings} warning(s)")
        return 1
    print(f"VALID: 0 errors, {warnings} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
