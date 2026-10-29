#!/usr/bin/env python3
"""CI check: every rule document in this repo is a well-formed skill.

Per <root>/<id>/SKILL.md:
- frontmatter present: the text between the first '---' line and the next
  '---' line, and it must parse (yaml.safe_load) to a mapping
- name: a str matching ^gfn-[a-z0-9]+(-[a-z0-9]+)*$, at most 64 chars,
  and equal to the parent directory name
- description: a non-empty str after strip, at most 1024 chars
- metadata, when present, is a mapping
- the body after the closing '---' is non-empty after strip

Repo-wide:
- skill names are globally unique
- SKILL.md lives only at <root>/<id>/SKILL.md (no nesting)
- every gfn-* directory contains a SKILL.md
- root *.md files are limited to README.md and AGENTS.md
- README.md carries no skill description
- every backticked `gfn-...` id in any SKILL.md body or in README.md
  matches an existing skill directory
"""
import re
import sys
from pathlib import Path

import yaml

NAME_RE = re.compile(r"^gfn-[a-z0-9]+(-[a-z0-9]+)*$")
REF_RE = re.compile(r"`(gfn-[a-z0-9-]+)`")
ROOT_MD_ALLOWED = {"README.md", "AGENTS.md"}


def split_frontmatter(text):
    """Split into (frontmatter_text, body) or (None, None, error_message)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, None, "missing frontmatter (file must start with '---')"
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:]), None
    return None, None, "frontmatter not closed (missing closing '---')"


def parse_frontmatter(text):
    """Parse frontmatter into (mapping, None) or (None, error_message)."""
    fm_text, _, err = split_frontmatter(text)
    if err:
        return None, err
    try:
        data = yaml.safe_load(fm_text)
    except yaml.YAMLError as exc:
        return None, f"frontmatter is not valid YAML: {exc}"
    if not isinstance(data, dict):
        return None, "frontmatter must parse to a mapping"
    return data, None


def collect_errors(root):
    """Return a list of human-readable problems found under root."""
    root = Path(root)
    errors = []
    names = {}
    skill_dirs = set()
    skill_files = []
    for path in sorted(root.glob("**/SKILL.md")):
        rel = path.relative_to(root)
        if len(rel.parts) != 2:
            errors.append(
                f"{rel}: SKILL.md must live directly under <root>/<id>/ "
                f"(found {len(rel.parts) - 1} directories deep)"
            )
            continue
        skill_files.append(path)
        skill_dirs.add(rel.parts[0])
        text = path.read_text(encoding="utf-8")
        meta, err = parse_frontmatter(text)
        if err:
            errors.append(f"{rel}: {err}")
            continue
        name = meta.get("name")
        if not isinstance(name, str) or not name:
            errors.append(f"{rel}: frontmatter has no 'name'")
            continue
        if name != rel.parts[0]:
            errors.append(f"{rel}: name {name!r} does not match directory {rel.parts[0]!r}")
        if len(name) > 64:
            errors.append(f"{rel}: name exceeds 64 characters ({len(name)})")
        if not NAME_RE.match(name):
            errors.append(f"{rel}: name {name!r} does not match pattern {NAME_RE.pattern}")
        desc = meta.get("description")
        if not isinstance(desc, str) or not desc.strip():
            errors.append(f"{rel}: frontmatter has no non-empty 'description'")
        elif len(desc.strip()) > 1024:
            errors.append(f"{rel}: description exceeds 1024 characters ({len(desc.strip())})")
        metadata = meta.get("metadata")
        if metadata is not None and not isinstance(metadata, dict):
            errors.append(f"{rel}: metadata must be a mapping")
        _, body, body_err = split_frontmatter(text)
        if not body_err and not body.strip():
            errors.append(f"{rel}: body is empty after frontmatter")
        names.setdefault(name, []).append(str(rel))
    for name, paths in sorted(names.items()):
        if len(paths) > 1:
            errors.append(f"duplicate skill name {name!r} in: {', '.join(paths)}")
    # a rule added the old way (root *.md) or a skill dir without SKILL.md is never loaded
    for path in sorted(root.glob("*.md")):
        if path.name not in ROOT_MD_ALLOWED:
            errors.append(f"{path.name}: rule documents must be <id>/SKILL.md, not root *.md")
    for path in sorted(root.glob("gfn-*/")):
        if not (path / "SKILL.md").is_file():
            errors.append(f"{path.name}/: skill directory has no SKILL.md")
    # backticked skill ids must reference an existing skill directory
    scan_targets = [(p, p.relative_to(root)) for p in skill_files]
    readme = root / "README.md"
    if readme.exists():
        scan_targets.append((readme, Path("README.md")))
    for path, rel in scan_targets:
        _, body, body_err = split_frontmatter(path.read_text(encoding="utf-8"))
        for match in REF_RE.finditer(body_err is None and body or ""):
            ref = match.group(1)
            if ref not in skill_dirs:
                errors.append(f"{rel}: references unknown skill id `{ref}`")
    readme = root / "README.md"
    if readme.exists():
        meta, _ = parse_frontmatter(readme.read_text(encoding="utf-8"))
        if meta and meta.get("description"):
            errors.append("README.md: must not have frontmatter with a 'description' (it is not a skill)")
    return errors


def main():
    root = Path(__file__).resolve().parent.parent
    errors = collect_errors(root)
    for err in errors:
        print(f"ERROR: {err}")
    if errors:
        print(f"{len(errors)} problem(s) found")
        return 1
    print("OK: all skills valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
