#! encoding:utf-8
""""
Editeur: Mistayan
Projet: Comptes-Bancaires
"""
# ###############################  IMPORTS  ###############################
from .compte import Compte


# #############################  Class definition  #############################
class CompteEpargne(Compte):
    """
    Instancie un Compte-Epargne (instance de Compte). \n
    Args:
    - interets: le taux d'intérêt du compte (5-25%)
     """
    _pourcentage_interets: float

    # ##############################  Class Init  ##############################
    def __init__(self, interets: float = 5, **kwargs):
        super().__init__(**kwargs)
        if interets < 5 or interets > 25:
            interets = 5
        self._pourcentage_interets = 1 + interets / 100
        print(f"Celui-ci est de type Compte Epargne,"
              f" avec un taux d'interets de {round(interets, 2)}%")

    # ###############################  GETTERS  ################################
    def get_interets(self):
        """ :return: Le taux d'intérêts du compte. (en %)"""
        return self._pourcentage_interets

    # ###############################  Methodes  ###############################
    def versement(self, valeur: float):  # Override, pour appliquer les taux d'intérêts
        """
        Permet d'ajouter de l'argent sur le compte.
        :arg valeur: le montant a verser sur le compte
        :return: le nouveau solde.
        """
        super().versement(valeur=valeur)
        return self.appliquer_interets()

    def appliquer_interets(self):
        """
            Par decret, les interets sont actuellement fixés à 5% par depot.
            :return: Le nouveau solde, après opérations.
        """
        interets = self._pourcentage_interets * self._solde - self._solde
        print(f"Interets acquis : {interets:.2f} {self.monnaie}")
        super().versement(abs(interets))
        return self._solde

    def __str__(self):
        return str(self.__to_json__())

    def __to_json__(self) -> dict:
        """ :return: les informations du compte au format json"""
        infos_compte = {
            "nom": self.nom_proprietaire,
            "type_compte": "Epargne",
            "interets": round(self.get_interets(), 2),
            "solde": round(self.get_solde(), 2),
            "num_compte": self.get_num(),
            "code": self._recuperer_code(),
            "monnaie": self.monnaie,
        }
        return infos_compte
