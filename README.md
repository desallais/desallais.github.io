# desallais.github.io

Source of the bilingual (EN/FR) personal site of Mario Desallais, built with
[Quarto](https://quarto.org) and published to GitHub Pages on every push to
`main`.

```bash
quarto preview --profile en    # English site
quarto preview --profile fr    # French site
./build.sh serve               # both, merged, on http://localhost:4000
```

English pages live at the repository root, French ones under `fr/` with the
same file names. `refs.bib` is the single source for the publication list and
`assets/cv.pdf` for the downloadable CV.

See [CLAUDE.md](CLAUDE.md) for the working rules and the list of provisional
content still to be replaced.
