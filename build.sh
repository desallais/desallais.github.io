#!/usr/bin/env bash
# Build the complete bilingual site into _site/.
#
#   ./build.sh          build both languages
#   ./build.sh serve    build, then serve the merged site on http://localhost:4000
#
# Rendering a Quarto profile prunes output files the profile does not list, so
# the two languages are rendered into separate directories and merged here:
#   profile en -> _site      (English pages at the root)
#   profile fr -> _site-fr   (French pages under fr/)
# For editing a single language, `quarto preview --profile en|fr` is faster;
# use this script when the language switcher or cross-language links matter.

set -euo pipefail
cd "$(dirname "$0")"

quarto render --profile en
quarto render --profile fr

rsync -a --delete _site-fr/fr/ _site/fr/
rsync -a _site-fr/site_libs/ _site/site_libs/

# Each render writes a sitemap for its own language only; splice them together.
python3 - <<'PY'
import pathlib, re
en, fr = pathlib.Path("_site/sitemap.xml"), pathlib.Path("_site-fr/sitemap.xml")
if en.exists() and fr.exists():
    urls = re.findall(r"\s*<url>.*?</url>", fr.read_text(encoding="utf-8"), re.S)
    en.write_text(
        en.read_text(encoding="utf-8").replace("</urlset>", "".join(urls) + "\n</urlset>"),
        encoding="utf-8",
    )
PY

echo "Merged bilingual site in _site/"

if [[ "${1:-}" == "serve" ]]; then
  echo "Serving http://localhost:4000 (Ctrl-C to stop)"
  python3 -m http.server 4000 --directory _site
fi
