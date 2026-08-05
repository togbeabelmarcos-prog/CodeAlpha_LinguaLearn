# LinguaLearn 🌍 (version Django)

Application web d'apprentissage des langues (Français, Anglais,
Espagnol) : vocabulaire, grammaire, flashcards, quiz et suivi de
progression avec badges — réécrite en Django après les blocages
rencontrés avec la version Flutter/Android.

Ce projet a été **testé de bout en bout** (inscription, connexion,
favoris, quiz complet, progression, réglages) avant livraison : tout
fonctionne dès l'installation, sans configuration externe (pas de
Firebase, pas d'Android Studio, pas de toolchain mobile).

## Fonctionnalités

- **Authentification** : inscription, connexion, déconnexion,
  réinitialisation de mot de passe
- **Tableau de bord** : leçon du jour, accès rapide, série en cours
- **Vocabulaire** : 12 catégories, mot/traduction/prononciation/
  exemple, favoris (❤️/🤍 en un clic)
- **Grammaire** : leçons par niveau (débutant/intermédiaire/avancé),
  marquables comme terminées
- **Flashcards** : cartes retournables (recto mot / verso traduction
  + exemple), navigation précédent/suivant
- **Quiz** : QCM avec score et pourcentage de réussite
- **Progression** : mots appris, leçons terminées, badges, série de
  jours consécutifs (streak)
- **Réglages** : mode sombre, langue d'apprentissage active,
  notifications

38 mots de vocabulaire, 5 leçons de grammaire et 2 quiz sont
pré-chargés dans les 3 langues (via la commande `seed_data`).

## Installation

### Prérequis
- Python 3.10 ou plus récent

### Étapes

```bash
cd lingualearn_django

# Environnement virtuel (recommandé)
python3 -m venv venv
source venv/bin/activate        # Sous Windows : venv\Scripts\activate

# Dépendances
pip install -r requirements.txt

# Base de données
python manage.py migrate

# Données de démonstration (vocabulaire, leçons, quiz, badges)
python manage.py seed_data

# (Optionnel) Compte administrateur pour l'interface /admin/
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
```

Puis ouvrez **http://127.0.0.1:8000/** dans votre navigateur.
Créez un compte via « S'inscrire » et vous accédez immédiatement à
toutes les fonctionnalités.

L'interface d'administration Django (gestion du contenu : ajouter
des langues, du vocabulaire, des leçons, des quiz) est disponible sur
**http://127.0.0.1:8000/admin/** avec le compte créé via
`createsuperuser`.

## Architecture du projet

```
lingualearn_django/
├── manage.py
├── requirements.txt
├── config/                  # Réglages et routage principal du projet
│   ├── settings.py
│   └── urls.py
├── accounts/                 # Authentification, profil, réglages
│   ├── models.py             # Profile (langue active, mode sombre...)
│   ├── forms.py
│   ├── views.py
│   └── templates/accounts/
├── content/                  # Contenu pédagogique
│   ├── models.py             # Language, Category, Vocabulary, Lesson, Quiz, Question, Answer
│   ├── views.py               # Vocabulaire, grammaire, flashcards, quiz
│   ├── management/commands/seed_data.py   # Peuple la base avec le contenu de démo
│   └── templates/content/
├── learning/                  # Suivi de l'apprentissage
│   ├── models.py             # Progress, Badge, Favorite, QuizResult, LessonProgress
│   ├── views.py               # Favoris, progression
│   └── templates/learning/
├── dashboard/                 # Tableau de bord principal
│   ├── views.py
│   └── templates/dashboard/
├── templates/base.html        # Gabarit commun (navigation, styles)
└── static/css/style.css       # Design personnalisé (palette violette/orange)
```

## Base de données

SQLite par défaut (`db.sqlite3`, créé automatiquement par
`migrate`) — aucune configuration requise. Pour passer à
PostgreSQL/MySQL en production, il suffit d'adapter `DATABASES` dans
`config/settings.py`.

## Prochaines étapes suggérées

- Ajout de nouvelles langues (ajoutez simplement une `Language` et du
  contenu associé via l'admin — l'architecture le permet directement)
- Prononciation audio réelle (le modèle `Vocabulary` a déjà un champ
  `audio`)
- Classement / mode compétitif entre utilisateurs
- API REST (Django REST Framework) pour une future app mobile
- Déploiement (Gunicorn + Nginx, ou une plateforme comme Railway/
  Render/PythonAnywhere)

## Livrables inclus

- Code source complet du projet Django
- Commande de peuplement des données de démonstration
- Cahier des charges d'origine
- Ce README
