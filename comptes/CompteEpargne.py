#! encoding:utf-8
""""
Editeur: Mistayan
Projet: Comptes-Bancaires
"""
##########################################  IMPORTS  ###############################################
import messages.static_strings as message
from .Compte import Compte


##########################################  Class definition  ######################################


class CompteEpargne(Compte):
    """
    Instancie un CompteEpargne (instance de Compte).

    """
    _pourcentage_interets: float

    ##########################################  Class Init  ########################################
    def __init__(self, interets: float = 5, **kwargs):
        super().__init__(**kwargs)
        if interets < 5 or interets > 5:
            interets = 1 + 5 / 100
        self._pourcentage_interets = interets
        if message.DEBUG:
            print(
                f"Celui-ci est de type Compte Epargne, avec un taux d'interets"
                f" annuel de {interets}{self.monnaie}"
            )

    ##########################################  GETTERS  ########################################
    def get_interets(self):
        return self._pourcentage_interets

    ##########################################  SETTERS  ########################################

    ##########################################  Methodes  ##########################################
    def versement(self, valeur: float):  # Override, pour appliquer les taux d'intérêts
        """
            Permet d'ajouter de l'argent sur le compte.
          :return :
          retourne le nouveau solde.
        """
        super().versement(valeur=valeur)
        return self.appliquer_interets()

    def appliquer_interets(self):
        """
            Par decret, les interets sont actuellement fixés à 5% par depot.
            :return:
            retourne le nouveau solde.
        """
        interets = self._pourcentage_interets * self._solde - self._solde
        print(f"Interets acquis : {interets:.2f} {self.monnaie}")
        super().versement(abs(interets))
        return self._solde

    def __str__(self):
        return str(self.__to_json__())

    def __to_json__(self) -> dict:
        """
        Permet de renvoyer les informations du compte au format json
        """
        infos_compte = {
            "nom": self.nom_proprietaire,
            "type_compte": "Epargne",
            "interets": self.get_interets(),
            "solde": self.get_solde(),
            "num_compte": self.get_num(),
            "code": self._recuperer_code(),
            "monnaie": self.monnaie,
        }
        return infos_compte
