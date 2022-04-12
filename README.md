# Comment utiliser ce module :

Il est fortement conseillé d'utiliser Main.py

  Une interface vous guidera pas à pas pour la création et la gestion de vos comptes.
  Vous pouvez utiliser des arguments pour effectuer
  rapidement plusieurs opérations successives.

  ###Menu principal :
Suivez les instructions et laissez-vous guider pour une experience utilisateur

### Disclaimer:
Aucun des fichiers créé localement n'est représentatif du système réellement
mis en place pour la gestion de la persistance des données.\
Ils sont générés comme simples données éducatives.

## Sujet de l'exercice

Ecrire un programme qui implémente en POO un fonctionnement bancaire basique :

- une classe Compte
    - **attributs :** numeroCompte, nomProprietaire, solde
    - **méthodes :** retrait, versement, afficher_solde

- une classe fille CompteCourant, qui ajoute une gestion du découvert (montant maximum négatif possible) et des agios (
  pénalité de X % si le solde est inférieur à zéro) :
    - **attributs :** autorisationDecouvert, pourcentageAgios
    - **méthodes :** appliquerAgios

- une classe fille CompteEpargne, qui ajoute :
    - **attributs :** pourcentageInterets
    - **méthodes :** appliquer Interets

Le programme doit demander à l’utilisateur le compte concerné (« courant » ou « epargne ») et le montant de la
transaction (positif pour un versement, négatif pour un retrait)

Chaque appel de méthode doit afficher le solde avant opération, le détail de l’opération et le solde après opération. On
suppose pour la simplicité de l’exercice que chaque modification du solde applique les agios ou intérêts du compte
modifié.

