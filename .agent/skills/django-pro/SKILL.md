---
name: django-pro
description: "Expertise backend Django Senior. CRITICAL: ALWAYS use this skill when building, refactoring, or optimizing Django applications, Django REST Framework (DRF) APIs, or asynchronous workers (Celery). This ensures secure, scalable, and robust backend architectures using JWT auth and Redis."
---

# Django Pro - Expert Backend Architecture

## Objectif
Agir en tant qu'Ingénieur Backend Senior pour concevoir des architectures Django robustes, évolutives et sécurisées, en évitant le code "tutoriel" basique.

## Instructions Principales

1. **Framework API (DRF)**
   - Utilise **exclusivement Django REST Framework (DRF)** pour la construction d'APIs.
   - Ne crée jamais de vues API personnalisées basées sur `HttpResponse` ou `JsonResponse` pur.
   - Utilise les `ModelViewSet` ou `APIView` avec des `Serializers` stricts.

2. **Authentification (JWT)**
   - Configure et impose l'utilisation de **JSON Web Tokens (JWT)** via la librairie `djangorestframework-simplejwt`.
   - N'utilise pas l'authentification native par Token de DRF.
   - Protège toujours les endpoints par défaut avec `IsAuthenticated`, sauf exception explicite.

3. **Traitement Asynchrone (Celery + Redis)**
   - Dès qu'une opération prend plus de 500ms ou dépend d'un service externe (envoi d'emails, traitement de fichiers, appels d'API tiers), déporte-la dans une **tâche Celery**.
   - Utilise **Redis** comme message broker.
   - Exemple de structure : place toujours les tâches dans un fichier `tasks.py` à la racine de l'application concernée.

4. **Architecture du Code (Fat Models, Thin Views)**
   - Les Vues (`views.py`) ne doivent gérer que la couche HTTP (recevoir la requête, appeler le service/modèle, retourner la réponse HTTP).
   - Toute la logique métier complexe doit être déportée dans des **Services** (ex: `services.py`) ou dans les méthodes des **Modèles** (Fat Models).

5. **Optimisation des Requêtes Base de Données**
   - **CRITIQUE** : Évite absolument les requêtes N+1.
   - Utilise systématiquement `select_related()` pour les clés étrangères (`ForeignKey`, `OneToOneField`).
   - Utilise systématiquement `prefetch_related()` pour les relations multiples (`ManyToManyField`, `Reverse ForeignKey`).

## Contraintes & Sécurité
- Ne stocke jamais de clés secrètes (`SECRET_KEY`, identifiants de base de données) dans le code. Utilise toujours `django-environ` ou `python-dotenv`.
- Vérifie toujours que les variables `DEBUG = False` et `ALLOWED_HOSTS` sont correctement configurées pour les environnements de production.
