#! coding:utf-8
""""
Editeur: Mistayan
Projet: Comptes-Bancaires
"""
##########################################  IMPORTS  ###############################################
from comptes import Compte
from messages import static_strings as msg
from vertifications import ErreurUtilisateurNonDefini


##########################################  Definition Classe  #####################################
#
class CompteCourant(Compte):
    """
        Cree un compte Courant avec des possibilites de retraits sous le seuil de 0.0.
        A chaque retrait, si l'utilisateur possede un solde negatif :
         on apposera des frais equivalents aux taux en vigueur pour ce compte.

        : ARGUMENTS :
         autorisation : int/float
         interet_debiteur : int/float
         agios : int (12, pour 12% par exemple)
    """

    _autorisation_decouvert: float
    _pourcentage_agios: float
    __coup_de_pouce: bool = True  # On autorise un retrait a decouvert par mois, sans frais. ;)

    #
    ##########################################  __init__  ##########################################
    def __init__(self, autorisation: float = 50, agios: float = 4.73, **extra):
        if hasattr(extra, "nom"):
            nom = extra.get("nom")
            if nom in ("" or "Anonymous"):
                raise ErreurUtilisateurNonDefini(self)

        super().__init__(**extra)
        self._autorisation_decouvert = autorisation if autorisation >= 0 else 0

        if agios >= 50 or agios <= 5:
            agios = 5
        self._pourcentage_agios = agios / 100

        print(f"Ce compte est de type CompteCourant, avec autorisation de decouvert de"
              f" {self._autorisation_decouvert}{self.monnaie}, "
              f"et un taux d'interets de {self._pourcentage_agios * 100}%")

    ########################################## GETTERS  #################################
    def get_agios(self):
        return self._pourcentage_agios

    def get_autorisation(self):
        return self._autorisation_decouvert

    #
    ##########################################  Methodes Normale  #################################

    def retrait(self, valeur: float, autorisation: float = 0) -> float:
        """
        Surcharge de la methode mere pour pouvoir appliquer l'autorisation de decouvert.
         Appel ensuite la méthode de la classe mere avec les arguments supplementaires,
        Et enfin, nous appliquerons des agios si l'utilisateur etait a 0 ou moins avant son retrait
        (ou sa tentative de retrait).
        """
        if not valeur:
            return self.get_solde()
        super().retrait(valeur, self.get_autorisation())
        self.appliquer_agios()
        return self.get_solde()

    def appliquer_agios(self):
        """
        Si l'utilisateur effectue un retrait lors du decouvert: on appliquera cette methode !
        L'on considerera qu'à 0 euro, nous sommes deja a decouvert, n'ayant pas les capacites
         de retrait suffisantes
        On lui evitera cependant les frais de retraits lors du premier evenement qui l'aura
         mis en negatif (une seule fois)
        Attention ! Hors 'coup de pouce', CHAQUE operation a-decouvert appliquera des frais.
        """
        solde = self.get_solde()
        if solde >= 0:
            pass  # Rien a faire si rien a retirer.
        elif solde < 0 and self.__coup_de_pouce is True:
            # En negatif et pas encore utilise le coup de pouce ?
            self.__coup_de_pouce = False
        else:
            # Nous avons donc un depensier .... Il va payer !
            facturation = abs(solde * self.get_agios())
            print(f"Votre compte est debite de {facturation} {self.monnaie},"
                  f" dans le cadre de notre politique de retraits.")
            self._solde = solde - facturation
            # self.afficher_solde()
        return self._solde

    #
    ##########################################  Fonctions Magiques  ################################

    def __str__(self) -> str:  # Surcharge
        """
        Permet de renvoyer les informations du compte au format str(json)
        """
        # Mais on appelle quand meme maman pour recuperer ses informations.
        # infos_parent = super().__str__()
        # infos_enfant = f"\"autorisation\":\"{self._autorisation_decouvert}\"," \
        #                f"\"interets\":\"{self._pourcentage_agios}\"," \
        #                f"\"pouce\":\"{self.__coup_de_pouce}\"" \
        #                "}"
        return str(self.__to_json__())

    def __to_json__(self) -> dict:
        """
        Permet de renvoyer les informations du compte au format json
        """
        infos_compte = {
            "nom": self.nom_proprietaire,
            "type_compte": "Courant",
            "autorisation": self.get_autorisation(),
            "agios": self.get_agios(),
            "solde": self.get_solde(),
            "num_compte": self.get_num(),
            "code": self._recuperer_code(),
            "monnaie": self.monnaie,
            "pouce": self.__coup_de_pouce,
        }
        return infos_compte


##########################################  Fonction test_module  ##################################


if __name__ == '__main__':
    print(msg.EXECUTE)
