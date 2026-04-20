
# Mini-Jeu de Survie Routier

## Installation et lancement

Pour installer et exécuter le jeu :

1. **Pré-requis** : Python 3.12+ et Pygame 2.6.1.
2. **Cloner ou copier** le projet dans un dossier, en conservant la structure :


```markdown
/assets
  car.png, car1.png, ..., car4.png
  travel.png
  gasoline.png
  gasoline-pump.png
  gamebonus.mp3
  carcrash.mp3
  collect_coins.mp3
main.py
player.py
obstacle.py
fuel.py
background.py
```

3. **Installer Pygame** si ce n’est pas déjà fait :

```bash
pip install pygame
````

4. **Lancer le jeu** :

```bash
python main.py
```

---

## Comment jouer

* **Déplacer le joueur** avec les flèches gauche, droite, haut et bas.
* **Éviter les voitures obstacles**. La collision retire une vie.
* **Ramasser les bonus fuel verts** pour gagner des points (+10).
* **Ramasser les Gold Fuel** (pompe à essence) pour doubler les points (+20).
* **Objectif** : survivre le plus longtemps possible et accumuler des points.
* **Progression** : tous les 30 secondes, la vitesse des obstacles augmente et un niveau supérieur est affiché.
* **Game Over** : lorsqu’il n’y a plus de vies, le jeu s’arrête et propose deux boutons : *Rejouer* ou *Quitter*.
* **Sons** : collision, ramassage de fuel normal ou Gold Fuel, et musique lors du ramassage du bonus spécifique.
  
## Lien video test jeu
https://drive.google.com/file/d/1pkpkT4QkJ32oG6rhtFYz0li8d1AYZ1jB/view?usp=sharing
