#!/usr/bin/env python3
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTHOR = "mikewang6700"

EXT_CONFIG = {
@Author  : mikewang6700
    ".ts": {"prefix": "//", "marker": "Author"},
    ".js": {"prefix": "//", "marker": "Author"},
    ".vue": {"prefix": "<!--", "suffix": "-->", "marker": "Author"},
    ".md": {"prefix": "<!--", "suffix": "-->", "marker": "Author"},
}

SKIP_DIRS = {".git", "node_modules", "venv", ".venv", "dist", "build"}


def should_skip(path: Path):
    for part in path.parts:
        if part in SKIP_DIRS:
            return True
    return False


def process_py(content_lines):
    # preserve shebang and coding lines
    insert_at = 0
    if content_lines and content_lines[0].startswith("#!"):
        insert_at = 1
    if len(content_lines) > insert_at and content_lines[insert_at].startswith("# -*- coding:"):
        insert_at += 1

    # search for existing author markers in first 10 lines
    for i in range(min(10, len(content_lines))):
        if "@Author" in content_lines[i] or "Author" in content_lines[i] and "@" not in content_lines[i]:
            # replace line
            content_lines[i] = f"@Author  : {AUTHOR}\n"
            return content_lines, True

    header = [f"@Author  : {AUTHOR}\n"]
    # ensure header is within a docstring if file starts with triple-quote
    if content_lines and content_lines[insert_at].startswith('"""'):
        # insert after opening triple quote line
        content_lines.insert(insert_at + 1, f"@Author  : {AUTHOR}\n")
    else:
        # add a short comment block
        content_lines.insert(insert_at, f"# @Author: {AUTHOR}\n")
    return content_lines, True


def process_generic(content_lines, ext):
    cfg = EXT_CONFIG.get(ext, {})
    marker = cfg.get("marker", "Author")
    prefix = cfg.get("prefix", "#")
    suffix = cfg.get("suffix", None)

    # check top 6 lines for existing marker
    for i in range(min(6, len(content_lines))):
        if marker in content_lines[i]:
            # replace line
            if suffix:
                content_lines[i] = f"{prefix} Author: {AUTHOR} {suffix}\n"
            else:
                content_lines[i] = f"{prefix} Author: {AUTHOR}\n"
            return content_lines, True

    # insert at top
    if suffix:
        new = f"{prefix} Author: {AUTHOR} {suffix}\n"
    else:
        new = f"{prefix} Author: {AUTHOR}\n"
    content_lines.insert(0, new)
    return content_lines, True


def main():
    changed = []
    exts = list(EXT_CONFIG.keys())
    for path in ROOT.rglob("*"):
        if path.is_file():
            if should_skip(path):
                continue
            if path.suffix.lower() in exts:
                try:
                    with path.open("r", encoding="utf-8") as f:
                        lines = f.readlines()
                except Exception:
                    continue

                orig = list(lines)
                if path.suffix == ".py":
                    lines, modified = process_py(lines)
                else:
                    lines, modified = process_generic(lines, path.suffix)

                if modified and lines != orig:
                    try:
                        with path.open("w", encoding="utf-8") as f:
                            f.writelines(lines)
                        changed.append(str(path.relative_to(ROOT)))
                    except Exception:
                        continue

    print(f"Updated {len(changed)} files with author header")
    for p in changed:
        print(p)


if __name__ == "__main__":
    main()
