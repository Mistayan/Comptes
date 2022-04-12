#!-- encoding:latin-1 --!#

##########################################  IMPORTS  #####################################################
from _md5 import md5
from abc import ABCMeta, abstractmethod
from imports import *
import Messages.Static_strings as Message
##########################################  Globales  #####################################################

global DEBUG


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
                 monnaie: str = u"\x24", **extra):
        super().__init__()  # On initialise la classe 'racine'... m�me si �a sert � rien dans ce cas-l�.

        ################################### Initialisation des variables publiques ##################################
        self.monnaie = monnaie
        self.nom_proprietaire = "Anonymous" if nom is None else nom

        ################################### Initialisation des variables priv�es ##################################
        self._solde = solde_initial if solde_initial >= 0 else 0

        while self._numero_compte is None:
            un_num = Secu.Verif.dispo(compte=num_compte)
            if un_num is False or type(un_num) is str:
                num_compte = Gen.chaine_aleatoire(longueur=10, style=Message.DIGITS)
            else:
                self._numero_compte = num_compte

        ################################### Initialisation des variables prot�g�es ##################################
        if extra_secu:
            self.__code = Gen.chaine_aleatoire(longueur=6, style=Message.HEXADECIMAL) if code == '' else code
        else:
            self.__code = Gen.chaine_aleatoire(longueur=4, style=Message.DIGITS)

        if Message.DEBUG:
            message_nouveau_compte = f"Un compte pour {self.nom_proprietaire}," \
                                     f" avec le n� de compte: {self._numero_compte}," \
                                     f"avec un solde initial de {self._solde}{self.monnaie}," \
                                     f"et le code secret: {self.__code}.\n vient d'etre cr��."
            print(message_nouveau_compte)
        else:
            print(f"Votre compte n�{self._numero_compte}, avec le code: {self.__code} vient d'�tre cr��.")
        # self._enregistrer()

    ##########################################  Fonctions Priv�es  #####################################################
    ##########################################  Wrappers #####################################################

    def __valeurs(self, func):

        def verif(num):
            if type(num) is not (int, float):
                Gen.fraude(self._numero_compte, str(func), str(num))
            return func(num)

        return verif

    ##########################################  Fonctions Partag�es  ###################################################

    def retrait(self, valeur: float, autorisation=0):
        """
        Permet le retrait d'une somme demand�e
            Si une valeur non positive est rentr�e (tentative de fraude), l'op�ration est enregistr�e dans fraudes.txt

            Si l'utilisateur ne donne pas le bon code.... Pas de sous !

            Si le solde est insuffisant, l'op�ration est refus�e, avec un message d'erreur ;
            Exception faite : Si un compte courant a une autorisation adapt�e.
        """

        if isinstance(valeur, str):
            return print(Message.ONLY_NUMBERS_ERROR)
        elif valeur < 0:
            return print(Message.SOLDE_ERROR_MSG)
        print(f"Vous souhaitez retirer: {valeur}{self.monnaie}")

        # En mode curieux, on ne demandera pas le code, sauf si vous d�sactivez l'option (Messages/Static_strings.py).
        if Message.NO_CODE:
            pass
        else:
            code = input(Message.ASK_CODE)
            if code != self.__code:
                Gen.fraude(self._numero_compte, "code_invalide", code)
                return print("Code Faux !")
        # fin if DEBUG
        if self._solde + autorisation < valeur:
            return print("Solde insuffisant!")
        self._solde -= valeur
        print(f"Un retrait de {valeur}{self.monnaie} a �t� effectue")
        Gen.historique(self._numero_compte, valeur)
        self.afficher_solde()

    def versement(self, valeur: float) -> None:
        """ Permet l'ajout d'une somme demand�e sur le compte
            Si une valeur non num�raire est rentr�e (tentative de fraude), l'op�ration est enregistr�e dans fraudes.txt

        """
        if isinstance(valeur, str):
            return print(Message.ONLY_NUMBERS_ERROR)
        if type(valeur) is not (int or float):
            Gen.fraude(self._numero_compte, "versement")
            return print(Message.NEGATIF_MSG)
        valeur = abs(valeur)  # esquiver

        self._solde += valeur
        print(f"Un depot de {valeur}{self.monnaie} a ete effectue")
        Gen.historique(self._numero_compte, valeur)
        self.afficher_solde()

    def afficher_solde(self) -> None:
        """Affiche le solde actuel
        """
        print(f"Votre solde: {self._solde}{self.monnaie}")

    ##########################################  Fonctions Sp�ciales  #################################################
    def _connect(self) -> bool:
        """
        Permettra (TBD) de se connecter sur un compt� d�j� existant (d�j� possible en interface ?)
        """
        # TODO fonction _connect, pour g�rer l'acc�s � un compte utiliser mysql ?
        pass

    def _recuperer_code(self) -> None:
        """ Permet de r�cup�rer un code oubli�
        """
        # TODO: g�rer une interface externe permettant de v�rifier si c'est "Manu, Le Vrai"

        print(self.__code)  # Aller, on est gentil ;)

    def __enregistrer(self, un_compte):  # DEPRECATED : Ne pas utiliser...
        """ Permet la sauvegarde d'un compte, pour la persistance des donn�es.

            #format:
            {nom:compte:solde:monnaie:code:type:arg1:arg2:pouce:arg4}

        """
        # TODO: _enregistrer : faire en sorte que les informations des enfants puissent �tre enregistr�es.

        if Secu.Verif.dispo(compte=self._numero_compte) is True:
            with Gen.my_open("Comptes.json", "a+") as f:  # Ajouter le compte au fichier
                to_save = str(self)
                try:  # CompteCourant
                    to_save += ""
                except:
                    pass

                try:  # CompteEpargne
                    to_save
                except:
                    pass
                """# if anti-json:
                # print(to_save, file=f)"""
        f.close()

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
                la comparaison de deux comptes  pour savoir si le propri�taire est le m�me
                la comparaison � un nombre
        """
        # TODO: ajouter une s�curit� suppl�mentaire pour assignation.
        if isinstance(autre, int) or isinstance(autre, float):
            return self._solde == autre
        elif self.nom_proprietaire == autre.nom_proprietaire:
            return True

        return (f"assignation de {type(autre)} � {type(Compte)} impossible.\n\
                                Compte / int / float, accept�s)")

    def __gt__(self, other) -> int:  # int plus rapide que bool <- une classe en moins � instancier
        """
        '>' permet la comparaison du solde avec un nombre (int ou float)
        """
        if isinstance(int, other) or isinstance(float, other):
            return self._solde > other
        print("Impossible de comparer a autre chose qu'un nombre.")

    def __ge__(self, other) -> int:  # int plus rapide que bool <- une classe en moins � instancier
        """
        permet la comparaison via '>=' du solde avec un nombre (int ou float)
        """
        if isinstance(int, other) or isinstance(float, other):
            return self._solde > other
        print("Impossible de comparer a autre chose qu'un nombre.")

    def __lt__(self, other) -> int:  # int plus rapide que bool <- une classe en moins � instancier
        """
        permet la comparaison via '<' du solde avec un nombre (int ou float)
        """
        if isinstance(int, other) or isinstance(float, other):
            return self._solde > other
        print("Impossible de comparer a autre chose qu'un nombre.")

    def __le__(self, other) -> int:  # int plus rapide que bool <- une classe en moins � instancier
        """
        permet la comparaison via '<=' du solde avec un nombre (int ou float)
        """
        if isinstance(int, other) or isinstance(float, other):
            return self._solde > other
        print("Impossible de comparer a autre chose qu'un nombre.")

    def __str__(self):
        """
        Renvoie les informations du compte en clair (sauf le mdp, qui est hash�), pr�format� pour JSON,
        dans le cadre d'une int�gration future avec interfacing

        remarque : Ne pas oublier de r�cup�rer les __str__ du child pour finir la chaine. Sinon, fermer avec "}"
        """
        cat_string = "{\n" + \
                     f"\"nom\":{self.nom_proprietaire},\n\"solde\":\"{self._solde}\",\n" \
                     f"\"num_compte\":\"{self._numero_compte}\",\n" \
                     f"\"code\":\"{md5(self.__code.encode('utf-8')).hexdigest()}\",\n\"monnaie\":\"{self.monnaie}\",\n"

        # a_retourner = cat_string  ##TODO: si jamais le client ne souhaite pas le json, formatage classique x:x:x:x
        return cat_string


##########################################  Fonction test_module  ####################################################
if __name__ == '__main__':
    print(EXECUTE)
