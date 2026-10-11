---
name: playwright-skill
description: "Expert en Tests Automatisés E2E (End-to-End) avec Playwright. CRITICAL: ALWAYS use this skill when creating or modifying automated browser tests, integration tests, or QA scripts to ensure reliable Page Object Model architecture."
---

# Playwright Expert - QA Automatisé

## Objectif
Garantir des tests E2E robustes, rapides et maintenables, qui résistent aux petits changements d'interface, en utilisant la puissance de Playwright et l'architecture POM.

## Instructions Principales

1. **Architecture (Page Object Model - POM)**
   - N'écris jamais toute la logique d'interaction et les sélecteurs directement dans les fichiers de spécifications (`.spec.ts`).
   - Sépare obligatoirement le code en deux parties :
     1. **Les Classes de Pages (`pages/`)** : Contiennent les sélecteurs (locators) et les méthodes d'interaction (ex: `login(user, pass)`).
     2. **Les Scripts de Tests (`tests/`)** : Importent les pages et contiennent uniquement la logique d'assertion (ex: `await expect(page).toHaveTitle('Dashboard')`).

2. **Résilience des Sélecteurs (Locators)**
   - Banni l'utilisation des sélecteurs CSS fragiles (ex: `.btn-primary > div > span`) ou XPath.
   - Utilise toujours les sélecteurs "user-facing" de Playwright, par ordre de priorité :
     1. `getByRole()` (ex: `getByRole('button', { name: 'Submit' })`) - Excellent pour l'accessibilité !
     2. `getByText()`
     3. `getByLabel()`
     4. `getByTestId()` (si `data-testid` est présent dans le code source).

3. **Assertions et Auto-Retry**
   - Utilise toujours les "web-first assertions" (les assertions qui attendent automatiquement).
   - *Bon exemple* : `await expect(locator).toBeVisible()` (Playwright attendra jusqu'au timeout si l'élément n'est pas encore là).
   - *Mauvais exemple* : `const isVisible = await locator.isVisible(); expect(isVisible).toBeTruthy();` (Cela n'attendra pas et fera échouer le test si l'élément met 100ms à apparaître).

## Contraintes
- Utilise TypeScript (`.ts`) par défaut pour tous les fichiers Playwright.
- Ne jamais utiliser `page.waitForTimeout(5000)` (les délais codés en dur). Utiliser plutôt `page.waitForLoadState('networkidle')` ou attendre qu'un élément spécifique devienne visible.
