#!- coding: latin-1 -!#

##########################################  IMPORTS  #####################################################
import Generators.Generateurs as Gen

##########################################  Definition classe  #####################################################


class Verif:  # Définition d'une classe pour future maitrise de la sécurité des outils de vérifications
    def dispo(self=None, compte: str = None):
        """
            Vérifie la disponibilité d'un numéro de compte (PKID)

             Si le numéro n'est pas au format valide, retourne False

             Si le compte est trouvé, retourne le compte

             Si le compte n'existe pas, retourne True
        """
        if not compte or not compte.isdigit() or not len(compte) == 10:
            return False
        else:
            f = Gen.my_open("comptes.txt")
            for line in f.readline():
                if compte in line:
                    return line.split(":")[0]  # Ne récupérer que la première partie
        return True

##########################################  Fonctions Partagées  ###################################################

##########################################  Fonctions Privées  #####################################################


##########################################  Fonctions Spéciales  ####################################################

##########################################  Fonctions Magiques  ####################################################
