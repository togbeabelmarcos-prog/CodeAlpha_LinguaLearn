#!/bin/bash
# Installation et lancement rapide de LinguaLearn (Django)
set -e

echo "== Création de l'environnement virtuel =="
python3 -m venv venv
source venv/bin/activate

echo "== Installation des dépendances =="
pip install -r requirements.txt

echo "== Migration de la base de données =="
python manage.py migrate

echo "== Chargement des données de démonstration =="
python manage.py seed_data

echo ""
echo "Installation terminée. Lancez le serveur avec :"
echo "  source venv/bin/activate && python manage.py runserver"
echo "Puis ouvrez http://127.0.0.1:8000/"
