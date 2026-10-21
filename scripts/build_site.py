#!/usr/bin/env python3
"""Build a static site from an Obsidian vault for GitHub Pages deployment.

Walks the vault, renders every Markdown note to HTML at the same relative path
with the extension changed, converts Obsidian wikilinks and embeds to RELATIVE
links, copies every other file verbatim, and writes a landing page plus a small
stylesheet.

The site is served from a subpath (https://<user>.github.io/<repo>/), so every
internal link this script emits is relative - it never starts with "/".

Standard library only. Run from the vault root: python scripts/build_site.py
"""

from __future__ import annotations

import html
import os
import posixpath
import re
import shutil
import urllib.parse
from pathlib import Path

OUT_DIR_NAME = "_site"
SITE_TITLE = "Obsidian Vault"

# Directories never published. Any path segment starting with "." (".git",
# ".obsidian", ".github", ...) is skipped too - see is_excluded().
EXCLUDE_DIRS = {"scripts", "_site", "__pycache__"}

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".avif", ".bmp"}

EXTERNAL_PREFIXES = (
    "http://",
    "https://",
    "//",
    "mailto:",
    "tel:",
    "data:",
    "obsidian:",
    "javascript:",
)

FENCE_RE = re.compile(r"^\s*```(.*)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
HR_RE = re.compile(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$")
LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{1,}:?\s*(\|\s*:?-{1,}:?\s*)*\|?\s*$")
TOKEN_RE = re.compile(
    r"(!\[\[[^\]]*\]\]|\[\[[^\]]*\]\]|!\[[^\]]*\]\([^)]*\)|\[[^\]]*\]\([^)]*\))"
)


# --------------------------------------------------------------------------- #
# Path helpers
# --------------------------------------------------------------------------- #
def is_excluded(rel_parts):
    """Return True if a path (tuple of segments) must not be published."""
    for part in rel_parts:
        if part.startswith("."):
            return True
        if part in EXCLUDE_DIRS:
            return True
    return False


def collect_files(root):
    """Walk the vault and return (note_rel_paths, asset_rel_paths), sorted.

    Paths are posix-style and relative to the vault root. Excluded directories
    are pruned so the walk never descends into .git/ or _site/.
    """
    notes = []
    assets = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        rel_parts = () if rel_dir == "." else tuple(rel_dir.split(os.sep))

        dirnames[:] = sorted(
            d for d in dirnames if not is_excluded(rel_parts + (d,))
        )

        for name in sorted(filenames):
            parts = rel_parts + (name,)
            if is_excluded(parts):
                continue
            rel_posix = "/".join(parts)
            if name.lower().endswith(".md"):
                notes.append(rel_posix)
            else:
                assets.append(rel_posix)

    return sorted(notes), sorted(assets)


def md_to_html(rel_posix):
    """Turn a note path into its output path (same path, .md -> .html)."""
    stem, _ = posixpath.splitext(rel_posix)
    return stem + ".html"


def encode_path(rel_posix):
    """Percent-encode each segment of a relative path (spaces -> %20)."""
    rel_posix = rel_posix.lstrip("/")  # never absolute
    return "/".join(urllib.parse.quote(seg) for seg in rel_posix.split("/"))


def rel_link(from_dir, to_rel):
    """Relative, percent-encoded link from a page directory to a site path."""
    rel = posixpath.relpath(to_rel, from_dir or ".")
    return encode_path(rel)


def slugify(text):
    """Lowercase, hyphenated id fragment for HTML anchors."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"


# --------------------------------------------------------------------------- #
# Frontmatter
# --------------------------------------------------------------------------- #
def split_frontmatter(text):
    """Split optional leading YAML frontmatter from the Markdown body."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return "\n".join(lines[1:i]), "\n".join(lines[i + 1:])
    return "", text


def _clean_scalar(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value


def parse_frontmatter(text):
    """Parse the subset of YAML we support: scalars and simple lists."""
    meta = {}
    current_key = None
    for raw in text.split("\n"):
        if not raw.strip():
            continue

        # Continuation of a "key:" block list ("  - item") or its scalar value.
        if raw[:1] in (" ", "\t"):
            item = raw.strip()
            if item.startswith("- "):
                item = item[2:].strip()
            elif item.startswith("-"):
                item = item[1:].strip()
            else:
                continue
            if current_key:
                if not isinstance(meta.get(current_key), list):
                    meta[current_key] = []
                meta[current_key].append(_clean_scalar(item))
            continue

        if ":" not in raw:
            continue
        key, _, value = raw.partition(":")
        key = key.strip()
        value = value.strip()
        current_key = key

        if value == "":
            meta[key] = []
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            meta[key] = [
                _clean_scalar(part) for part in inner.split(",") if part.strip()
            ] if inner else []
        else:
            meta[key] = _clean_scalar(value)
    return meta


# --------------------------------------------------------------------------- #
# Markdown + Obsidian renderer
# --------------------------------------------------------------------------- #
class Renderer:
    """Render the Markdown/Obsidian subset used by the vault."""

    def __init__(self, note_index, asset_index):
        self.note_index = note_index
        self.asset_index = asset_index

    # -- resolution ------------------------------------------------------- #
    def resolve_note(self, name):
        key = name.strip().lower()
        if key.endswith(".md"):
            key = key[:-3]
        return self.note_index.get(key)

    def resolve_asset(self, name):
        base = posixpath.basename(name.strip()).lower()
        return self.asset_index.get(base)

    # -- block level ------------------------------------------------------ #
    def render(self, body, page_dir):
        lines = body.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        out = []
        i = 0
        n = len(lines)
        while i < n:
            line = lines[i]
            if line.strip() == "":
                i += 1
                continue
            if FENCE_RE.match(line):
                i = self._fence(lines, i, out)
                continue
            m = HEADING_RE.match(line)
            if m:
                level = len(m.group(1))
                out.append(
                    f"<h{level}>{self.render_inline(m.group(2), page_dir)}</h{level}>"
                )
                i += 1
                continue
            if HR_RE.match(line):
                out.append("<hr>")
                i += 1
                continue
            if self._is_table_start(lines, i):
                i = self._table(lines, i, out, page_dir)
                continue
            if LIST_RE.match(line):
                i = self._list(lines, i, out, page_dir)
                continue
            if line.lstrip().startswith(">"):
                i = self._blockquote(lines, i, out, page_dir)
                continue
            i = self._paragraph(lines, i, out, page_dir)
        return "\n".join(out)

    def _starts_block(self, lines, i):
        line = lines[i]
        if line.strip() == "":
            return True
        if FENCE_RE.match(line) or HEADING_RE.match(line) or HR_RE.match(line):
            return True
        if LIST_RE.match(line) or line.lstrip().startswith(">"):
            return True
        return self._is_table_start(lines, i)

    def _fence(self, lines, i, out):
        lang = FENCE_RE.match(lines[i]).group(1).strip()
        i += 1
        buf = []
        while i < len(lines) and not FENCE_RE.match(lines[i]):
            buf.append(lines[i])
            i += 1
        if i < len(lines):
            i += 1  # consume the closing fence
        code = html.escape("\n".join(buf))
        cls = f' class="language-{html.escape(lang, quote=True)}"' if lang else ""
        out.append(f"<pre><code{cls}>{code}</code></pre>")
        return i

    def _is_table_start(self, lines, i):
        if "|" not in lines[i]:
            return False
        return i + 1 < len(lines) and bool(TABLE_SEP_RE.match(lines[i + 1]))

    @staticmethod
    def _split_cells(line):
        line = line.strip()
        if line.startswith("|"):
            line = line[1:]
        if line.endswith("|"):
            line = line[:-1]
        return [cell.strip() for cell in line.split("|")]

    def _table(self, lines, i, out, page_dir):
        headers = self._split_cells(lines[i])
        i += 2  # header row + separator row
        rows = []
        while i < len(lines) and lines[i].strip() != "" and "|" in lines[i]:
            rows.append(self._split_cells(lines[i]))
            i += 1
        head = "".join(
            f"<th>{self.render_inline(c, page_dir)}</th>" for c in headers
        )
        body = []
        for row in rows:
            cells = "".join(
                f"<td>{self.render_inline(c, page_dir)}</td>" for c in row
            )
            body.append(f"<tr>{cells}</tr>")
        out.append(
            f"<table><thead><tr>{head}</tr></thead>"
            f"<tbody>{''.join(body)}</tbody></table>"
        )
        return i

    def _list(self, lines, i, out, page_dir):
        items = []
        while i < len(lines):
            line = lines[i]
            if line.strip() == "":
                break
            m = LIST_RE.match(line)
            if not m:
                break
            indent = len(m.group(1).expandtabs(4))
            marker = m.group(2)
            items.append((indent, marker[0].isdigit(), m.group(3)))
            i += 1
        rendered, _ = self._build_list(items, 0, items[0][0], page_dir)
        out.append(rendered)
        return i

    def _build_list(self, items, start, indent, page_dir):
        tag = "ol" if items[start][1] else "ul"
        parts = [f"<{tag}>"]
        i = start
        while i < len(items):
            ind, _ordered, content = items[i]
            if ind < indent:
                break
            parts.append(f"<li>{self.render_inline(content, page_dir)}")
            j = i + 1
            if j < len(items) and items[j][0] > indent:
                child, j = self._build_list(items, j, items[j][0], page_dir)
                parts.append(child)
            parts.append("</li>")
            i = j
        parts.append(f"</{tag}>")
        return "".join(parts), i

    def _blockquote(self, lines, i, out, page_dir):
        collected = []
        while i < len(lines) and lines[i].lstrip().startswith(">"):
            text = lines[i].lstrip()[1:]
            if text.startswith(" "):
                text = text[1:]
            collected.append(text)
            i += 1
        paragraphs = []
        current = []
        for text in collected:
            if text.strip() == "":
                if current:
                    paragraphs.append(" ".join(current))
                    current = []
            else:
                current.append(text.strip())
        if current:
            paragraphs.append(" ".join(current))
        inner = "".join(
            f"<p>{self.render_inline(p, page_dir)}</p>" for p in paragraphs
        )
        out.append(f"<blockquote>{inner}</blockquote>")
        return i

    def _paragraph(self, lines, i, out, page_dir):
        buf = []
        while i < len(lines) and not self._starts_block(lines, i):
            buf.append(lines[i].strip())
            i += 1
        out.append(f"<p>{self.render_inline(' '.join(buf), page_dir)}</p>")
        return i

    # -- inline level ----------------------------------------------------- #
    def render_inline(self, text, page_dir):
        parts = re.split(r"`", text)
        out = []
        for idx, segment in enumerate(parts):
            if idx % 2 == 1:
                out.append(f"<code>{html.escape(segment)}</code>")
            else:
                out.append(self._render_text(segment, page_dir))
        return "".join(out)

    def _render_text(self, raw, page_dir):
        out = []
        pos = 0
        for match in TOKEN_RE.finditer(raw):
            literal = html.escape(raw[pos:match.start()], quote=False)
            out.append(self._emphasis(literal))
            token = match.group(0)
            if token.startswith("![["):
                out.append(self._embed(token[3:-2], page_dir))
            elif token.startswith("[["):
                out.append(self._wikilink(token[2:-2], page_dir))
            elif token.startswith("!["):
                out.append(self._md_image(token, page_dir))
            else:
                out.append(self._md_link(token, page_dir))
            pos = match.end()
        tail = html.escape(raw[pos:], quote=False)
        out.append(self._emphasis(tail))
        return "".join(out)

    def _wikilink(self, inner, page_dir):
        target = inner
        alias = None
        if "|" in inner:
            target, alias = inner.split("|", 1)
        target = target.strip()
        name = target.split("#", 1)[0].strip()
        label = alias.strip() if alias else target
        note = self.resolve_note(name)
        if note is not None:
            href = html.escape(rel_link(page_dir, note), quote=True)
            return f'<a class="wikilink" href="{href}">{html.escape(label)}</a>'
        return f'<span class="wikilink-missing">{html.escape(label)}</span>'

    def _embed(self, inner, page_dir):
        target = inner
        alias = None
        if "|" in inner:
            target, alias = inner.split("|", 1)
        target = target.strip()
        alias = alias.strip() if alias else None
        name = target.split("#", 1)[0].strip()

        asset = self.resolve_asset(name)
        if asset is not None:
            href = html.escape(rel_link(page_dir, asset), quote=True)
            ext = posixpath.splitext(asset)[1].lower()
            if ext in IMAGE_EXTS:
                if alias and alias.isdigit():
                    alt, width = name, f' width="{html.escape(alias, quote=True)}"'
                else:
                    alt, width = (alias or name), ""
                return (
                    f'<img class="embed" src="{href}" '
                    f'alt="{html.escape(alt, quote=True)}"{width}>'
                )
            label = alias or posixpath.basename(name)
            return (
                f'<a class="embed-file" href="{href}">{html.escape(label)}</a>'
            )

        note = self.resolve_note(name)
        if note is not None:
            href = html.escape(rel_link(page_dir, note), quote=True)
            label = alias or name
            return f'<a class="embed-note" href="{href}">{html.escape(label)}</a>'

        label = alias or name or inner
        return f'<span class="wikilink-missing">{html.escape(label)}</span>'

    def _resolve_url(self, url, page_dir):
        url = url.strip()
        if not url or url.startswith(EXTERNAL_PREFIXES) or url.startswith("#"):
            return url
        clean = url.split("#", 1)[0].split("?", 1)[0]
        base = posixpath.basename(clean)
        asset = self.resolve_asset(base)
        if asset is not None:
            return rel_link(page_dir, asset)
        note = self.resolve_note(base)
        if note is not None:
            return rel_link(page_dir, note)
        return url

    def _md_image(self, token, page_dir):
        m = re.match(r"!\[([^\]]*)\]\(([^)]*)\)", token)
        alt, src = m.group(1), m.group(2)
        href = html.escape(self._resolve_url(src, page_dir), quote=True)
        return f'<img src="{href}" alt="{html.escape(alt, quote=True)}">'

    def _md_link(self, token, page_dir):
        m = re.match(r"\[([^\]]*)\]\(([^)]*)\)", token)
        text, url = m.group(1), m.group(2)
        href = html.escape(self._resolve_url(url, page_dir), quote=True)
        return f'<a href="{href}">{html.escape(text)}</a>'

    @staticmethod
    def _emphasis(text):
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"__(.+?)__", r"<strong>\1</strong>", text)
        text = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", text)
        text = re.sub(
            r"(?<![A-Za-z0-9_])_(?!\s)(.+?)(?<!\s)_(?![A-Za-z0-9_])",
            r"<em>\1</em>",
            text,
        )
        return text


# --------------------------------------------------------------------------- #
# Page / index templates
# --------------------------------------------------------------------------- #
STYLESHEET = """\
:root {
  --bg: #f7f8fb;
  --surface: #ffffff;
  --ink: #101828;
  --muted: #667085;
  --line: #e4e7ec;
  --brand: #4f46e5;
  --brand-600: #4338ca;
  --brand-50: #eef2ff;
  --code-bg: #f2f4f7;
  --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica,
    Arial, sans-serif;
  --mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: var(--font);
  line-height: 1.65;
  -webkit-text-size-adjust: 100%;
}

.site-header {
  background: var(--surface);
  border-bottom: 1px solid var(--line);
}

.site-nav {
  max-width: 860px;
  margin: 0 auto;
  padding: 14px 24px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px 16px;
}

.site-nav .brand {
  font-weight: 700;
  color: var(--brand-600);
  text-decoration: none;
  margin-right: auto;
}

.site-nav a {
  color: var(--muted);
  text-decoration: none;
  font-size: 0.9rem;
}

.site-nav a:hover { color: var(--brand-600); }

.content, .site-footer {
  max-width: 860px;
  margin: 0 auto;
  padding: 32px 24px;
}

.site-footer {
  color: var(--muted);
  font-size: 0.85rem;
  border-top: 1px solid var(--line);
  margin-top: 48px;
}

h1, h2, h3, h4, h5, h6 {
  line-height: 1.3;
  margin: 1.6em 0 0.5em;
  scroll-margin-top: 16px;
}

h1 { font-size: 2rem; }
h2 { font-size: 1.5rem; border-bottom: 1px solid var(--line); padding-bottom: 0.2em; }
h3 { font-size: 1.2rem; }

p, ul, ol, blockquote, table, pre { margin: 0 0 1em; }

a { color: var(--brand-600); }
a:hover { text-decoration: none; }

code {
  font-family: var(--mono);
  font-size: 0.9em;
  background: var(--code-bg);
  padding: 0.1em 0.35em;
  border-radius: 4px;
}

pre {
  background: var(--code-bg);
  padding: 14px 16px;
  border-radius: 8px;
  overflow-x: auto;
}

pre code { background: none; padding: 0; }

blockquote {
  margin-left: 0;
  padding: 0.2em 0 0.2em 1em;
  border-left: 3px solid var(--brand);
  color: var(--muted);
}

blockquote p { margin: 0 0 0.5em; }
blockquote p:last-child { margin-bottom: 0; }

table {
  border-collapse: collapse;
  width: 100%;
  display: block;
  overflow-x: auto;
}

th, td {
  border: 1px solid var(--line);
  padding: 8px 12px;
  text-align: left;
  vertical-align: top;
}

th { background: var(--brand-50); font-weight: 600; }

hr { border: none; border-top: 1px solid var(--line); margin: 2em 0; }

img.embed, img { max-width: 100%; height: auto; border-radius: 8px; }

.meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px 14px;
  margin-bottom: 24px;
  padding: 12px 16px;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 10px;
  font-size: 0.85rem;
}

.meta-item { color: var(--muted); }
.meta-key {
  text-transform: uppercase;
  letter-spacing: 0.04em;
  font-size: 0.7rem;
  color: var(--muted);
  margin-right: 4px;
}

.tags { display: flex; flex-wrap: wrap; gap: 6px; margin-left: auto; }

.tag {
  background: var(--brand-50);
  color: var(--brand-600);
  border-radius: 999px;
  padding: 2px 10px;
  font-size: 0.75rem;
}

.wikilink { text-decoration: none; border-bottom: 1px solid var(--brand); }
.wikilink:hover { border-bottom-style: dashed; }

.wikilink-missing {
  color: #b42318;
  background: #fef3f2;
  border-bottom: 1px dashed #fda29b;
  padding: 0 3px;
  border-radius: 3px;
}

.embed-note, .embed-file { text-decoration: none; border-bottom: 1px solid var(--brand); }

.index-group { margin-bottom: 32px; }
.index-group h2 { margin-top: 1em; }
.note-list { list-style: none; padding: 0; margin: 0; }
.note-list li { padding: 6px 0; border-bottom: 1px solid var(--line); }
.note-list a { text-decoration: none; font-weight: 500; }
.note-list a:hover { text-decoration: underline; }

.proto-list { list-style: none; padding: 0; margin: 0; }
.proto-list li { padding: 6px 0; border-bottom: 1px solid var(--line); }
.proto-list a { text-decoration: none; font-weight: 500; }
"""


def meta_block(meta):
    """Render type/status/updated plus tag chips, or an empty string."""
    items = []
    for key in ("type", "status", "updated"):
        value = meta.get(key)
        if value:
            items.append((key, value if isinstance(value, str) else " ".join(value)))
    tags = meta.get("tags")
    if not isinstance(tags, list):
        tags = []
    if not items and not tags:
        return ""
    parts = ['<div class="meta">']
    for key, value in items:
        parts.append(
            f'<span class="meta-item"><span class="meta-key">{html.escape(key)}'
            f"</span>{html.escape(value)}</span>"
        )
    if tags:
        chips = "".join(f'<span class="tag">{html.escape(t)}</span>' for t in tags)
        parts.append(f'<span class="tags">{chips}</span>')
    parts.append("</div>")
    return "\n".join(parts)


def build_page(title, meta, body_html, page_dir, top_folders):
    """Wrap rendered body HTML in the full page shell with nav + stylesheet."""
    css = html.escape(rel_link(page_dir, "assets/site.css"), quote=True)
    home = html.escape(rel_link(page_dir, "index.html"), quote=True)
    index_rel = rel_link(page_dir, "index.html")
    links = [f'<a href="{home}">Home</a>']
    for folder in top_folders:
        anchor = html.escape(f"{index_rel}#folder-{slugify(folder)}", quote=True)
        links.append(f'<a href="{anchor}">{html.escape(folder)}</a>')
    nav = "\n      ".join(links)
    meta_html = meta_block(meta)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)} · {SITE_TITLE}</title>
  <link rel="stylesheet" href="{css}">
</head>
<body>
  <header class="site-header">
    <nav class="site-nav">
      <a class="brand" href="{home}">{SITE_TITLE}</a>
      {nav}
    </nav>
  </header>
  <main class="content">
    <h1>{html.escape(title)}</h1>
{meta_html}
{body_html}
  </main>
  <footer class="site-footer">
    Built with the Python standard library · Deployed to GitHub Pages
  </footer>
</body>
</html>
"""


def build_index(entries, prototypes, page_dir=""):
    """Render the landing page: notes grouped by folder + live prototypes."""
    groups = {}
    for entry in entries:
        groups.setdefault(entry["folder"], []).append(entry)

    ordered = sorted(groups.items(), key=lambda kv: (kv[0] != "", kv[0].lower()))
    sections = []
    for folder, items in ordered:
        heading = folder or "Vault root"
        anchor = f'folder-{slugify(folder or "root")}'
        rows = "\n".join(
            f'        <li><a href="{html.escape(rel_link(page_dir, it["href"]), quote=True)}">'
            f'{html.escape(it["title"])}</a></li>'
            for it in items
        )
        sections.append(
            f'    <section class="index-group" id="{anchor}">\n'
            f"      <h2>{html.escape(heading)}</h2>\n"
            f'      <ul class="note-list">\n{rows}\n      </ul>\n'
            f"    </section>"
        )

    if prototypes:
        proto_rows = "\n".join(
            f'        <li><a href="{html.escape(rel_link(page_dir, p), quote=True)}">'
            f"{html.escape(p)}</a></li>"
            for p in prototypes
        )
        proto_section = (
            '    <section class="index-group" id="live-prototypes">\n'
            "      <h2>Live prototypes</h2>\n"
            '      <ul class="proto-list">\n'
            f"{proto_rows}\n"
            "      </ul>\n"
            "    </section>"
        )
    else:
        proto_section = ""

    css = html.escape(rel_link(page_dir, "assets/site.css"), quote=True)
    note_count = len(entries)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{SITE_TITLE}</title>
  <link rel="stylesheet" href="{css}">
</head>
<body>
  <header class="site-header">
    <nav class="site-nav">
      <a class="brand" href="index.html">{SITE_TITLE}</a>
    </nav>
  </header>
  <main class="content">
    <h1>{SITE_TITLE}</h1>
    <p>A published view of the vault — {note_count} note(s) and the runnable prototypes.</p>
    <section class="index-group" id="notes">
      <h2>Notes</h2>
    </section>
{chr(10).join(sections)}
{proto_section}
  </main>
  <footer class="site-footer">
    Built with the Python standard library · Deployed to GitHub Pages
  </footer>
</body>
</html>
"""


def find_prototypes(assets):
    """Detect runnable standalone apps among the copied files."""
    found = set()
    for rel in assets:
        if not rel.lower().endswith(".html"):
            continue
        parts = rel.split("/")
        base = parts[-1]
        if base == "index.html" and "prototype" in parts:
            found.add(rel)
        elif len(parts) in (1, 2):
            found.add(rel)
    return sorted(found)


def plan_asset_outputs(assets, note_outputs):
    """Map every asset to the output path it is copied to.

    A rendered note page and a verbatim asset can collide: "Peers App.md"
    renders to "Peers App.html", which is also the name of a standalone
    prototype in the vault. The note wins its natural path (see the task's
    build spec); the colliding asset is copied under a de-duplicated
    "(standalone)" name so nothing is lost and both remain reachable.
    """
    taken = set(note_outputs)
    mapping = {}
    for rel in assets:
        final = rel
        if final in taken:
            stem, ext = posixpath.splitext(rel)
            final = f"{stem} (standalone){ext}"
            counter = 2
            while final in taken:
                final = f"{stem} (standalone {counter}){ext}"
                counter += 1
        mapping[rel] = final
        taken.add(final)
    return mapping


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #
def main():
    root = Path.cwd()
    out_dir = root / OUT_DIR_NAME

    notes, assets = collect_files(root)
    print(f"Vault root: {root}")
    print(f"Found {len(notes)} note(s) and {len(assets)} asset(s)")
    print()

    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Created clean output directory: {out_dir}")
    print()

    note_index = {}
    for rel in notes:
        stem = posixpath.splitext(posixpath.basename(rel))[0]
        note_index.setdefault(stem.lower(), md_to_html(rel))
    note_outputs = {md_to_html(rel) for rel in notes}
    asset_outputs = plan_asset_outputs(assets, note_outputs)

    asset_index = {}
    for rel in assets:
        asset_index.setdefault(
            posixpath.basename(rel).lower(), asset_outputs[rel]
        )

    renderer = Renderer(note_index, asset_index)

    top_folders = sorted(
        {posixpath.dirname(rel).split("/")[0] for rel in notes if "/" in rel},
        key=str.lower,
    )

    print(f"Rendering {len(notes)} note page(s):")
    entries = []
    for rel in notes:
        src = root.joinpath(*rel.split("/"))
        text = src.read_text(encoding="utf-8", errors="replace")
        frontmatter, body = split_frontmatter(text)
        meta = parse_frontmatter(frontmatter)
        title = meta.get("title") or posixpath.splitext(
            posixpath.basename(rel)
        )[0]
        page_dir = posixpath.dirname(rel)
        body_html = renderer.render(body, page_dir)
        page = build_page(title, meta, body_html, page_dir, top_folders)
        html_rel = md_to_html(rel)
        dest = out_dir.joinpath(*html_rel.split("/"))
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page, encoding="utf-8")
        entries.append(
            {
                "href": html_rel,
                "title": title,
                "folder": page_dir.split("/")[0] if "/" in rel else "",
            }
        )
    print()

    print(f"Copying {len(assets)} asset(s) verbatim:")
    for rel in assets:
        final = asset_outputs[rel]
        if final != rel:
            print(f"  [renamed] {rel} -> {final} (collides with a note page)")
        src = root.joinpath(*rel.split("/"))
        dest = out_dir.joinpath(*final.split("/"))
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    print()

    css_path = out_dir / "assets" / "site.css"
    css_path.parent.mkdir(parents=True, exist_ok=True)
    css_path.write_text(STYLESHEET, encoding="utf-8")
    print(f"Wrote {css_path.relative_to(out_dir).as_posix()}")

    (out_dir / ".nojekyll").write_text("", encoding="utf-8")
    print("Wrote .nojekyll")

    prototypes = find_prototypes(list(asset_outputs.values()))
    index_html = build_index(entries, prototypes)
    (out_dir / "index.html").write_text(index_html, encoding="utf-8")
    print(f"Wrote index.html ({len(prototypes)} prototype link(s))")
    print()

    print("Build complete!")
    print(f"  note pages : {len(entries)}")
    print(f"  assets     : {len(assets)}")
    print(f"  index      : yes")
    print(f"Output: {out_dir}")


if __name__ == "__main__":
    main()
