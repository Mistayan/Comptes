#!-- coding:utf-8 --!#

##########################################  IMPORTS  #####################################################

import Generators.Generateurs as Gen
import Verifications.Base as Secu
from string import digits as DIGITS
from string import hexdigits as HEXADECIMAL
from Verifications.ErrorsHandling import *

##########################################  Globales  #####################################################


"fonctionnalités"
##########################################  Definition classe  #####################################################


class Compte(object):
    """Créer un compte de base.\n
    Aucun argument n'est obligatoire

    :nom\n
    Si aucun nom n'est donné, l'application accepte l'anonymat.
    Pour des raisons éthiques, sera cependant obligatoire pour un compte courant.\n

    :num_compte\n
    Si un numéro de compte est donné, on s'assurera qu'il corresponde au format légal, et qu'il n'existe pas déjà.
    Si le numéro de compte donné existe, on chargera le compte dans l'interface.
    Si aucun numéro de compte n'est renseigné (nouveau client), on en génèrera un (qui n'existe pas encore).

    :solde_initial\n
    Si aucune valeur ou une valeur erronée est renseignée, initialise à 0.
    Si une valeur est renseignée, on initialisera à cette valeur.

    :code\n
    Parce que nous ferions tout pour nos clients, on laisse la possibilité d'avoir une protection forte
    Si aucun argument n'est renseigné, génère un code

    :extra_secu\n
    Parce que la sécurité est importante pour nos clients, nous leur proposons une offre de sécurité renforcée.
    Si activé, le code de compte sera en HEXADECIMAL d'une longueur de 6
    """
    nom_proprietaire: str
    monnaie: str
    _numero_compte: str = None  # On initialise à None, au cas où le num_compte fournit est invalide.
    _solde: float
    __code: str

    def __init__(self, nom: str = None, num_compte: str = 'None',
                 solde_initial: int = 0, code: str = '', extra_secu: bool = False,
                 monnaie: str = "€", **extra):
        super().__init__()  # On initialise la classe objet... même si ça sert à rien dans ce cas-là.

        # Initialisation des variables publiques
        self.monnaie = monnaie
        self.nom_proprietaire = "Anonymous" if nom is None else nom

        # Initialisation des variables privées
        self._solde = solde_initial if solde_initial >= 0 else 0

        while self._numero_compte is None:
            un_num = Secu.Verif.dispo(compte=num_compte)
            if un_num is False or type(un_num) is str:
                num_compte = Gen.random_string(longueur=10, style=DIGITS)
            else:
                self._numero_compte = num_compte

        # Initialisation des variables protégées
        if extra_secu:
            self.__code = Gen.random_string(longueur=6, style=HEXADECIMAL) if code == '' else code
        else:
            self.__code = Gen.random_string(longueur=4, style=DIGITS) if code == '' else code

        print(f"Un compte pour {self.nom_proprietaire}, avec le n° de compte: {self._numero_compte}, \
              avec un solde initial de {self._solde}, \
              et le code secret: {self.__code} (Retenez-le bien), vient d'etre cree.")

    ##########################################  Fonctions Privées  #####################################################

    ##########################################  Fonctions Partagées  ###################################################

    def retrait(self, valeur: float, autorisation=0):
        """
        Permet le retrait d'une somme demandée
            Si une valeur non positive est rentrée (tentative de fraude), l'opération est enregistrée dans fraudes.txt

            Si l'utilisateur ne donne pas le bon code.... Pas de sous !

            Si le solde est insuffisant, l'opération est refusée, avec un message d'erreur ;
            Exception faite: Si un compte courant a une autorisation adaptée.
        """
        if valeur < 0:
            Gen.fraude(self._numero_compte, "tentative_retrait")
            raise SoldeError("impossible de retirer une valeur negative sur le compte!")
        print(f"Vous souhaitez retirer: {valeur}{self.monnaie}")
        code = input("Quel est votre code?")
        if code != self.__code:
            Gen.fraude(self._numero_compte, "code_invalide")
            return print("Code Faux !")
        self.afficherSolde()
        if self._solde + autorisation < valeur:
            return print("Solde insuffisant!")
        self._solde -= valeur
        print(f"Un retrait de {valeur}{self.monnaie} a été effectue")
        self.afficherSolde()

    def versement(self, valeur: float) -> None:
        """ Permet l'ajout d'une somme demandée sur le compte
            Si une valeur non positive est rentrée (tentative de fraude), l'opération est enregistrée dans fraudes.txt

        """
        if valeur < 0:
            Gen.fraude(self._numero_compte, "versement")
            raise ValueError("impossible de déposer une valeur negative sur le compte!")

        self.afficherSolde()
        self._solde += valeur
        print(f"Un depot de {valeur}{self.monnaie} a ete effectue")
        self.afficherSolde()

    def afficherSolde(self) -> None:
        """Affiche le solde actuel
        """
        print(f"Votre solde actuel: {self._solde}{self.monnaie}")

    ##########################################  Fonctions Spéciales  ####################################################
    def _recupererCode(self) -> None:
        """ Permet de récupérer un code oublié
        """
        # TODO: gérer une interface externe permettant de vérifier si c'est "Manu, Le Vrai"

        print(self.__code)  # Aller, on est gentil ;)

    def _enregistrer(self):
        """ Permet la sauvegarde d'un compte, pour la persistance des données.
        """
        # TODO: faire en sorte que ça marche, c'est mieux (ne fait pas grand chose... Mais au moins ça plante pas !)

        cpt = Secu.Verif.dispo(compte=self._numero_compte)
        if cpt is False:
            f = Gen.my_open("comptes.txt", 'a+')  # Ajouter le compte au fichier
            print(f"{self.nom_proprietaire}:{self._numero_compte}:{self._solde}:{self.monnaie}:{self.__code}", file=f)
        else:
            f = Gen.my_open("Comptes.txt", "w+")  # Modifier

    ##########################################  Fonctions Magiques  ####################################################
    def __add__(self, num):
        """ Permet un versement via '+'  avec un nombre (int ou float).
        """
        return self.versement(num)

    def __sub__(self, num):
        """ Permet le retrait via '-'  avec un nombre (int ou float).
        """
        return self.retrait(num)

    def __eq__(self, autre):
        """ '==' permet:
                la comparaison de deux comptes  pour savoir si le propriétaire est le même
                la comparaison à un nombre
        """
        # TODO: ajouter une sécurité supplémentaire pour assignation.
        if isinstance(autre, int) or isinstance(autre, float):
            return self._solde == autre
        elif self.nom_proprietaire == autre.nom_proprietaire:
            return True
        raise ValueError(f"assignation de {type(autre)} à {type(Compte)} impossible.\n\
                                Compte / int / float, acceptés)")

    def __gt__(self, other) -> int:  # int plus rapide que bool <- une classe en moins à instancier
        """
        '>' permet la comparaison du solde avec un nombre (int ou float)
        """
        if isinstance(int, other) or isinstance(float, other):
            return self._solde > other
        raise ValueError("Impossible de comparer a autre chose qu'un nombre.")

    def __ge__(self, other) -> int:  # int plus rapide que bool <- une classe en moins à instancier
        """
        permet la comparaison via '>=' du solde avec un nombre (int ou float)
        """
        if isinstance(int, other) or isinstance(float, other):
            return self._solde > other
        raise ValueError("Impossible de comparer a autre chose qu'un nombre.")

    def __lt__(self, other) -> int:  # int plus rapide que bool <- une classe en moins à instancier
        """
        permet la comparaison via '<' du solde avec un nombre (int ou float)
        """
        if isinstance(int, other) or isinstance(float, other):
            return self._solde > other
        raise ValueError("Impossible de comparer a autre chose qu'un nombre.")

    def __le__(self, other) -> int:  # int plus rapide que bool <- une classe en moins à instancier
        """
        permet la comparaison via '<=' du solde avec un nombre (int ou float)
        """
        if isinstance(int, other) or isinstance(float, other):
            return self._solde > other
        raise ValueError("Impossible de comparer a autre chose qu'un nombre.")


if __name__ == '__main__':
    cpt = Compte(nom="Julie Dubois", code="0000")
    cpt + 25
    cpt - 24
