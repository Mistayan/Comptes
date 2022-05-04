# Comment utiliser ce module :

Il est fortement conseille d'utiliser Main.py

Une interface vous guidera pas a pas pour la creation et la gestion de vos comptes. Vous pouvez
utiliser des arguments pour effectuer rapidement plusieurs operations successives.

### Menu principal :

Suivez les instructions et laissez-vous guider pour une experience utilisateur

### Disclaimer:

Aucun des fichiers cree localement n'est representatif du systeme reellement mis en place pour la
gestion de la persistance des donnees.\
Ils sont generes comme simples donnees educatives.

## Sujet de l'exercice

Ecrire un programme qui implemente en POO un fonctionnement bancaire basique :

- une classe Compte
    - **attributs :** numeroCompte, nomProprietaire, solde
    - **methodes :** retrait, versement, afficher_solde

- une classe fille CompteCourant, qui ajoute une gestion du decouvert (montant maximum negatif
  possible) et des agios (
  penalite de X % si le solde est inferieur a zero) :
    - **attributs :** autorisationDecouvert, pourcentageAgios
    - **methodes :** appliquerAgios

- une classe fille CompteEpargne, qui ajoute :
    - **attributs :** pourcentageInterets
    - **methodes :** appliquer Interets

Le programme doit demander a l’utilisateur le compte concerne (« courant » ou « epargne ») et le
montant de la transaction (positif pour un versement, negatif pour un retrait)

Chaque appel de methode doit afficher le solde avant operation, le detail de l’operation et le solde
apres operation. On suppose pour la simplicite de l’exercice que chaque modification du solde
applique les agios ou interets du compte modifie.

