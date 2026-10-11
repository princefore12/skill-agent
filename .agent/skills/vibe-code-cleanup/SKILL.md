---
name: vibe-code-cleanup
description: "Expert en Clean Code et Refactoring. CRITICAL: ALWAYS use this skill when the user asks to clean, refactor, reorganize, or fix the structure of an existing codebase or specific files."
---

# Vibe Code Cleanup - Le Nettoyeur

## Objectif
Maintenir un code propre, lisible, et structuré de manière professionnelle, en éliminant la dette technique et en séparant clairement la logique de l'interface utilisateur.

## Instructions Principales

1. **Le Grand Ménage (Nettoyage de Surface)**
   - Supprime tous les `console.log`, `console.warn` (sauf s'ils font partie d'un logger structuré ou gèrent des erreurs critiques).
   - Identifie et supprime les imports inutilisés (`unused imports`).
   - Supprime le code mort (variables non utilisées, fonctions obsolètes, code commenté).
   - Formate le fichier selon les standards ESLint et Prettier (indentation, points-virgules, guillemets).

2. **Séparation Logique (Refactoring en Profondeur)**
   - **Règle d'Or** : Un composant UI doit rester "bête" (Dumb Component) au maximum. 
   - Dès qu'un composant dépasse ~100 lignes ou contient une logique complexe :
     - **Custom Hooks** : Extraire toute la logique d'état (`useState`, `useReducer`), les Effets (`useEffect`), et les appels API dans un Hook personnalisé (ex: `useUserManagement.ts`).
     - **Utilitaires** : Extraire les algorithmes purs, les calculs mathématiques ou les transformations de données dans des fichiers `/utils/` ou `/helpers/`.

3. **Organisation des Imports**
   - Regroupe et ordonne les imports de manière logique :
     1. Librairies externes (React, Next.js, Zod, etc.)
     2. Composants internes / UI
     3. Hooks / Contexts
     4. Utils / Types
     5. Fichiers de styles ou assets

## Contraintes
- Lors d'un nettoyage, **ne modifie jamais le comportement fonctionnel de l'application**. Le résultat final doit être strictement identique pour l'utilisateur.
- Avant de créer un nouveau fichier pour un Custom Hook, vérifie toujours la structure des dossiers existante (ex: préférer le dossier `hooks/` à la racine de la feature).
- Ajoute ou corrige les types TypeScript manquants si tu rencontres des `any` au cours du refactoring.
