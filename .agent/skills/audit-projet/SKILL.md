---
name: audit-projet
description: "Fait un audit complet du projet (code, architecture, sécurité, performances). Utilise ce skill quand l'utilisateur demande d'auditer le projet, de vérifier la qualité du code ou de chercher des vulnérabilités structurelles."
---
# Audit de Projet Complet

## Objectif
Analyser l'intégralité du code source, de l'architecture et de l'infrastructure d'un projet pour produire un rapport d'audit professionnel avec un score transparent, des preuves concrètes et des recommandations priorisées.

---

## Phase 1 — Découverte Autonome (ne rien demander à l'utilisateur)
1. **Cartographier le projet** : arborescence des dossiers, stack technique (langage, framework, ORM, base de données), fichiers de configuration (`package.json`, `requirements.txt`, `docker-compose.yml`, etc.).
2. **Identifier les points d'entrée** : routes API, pages frontend, commandes CLI, workers/crons.
3. **Repérer les frontières de confiance** : entrées utilisateur, appels externes, middleware d'authentification, gestion des rôles.

---

## Phase 2 — Les 7 Dimensions d'Audit

Auditer le projet selon ces 7 axes, dans cet ordre de priorité :

### 1. 🔒 Sécurité (Priorité maximale)
- Secrets/clés en dur dans le code (API keys, tokens, mots de passe).
- Injections : SQL, XSS, Command Injection, Path Traversal.
- Désérialisation non sécurisée, usage de `eval()`.
- Hachage faible (MD5, SHA1 pour les mots de passe au lieu de bcrypt/argon2).
- Validation des entrées manquante (absence de Zod, Joi, ou équivalent).
- Fichier `.env` non protégé par `.gitignore`, absence de `.env.example`.
- Fuite de données sensibles dans les logs ou les réponses API.
- **Analyse contradictoire** : pour chaque fonctionnalité critique, se poser la question *"Comment un attaquant pourrait-il exploiter ceci ?"*.
- **Traçage Source-to-Sink** : pour chaque vulnérabilité signalée, tracer le flux de données complet (point d'entrée → traitement → exécution vulnérable) pour éliminer les faux positifs.

### 2. 🏗️ Architecture & Design
- Séparation des couches (Controllers / Services / Repositories / Models).
- Dépendances circulaires entre modules.
- God classes (>500 lignes) ou god functions (>50 lignes).
- Couplage fort entre les modules (un changement dans A casse B).
- Frontières claires entre le code métier et le code technique.

### 3. ⚡ Performance
- Requêtes N+1 (ORM sans eager loading).
- Opérations synchrones bloquantes dans du code async.
- Index manquants sur les requêtes fréquentes.
- Pagination absente sur les endpoints de liste.
- Taille des bundles frontend (si applicable).
- **Règle absolue** : ne JAMAIS spéculer sur les performances ("ça pourrait être lent"). Toute remarque doit être justifiée par un pattern mesurable (N+1, complexité O(n²), copie d'objets lourds en boucle).

### 4. 🧹 Qualité & Propreté du Code
- Complexité cyclomatique > 10.
- Magic numbers / magic strings (constantes non nommées).
- Duplication de code (blocs copiés-collés).
- Nommage incohérent ou trompeur.
- Code commenté laissé dans le codebase.
- `console.log` / `print()` de debug oubliés.
- Imports orphelins (importés mais jamais utilisés).
- Inégalité lâche `==` au lieu de `===` (JavaScript/TypeScript).
- Types `any` en TypeScript.
- Promesses sans `await` ou sans `.catch()`.

### 5. 🤖 Code Mort ou Halluciné (spécial code généré par IA)
- Bibliothèques importées mais absentes de `package.json` / `requirements.txt`.
- Méthodes d'API appelées qui n'existent pas ou sont obsolètes.
- Arguments de fonction passés qui ne correspondent à aucun paramètre réel.
- Blocs de code inatteignables (dead code après un `return` / `throw`).
- Variables déclarées mais jamais lues.
- Fonctions définies mais jamais appelées.

### 6. 🧪 Tests & Couverture
- Présence ou absence de tests unitaires / d'intégration / E2E.
- Couverture des chemins critiques (authentification, paiement, formulaires).
- Tests fragiles : `test.only()`, `fdescribe()`, `fit()` oubliés.
- Assertions significatives (pas de tests qui ne vérifient rien).

### 7. 🚀 Production Readiness (Infrastructure)
- Endpoint `/health` ou `/ready` pour les sondes de santé.
- Logs structurés (Winston, Pino, structlog) au lieu de `console.log`.
- Gestion centralisée des erreurs (error handler global, Sentry/APM).
- Graceful shutdown (fermeture propre des connexions DB/Redis).
- Variables d'environnement documentées dans `.env.example`.
- Dockerfile / docker-compose fonctionnel (si applicable).
- Pipeline CI/CD présent et fonctionnel.
- Pages d'erreur personnalisées (404, 500).

---

## Phase 3 — Scoring Transparent

Calculer un score sur 100 avec cette formule déterministe :

```
Score de départ : 100
- Faille de sécurité critique    : -20 par occurrence
- Bug critique                   : -15 par occurrence
- Anomalie haute                 : -8 par occurrence
- Anomalie moyenne               : -3 par occurrence
- Motif récurrent (3+ fois)      : -5 supplémentaires
Score minimum : 0
```

**Bandes de notation :**
| Score | Note | Verdict |
|-------|------|---------|
| 90-100 | A | Production-ready 🟢 |
| 75-89 | B | Solide, améliorations mineures 🟢 |
| 60-74 | C | Correct mais dette technique 🟠 |
| 40-59 | D | Risques importants 🟠 |
| 0-39 | F | Dangereux, refonte nécessaire 🔴 |

---

## Phase 4 — Format du Rapport Final

Structurer le rapport en ces sections :

### 1. Résumé Exécutif (1 ligne)
> Score : XX/100 (Note X) — Verdict en une phrase.

### 2. Tableau de Synthèse
| Dimension | Statut | Nb problèmes |
|-----------|--------|---------------|
| Sécurité  | 🔴/🟠/🟢 | X |
| Architecture | 🔴/🟠/🟢 | X |
| ... | ... | ... |

### 3. Top 10 des Problèmes (maximum 10)
Pour chaque problème, fournir **obligatoirement** :
- **[Dimension][Sévérité]** `fichier:ligne` — Description du problème
- **Preuve** : extrait de code incriminé
- **Flux** : source → sink (pour les failles de sécurité)
- **Fix proposé** : extrait de code corrigé
- **Référence** : CWE/OWASP si applicable

### 4. 🏆 Points Forts
Lister ce qui est bien fait (minimum 3 points positifs).

### 5. ⚡ Quick Wins (< 1 heure)
Lister les corrections à fort impact réalisables en moins d'une heure.

### 6. 🗺️ Chantiers Lourds
Lister les refactorisations nécessitant plus d'une journée de travail.

### 7. Proposition Proactive
Terminer systématiquement par :
> "Voulez-vous que je corrige le problème #1 en priorité ? Je peux vous montrer le diff."

---

## Contraintes Impératives

1. **NE JAMAIS modifier le code** sans l'autorisation explicite de l'utilisateur. Toujours présenter un diff et attendre la validation.
2. **Maximum 10 remarques critiques** dans le rapport. Au-delà, signaler que le projet nécessite une refonte et proposer un plan d'action par lots.
3. **Zéro spéculation** : chaque remarque doit être justifiée par un extrait de code, un pattern mesurable ou une référence (CWE, OWASP).
4. **Zéro nitpick de style** : ne PAS commenter les préférences de formatage (tabs vs spaces, guillemets simples vs doubles) sauf si cela crée une incohérence dans le projet.
5. **Toujours vérifier l'atteignabilité** : une vulnérabilité dans du code mort n'est pas une vulnérabilité critique.
