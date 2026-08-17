#!/usr/bin/env python3
"""Build the publication list from refs.bib.

refs.bib is the single source of truth (CLAUDE.md, rule 2). This script is run
by Quarto before every render (`pre-render` in _quarto.yml) and writes
`_publications.md`, a language-neutral HTML fragment included by both
publications.qmd and fr/publications.qmd. The generated file is not committed.

    python3 scripts/gen_publications.py
"""

from __future__ import annotations

import html
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIB = ROOT / "refs.bib"
OUT = ROOT / "_publications.md"

# Author name highlighted in the list.
ME = ("Desallais", "Mario")

LATEX = {
    r"\&": "&", r"\%": "%", r"\_": "_", r"\#": "#", r"\$": "$",
    r"\textendash{}": "–", r"--": "–", r"\ldots": "…",
    r"\'e": "é", r"\`e": "è", r"\^e": "ê", r"\"e": "ë",
    r"\'a": "á", r"\`a": "à", r"\^a": "â",
    r"\'o": "ó", r"\^o": "ô", r"\"o": "ö",
    r"\'i": "í", r"\^i": "î", r"\"i": "ï",
    r"\'u": "ú", r"\`u": "ù", r"\^u": "û", r"\"u": "ü",
    r"\c c": "ç", r"\~n": "ñ",
}


def clean(value: str) -> str:
    """Turn a raw BibTeX field into plain text."""
    text = " ".join(value.split())
    for src, dst in LATEX.items():
        text = text.replace(src, dst)
    text = re.sub(r"\\[a-zA-Z]+\{([^{}]*)\}", r"\1", text)  # \emph{x} -> x
    text = text.replace("{", "").replace("}", "")
    return unicodedata.normalize("NFC", text).strip()


def parse_bib(path: Path) -> list[dict]:
    """Minimal BibTeX reader: entry type, key and brace/quote-delimited fields."""
    raw = path.read_text(encoding="utf-8")
    entries = []
    for match in re.finditer(r"@(\w+)\s*\{", raw):
        kind = match.group(1).lower()
        if kind in ("comment", "preamble", "string"):
            continue
        start = match.end()
        depth, i = 1, start
        while i < len(raw) and depth:
            depth += {"{": 1, "}": -1}.get(raw[i], 0)
            i += 1
        body = raw[start : i - 1]

        key, _, rest = body.partition(",")
        entry = {"type": kind, "key": key.strip()}
        pos = 0
        while pos < len(rest):
            fm = re.compile(r"\s*([a-zA-Z][\w-]*)\s*=\s*").match(rest, pos)
            if not fm:
                break
            pos = fm.end()
            if rest[pos] in "{\"":
                opener = rest[pos]
                closer = "}" if opener == "{" else '"'
                depth, j = 1, pos + 1
                while j < len(rest) and depth:
                    if opener == "{":
                        depth += {"{": 1, "}": -1}.get(rest[j], 0)
                    elif rest[j] == closer:
                        depth = 0
                    j += 1
                value, pos = rest[pos + 1 : j - 1], j
            else:  # bare value (a number, typically)
                j = rest.find(",", pos)
                j = len(rest) if j == -1 else j
                value, pos = rest[pos:j], j
            entry[fm.group(1).lower()] = value
            pos = rest.find(",", pos) + 1 or len(rest)
        entries.append(entry)
    return entries


def format_authors(field: str) -> str:
    """'Doe, Jane and Roe, R.' -> 'J. Doe & R. Roe', with my name in bold."""
    people = []
    for raw in re.split(r"\s+and\s+", clean(field)):
        raw = raw.strip()
        if not raw:
            continue
        if "," in raw:
            last, first = (part.strip() for part in raw.split(",", 1))
        else:
            bits = raw.split()
            last, first = bits[-1], " ".join(bits[:-1])
        initials = " ".join(
            f"{part[0]}." for part in re.split(r"[\s-]+", first) if part
        ).replace(". ", ".-" if "-" in first else ". ")
        name = f"{initials} {last}".strip()
        name = html.escape(name)
        if last == ME[0] and first.startswith(ME[1][0]):
            name = f"<strong>{name}</strong>"
        people.append(name)
    if len(people) > 1:
        return ", ".join(people[:-1]) + " &amp; " + people[-1]
    return people[0] if people else ""


def venue(entry: dict) -> str:
    for field in ("journal", "journaltitle", "booktitle", "publisher", "howpublished"):
        if entry.get(field):
            return clean(entry[field])
    return ""


def doi_of(entry: dict) -> str:
    doi = clean(entry.get("doi", ""))
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi)
    return doi


def render_entry(entry: dict) -> str:
    parts = [format_authors(entry.get("author", "")), f"({clean(entry.get('year', 'n.d.'))})."]
    title = html.escape(clean(entry.get("title", "Untitled")))
    parts.append(f"{title}.")

    where = html.escape(venue(entry))
    if where:
        detail = ""
        if entry.get("volume"):
            detail = f" {html.escape(clean(entry['volume']))}"
            if entry.get("number"):
                detail += f"({html.escape(clean(entry['number']))})"
        if entry.get("pages"):
            detail += f", {html.escape(clean(entry['pages']))}"
        parts.append(f'<span class="pub-venue">{where}</span>{detail}.')

    doi = doi_of(entry)
    if doi:
        url = f"https://doi.org/{doi}"
        parts.append(
            f'<span class="pub-doi"><a href="{html.escape(url)}">doi:{html.escape(doi)}</a></span>'
        )
    elif entry.get("url"):
        url = html.escape(clean(entry["url"]))
        parts.append(f'<span class="pub-doi"><a href="{url}">link</a></span>')

    return "  <li>" + " ".join(p for p in parts if p) + "</li>"


def main() -> None:
    entries = parse_bib(BIB)
    if not entries:
        raise SystemExit(f"no entries parsed from {BIB}")

    def sort_key(e: dict):
        year = clean(e.get("year", "0"))
        year = int(re.sub(r"\D", "", year) or 0)
        return (-year, clean(e.get("author", "")).lower(), clean(e.get("title", "")).lower())

    entries.sort(key=sort_key)

    lines = ["<!-- Generated by scripts/gen_publications.py from refs.bib. Do not edit. -->", ""]
    current_year = None
    for entry in entries:
        year = clean(entry.get("year", "")) or "In preparation"
        if year != current_year:
            if current_year is not None:
                lines += ["</ul>", ""]
            current_year = year
            lines += [f'<h2 class="pub-year">{html.escape(year)}</h2>', '<ul class="pub-list">']
        lines.append(render_entry(entry))
    lines += ["</ul>", ""]

    text = "\n".join(lines)
    if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
        OUT.write_text(text, encoding="utf-8")
        print(f"gen_publications: wrote {OUT.name} ({len(entries)} entries)")
    else:
        print(f"gen_publications: {OUT.name} up to date ({len(entries)} entries)")


if __name__ == "__main__":
    main()
