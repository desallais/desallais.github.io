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
3. **Anglais britannique** pour tout le texte anglais du site
   (*organisation*, *favour*, *behaviour*, *-ise* plutôt que *-ize*), sauf
   dans les noms propres, les titres d'articles cités et les termes
   techniques consacrés. Le français suit la typographie française
   (espaces insécables avant `: ; ? !`, guillemets « … »).
4. **Petites itérations.** Un commit par changement cohérent, message clair.
5. **`noindex` tant que le contenu est provisoire.** La balise vit dans
   `assets/head.html` et s'applique à toutes les pages ; `robots.txt`
   interdit l'indexation du site entier.
   **À faire au début de chaque session : rappeler à Mario que le site est
   toujours en `noindex`**, et lui demander si le moment est venu de le
   retirer (voir « Passer le site en public » plus bas).
6. **Hygiène du bloc Actualités.** L'accueil (`index.qmd`, `fr/index.qmd`)
   ne porte jamais plus de **quatre** entrées, en ordre chronologique
   inverse (la plus récente en haut). Toute entrée de plus de douze mois est
   retirée : ajouter une actualité, c'est aussi vérifier si la plus ancienne
   doit sortir. Les deux langues restent alignées entrée pour entrée.

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

Les **identifiants de sections sont en anglais des deux côtés**, dérivés des
titres anglais : `#current-position`, `#education`, `#teaching`,
`#conference-presentations` (CV) ; `#current-projects`, `#news`
(Accueil). C'est ce qui fait que les ancres se correspondent d'une langue à
l'autre. Renommer une section = mettre à jour l'id des deux côtés **et**
tout lien qui la vise. La page Au-delà n'a plus de titres de section depuis
la session du 22 août 2026 : les deux citations en tiennent lieu.

Autres fichiers :

- `_quarto.yml` — configuration commune (thème, pied de page/contact, math,
  `noindex`, script de pré-rendu).
- `_quarto-en.yml` / `_quarto-fr.yml` — un profil de rendu par langue : liste
  des pages, barre de navigation traduite, `lang`.
- `assets/styles.scss` — thème et palette (voir ci-dessous).
- `assets/head.html` — balise `noindex`.
- `assets/lang-switch.html` — script du sélecteur de langue.
- `assets/portrait.jpg` — portrait de l'accueil (600 × 600), recadré depuis
  la photo brute par `figures/crop_portrait.py`.
- `scripts/gen_publications.py` — construit `_publications.md` depuis
  `refs.bib` (fichier généré, non versionné). Après un clone neuf, le lancer
  une fois (ou lancer `./build.sh`) avant le premier `quarto preview` :
  Quarto résout les `{{< include >}}` avant d'exécuter ses scripts de
  pré-rendu.
- `scripts/make_placeholders.py` — vestige : il régénérait les images et le
  CV placeholders, tous retirés depuis. À supprimer.
- `figures/crop_portrait.py` — recadre le portrait de l'accueil depuis la
  photo d'appareil (source non versionnée ; bornes commentées dans le
  script). Relancer seulement si la source ou le cadrage changent.
- `build.sh` — construit les deux langues et les fusionne dans `_site/`.

## Palette

Trois teintes, définies en tête de `assets/styles.scss` et **nulle part
ailleurs** — pas de couleur écrite en dur dans un `.qmd` ou ailleurs dans le
SCSS :

| Variable | Valeur | Contraste sur blanc | Emploi |
|---|---|---|---|
| `$slate` | `#2a5d78` | 7,15:1 (AAA) | accent dominant : liens, titres, navigation, repli de l'en-tête photo |
| `$forest` | `#4f6b52` | 5,90:1 (AA) | accent secondaire, discret : filet des encadrés « prises de position », survol des liens |
| `$stone` | `#b8a678` | 2,40:1 | **accents fins seulement** : filets (`$border-color`), puces, séparateurs. Jamais de texte |

Le slate reste dominant : le forest et le stone ne servent qu'à réchauffer.
`$accent` est un alias de `$slate`, conservé pour les règles déjà écrites.
Toute nouvelle couleur passe par une de ces trois variables ; si une
quatrième teinte semble nécessaire, c'est le signe qu'il faut en discuter
plutôt que de l'ajouter.

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

## État du contenu

Toutes les pages portent le texte définitif de Mario (sessions du 18 au
22 août 2026) ; ne pas le reformuler, il le retravaillera lui-même. Plus une
ligne de lorem ipsum ni une image provisoire sur le site.

Deux pages sont volontairement incomplètes, Mario écrira la suite lui-même :

- **Recherche** — l'introduction et l'aquarelle de Sargent seulement ; les
  trois sections (architecture, mathématiques, biodiversité-climat) et leurs
  figures ont été retirées le 22 août 2026, de nouvelles sections viendront.
- **Au-delà** — les deux encadrés « prises de position » seulement ; les
  sections Influences et À côté viendront plus tard.

Deux points de vigilance :

- L'adresse e-mail est encore l'adresse personnelle — à remplacer par
  l'institutionnelle si besoin. Les quatre liens de contact (e-mail, ORCID,
  Google Scholar, GitHub) vivent à **deux** endroits, le pied de page
  (`_quarto.yml`) et la rangée de contact de l'accueil (`index.qmd`,
  `fr/index.qmd`) ; toute correction se fait aux deux, sinon les deux rangées
  divergent.
- `assets/cv.pdf` est un placeholder qu'**aucune page ne lie** ; sujet mis de
  côté par Mario. Le fichier reste copié dans le site par les `resources` de
  `_quarto.yml`.

## Passer le site en public

Il n'y a plus de contenu provisoire : le site n'attend que le feu vert de
Mario. Le jour où il le donne :

1. supprimer la balise dans `assets/head.html` (garder le fichier vide ou
   retirer `include-in-header` de `_quarto.yml`) ;
2. remplacer `robots.txt` par un `Allow` (ou le supprimer et le retirer des
   `resources`) ;
3. supprimer `scripts/make_placeholders.py` et cette section.
