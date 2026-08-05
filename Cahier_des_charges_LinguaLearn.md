# Cahier des Charges – LinguaLearn

## 1. Présentation
**Nom du projet :** LinguaLearn

### Contexte
L'application mobile LinguaLearn vise à faciliter l'apprentissage des langues grâce à des leçons interactives, du vocabulaire, des flashcards, des quiz et un suivi de progression.

## 2. Objectif général
Développer une application mobile intuitive permettant aux utilisateurs d'apprendre une ou plusieurs langues de manière progressive et ludique.

## 3. Objectifs spécifiques
- Apprendre du vocabulaire.
- Étudier la grammaire.
- Écouter la prononciation.
- Réaliser des quiz.
- Suivre sa progression.
- Recevoir une leçon quotidienne.

## 4. Public cible
Élèves, étudiants, enseignants, professionnels, voyageurs et toute personne souhaitant apprendre une langue.

## 5. Plateforme
- Flutter (Android, évolutif iOS)
- Firebase (Authentication, Firestore, Storage)

## 6. Fonctionnalités
### Authentification
- Inscription
- Connexion
- Déconnexion
- Réinitialisation du mot de passe
- Gestion du profil

### Tableau de bord
- Progression
- Leçon du jour
- Statistiques
- Reprise de l'apprentissage

### Langues
- Français
- Anglais
- Espagnol
- Architecture extensible

### Vocabulaire
Catégories : Salutations, Famille, Nourriture, Couleurs, Animaux, École, Travail, Voyage, Santé, Loisirs, Sports, Maison.

Chaque fiche contient : mot, traduction, prononciation, image, exemple, audio.

### Grammaire
Leçons classées par niveau avec explications, exemples et exercices.

### Flashcards
Recto/verso, favoris, navigation.

### Exercices
QCM, Vrai/Faux, Association, Compléter, Ordonner une phrase.

### Quiz
Score, temps, corrections, pourcentage.

### Progression
Leçons terminées, mots appris, badges, séries quotidiennes.

### Favoris
Enregistrement des mots et leçons.

### Notifications
Rappels quotidiens et objectifs.

### Paramètres
Mode sombre, langue, notifications, profil.

## 7. Exigences non fonctionnelles
- Interface moderne
- Navigation intuitive
- Sécurité
- Rapidité
- Évolutivité
- Maintenance facilitée

## 8. Base de données
Tables :
- Utilisateurs
- Langues
- Catégories
- Leçons
- Vocabulaire
- Exercices
- Quiz
- Questions
- Réponses
- Progression
- Favoris
- Notifications
- Badges

## 9. Architecture Flutter
- models/
- services/
- screens/
- widgets/
- data/
- assets/

## 10. Sécurité
Authentification sécurisée, validation des données, synchronisation Firebase.

## 11. Livrables
- Application Flutter
- Code source
- Documentation
- Cahier des charges

## 12. Perspectives
Ajout de nouvelles langues, IA, reconnaissance vocale, classement, mode hors ligne enrichi.

## Conclusion
LinguaLearn est une application d'apprentissage des langues moderne offrant un environnement interactif combinant leçons, vocabulaire, grammaire, flashcards, quiz et suivi de progression.
