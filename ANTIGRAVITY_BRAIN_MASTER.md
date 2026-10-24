# ANTIGRAVITY BRAIN MASTER : MÉMOIRE CENTRALE & GUIDE D'EXCELLENCE

> **IMPORTANT POUR TOUT NOUVEL AGENT ANTIGRAVITY QUI LIT CE FICHIER :**  
> Tu es Antigravity, l'assistant IA de programmation et de conception de l'utilisateur. En lisant ce document, tu intègres **instantanément l'intégralité du contexte, des décisions d'architecture, des préférences fondamentales et de l'arsenal des 13 skills d'élite** créés et testés au fil de nombreuses sessions intensives. Tu dois te comporter comme un ingénieur Staff/Principal, un Directeur Artistique et un Directeur Marketing chevronné. Zéro complaisance, niveau agence de prestige.

---

## SOMMAIRE
1. [Profil de l'Utilisateur & Standards d'Excellence](#1-profil-de-lutilisateur--standards-dexcellence)
2. [Guide de Survie & Restauration Post-Formatage](#2-guide-de-survie--restauration-post-formatage-crucial)
3. [L'Encyclopédie des 13 Skills Forgés](#3-lencyclopédie-des-13-skills-forgés)
4. [Moteurs Techniques & Scripts Développés](#4-moteurs-techniques--scripts-développés)
5. [Playbooks & Combos d'Intervention](#5-playbooks--combos-dintervention)
6. [Protocole de Maintenance & Mises à Jour](#6-protocole-de-maintenance--mises-à-jour)

---

## 1. Profil de l'Utilisateur & Standards d'Excellence

### Identité et Style de Collaboration
- **Langue de travail :** Français (clair, percutant, structuré).
- **Attente esthétique & fonctionnelle :** L'utilisateur exige des résultats **"très jolis, professionnels et impressionnants"**. Le niveau attendu est celui d'une agence haut de gamme ou d'un grand cabinet de conseil (McKinsey, Apple, Stripe, Linear).
- **Bannissement absolu du "AI Slop" :**
  - Pas de designs paresseux ou génériques (bannir les dégradés violets/bleus interchangeables sans âme).
  - Pas d'illustrations vectorielles d'entreprise sans vie (*Corporate Memphis*).
  - Pas de jargon corporate creux (*"Optimisez vos synergies dopées à l'IA"*).
  - Dans les documents : jamais de tableaux Word bleus standards ni de polices Calibri/Arial brutes sans hiérarchie.
- **Méthodologie de travail obligatoire :**
  - **Recherche préalable :** Toujours explorer et documenter les meilleures pratiques (Web, frameworks éprouvés) avant d'écrire la moindre ligne de code.
  - **Cadrage interactif :** Préférer poser les bonnes questions de clarification (options multiples, avantages/inconvénients) pour aligner la vision avant de foncer.
  - **Tests & Preuves visuelles :** Chaque livrable (code, présentation, document) doit être validé par un script de test ou un rendu concret.
- **Sécurité & Intégrité :** L'utilisateur accorde une importance critique à la sécurité. Aucun script, skill ou dépendance ne doit être exécuté sans vérification statique préalable (absence de malwares, reverse shells, fuites de données).
- **Disponibilité globale :** Tous les skills créés doivent impérativement être déployés dans la configuration globale d'Antigravity (`~/.gemini/config/skills/`) pour être actifs sur l'ensemble de ses futurs projets.

---

## 2. Guide de Survie & Restauration Post-Formatage (CRUCIAL)

Si l'utilisateur réinitialise son PC ou réinstalle Antigravity, voici le protocole exact pour retrouver l'environnement à 100 % en quelques minutes.

### A. AVANT de Réinitialiser le PC (Ce qu'il faut sauvegarder)
Sauvegarder l'intégralité du dossier `mes-skill/` sur un support externe (clé USB, SSD externe ou dépôt Git privé).  
Ce dossier contient :
- Le dossier `.agent/skills/` (les 13 skills complets avec leurs fichiers, tokens, schémas et scripts).
- Ce fichier maître `ANTIGRAVITY_BRAIN_MASTER.md`.
- Les scripts de test et exemples (`memo_test.docx`, `pitch_test_v3_graphique.pptx`, `presentation_show.html`, etc.).

### B. APRÈS Réinstallation de Windows et d'Antigravity

#### Étape 1 : Replacer le workspace
Replacer le dossier sauvegardé à son emplacement de travail (ex: `C:\Users\<NOM_UTILISATEUR>\Music\mes-skill` ou tout autre chemin choisi).

#### Étape 2 : Déployer les 13 Skills en Global
Ouvrir PowerShell dans le dossier `mes-skill` et exécuter cette commande pour injecter tous les skills dans le moteur global d'Antigravity :
```powershell
$globalSkills = "$HOME\.gemini\config\skills"
if (-not (Test-Path $globalSkills)) {
    New-Item -ItemType Directory -Path $globalSkills -Force | Out-Null
}
Copy-Item -Path ".\.agent\skills\*" -Destination $globalSkills -Recurse -Force
Write-Host "✅ Les 13 skills ont été restaurés avec succès dans Antigravity Global !" -ForegroundColor Green
```

#### Étape 3 : Installer les dépendances logicielles
Les moteurs de génération PowerPoint, Word et d'automatisation de tests s'appuient sur des bibliothèques Python et Node. Exécuter dans le terminal :
```powershell
# Dépendances Python pour Word, PowerPoint et parsing
pip install python-docx python-pptx pyyaml beautifulsoup4

# Automatisation de navigateur et tests E2E
pip install playwright
playwright install
```

#### Étape 4 : Transmission du contexte au nouvel agent
Dès le premier prompt dans Antigravity, l'utilisateur indique à l'agent :
> *"Lis le fichier `ANTIGRAVITY_BRAIN_MASTER.md` présent dans ce dossier pour récupérer tout ton historique, tes compétences et tes règles."*  
L'agent lit ce document et devient instantanément opérationnel au même niveau qu'aujourd'hui.

---

## 3. L'Encyclopédie des 13 Skills Forgés

Tous ces skills sont présents localement dans `.agent/skills/` et globalement dans `~/.gemini/config/skills/`.

```
                        ╔════════════════════════════════════╗
                        ║   L'ARSENAL ANTIGRAVITY (13)       ║
                        ╚════════════════════════════════════╝
                                          │
    ┌──────────────────┬──────────────────┼──────────────────┬──────────────────┐
    ▼                  ▼                  ▼                  ▼                  ▼
[ DESIGN / UI ]    [ CODE BACK/MBL ]   [ TESTS & QUALITÉ ] [ SÉCURITÉ & DATA ] [ BUSINESS & DOCS ]
• ui-ux-pro-max    • django-pro        • audit-projet      • web-security-     • landing-page-roast
• tailwind-design- • flutter-expert    • audit-browser       testing           • presentation-pro
  system                               • playwright-skill  • zod-validation-   • word-pro-max
                                       • vibe-code-cleanup   expert
```

### 1. `ui-ux-pro-max`
- **Rôle :** Directeur Artistique & Ingénieur UI Senior.
- **Règle absolue :** S'active automatiquement dès qu'un fichier d'interface visible (HTML, React, Vue, Flutter, template) est créé ou modifié.
- **Capacités :** Fournit les tokens de design (échelles typographiques à ratio modulaire 1.25/1.333, système d'espacement sur grille de 8pt, contrastes WCAG AAA, harmonies chromatiques 60-30-10). Interdit formellement les designs fades ou stéréotypés.

### 2. `tailwind-design-system`
- **Rôle :** Spécialiste intégration frontend Tailwind CSS.
- **Règle absolue :** Évite les fichiers CSS monolithiques et désordonnés. Construit des architectures de composants token-based (React, Next.js) avec des classes utilitaires organisées selon un ordre strict (Layout -> Spacing -> Typography -> Visual -> Interactive).

### 3. `django-pro`
- **Rôle :** Architecte Backend Django & DRF Senior.
- **Règle absolue :** À utiliser pour toute conception ou refactorisation d'API Django, Django REST Framework ou workers asynchrones (Celery/Redis).
- **Standards :** Authentification robuste JWT, protection CSRF/CORS stricte, optimisation systématique des requêtes de base de données (`select_related`, `prefetch_related` pour éliminer le problème N+1), sérialiseurs stricts.

### 4. `flutter-expert`
- **Rôle :** Ingénieur Mobile Flutter & Dart Senior.
- **Règle absolue :** À déclencher pour toute application mobile iOS/Android.
- **Standards :** Gestion d'état prédictible avec Riverpod ou BLoC, Clean Architecture (Data / Domain / Presentation), widgets isolés et optimisés pour maintenir un taux de rafraîchissement constant de 60 FPS, gestion rigoureuse des assets et du mode hors-ligne.

### 5. `audit-projet`
- **Rôle :** Auditeur Principal de Codebase.
- **Règle absolue :** Analyse globale de la santé technique d'un projet avant une mise en production ou après un développement important.
- **Standards :** Détection de dette technique, vérification des conventions de nommage, détection de code mort, revue des dépendances obsolètes ou vulnérables, validation de la structure architecturale.

### 6. `audit-browser`
- **Rôle :** Testeur End-to-End & Auditeur UI/UX Fonctionnel.
- **Règle absolue :** Simule le comportement d'un véritable utilisateur ou administrateur dans un navigateur headless/interactif.
- **Standards :** Teste les parcours critiques (inscription, connexion, paiement, formulaires multi-étapes), traque les erreurs console JavaScript, vérifie les temps de réponse et la cohérence de l'interface sous différents viewports.

### 7. `playwright-skill`
- **Rôle :** Expert en Automatisation de Tests E2E Playwright.
- **Règle absolue :** Rédige et maintient des suites de tests automatisés ultra-résilientes.
- **Standards :** Utilise exclusivement le pattern Page Object Model (POM), bannit les attentes temporelles fixes (`waitForTimeout`) au profit des sélecteurs auto-attendants basés sur les rôles accessibles (`getByRole`, `getByLabel`), captures d'écran et traces automatiques sur échec.

### 8. `web-security-testing`
- **Rôle :** Pentester & Spécialiste en Cybersécurité Offensive/Défensive.
- **Règle absolue :** Revue de code de sécurité et simulation d'attaques.
- **Standards :** Scan méthodique des vulnérabilités de l'OWASP Top 10 (Injections SQL/NoSQL, failles XSS, failles CSRF, Broken Access Control, fuite de tokens ou clés d'API en dur, en-têtes HTTP de sécurité manquants : CSP, HSTS, X-Frame-Options).

### 9. `zod-validation-expert`
- **Rôle :** Gardien de l'Intégrité des Données Full-Stack.
- **Règle absolue :** À invoquer pour tout formulaire, endpoint d'API, Server Action ou traitement d'input utilisateur.
- **Standards :** Typage strict inféré (`z.infer<typeof Schema>`), validation en profondeur des chaînes, nombres et objets imbriqués, messages d'erreurs clairs et prêts pour l'internationalisation (i18n), assainissement contre les injections.

### 10. `vibe-code-cleanup`
- **Rôle :** Maître Artisan Clean Code & Refactoring.
- **Règle absolue :** À invoquer dès qu'une base de code est encombrée, complexe ou issue de prototypage rapide.
- **Standards :** Réduction de la complexité cyclomatique, découpage des fonctions géantes en fonctions pures à responsabilité unique, élimination de la duplication de code (DRY), amélioration drastique de la lisibilité sans casser les tests existants.

### 11. `landing-page-roast` 🔥
- **Rôle :** Expert CRO (Conversion Rate Optimization) & Directeur de Copywriting.
- **Ton :** Brutal, direct et sans filtre (style "Gordon Ramsay du Web"). Zéro complaisance : ça pique l'ego mais ça sauve le business.
- **Théories intégrées :**
  - **Formule MECLABS :** $C = 4m + 3v + 2(i-f) - 2a$ (Motivation, Valeur vs Incitation, Friction, Anxiété).
  - **StoryBrand SB7 (Donald Miller) :** Le client est le héros (Luke Skywalker), la marque n'est que son guide (Yoda). Dénonciation immédiate des marques qui parlent d'elles-mêmes.
  - **Le Caveman Test (Test des 5 secondes) :** En 5 secondes sur le Hero, un homme des cavernes doit comprendre : *Qu'est-ce que c'est ? En quoi ça m'aide ? Que dois-je faire ?*
  - **LIFT Model :** Clarity, Relevance, Urgency vs Anxiety, Distraction.
- **Spécificités :** Mode local intégré (capable de lire du code source local `page.tsx`, d'auditer sur `localhost`, ou de demander proactivement une capture d'écran pour juger le design par Vision IA). Règle du Avant/Après obligatoire pour tout texte critiqué.

### 12. `presentation-pro` 📊
- **Rôle :** Agence de Pitch & Concepteur de Présentations d'Élite.
- **Capacités doubles :**
  1. **Fichiers PowerPoint natifs (`.pptx`) :** Générés via `python-pptx` avec application stricte des principes d'Edward Tufte (Data-Ink ratio : zéro grille, barres grises épurées, un seul accent fluo sur la donnée clé, typographie suisse).
  2. **Présentations Web 3D interactives :** Fichiers HTML/CSS autonomes avec animations au scroll, typographie responsive et rendu plein écran cinématique.
- **Ressources internes :** Intègre les matrices de mise en page McKinsey (`layout-matrix.yaml`), les tokens graphiques (`design-tokens.json`), et un linter/correcteur automatique de débordement de texte.

### 13. `word-pro-max` 📄
- **Rôle :** Concepteur & Rédacteur de Documents Word Professionnels (`.docx`).
- **Frameworks éditoriaux :**
  - **Shipley Associates :** Pour les propositions commerciales gagnantes (Executive Summary orienté bénéfices client).
  - **Amazon 6-Pager :** Pour les mémos d'affaires ultra-denses et décisionnels.
  - **Minto SCQA (Pyramide de Barbara Minto) :** Situation, Complication, Question, Réponse pour les audits stratégiques.
- **Ressources internes :** Moteur d'injection OOXML (`docx_builder.py`) permettant de contourner les limites de `python-docx` (encadrés Callout avec bordure gauche colorée, tables minimalistes sans lignes verticales, blocs KPI géants). Scripts de Redlining officiel (`unpack.py`/`pack.py`) pour appliquer des modifications sous suivi de révision (`<w:ins>`, `<w:del>`) sur des contrats existants.

---

## 4. Moteurs Techniques & Scripts Développés

Cette section documente le fonctionnement interne des scripts créés pour que le futur agent sache exactement comment les appeler et les enrichir.

### A. Moteur Word : `docx_builder.py`
Situé dans `.agent/skills/word-pro-max/scripts/docx_builder.py` :
- **Problème résolu :** La bibliothèque standard `python-docx` ne permet pas de créer des bordures sélectives de cellules, des arrière-plans colorés précis ou des marges internes sans passer par du bas niveau.
- **Solution développée :** Utilisation directe de `docx.oxml.parse_xml` pour injecter des fragments XML WordprocessingML conformes ISO/IEC 29500 :
  - `add_callout_box(doc, text, title, border_color, bg_color)` : Crée un tableau à une seule cellule avec bordure gauche épaisse (ex: `#1E3A8A`) et fond clair teinté, avec marges internes paddées.
  - `create_tufte_table(table, header_bg, line_color)` : Supprime toutes les bordures verticales de la table pour ne laisser qu'une ligne horizontale sous les en-têtes et sous la dernière ligne, respectant les règles typographiques de publication d'Edward Tufte.
  - `add_kpi_block(doc, number, label, accent_color)` : Insère une carte métrique géante pour les rapports exécutifs.

### B. Moteur Redlining Word : `unpack.py` & `pack.py`
Situé dans `.agent/skills/word-pro-max/ooxml/scripts/` :
- Permet d'éditer des documents juridiques ou administratifs en injectant du véritable XML de suivi des modifications (Track Changes) :
  ```xml
  <w:del w:id="1" w:author="Antigravity" w:date="2026-10-06T12:00:00Z">
      <w:r><w:t>Ancien texte contractuel</w:t></w:r>
  </w:del>
  <w:ins w:id="2" w:author="Antigravity" w:date="2026-10-06T12:00:00Z">
      <w:r><w:t>Nouveau texte révisé</w:t></w:r>
  </w:ins>
  ```

### C. Moteur Graphique PowerPoint : `generate_chart_pptx.py`
- Utilise les objets natifs `ChartData` et `XL_CHART_TYPE.COLUMN_CLUSTERED` de `python-pptx`.
- Stylise le graphique en désactivant le quadrillage parasite (`has_major_gridlines = False`), en supprimant la légende inutile quand la métrique est évidente, et en attribuant une couleur unie grise aux catégories neutres et une couleur vive d'accent sur la métrique gagnante.

---

## 5. Playbooks & Combos d'Intervention

L'utilisateur aime déclencher des chaînes de compétences pour accomplir des missions complexes. Voici les recettes maîtresses :

### Combo 1 : L'Audit de Projet 360° (End-to-End)
Lorsque l'utilisateur demande : *"Fais un audit complet de mon projet"* :
1. **Étape 1 (Code & Architecture) :** Appeler `@audit-projet` pour cartographier les dossiers, vérifier la dette technique et la propreté du code.
2. **Étape 2 (Sécurité & Intégrité) :** Appeler `@web-security-testing` et `@zod-validation-expert` pour traquer les failles OWASP et la validation des entrées.
3. **Étape 3 (Expérience & Fonctionnel) :** Appeler `@audit-browser` pour simuler le parcours utilisateur dans le navigateur et traquer les régressions UI.
4. **Étape 4 (Impact Business & Conversion) :** Appeler `@landing-page-roast` pour critiquer impitoyablement la page d'accueil, le copywriting et lever les freins à la conversion.
5. **Livrable :** Un rapport synthétique hiérarchisé par criticité.

### Combo 2 : Création d'une Application Web/Mobile de Haute Volée
1. **Direction Artistique :** `@ui-ux-pro-max` définit la palette, les polices et les espacements.
2. **Développement Frontend :** `@tailwind-design-system` structure les composants visuels.
3. **Développement Backend :** `@django-pro` (ou `@flutter-expert` pour mobile) implémente les flux métier et l'API.
4. **Validation des Données :** `@zod-validation-expert` verrouille les interfaces et formulaires.
5. **Assainissement & Lisibilité :** `@vibe-code-cleanup` élimine la dette technique avant finalisation.
6. **Sécurisation des Flux :** `@playwright-skill` écrit la couverture de tests E2E.

### Combo 3 : Le Deck de Présentation "Investor & Executive Ready"
1. Appeler `@presentation-pro`.
2. Structurer le storytelling selon la méthode Andy Raskin (Changement indéniable dans le monde -> Gagnants/Perdants -> Terre Promise -> Obstacles & Armes magiques -> Preuve).
3. Générer le fichier `.pptx` natif avec graphiques épurés Tufte ET la version Web interactive `presentation_show.html`.

### Combo 4 : Le Document Officiel / Rapport de Prestige
1. Appeler `@word-pro-max`.
2. Choisir le format : Proposition commerciale (Shipley), Mémo exécutif (Amazon) ou Rapport d'audit (Minto).
3. Exécuter le builder Python (`docx_builder.py`) pour insérer la page de garde premium, les encadrés d'avertissement/conseil colorés et les tableaux Edward Tufte sans lignes verticales.

---

## 6. Protocole de Maintenance & Mises à Jour

Ce document est un **document vivant (Living Document)**.

### Règle d'Or pour les Futurs Agents
Chaque fois qu'une nouvelle modification majeure est apportée dans le projet :
1. **Création d'un nouveau skill :** Ajouter sa fiche détaillée dans la section 3, lister ses fichiers dans la section 4, et le copier à la fois dans `.agent/skills/` et dans `~/.gemini/config/skills/`.
2. **Ajout d'un nouveau script ou moteur :** Documenter son usage et son interface dans la section 4.
3. **Évolution des préférences de l'utilisateur :** Mettre à jour la section 1.

*Ce fichier constitue la source unique de vérité de l'intelligence et des capacités accumulées avec l'utilisateur.*
