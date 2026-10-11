---
name: presentation-pro
description: "Expert en création de présentations et de Pitch Decks. CRITICAL: ALWAYS use this skill when asked to create a presentation, a slide deck, a PowerPoint, or a Pitch. Generates BOTH highly visual, animated native .pptx files AND interactive 3D Web presentations."
---

# Presentation Pro - Architecte de Présentations Haut de Gamme

## Objectif
Créer des présentations de niveau "Agence de Design à 150k$" et des Pitchs persuasifs (basés sur la psychologie cognitive). 
Tu dois systématiquement générer **DEUX** formats lors de la création :
1. Un fichier **`.pptx` (Microsoft PowerPoint)** natif avec des transitions.
2. Un fichier **`.html` (Web Présentation)** avec des animations 3D complexes.

---

## 1. Moteur de Données Local (Data Engine)
Ton dossier `.agent/skills/presentation-pro/` contient des données indispensables. **Tu dois toujours les consulter** avant de générer une présentation :
- **`data/design-tokens.json`** : Contient les règles mathématiques exactes pour les polices (Eyebrow, Action Title, Big Metric), les couleurs et les grilles.
- **`data/layout-matrix.yaml`** : La bible des mises en page (McKinsey). Utilise ces structures pour éviter les designs aléatoires.
- **`references/`** : Contient de multiples manuels (`color-palette.md`, `layouts.md`, `rules.md`, et les dossiers `charts/`, `playbooks/`) sur les règles de dataviz du Financial Times et les frameworks de pitch.

## 2. La Psychologie de la Persuasion (Storytelling)
Applique l'arc narratif du **Strategic Narrative (Andy Raskin)** :
- **The Shift** : Nommer le changement tectonique incontestable dans le monde du client.
- **Winners & Losers** : Montrer ceux qui survivent au changement vs ceux qui meurent.
- **The Promised Land** : Dessiner le futur idéal (sans parler du produit).
- **Magic Gifts** : Présenter les capacités clés (le produit) nécessaires pour atteindre ce futur.
- **Evidence** : Preuves chiffrées (utilisation obligatoire de la règle du "So What?" dans les titres).

## 3. Le Livrable PowerPoint (`.pptx` Impressionnant)
Même si le format PPTX est statique de nature, tu dois appliquer les règles du **Design d'Agence Haute Couture** (définies dans tes `design-tokens.json`) :
- **Luxe et Respiration** : Laisse des espaces blancs (whitespace) massifs.
- **Zéro Ombre Baveuse** : Interdiction d'utiliser des ombres portées noires par défaut.
- **Data-Ink Ratio (Tufte)** : 90% d'un graphique doit être gris. Seule la donnée vitale est colorée avec la couleur d'accentuation (Accent Color).
- **Transitions XML** : Modifie le XML (`ppt/slides/slideX.xml`) avec les scripts fournis pour injecter des transitions natives (`<p:fade/>`, `<p:push/>`).

## 4. Outils Techniques et Linters de Qualité (Local Scripts)
Tu disposes d'un arsenal d'outils dans ton dossier `scripts/` pour garantir la perfection. **Tu dois valider ton travail avec ces outils :**

### A. Génération et Modification
- `scripts/html2pptx.js` : Convertit des designs HTML complexes en vrai fichier PPTX.
- `scripts/generate_icons.py` : Injecte des icônes ultra-fines (Phosphor Light).
- `ooxml/scripts/unpack.py` et `pack.py` : Pour dépaqueter le `.pptx` et injecter des transitions dans les fichiers XML.

### B. Validation Qualité (QA & Linting)
- **`scripts/inspect_pptx.py`** : *OBLIGATOIRE*. Lance ce linter sur le fichier PowerPoint généré. Il vérifiera le respect des contrastes, les tailles de police minimales et les chevauchements. Corrige les erreurs qu'il signale avant de livrer.
- **`scripts/visual_qa.py`** et **`scripts/thumbnail.py`** : Pour valider visuellement le rendu final.

---
## Processus d'Exécution Strict
1. **Initialisation** : Lis `data/design-tokens.json` et `data/layout-matrix.yaml`.
2. **Narration** : Applique le Strategic Narrative d'Andy Raskin.
3. **Création PPTX** : Exécute tes scripts Python pour générer le PowerPoint.
4. **Validation QA** : Lance OBLIGATOIREMENT `python scripts/inspect_pptx.py` sur ton fichier généré. Si le linter échoue, modifie ton code PPTX.
5. **Création Web 3D** : Génère `presentation_show.html` avec Tilt 3D et IntersectionObserver.
6. **Livraison** : Fournis les deux fichiers à l'utilisateur.
