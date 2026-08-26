#!/usr/bin/env python3
"""词库一致性检查（vocabulary consistency checker）.

用途 / What it does
- 校验 `vocabulary/words.md` 索引与 `vocabulary/entries/*.md` 条目是否一一对应。
- 校验索引中的链接指向的文件真实存在，没有死链或孤儿条目。
- 校验每个条目有一级标题，并提示缺失的推荐小节（原子意思 / 词根 / 短语 / 句子等）。

退出码 / Exit codes
- 0：没有完整性错误（可能仍有提示性 warning）。
- 1：存在完整性错误（死链、孤儿条目、缺标题等）。
- 加 `--strict` 时，缺失推荐小节也会算作错误。

只用标准库，无需第三方依赖。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VOCAB_DIR = REPO_ROOT / "vocabulary"
ENTRIES_DIR = VOCAB_DIR / "entries"
WORDS_INDEX = VOCAB_DIR / "words.md"

# 索引表格里的条目链接：[text](entries/<name>.md)
LINK_RE = re.compile(r"\]\(entries/([^)]+\.md)\)")

# 条目内推荐小节（缺失只作提示，除非 --strict）
RECOMMENDED_SECTIONS = [
    ("## 1.", "高频常用意思"),
    ("## 2.", "原子意思"),
    ("## 3.", "词根"),
    ("## 4.", "常用短语"),
    ("## 5.", "常用句子"),
]


def entry_files() -> list[Path]:
    return sorted(
        p for p in ENTRIES_DIR.glob("*.md") if p.name != ".gitkeep"
    )


def indexed_entries() -> set[str]:
    if not WORDS_INDEX.exists():
        return set()
    text = WORDS_INDEX.read_text(encoding="utf-8")
    return set(LINK_RE.findall(text))


def main() -> int:
    parser = argparse.ArgumentParser(description="Check vocabulary index/entry consistency.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="把缺失的推荐小节也当作错误（默认只当作提示）。",
    )
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    if not ENTRIES_DIR.is_dir():
        print(f"ERROR: entries 目录不存在: {ENTRIES_DIR}")
        return 1
    if not WORDS_INDEX.exists():
        print(f"ERROR: 索引文件不存在: {WORDS_INDEX}")
        return 1

    files = entry_files()
    file_names = {p.name for p in files}
    indexed = indexed_entries()

    # 1) 索引里的链接必须对应真实文件（无死链）
    for name in sorted(indexed):
        if name not in file_names:
            errors.append(f"死链: words.md 指向 entries/{name}，但该文件不存在")

    # 2) 每个条目文件都应被索引收录（无孤儿）
    for name in sorted(file_names):
        if name not in indexed:
            errors.append(f"孤儿条目: entries/{name} 未出现在 words.md 索引中")

    # 3) 每个条目：一级标题 + 推荐小节
    for path in files:
        text = path.read_text(encoding="utf-8")
        rel = f"entries/{path.name}"
        if not re.search(r"^#\s+\S", text, re.MULTILINE):
            errors.append(f"缺一级标题: {rel} 没有 `# <word>` 标题")
        for marker, label in RECOMMENDED_SECTIONS:
            if marker not in text:
                msg = f"缺小节: {rel} 缺少「{label}」({marker} …)"
                (errors if args.strict else warnings).append(msg)

    total = len(files)
    print(f"检查条目 {total} 个，索引链接 {len(indexed)} 条。")
    if warnings:
        print(f"\n提示 (warning) {len(warnings)} 条:")
        for w in warnings:
            print(f"  - {w}")
    if errors:
        print(f"\n错误 (error) {len(errors)} 条:")
        for e in errors:
            print(f"  - {e}")
        print("\n结果: 失败 ❌")
        return 1

    print("\n结果: 索引与条目一致，无完整性错误 ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
