# 🏎️ Jeu de Survie Routier - VR & Voice Mode
## 📝 Présentation du projet
Ce jeu de survie est une expérience immersive développée en Python utilisant Pygame. Il propose un gameplay innovant en intégrant des technologies de vision par ordinateur et de reconnaissance vocale pour offrir une expérience de type "Réalité Augmentée" (AR) / "VR sans casque".

# Projet réalisé par : Salma WADOUACHI et Ketsukana SON ESSOME MOUKOURI.

# 🚀 Fonctionnalités Avancées
Head Tracking (OpenCV) : Pilotez votre véhicule par des mouvements de tête. Le système utilise votre webcam pour détecter l'offset de votre visage et le traduire en mouvement fluide dans le jeu.

Commande Vocale (Vosk) : Utilisez des commandes vocales pour activer le "Boost", passer en "Mode Rapide", relancer une partie ("Restart") ou quitter le jeu.

Système de Difficulté Dynamique : La vitesse des obstacles augmente toutes les 30 secondes, faisant passer le joueur aux niveaux supérieurs.

Gestion de l'Énergie : Ramassez des bidons de Fuel (classique ou Gold) pour augmenter votre score et survivre.

# 🛠️ Installation et Lancement
1. Pré-requis

Python 3.12 ou supérieur.

Une webcam fonctionnelle (pour le Head Tracking).

Un microphone (pour les commandes vocales).

2. Installation

Depuis le terminal, à la racine du projet :

Bash
Activation de l'environnement virtuel (Optionnel mais recommandé)
source venv/bin/activate 

Installation des dépendances
pip install -r requirements.txt

3. Lancement

Bash
python main.py

# 🎮 Comment jouer ?

Contrôles

Tête : Inclinez la tête à gauche ou à droite pour déplacer la voiture latéralement.

Clavier : Utilisez les flèches directionnelles comme contrôle de secours.

Voix :

"boost" : Accélération temporaire.

"speed" : Active le mode rapide permanent.

"restart" : Relance le jeu après un Game Over.

"quit" : Ferme proprement l'application.

Gameplay

Score : 🟢 Fuel Vert (+10) | ⛽ Pompe Gold (+20).

Vies : Vous commencez avec 3 vies. Une collision avec un véhicule adverse vous retire une vie.

Niveaux : Le niveau augmente toutes les 30 secondes, rendant le jeu plus rapide et difficile.

# 🧠 Points Complexes & Défis Techniques
Multithreading : Pour éviter les lags, le traitement de la caméra (OpenCV) et de la voix (Vosk) tournent sur des threads séparés du moteur graphique (Pygame).

Lissage de données (Smoothing) : Implémentation d'un algorithme d'interpolation linéaire pour convertir les données brutes de la webcam en mouvements de voiture fluides et agréables.
