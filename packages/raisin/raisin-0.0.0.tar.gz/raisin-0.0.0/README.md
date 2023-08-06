# Dans module raisin.py:
## Dans class Str:
### Dans def indice:
* dans le dictionaire 'correspondance', remplacer les "?" par le bon symbole unicode
### Dans def exposant:
* dans le dictionaire 'correspondance', remplacer les "?" par le bon symbole unicode
## Dans class Timeout:
### Dans def __enter__:
#### Dans if "win" in sys.platform:
* remplacer le raise par un bloc d'instruction qui permete d'avoir sous windaube, un comportement similaire a linux l'orsque l'on utilise cet objet
#### Dans else:
* faire en sorte que ca fonctionne aussi l'orsque un thread utilise le timeout. Pour le moment, cela fonctionne uniquement lorsque la branche principale du programme utilise cet objet.


# Dans module geometry.py:
## Dans class Function:
* tout recoder en se basant le plus possible sur _Simple_Function
### Dans def _symbolic:
* il faut aller lire le code source de la fonction pour vraiment comprende ce qu'elle fait
            afin d'en extraire une equation formelle qui la caracterise
* la methode de passer des parametres symbolic pour voir ce que la fonction ressort, ne fonctionne pas tout
            le temps, par example si il y a dur random, du tem qui intervient, une lecture dans un fichier...
            bref, il faut trouver un moyen de s'assurer que le resultat est juste!
### Dans def _regressi:
* il faut trouver une methode efficace pour trouver un model de fonction formel
        sur un nuage de points afin de passer d'une fonction dont on ne connait pas le mecanisme
        a une fonction dont on connait l'expression formelle. Il y aura surement du moindre carre tout ca tout ca


# Dans module csvreader.py:
## Dans def _find_separator:
* trouver le meilleur separateur possible

# Dans module setup.py:
## Dans class Storage_Space:
* remplir les methode qui sont vides
## Dans class Modules:
### Dans def test_modules:
* trouver un test qui permet pour un module donne fixe, de verifier que ce module est bien valide
            chaque module peut comporter son propre test
