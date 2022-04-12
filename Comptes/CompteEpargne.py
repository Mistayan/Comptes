##########################################  IMPORTS  ####################################################
from .Compte import Compte


##########################################  Class definition  ####################################################


class CompteEpargne(Compte):
    """
    Instancie un CompteEpargne (instance de Compte).

    """
    _pourcentageInterets: float

    ##########################################  Class Init  ####################################################
    def __init__(self, interets: float = 1.05, **kwargs):

        super().__init__(**kwargs)
        self._pourcentageInterets = interets
        print(f"Celui-ci est de type Compte Epargne, avec un taux d'interets annuel de {interets}{self.monnaie}")

    ##########################################  Methodes  ####################################################
    def versement(self, valeur: float) -> None:  # Override, pour appliquer les taux d'intérêts
        super().versement(valeur=valeur)
        self.appliquer_interets()

    def appliquer_interets(self):
        """
            Par décret, les intérêts sont actuellement fixés à 1.05% par mois.
        """
        # FIXME : bien appliquer le calcul
        print("Nous allons appliquer votre taux d'intérêt.")
        interets = self._solde * (self._pourcentageInterets * 100 * self._solde)
        print(f"Interets acquis : {interets}")
        super().versement(interets)

    def __str__(self) -> str:  # Surcharge
        """
        Permet de renvoyer les informations du compte au format json
        """
        # Mais on appelle quand même maman pour la prévenir qu'on reste chez Salomé ce soir;)
        infos_parent = super().__str__()
        infos_enfant = f"\"autorisation\":\"{self._pourcentageInterets}\",\n" \
                       "}\n"
        return infos_parent + infos_enfant