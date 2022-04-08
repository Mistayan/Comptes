from Compte import Compte



class CompteCourant(Compte):
    """
        Crée un compte avec des possibilités de retraits sous le seuil de 0.0.
        À chaque retrait, si l'utilisateur possède un solde négatif,
         on apposera des frais équivalents aux taux classiques en vigueur

        ARGUMENTS :
         autorisation : int/float
         interet_debiteur : int/float
         agios : int
    """
    _autorisation_decouvert: float
    _pourcentage_agios: float
    __coup_de_pouce: bool=True  # On autorise un retrait à découvert par mois, sans frais. ;)

    def __init__(self, autorisation: float = 50, agios: float = 12, **extra):
        try:
            nom = extra.get("nom")
            if nom == "" or nom == "Anonymous":
                raise UndefinedUserError
        except AttributeError:
            print("ok/NOK ? ")
            pass

        super().__init__(**extra)
        self._autorisation_decouvert = autorisation
        self._pourcentage_agios = agios / 100
        print(f"Ce compte est de type CompteCourant, avec autorisation de découvert de\
                {self._autorisation_decouvert}{self.monnaie}")

    def retrait(self, valeur: float, autorisation: int = 0):
        super().retrait(valeur, autorisation=self._autorisation_decouvert)

    def appliquer_agios(self):
        """
            Montant du découvert x durée du découvert x taux de la banque) ÷ nombre de jours dans l'année.
         ✍️ Prenons un exemple ! Pour une personne à découvert de 100 € pendant 15 jours, à un taux de 12%,
          le calcul sera le suivant : (100 x 15 x 12 %) ÷ 365 = (1500 x 12%) ÷ 365 = 180 ÷ 365 = 0,50 € d'agios
          sur la période écoulée

           Si l'utilisateur effectue un retrait lors du découvert.... ça pique !
               On lui évitera cependant les frais de retraits lors du premier évènement qui l'aura mis en négatif
               (1 fois par mois)
        """

        if self._solde > 0:
            return print("Rien à faire. L'utilisateur est en positif")
        if self._solde < 0 and self.__coup_de_pouce is True:  # En négatif et Deja utilisé le coup de pouce ?
            self.__coup_de_pouce = False
            return print("Rien à faire. L'utilisateur utilise son coup de pouce")

        # Nous avons donc un dépensier .... Il va payer !
        facturation = 0

        self._solde = self._solde - facturation


if __name__ == '__main__':
    cpt = CompteCourant(nom="Julie Blois", autorisation=50, agios=5)
    cpt + 25
    cpt - 25
    cpt - 75
    cpt - 25

