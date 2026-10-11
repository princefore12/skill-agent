---
name: word-pro-max
description: "Expert en conception, rédaction et design de documents Microsoft Word professionnels (.docx). CRITICAL: ALWAYS use this skill when asked to create a report, a proposal, a memo, a contract, or any Word document."
---

# Word Pro Max - Architecte de Documents Word Haut de Gamme

## Objectif
Éradiquer les documents Word génériques ("Word Slop") et produire des rapports, propositions commerciales et mémos de niveau "Cabinet de Conseil / Agence de Design".

## 1. Moteur de Données Local (Data Engine)
Ton dossier `.agent/skills/word-pro-max/` contient les données indispensables. **Tu dois toujours les consulter** :
- **`data/design-tokens.json`** : Règles strictes pour la typographie, les tailles de police, les marges (en DXA) et la palette de couleurs.
- **`references/frameworks.md`** : Les 4 frameworks de rédaction que tu dois utiliser (Shipley, Amazon 6-pager, Minto SCQA, et Copywriting Psychologist).

## 2. Le Workflow de Rédaction (Les 4 Frameworks)
Avant d'écrire le document, choisis le framework approprié :
1. **Proposition Commerciale** -> Applique **Shipley** + **Copywriting Psychologist**. (Focus client, Hot Buttons, Bénéfice avant Feature).
2. **Mémo Exécutif / Stratégie** -> Applique **Amazon 6-pager**. (Ultra dense, State of the Business, Pas de superflu).
3. **Audit / Rapport de Recherche** -> Applique **Minto (SCQA)**. (BLUF : Conclusion au début. Titres d'Action obligatoires).

## 3. Règles d'Ingénierie Visuelle (L'Anti-Slop)
Lors de la génération du fichier `.docx` (via `python-docx`), tu dois **obligatoirement** respecter ces règles :
- **Interlignage et Rythme** : Interdiction absolue d'utiliser `\n\n` pour séparer des paragraphes. Utilise toujours `space_after = Pt(6)`.
- **Contrôle des Orphelines** : Tous les titres (Heading 1, 2, 3) doivent avoir `keep_with_next = True` pour ne pas se retrouver seuls en bas de page.
- **Marges** : Utilise des marges généreuses (3.0 cm) pour limiter la longueur des lignes à 65-75 caractères.

## 4. Les Outils Python (Local Scripts)
Dans ton dossier `scripts/`, tu trouveras `docx_builder.py` qui contient des fonctions magiques OXML que tu **dois** importer et utiliser pour styliser le document :
- **`apply_callout_style(cell)`** : Crée un tableau à une cellule et applique cette fonction pour créer un magnifique encadré de citation (Bordure colorée gauche épaisse, fond léger, padding).
- **`create_tufte_table(table)`** : Applique cette fonction sur tous tes tableaux. Elle supprime les bordures verticales oppressantes et ajoute un padding parfait.
- **`create_kpi_block(doc, metrics)`** : Génère un bloc de Mégachiffres alignés (sans bordure) pour tes Executive Summaries.

## 5. Édition et Suivi des Modifications (Redlining OXML)
Si l'utilisateur te demande de modifier un fichier `.docx` existant (correction, relecture, révision de contrat), **n'utilise pas `python-docx`**. Utilise le flux d'ingénierie inversée via `ooxml` :
1. Dépaquette le fichier : `python ooxml/scripts/unpack.py <fichier.docx> <dossier_sortie>`
2. Modifie directement le XML dépaqueté (dans `word/document.xml`) via un script Python. **Utilise les balises `<w:del>` et `<w:ins>` pour générer un vrai suivi des modifications (Tracked Changes)** comme un vrai avocat !
3. Rempaquette le fichier : `python ooxml/scripts/pack.py <dossier_sortie> <fichier_corrigé.docx>`

## Processus d'Exécution
1. Identifie l'intention du document (Vente, Décision, Audit).
2. Lis `references/frameworks.md` pour adopter la bonne structure mentale.
3. Crée un script Python qui importe `docx` et les fonctions de `scripts/docx_builder.py` (ou utilise le flux de Redlining OXML si c'est une modification).
4. Génère un document ultra-stylisé avec couverture asymétrique, titres d'action (SCQA), tableaux Tufte et encadrés Callout.
5. Sauvegarde en `.docx` et fournis-le à l'utilisateur.
