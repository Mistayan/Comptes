from .Compte import Compte


class CompteEpargne(Compte):
    _pourcentageInterets: float

    def __init__(self, interets: float):
        super().__init__()
        self._pourcentageInterets = interets
        print(f"Celui-ci est de type Compte Epargne, avec un taux d'interets annuel de {interets}{self.monnaie}")

    def appliquerInterets(self):
        pass
