# Arsenal Antigravity & Skills Hub

Bienvenue dans le dépôt central des compétences et frameworks d'Antigravity.

## 🧠 Mémoire Centrale & Cerveau du Projet
Le document de référence complet pour tout agent Antigravity (notamment après réinitialisation du PC ou nouvelle session) est situé ici :
👉 **[`ANTIGRAVITY_BRAIN_MASTER.md`](./ANTIGRAVITY_BRAIN_MASTER.md)**

Ce fichier contient :
- Le profil et les exigences d'excellence de l'utilisateur.
- Le protocole de restauration en 3 étapes post-formatage.
- L'encyclopédie détaillée des **13 skills forgés** (Design, Backend, Mobile, Tests, Sécurité, Documents, Présentations, Roast CRO).
- Les scripts et moteurs Python développés (`docx_builder.py`, `unpack.py`, `pack.py`, générateurs PPTX, etc.).
- Les playbooks et combos de travail complets (Audit 360°, Lancement d'app, Présentation, etc.).

---

## 🚀 Restauration Rapide des Skills en Global (PowerShell)
Si tu réinstalles Antigravity sur une nouvelle machine :
```powershell
$globalSkills = "$HOME\.gemini\config\skills"
if (-not (Test-Path $globalSkills)) { New-Item -ItemType Directory -Path $globalSkills -Force }
Copy-Item -Path ".\.agent\skills\*" -Destination $globalSkills -Recurse -Force
```
Puis installe les dépendances Python :
```powershell
pip install python-docx python-pptx pyyaml playwright beautifulsoup4
playwright install
```
