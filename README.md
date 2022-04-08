# Exercice autour de la Programation Orientée Objet

Aujourd'hui, le thème est la Comptabilité !

## Sujet

Ecrire un programme qui implémente en POO un fonctionnement bancaire basique :  

- une classe Compte 
    - **attributs :** numeroCompte, nomProprietaire, solde  
    - **méthodes :** retrait, versement, afficherSolde  

- une classe fille CompteCourant, qui ajoute une gestion du découvert (montant maximum négatif 
possible) et des agios (pénalité de X % si le solde est inférieur à zéro) :  
    - **attributs :** autorisationDecouvert, pourcentageAgios  
    - **méthodes :** appliquerAgios  

- une classe fille CompteEpargne, qui ajoute :  
    - **attributs :** pourcentageInterets  
    - **méthodes :** appliquer Interets  

 

Le programme doit demander à l’utilisateur le compte concerné (« courant » ou « epargne ») et le montant 
de la transaction (positif pour un versement, négatif pour un retrait)  

Chaque appel de méthode doit afficher le solde avant opération, le détail de l’opération et le solde après 
opération. On suppose pour la simplicité de l’exercice que chaque modification du solde applique les agios 
ou intérêts du compte modifié. 

## Livraison
 
Réalisez un fork de ce dépôt.
Implémentez votre code
Puis réalisez une merge request afin de livrer votre code au formateur. 
Ne vous tracassez pas avec des branches git.
