"""按一级标题切分 Markdown 文档。

用法:
    python split_notes.py [SOURCE] [OUTPUT_DIR]

默认行为:
    - SOURCE     : notes/modelisation_note.md
    - OUTPUT_DIR : notes/split/

每个一级标题 (以单个 `#` 开头, 不在代码块内) 会被切分到一个独立的 .md 文件中,
文件名由标题文本转换而来, 并在前面加上两位序号保持原始顺序.
同时会在输出目录下生成 index.md 作为目录/导航页。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Windows 下 PowerShell 默认使用 GBK, 打印含法语/特殊字符的路径会抛 UnicodeEncodeError。
# 尝试将 stdout/stderr 切到 UTF-8; 若运行环境不支持, 退而采用替换策略。
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except (AttributeError, ValueError):
        pass


# 匹配围栏代码块开头/结尾, 允许前置空白, 并允许 ``` 或 ~~~
_FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})")
# 一级标题: 行首恰好一个 #, 后面跟空格
_H1_RE = re.compile(r"^#\s+(.+?)\s*$")


def iter_sections(lines: list[str]):
    """遍历 markdown 行, 产出 (标题, 起始行号, 结束行号) 的分段。

    - 忽略围栏代码块 (```/~~~) 内部的 # 行, 避免把代码注释当作标题。
    - 若文档开头没有一级标题, 这段前言会作为第一个段落输出, 标题为 "前言"。
    """
    in_fence = False
    fence_marker: str | None = None

    sections: list[tuple[str, int]] = []  # (title, start_line_index)

    for idx, raw in enumerate(lines):
        stripped = raw.rstrip("\n")

        fence_match = _FENCE_RE.match(stripped)
        if fence_match:
            marker = fence_match.group(2)[:3]  # ``` or ~~~
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif fence_marker is not None and stripped.lstrip().startswith(fence_marker):
                in_fence = False
                fence_marker = None
            continue

        if in_fence:
            continue

        m = _H1_RE.match(stripped)
        if m:
            sections.append((m.group(1).strip(), idx))

    if not sections:
        return []

    # 若第一段一级标题不在文件开头, 前面的内容作为 "前言"
    result: list[tuple[str, int, int]] = []
    if sections[0][1] > 0:
        result.append(("前言", 0, sections[0][1]))

    for i, (title, start) in enumerate(sections):
        end = sections[i + 1][1] if i + 1 < len(sections) else len(lines)
        result.append((title, start, end))

    return result


def slugify(title: str, fallback: str) -> str:
    """将标题转换为适合做文件名的 slug, 保留中文字符。"""
    # 去掉 markdown 强调/删除线等符号
    cleaned = re.sub(r"[`*_~]+", "", title)
    # Windows 文件名非法字符替换
    cleaned = re.sub(r'[\\/:*?"<>|]+', " ", cleaned)
    # 空白压缩为 -
    cleaned = re.sub(r"\s+", "-", cleaned.strip())
    # 去掉首尾的点号 (Windows 不允许)
    cleaned = cleaned.strip(".")
    # 限长, 避免过长路径
    cleaned = cleaned[:80]
    return cleaned or fallback


def split_file(source: Path, output_dir: Path) -> list[Path]:
    text = source.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    sections = iter_sections(lines)
    if not sections:
        print(f"[!] 未在 {source} 中找到一级标题, 未生成任何文件。", file=sys.stderr)
        return []

    output_dir.mkdir(parents=True, exist_ok=True)

    written: list[tuple[str, Path]] = []
    used_names: set[str] = set()

    width = max(2, len(str(len(sections))))

    for i, (title, start, end) in enumerate(sections, start=1):
        slug = slugify(title, fallback=f"section-{i}")
        base = f"{str(i).zfill(width)}-{slug}"
        name = f"{base}.md"
        # 处理重名
        dedup = 2
        while name in used_names:
            name = f"{base}-{dedup}.md"
            dedup += 1
        used_names.add(name)

        target = output_dir / name
        content = "".join(lines[start:end])
        # 保证以单个换行结尾
        if not content.endswith("\n"):
            content += "\n"
        target.write_text(content, encoding="utf-8")
        written.append((title, target))

    # 生成 index.md
    index = output_dir / "index.md"
    rel_source = source.as_posix()
    index_lines = [
        f"# 目录\n",
        f"\n",
        f"由 `split_notes.py` 从 `{rel_source}` 自动生成, 请勿手工修改本文件。\n",
        f"\n",
    ]
    for i, (title, path) in enumerate(written, start=1):
        index_lines.append(f"{i}. [{title}]({path.name})\n")
    index.write_text("".join(index_lines), encoding="utf-8")

    return [p for _, p in written] + [index]


def main() -> int:
    parser = argparse.ArgumentParser(description="按一级标题切分 Markdown 文档")
    parser.add_argument(
        "source",
        nargs="?",
        default="notes/modelisation_note.md",
        help="待切分的 Markdown 文件路径 (默认: notes/modelisation_note.md)",
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default="notes/split",
        help="切分结果输出目录 (默认: notes/split)",
    )
    args = parser.parse_args()

    source = Path(args.source)
    output_dir = Path(args.output_dir)

    if not source.is_file():
        print(f"[x] 找不到源文件: {source}", file=sys.stderr)
        return 1

    written = split_file(source, output_dir)
    print(f"[OK] 共生成 {len(written)} 个文件 -> {output_dir}")
    for p in written:
        print(f"    - {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
