---
name: zod-validation-expert
description: "Expertise Zod pour la validation de données Full-Stack. CRITICAL: ALWAYS use this skill when creating forms, API endpoints, Server Actions, or handling user input to ensure strict type safety and i18n error handling."
---

# Zod Validation Expert

## Objectif
Standardiser la validation des données sur l'ensemble du projet en utilisant **Zod** comme "Single Source of Truth", en partageant les schémas entre le Frontend (formulaires) et le Backend (API / Server Actions).

## Instructions Principales

1. **Architecture Centralisée (Single Source of Truth)**
   - Ne crée jamais de validations manuelles (ex: `if (!email) throw Error`).
   - Définis toujours tes schémas Zod dans un dossier centralisé (ex: `schemas/` ou `types/`) pour qu'ils soient importables côté client et côté serveur.
   - Utilise `z.infer<typeof schema>` pour générer systématiquement les types TypeScript associés.

2. **Validation Frontend (React Hook Form)**
   - Pour les formulaires, utilise toujours **React Hook Form** couplé avec **`@hookform/resolvers/zod`**.
   - Ne gère jamais l'état d'un formulaire manuellement avec des `useState` si une validation complexe est requise.

3. **Validation Backend (API & Server Actions)**
   - Toute donnée entrante (Payload API, Server Action, Query Params) doit être passée au crible avec `schema.parse()` ou `schema.safeParse()` avant tout traitement de logique métier.

4. **Gestion des Erreurs et Internationalisation (i18n)**
   - N'écris pas les messages d'erreur en dur dans le schéma (ex: *ÉVITER* `z.string().min(5, "Trop court")`).
   - Implémente une configuration d'erreur multilingue. Utilise **`zod-i18n-map`** ou configure la méthode `z.setErrorMap()` pour que les messages d'erreurs Zod se branchent sur le système de traduction global de l'application (ex: `react-i18next` ou `next-intl`).

## Contraintes
- Chaque schéma doit être testé ou conçu pour empêcher les attaques par injection (utiliser `z.string().trim()`, limiter les longueurs maximales avec `.max()`).
- Si une donnée optionnelle est vide, utilise `.optional()` ou `.nullish()` proprement pour éviter les crashs TypeScript.
