#   Projet de compilation

Vous utiliserez ce dépôt comme point de départ pour votre projet de
compilation.

# Noms du binôme

- El Ammari Nordine
- Arthur Assima

##  Instructions pour rendre votre travail avec gitlab

Pour permettre à votre chargé de TD de suivre votre travail sur ce projet :

-   *forkez* ce dépôt (bouton _Fork_),
-   dans le dépôt *forké*, ajoutez votre chargé de TD aux membres du
    projet avec l’accès _Developer_,
-   éditez ce fichier `README.md` pour indiquer vos noms (membres du
    binôme) et supprimer ce paragraphe d’instructions.


##  Compte-rendu

À la fin de votre projet, ce `README.md` devra contenir un
compte-rendu du travail effectué : quelle partie du langage vous avez
couverte, quels choix vous avez faits, quel est l’état d’avancement de
vos différents outils, etc.

# Pretty-printer 

- Lancer la commande suivante :

```code
python3 evaluator.py filename.json
```

# Interprète

- Lancer la commande suivante :

```code
python3 interpreter.py filename.json
```
# Compilateur

- Lancer les commande suivantes:
``` code
python3 compiler.py 01-expressions.json > lib/compiled.c
cd lib
make
./compiled
```
