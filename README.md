## Projet 4: gestionnaire de tournoi d'échecs
Version Beta d'un projet de gestion de tournoi d'échecs, qui implémente les tournois "suisses"

***

### Installation et lancement
Se placer dans un dossier de travail vide et récupérer le code:
```
$ git clone https://github.com/martinschongauer/project_4_chess
```

Créer et activer un environnement Python pour ce projet:
```
$ python3 -m venv env
$ source env/bin/activate
```

Installer les dépendances listées dans le fichier requirements.txt:
```
$ pip install -r requirements.txt
```

Lancer le programme:
```
$ python3 main.py
```

Le rapport est généré par flake8:
```
$ flake8 --format=html --htmldir=flake-report
```

(flake8 est configuré à l'aide du fichier setup.cfg)

### Usage général
Le main entre directement dans la boucle principale du "controller" du modèle MVC. Cette dernière prend les commandes de l'utilisateur, 
que l'on peut obtenir en tapant "help", et qui sont affichées au lancement du programme. Le fichier ChessDB contient toute la base de
données, et la version fournie dans ce dépôt contient huit joueurs, un tournoi fini et un tournoi en cours qui permettent de tester
rapidement les commandes pour un nouvel utilisateur.
