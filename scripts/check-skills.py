#!/usr/bin/env python3
"""CI check: every rule document in this repo is a well-formed skill.

Validates all */SKILL.md files: frontmatter present, non-empty name and
description, name == parent directory, name matches ^gfn-[a-z0-9-]+$,
names globally unique, flat layout (only <root>/<id>/SKILL.md), no root
*.md besides README.md, no gfn-* directory without SKILL.md, and README.md
carrying no skill description. Stdlib only.
"""
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^gfn-[a-z0-9-]+$")


def parse_frontmatter(text):
    """Parse a simple flat 'key: value' frontmatter block.

    Returns (dict, None) on success or (None, error_message).
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "missing frontmatter (file must start with '---')"
    meta = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return meta, None
        if not line.strip() or line[:1].isspace():
            continue  # blank line or nested block (e.g. under 'metadata:')
        key, sep, value = line.partition(":")
        if not sep:
            return None, f"unparsable frontmatter line: {line!r}"
        meta[key.strip()] = value.strip()
    return None, "frontmatter not closed (missing closing '---')"


def collect_errors(root):
    """Return a list of human-readable problems found under root."""
    root = Path(root)
    errors = []
    names = {}
    for path in sorted(root.glob("**/SKILL.md")):
        rel = path.relative_to(root)
        if len(rel.parts) != 2:
            errors.append(
                f"{rel}: SKILL.md must live directly under <root>/<id>/ "
                f"(found {len(rel.parts) - 1} directories deep)"
            )
            continue
        meta, err = parse_frontmatter(path.read_text(encoding="utf-8"))
        if err:
            errors.append(f"{rel}: {err}")
            continue
        name = meta.get("name")
        if not name:
            errors.append(f"{rel}: frontmatter has no 'name'")
            continue
        if name != rel.parts[0]:
            errors.append(f"{rel}: name {name!r} does not match directory {rel.parts[0]!r}")
        if not NAME_RE.match(name):
            errors.append(f"{rel}: name {name!r} does not match pattern {NAME_RE.pattern}")
        if not meta.get("description", "").strip().strip('"\'').strip():
            errors.append(f"{rel}: frontmatter has no non-empty 'description'")
        names.setdefault(name, []).append(str(rel))
    for name, paths in sorted(names.items()):
        if len(paths) > 1:
            errors.append(f"duplicate skill name {name!r} in: {', '.join(paths)}")
    # a rule added the old way (root *.md) or a skill dir without SKILL.md is never loaded
    for path in sorted(root.glob("*.md")):
        if path.name != "README.md":
            errors.append(f"{path.name}: rule documents must be <id>/SKILL.md, not root *.md")
    for path in sorted(root.glob("gfn-*/")):
        if not (path / "SKILL.md").is_file():
            errors.append(f"{path.name}/: skill directory has no SKILL.md")
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
