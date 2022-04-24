##########################################  IMPORTS  ####################################################
from .Compte import Compte
import Message.Static_strings as Message

##########################################  Class definition  ####################################################


class CompteEpargne(Compte):
    """
    Instancie un CompteEpargne (instance de Compte).

    """
    _pourcentageInterets: float

    ##########################################  Class Init  ####################################################
    def __init__(self, interets: float = 5, **kwargs):
        super().__init__(**kwargs)
        if interets < 5 or interets > 5:
            interets = 1 + 5 / 100
        self._pourcentageInterets = interets
        if Message.DEBUG :
            print(f"Celui-ci est de type Compte Epargne, avec un taux d'interets annuel de {interets}{self.monnaie}")

    ##########################################  Methodes  ####################################################
    def versement(self, valeur: float):  # Override, pour appliquer les taux d'intérêts
        """
            Permet d'ajouter de l'argent sur le compte.
          :return :
          retourne le nouveau solde.
        """
        super().versement(valeur=valeur)
        return (self.appliquer_interets())

    def appliquer_interets(self):
        """
            Par decret, les interets sont actuellement fixés à 5% par depot.
            :return:
            retourne le nouveau solde.
        """
        interets = self._pourcentageInterets * self._solde - self._solde
        print(f"Interets acquis : {interets:.2f} {self.monnaie}")
        super().versement(abs(interets))
        return self._solde

    def __str__(self) -> str:  # Surcharge
        """
        Permet de renvoyer les informations du compte au format json
        """
        # Mais on appelle quand même maman pour la prévenir qu'on reste chez Salomé ce soir;)
        infos_parent = super().__str__()
        infos_enfant = f"\"autorisation\":\"{self._pourcentageInterets}\"" \
                       "}\n"
        return infos_parent + infos_enfant
