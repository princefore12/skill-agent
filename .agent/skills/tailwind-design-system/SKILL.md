---
name: tailwind-design-system
description: "Expertise UI/CSS avec Tailwind. CRITICAL: ALWAYS use this skill when styling frontend interfaces, writing Tailwind CSS classes, or building React/Next.js UI components. This ensures clean, maintainable, and token-based component architectures without bloated CSS files."
---

# Tailwind Design System - Architecte UI

## Objectif
Standardiser l'utilisation de Tailwind CSS pour garantir un code UI propre, réutilisable, maintenable, et aligné sur les meilleures pratiques des Design Systems modernes.

## Instructions Principales

1. **Architecture des Composants (Pas de `@apply`)**
   - **INTERDICTION** d'utiliser la directive `@apply` dans les fichiers CSS globaux pour créer des composants (sauf rares exceptions comme les styles de base du `body` ou des balises HTML).
   - Extraire systématiquement les éléments UI répétitifs en **Composants React/Next.js** (ex: `Button.tsx`, `Card.tsx`, `Input.tsx`).

2. **Gestion Dynamique des Classes (Utilitaire `cn`)**
   - Pour toute logique de classes conditionnelles ou de fusion de classes (ex: fusionner les classes par défaut d'un composant avec celles passées en props), utilise l'utilitaire `cn()`.
   - La fonction `cn()` doit combiner **`clsx`** (pour les conditions) et **`tailwind-merge`** (pour écraser intelligemment les conflits de classes Tailwind).
   - *Exemple* : `className={cn("px-4 py-2 bg-blue-500", isDisabled && "opacity-50", className)}`

3. **Design Tokens et Thématique**
   - N'utilise pas de valeurs arbitraires en dur (ex: `bg-[#2563EB]`, `w-[312px]`) si ce n'est pas strictement justifié par un cas très isolé.
   - Configure les couleurs, espacements et typographies dans le fichier `tailwind.config.js` via le système d'extension (`theme.extend`).
   - Utilise les variables CSS (CSS Custom Properties) déclarées à la racine pour gérer les thèmes (ex: `bg-primary`, `text-foreground`).

4. **Accessibilité (A11y) et UX**
   - Rends les états interactifs explicites : utilise toujours `hover:`, `active:`, et **SURTOUT** `focus-visible:` pour la navigation au clavier (ex: `focus-visible:ring-2 focus-visible:ring-offset-2`).
   - Gère le mode sombre en utilisant systématiquement le préfixe `dark:` (ex: `bg-white dark:bg-slate-900`).

## Contraintes
- Ne laisse jamais de chaînes de classes Tailwind s'étirer sur plus de 15-20 classes sans évaluer la possibilité de scinder l'élément HTML en sous-composants.
- Toujours vérifier que `tailwind-merge` et `clsx` sont installés dans le `package.json` lors du setup d'un nouveau projet ou composant.
