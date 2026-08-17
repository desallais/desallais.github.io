# Site web — règles de travail

Site personnel bilingue (EN/FR) de Mario Desallais, écologie théorique.
Quarto statique, déployé automatiquement sur GitHub Pages à chaque push sur
`main` (dépôt `desallais/desallais.github.io`, en ligne sur
<https://desallais.github.io>).

## Règles permanentes

1. **Parité bilingue stricte.** Toute modification d'une page EN est
   répercutée sur sa jumelle FR dans la même session, et réciproquement.
   Une session ne se termine jamais avec un écart EN/FR.
2. **Sources uniques.** `refs.bib` (publications) et `assets/cv.pdf` (CV
   téléchargeable) sont les seules sources de ces contenus. Jamais de
   duplication : pas de liste de publications écrite à la main, pas de second
   PDF.
3. **Petites itérations.** Un commit par changement cohérent, message clair.
4. **`noindex` tant que le contenu est provisoire.** La balise vit dans
   `assets/head.html` et s'applique à toutes les pages ; `robots.txt`
   interdit l'indexation du site entier.
   **À faire au début de chaque session : rappeler à Mario que le site est
   toujours en `noindex`**, et lui demander si le moment est venu de le
   retirer (voir « Passer le site en public » plus bas).

## Structure

| Rôle | EN (racine) | FR (`fr/`) |
|---|---|---|
| Accueil | `index.qmd` | `fr/index.qmd` |
| Recherche | `research.qmd` | `fr/research.qmd` |
| Publications | `publications.qmd` | `fr/publications.qmd` |
| CV | `cv.qmd` | `fr/cv.qmd` |
| Au-delà | `beyond.qmd` | `fr/beyond.qmd` |

Les **noms de fichiers sont identiques** dans les deux langues : c'est ce qui
permet au sélecteur EN|FR de pointer vers la page équivalente (`/x.html` ↔
`/fr/x.html`). Ne jamais renommer une page d'un seul côté.

Les **identifiants de sections sont en anglais des deux côtés**
(`#coexistence`, `#bef`, `#food-webs`, `#positions`, `#influences`,
`#asides`), pour que les ancres se correspondent d'une langue à l'autre.

Autres fichiers :

- `_quarto.yml` — configuration commune (thème, pied de page/contact, math,
  `noindex`, script de pré-rendu).
- `_quarto-en.yml` / `_quarto-fr.yml` — un profil de rendu par langue : liste
  des pages, barre de navigation traduite, `lang`.
- `assets/styles.scss` — thème (une seule couleur d'accent : `$accent`).
- `assets/head.html` — balise `noindex`.
- `assets/lang-switch.html` — script du sélecteur de langue.
- `assets/img/` — portrait et figures (placeholders SVG pour l'instant).
- `scripts/gen_publications.py` — construit `_publications.md` depuis
  `refs.bib` (lancé automatiquement avant chaque rendu ; fichier généré,
  non versionné).
- `scripts/make_placeholders.py` — régénère les placeholders (images, CV).
- `build.sh` — construit les deux langues et les fusionne dans `_site/`.

## Commandes

```bash
quarto preview --profile en     # aperçu anglais (rechargement à chaud)
quarto preview --profile fr     # aperçu français
./build.sh                      # site complet fusionné dans _site/
./build.sh serve                # idem + serveur sur http://localhost:4000
```

Le `preview` d'une seule langue suffit pour travailler le contenu ; il faut
`./build.sh serve` pour tester le sélecteur EN|FR et les liens entre langues,
qui ont besoin des deux sites côte à côte.

## Pourquoi des profils de rendu

Quarto n'autorise qu'une seule barre de navigation par projet : impossible
d'avoir « Home / Research / … » à la racine et « Accueil / Recherche / … »
sous `/fr/` avec un projet unique. Les profils de rendu (`--profile en|fr`)
sont la solution prévue par Quarto pour le multilingue : `_quarto.yml` porte
tout ce qui est commun, chaque profil ne redéfinit que sa langue, sa liste de
pages et sa navigation. Aucune duplication de configuration, et un contenu
partagé (`refs.bib`, `assets/`) pour les deux sites.

Deux pièges rencontrés, à ne pas réintroduire :

- Rendre un profil **supprime** les fichiers de sortie que ce profil ne liste
  pas. Les deux langues ne peuvent donc pas écrire dans le même
  `output-dir` : FR sort dans `_site-fr/`, puis `build.sh` le fusionne dans
  `_site/fr/`.
- Dans `_quarto-fr.yml`, `lang: fr` serait interprété comme un chemin (le
  dossier `fr/` existe) et produirait `lang="../fr"`. D'où `lang: fr-FR`.

## Contenu provisoire à remplacer

Tous les corps de texte sont du lorem ipsum, à remplacer bloc par bloc : un
bloc de lorem = un endroit unique dans un fichier `.qmd` (× 2 pour la parité
EN/FR). Restent aussi à remplacer :

- `_quarto.yml` : ORCID (`0000-0000-0000-0000`), Google Scholar
  (`REPLACE_ME`), et l'adresse e-mail (actuellement l'adresse personnelle —
  à remplacer par l'adresse institutionnelle si besoin).
- `index.qmd` / `fr/index.qmd` : ligne d'affiliation.
- `cv.qmd` / `fr/cv.qmd` : toutes les entrées (dates en `20XX`, intitulés
  « provisoire »).
- `assets/img/portrait.svg` — remplacer par un vrai portrait (600 × 750).
- `assets/img/coexistence.svg`, `bef.svg`, `food-webs.svg` — une figure par
  axe (1200 × 675).
- `assets/cv.pdf` — le vrai CV.
- L'équation de Lotka-Volterra dans `research.qmd` / `fr/research.qmd` est un
  exemple destiné à garder le rendu mathématique visible ; à remplacer ou
  supprimer avec le texte définitif.

Remplacer une image ou le CV = écraser le fichier au même chemin ; aucun
`.qmd` à modifier.

## Passer le site en public

Quand le contenu provisoire aura disparu :

1. supprimer la balise dans `assets/head.html` (garder le fichier vide ou
   retirer `include-in-header` de `_quarto.yml`) ;
2. remplacer `robots.txt` par un `Allow` (ou le supprimer et le retirer des
   `resources`) ;
3. supprimer `scripts/make_placeholders.py` et cette section.
