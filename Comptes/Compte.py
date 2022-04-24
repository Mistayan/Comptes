#!-- encoding:latin-1 --!#

##########################################  IMPORTS  #####################################################
from _md5 import md5
from abc import ABCMeta, abstractmethod
import Message.Static_strings as Message
import Generateurs as Generer
import Verifications as Securite
from logging import debug, info, warning, error, basicConfig


##########################################  Globales  #####################################################

##########################################  Definition classe  #####################################################


class Compte(metaclass=ABCMeta):  # Instancier avec ABC, permet d'utiliser @abstractmethod
    """Un compte de base. Ne peut �tre instanci�. (ABC)\n
    Aucun argument n'est obligatoire

    :nom\n
    Si aucun nom n'est donn�, l'application accepte l'anonymat.
    Pour des raisons �thiques, sera cependant obligatoire pour un compte courant.\n

    :num_compte\n
    Si un num�ro de compte est donn�, on s'assurera qu'il corresponde au format l�gal, et qu'il n'existe pas d�j�.
    Si le num�ro de compte donn� existe, on chargera le compte dans l'interface.
    Si aucun num�ro de compte n'est renseign� (nouveau client), on en g�n�rera un (qui n'existe pas encore).

    :solde_initial\n
    Si aucune valeur ou une valeur erron�e est renseign�e, initialise � 0.
    Si une valeur est renseign�e, on initialisera � cette valeur.

    :code\n
    Parce que nous ferions tout pour nos clients, on laisse la possibilit� d'avoir une protection forte
    Si aucun argument n'est renseign�, g�n�re un code

    :extra_secu\n
    Parce que la s�curit� est importante pour nos clients, nous leur proposons une offre de s�curit� renforc�e.
    Si activ�, le code de compte sera en HEXADECIMAL d'une longueur de 6
    """

    nom_proprietaire: str
    monnaie: str
    _numero_compte: str = None  # On initialise � None, au cas o� le num_compte fournit est invalide, ou d�j� pris.
    _solde: float
    __code: str

    @abstractmethod  # NON, pas le droit d'appeler Compte seul ! CompteXxxxxx obligatoire
    def __init__(self, nom: str = None, num_compte: str = None,
                 solde_initial: int = 0, code: str = '', extra_secu: bool = False,
                 monnaie: str = u"\x42", force=False, **extra):

        ################################### Initialisation des variables publiques ##################################
        self.monnaie = monnaie
        self.nom_proprietaire = "Anonymous" if nom is None else nom

        ################################### Initialisation des variables priv�es ##################################
        self._solde = solde_initial if solde_initial >= 0 else 0

        while self._numero_compte is None:
            if not force:  # Force n'est utile que pour l'init de l'application.
                un_num = Securite.dispo(num_compte)
                if un_num is False or type(un_num) is str:
                    num_compte = Generer.chaine_aleatoire(longueur=10, style=Message.DIGITS)
            else:  # fonctionnement standard, hors init application.
                self._numero_compte = num_compte

        ################################### Initialisation des variables prot�g�es ##################################
        if not force:
            if extra_secu:
                self.__code = Generer.chaine_aleatoire(longueur=6, style=Message.HEXADECIMAL) if code == '' else code
            else:
                self.__code = Generer.chaine_aleatoire(longueur=4, style=Message.DIGITS)
        else:
            self.__code = code
        if Message.DEBUG:
            message_nouveau_compte = f"Un compte pour {self.nom_proprietaire}," \
                                     f" avec le n� de compte: {self._numero_compte}," \
                                     f"avec un solde initial de {self._solde}{self.monnaie}," \
                                     f"et le code secret: {self.__code}.\n vient d'etre cr��."
            info(message_nouveau_compte)

    ##########################################  Fonctions Priv�es  #####################################################

    ##########################################  Fonctions Partag�es  ###################################################

    def retrait(self, valeur: float, autorisation=0) -> float:
        """
        Permet le retrait d'une somme demand�e
            Si une valeur non positive est rentr�e (tentative de fraude), l'op�ration est enregistr�e dans fraudes.txt

            Si l'utilisateur ne donne pas le bon code.... Pas de sous !

            Si le solde est insuffisant, l'op�ration est refus�e, avec un message d'erreur ;
            Exception faite : Si un compte courant a une autorisation adapt�e.
        """

        if isinstance(valeur, str):
            try:
                valeur = float(valeur)
            except :
                print("Error")
        if not (isinstance(valeur, int) or isinstance(valeur, float)):
            raise ValueError(Message.ERREUR_NOMBRES)

        # En mode curieux, on ne demandera pas le code, sauf si vous d�sactivez l'option (Message/Static_strings.py).
        if Message.NO_CODE:
            pass
        else:
            code = input(Message.ASK_CODE)
            if code != self.__code:
                Generer.fraude(self._numero_compte, "code_invalide", code)
                info("Code Faux !")
        # fin if NO_CODE

        if self._solde + autorisation < valeur:
            info("Solde insuffisant!")
            return self._solde
        self._solde -= valeur
        info(f"Un retrait de {valeur}{self.monnaie} a �t� effectue")
        Generer.historique(self._numero_compte, valeur)
        self.afficher_solde()
        return self._solde

    def versement(self, valeur: float) -> float:
        """ Permet l'ajout d'une somme demand�e sur le compte
            Si une valeur non num�raire est rentr�e (tentative de fraude), l'op�ration est enregistr�e dans fraudes.txt

        """
        if isinstance(valeur, str):
            try:
                valeur = float(valeur)
            except :
                print("Error")
        if not (isinstance(valeur, int) or isinstance(valeur, float)):
            raise ValueError(Message.ERREUR_NOMBRES)

        valeur = abs(valeur)  # esquiver

        self._solde += valeur
        info(f"Un depot de {valeur}{self.monnaie} a ete effectue")
        Generer.historique(self._numero_compte, valeur)
        self.afficher_solde()
        return self._solde

    def afficher_solde(self) -> None:
        """Affiche le solde actuel
        """
        print(f"Votre solde: { self._solde:.2f}{self.monnaie}")

    ##########################################  Fonctions Sp�ciales  #################################################
    def connect(self, num, code) -> bool:
        """
        Permet de se connecter sur un compt� deja existant, a condition que les arguments fournis soient valides
        """
        if self.__code == code and self._numero_compte == num:
            return True
        return False

    def _recuperer_code(self) -> None:
        """ Permet de r�cup�rer un code oubli�
        """
        # TODO: g�rer une interface externe permettant de v�rifier si c'est "Manu, Le Vrai"

        print(self.__code)  # Aller, on est gentil ;)

    ##########################################  Fonctions Magiques  ####################################################

    ##########################################  OPERATIONS  ####################################################

    def __add__(self, num):
        """ Permet un versement via '+'  avec un nombre (int ou float).
        """
        return self.versement(num)

    def __sub__(self, num):
        """ Permet le retrait via '-'  avec un nombre (int ou float).
        """
        return self.retrait(num)

    ##########################################  COMPARAISONS  ####################################################
    def __eq__(self, autre):
        """ '==' permet:
                la comparaison de deux comptes pour savoir si le propri�taire est le m�me
                la comparaison � un nombre
        """
        # TODO: ajouter une s�curit� suppl�mentaire pour assignation.
        if isinstance(autre, int) or isinstance(autre, float):
            return self._solde == autre
        elif self.nom_proprietaire == autre.nom_proprietaire:
            return True

        raise TypeError(f"assignation de {type(autre)} � {type(Compte)} impossible.\n\
                                Compte / int / float, accept�s)")

    def __gt__(self, other) -> int:  # int plus rapide que bool <- une classe en moins � instancier
        """
        '>' permet la comparaison du solde avec un nombre (int ou float)
        """
        if isinstance(int, other) or isinstance(float, other):
            return self._solde > other
        raise TypeError

    def __ge__(self, other) -> int:  # int plus rapide que bool <- une classe en moins � instancier
        """
        permet la comparaison via '>=' du solde avec un nombre (int ou float)
        """
        if isinstance(int, other) or isinstance(float, other):
            return self._solde > other
        raise TypeError

    def __lt__(self, other) -> int:  # int plus rapide que bool <- une classe en moins � instancier
        """
        permet la comparaison via '<' du solde avec un nombre (int ou float)
        """
        if isinstance(int, other) or isinstance(float, other):
            return self._solde > other
        raise TypeError

    def __le__(self, other) -> int:  # int plus rapide que bool <- une classe en moins � instancier
        """
        permet la comparaison via '<=' du solde avec un nombre (int ou float)
        """
        if isinstance(int, other) or isinstance(float, other):
            return self._solde > other
        raise ValueError()

    def __str__(self):
        """
        Renvoie les informations du compte en clair (sauf le mdp, qui est hash�), pr�format� pour JSON,
        dans le cadre d'une int�gration future avec interfacing

        /!\\ Remarque /!\\: Ne pas oublier de r�cup�rer les __str__ du child pour finir la chaine.
         Sinon, fermer avec "}"
        """
        cat_string = "{" \
                     f'"nom":"{self.nom_proprietaire}",' \
                     f'"solde":"{self._solde}",' \
                     f'"num_compte":"{self._numero_compte}",' \
                     f'"code":"{self.__code}",' \
                     f'"monnaie":"{self.monnaie}",'

        # a_retourner = cat_string  ##TODO: si jamais le client ne souhaite pas le json, formatage classique x:x:x:x
        return cat_string


##########################################  Fonction test_module  ####################################################
if __name__ == '__main__':
    print(Message.EXECUTE)
