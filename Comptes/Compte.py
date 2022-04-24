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
    """Un compte de base. Ne peut etre instancie. (ABC)\n
    Aucun argument n'est obligatoire

    :nom\n
    Si aucun nom n'est donne, l'application accepte l'anonymat.
    Pour des raisons ethiques, sera cependant obligatoire pour un compte courant.\n

    :num_compte\n
    Si un numero de compte est donne, on s'assurera qu'il corresponde au format legal, et qu'il n'existe pas déjà.
    Si le numero de compte donné existe, on chargera le compte dans l'interface.
    Si aucun numero de compte n'est renseigne (nouveau client), on en generera un (qui n'existe pas encore).

    :solde_initial\n
    Si aucune valeur ou une valeur erronee est renseignee, initialise a 0.
    Si une valeur est renseignee, on initialisera a cette valeur.

    :code\n
    Parce que nous ferions tout pour nos clients, on laisse la possibilite d'avoir une protection forte
    Si aucun argument n'est renseigne, genere un code

    :extra_secu\n
    Parce que la securite est importante pour nos clients, nous leur proposons une offre de securite renforcee.
    Si active, le code de compte sera en HEXADECIMAL d'une longueur de 6
    """

    nom_proprietaire: str
    monnaie: str
    _numero_compte: str = None  # On initialise à None, au cas ou le num_compte fournit est invalide, ou deja pris.
    _solde: float
    __code: str

    @abstractmethod  # NON, pas le droit d'appeler Compte seul ! CompteXxxxxx obligatoire
    def __init__(self, nom: str = None, num_compte: str = None,
                 solde_initial: int = 0, code: str = '', extra_secu: bool = False,
                 monnaie: str = u"\x42", force=False, **extra):

        ################################### Initialisation des variables publiques ##################################
        self.monnaie = monnaie
        self.nom_proprietaire = "Anonymous" if nom is None else nom

        ################################### Initialisation des variables privees ##################################
        self._solde = solde_initial if solde_initial >= 0 else 0

        while self._numero_compte is None:
            if not force:  # Force n'est utile que pour l'init de l'application.
                valeur_verif = Securite.dispo(num_compte)
                if valeur_verif is False or type(valeur_verif) is str:
                    num_compte = Generer.chaine_aleatoire(longueur=10, style=Message.DIGITS)
                elif valeur_verif is True:  # fonctionnement standard, hors init application.
                    self._numero_compte = num_compte
            else:  # fonctionnement standard, hors init application.
                self._numero_compte = num_compte

        ################################### Initialisation des variables protegees ##################################
        if not force:
            if extra_secu:
                self.__code = Generer.chaine_aleatoire(longueur=6, style=Message.HEXADECIMAL) if code == '' else code
            else:
                self.__code = Generer.chaine_aleatoire(longueur=4, style=Message.DIGITS)
        else:
            self.__code = code
        message_nouveau_compte = f"Le compte pour {self.nom_proprietaire}," \
                                 f" avec le n° de compte: {self._numero_compte}," \
                                 f"et le code secret: {self.__code}.\n vient d'etre cree.\n" \
                                 f"Nous vous conseillons TRES FORTEMENT de les noter !"

        if 'new' in extra and extra['new'] is True:  # Ne doit etre vrai que lors de la creation d'un compte dans l'app
            print(message_nouveau_compte)
            self.__code = md5(str(self.__code).encode("utf-8")).hexdigest()

    ##########################################  Fonctions Privées  #####################################################

    ##########################################  Fonctions Partagées  ###################################################

    def retrait(self, valeur: float, autorisation=0) -> float:
        """
        Permet le retrait d'une somme demandée
            Si une valeur non positive est rentrée (tentative de fraude), l'operation est enregistree dans fraudes.txt

            Si l'utilisateur ne donne pas le bon code.... Pas de sous !

            Si le solde est insuffisant, l'opération est refusee, avec un message d'erreur ;
            Exception faite : Si un compte courant a une autorisation adaptee.
        """

        if isinstance(valeur, str):
            try:
                valeur = float(valeur)
            except :
                print("Error")
        if not (isinstance(valeur, int) or isinstance(valeur, float)):
            raise ValueError(Message.ERREUR_NOMBRES)

        # En mode curieux, on ne demandera pas le code, sauf si vous désactivez l'option (Message/Static_strings.py).
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
        info(f"Un retrait de {valeur}{self.monnaie} a été effectue")
        Generer.historique(self._numero_compte, "retrait", valeur)
        self.afficher_solde()
        return self._solde

    def versement(self, valeur: float) -> float:
        """ Permet l'ajout d'une somme demandee sur le compte
            Si une valeur non numeraire est rentree (tentative de fraude), l'operation est enregistree dans fraudes.txt

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
        Generer.historique(self._numero_compte, "versement", valeur)
        self.afficher_solde()
        return self._solde

    def afficher_solde(self) -> None:
        """Affiche le solde actuel
        """
        print(f"Votre solde: { self._solde:.2f}{self.monnaie}")

    def get_num(self):
        """ Retourne le numero du compte. """
        return self._numero_compte
    ##########################################  Fonctions Spéciales  #################################################
    def connect(self, num, code) -> bool:
        """
        Permet de se connecter sur un compte deja existant, a condition que les arguments fournis soient valides
        """
        if self.__code == code and self._numero_compte == num:
            return True
        return False

    def _recuperer_code(self) -> None:
        """ Permet de recuperer un code oublie
        """
        print(self.__code)  # Aller, on est gentil... OU PAS ! ;)

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

    ##########################################  CASTINGS  ####################################################
    def __str__(self):
        """
        Renvoie les informations du compte en clair (sauf le mdp, qui est hashe), préformaté pour JSON,
        dans le cadre d'une integration future avec interfacing

        /!\\ Remarque /!\\: Ne pas oublier de récuperer les __str__ du child pour finir la chaine.
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
