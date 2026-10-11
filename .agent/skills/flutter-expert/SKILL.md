---
name: flutter-expert
description: "Expertise en développement mobile Flutter et Dart. CRITICAL: ALWAYS use this skill when building, modifying, or refactoring Flutter applications. Imposes strict state management with Riverpod, widget optimization, and clean architecture."
---

# Flutter Expert - Architecte Mobile

## Objectif
Produire des applications mobiles Flutter performantes (60/120fps), maintenables, et scalables en utilisant les standards les plus modernes de la communauté Dart.

## Instructions Principales

1. **Gestion d'État (State Management)**
   - Utilise **exclusivement Riverpod** (`flutter_riverpod` ou `hooks_riverpod`) pour toute gestion d'état qui dépasse la portée locale d'un widget.
   - Privilégie les `AsyncNotifierProvider` et `NotifierProvider` avec la nouvelle syntaxe basée sur les classes (Génération de code via `@riverpod` fortement encouragée).
   - Ne **JAMAIS** utiliser `setState` pour de la logique métier globale ou asynchrone (réservé aux petites animations ou toggle locaux).

2. **Architecture Clean (Séparation des préoccupations)**
   - **UI (Widgets)** : Les widgets doivent rester purs et n'être responsables que du rendu. Ils consomment les providers (via `ref.watch`).
   - **Contrôleurs/Notifiers** : Gèrent la logique métier, la mutation de l'état, et les appels aux repositories.
   - **Repositories** : Interagissent avec les API externes ou la base de données locale.
   - Les Modèles de données doivent être immuables (utiliser `freezed` et `json_serializable`).

3. **Performance & Rendu**
   - Utilise le mot-clé `const` partout où c'est possible (widgets sans état dynamique, EdgeInsets, Colors) pour éviter des re-builds coûteux de l'arbre des widgets.
   - Préfère `ListView.builder` à un `ListView` simple ou à un `SingleChildScrollView` + `Column` pour les longues listes, afin d'optimiser l'utilisation de la mémoire.
   - Utilise `SizedBox` au lieu de `Container` s'il s'agit juste d'ajouter de l'espacement.

## Contraintes
- Le code doit être "Null-Safe" de manière stricte (ne pas forcer le unwrapping avec `!` à moins d'être à 100% sûr ; préférer `?` ou des valeurs par défaut).
- Toujours penser au layout adaptatif (Responsive/Adaptive Design) : vérifier le comportement avec `LayoutBuilder` ou `MediaQuery` si le widget peut être utilisé sur tablette ou web.
