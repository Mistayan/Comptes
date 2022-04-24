#!-- coding:latin-1 --!#
##########################################  IMPORTS  ####################################################

import Message.Static_strings as Message
from Comptes.Compte import Compte
from Generateurs import Generateur as Gen
from Verifications import Securite as Secu
from Verifications import ErreurUtilisateurNonDefini


##########################################  Definition Classe  ####################################################
#
class CompteCourant(Compte):
    """
        Cree un compte avec des possibilites de retraits sous le seuil de 0.0.
        A chaque retrait, si l'utilisateur possede un solde n�gatif :
         on apposera des frais �quivalents aux taux classiques en vigueur (12% de la somme retir�e)

        ARGUMENTS :
         autorisation : int/float
         interet_debiteur : int/float
         agios : int (12, pour 12% par exemple)
    """

    _autorisation_decouvert: float
    _pourcentage_agios: float
    __coup_de_pouce: bool = True  # On autorise un retrait a decouvert par mois, sans frais. ;)

    #
    ##########################################  __init__  ####################################################
    def __init__(self, autorisation: float = 50, agios: float = 4.73, **extra):
        if hasattr(extra, "nom"):
            nom = extra.get("nom")
            if nom == "" or nom == "Anonymous":
                raise ErreurUtilisateurNonDefini(self)

        super().__init__(**extra)
        self._autorisation_decouvert = autorisation if autorisation >= 0 else 0

        if agios >= 50 or agios <= 5:
            agios = 5
        self._pourcentage_agios = agios / 100

        # print(f"Ce compte est de type CompteCourant, avec autorisation de decouvert de"
        #      f" {self._autorisation_decouvert}{self.monnaie}, "
        #      f"et un taux d'int�r�ts de {self._pourcentage_agios}%")

    #
    ##########################################  Fonctions Normale  ####################################################
    def retrait(self, valeur: float, autorisation: int = 0):
        """
        Surcharge de la m�thode m�re pour pouvoir appliquer l'autorisation de decouvert.
         Appel ensuite la m�thode de la classe m�re avec les arguments suppl�mentaires,
        Et enfin, nous appliquerons des agios si l'utilisateur �tait � 0 ou moins avant son retrait
        (ou sa tentative de retrait).
        """

        super().retrait(valeur, autorisation=self._autorisation_decouvert)
        #  TODO : pour etre plus gentil avec nos clients, on pourrait rajouter un if ? *wink* (et donc changer docs)
        self.appliquer_agios()

    def appliquer_agios(self):
        """
           Si l'utilisateur effectue un retrait lors du decouvert.... on appliquera cette m�thode !
            L'on consid�rera qu'� 0 euro, nous sommes d�j� � decouvert, n'ayant pas les capacit�s de retrait suffisantes
               On lui �vitera cependant les frais de retraits lors du premier �v�nement qui l'aura mis en n�gatif
               (une seule fois)
            Attention ! Hors 'coup de pouce', CHAQUE op�ration �-decouvert appliquera des frais. [Sujet de l'exercice]
        """
        if self._solde > 0:
            pass
        elif self._solde < 0 and self.__coup_de_pouce is True:  # En n�gatif et pas encore utilis� le coup de pouce ?
            self.__coup_de_pouce = False
        else:
            # Nous avons donc un d�pensier .... Il va payer !
            facturation = abs(self._solde * (self._pourcentage_agios / 100))
            # print(f"Votre compte va �tre d�bit� de {facturation}{self.monnaie},"
            #       f" dans le cadre de notre politique de retraits.")
            self._solde = self._solde - facturation
            self.afficher_solde()
        return self._solde

    #
    ##########################################  Fonctions Magiques  ####################################################

    def __str__(self) -> str:  # Surcharge
        """
        Permet de renvoyer les informations du compte au format str(json)
        """
        # Mais on appelle quand m�me maman pour r�cup�rer ses informations.
        infos_parent = super().__str__()
        infos_enfant = f"\"autorisation\":\"{self._autorisation_decouvert}\"," \
                       f"\"interets\":\"{self._pourcentage_agios}\"," \
                       f"\"pouce\":\"{self.__coup_de_pouce}\"" \
                       "}"
        return infos_parent + infos_enfant


##########################################  Fonction test_module  ####################################################


if __name__ == '__main__':
    print(Message.EXECUTE)
