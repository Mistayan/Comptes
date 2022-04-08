#!- coding: latin-1 -!#

##########################################  IMPORTS  #####################################################
import Generators.Generateurs as Gen

##########################################  Definition classe  #####################################################


class Verif:  # D�finition d'une classe pour future maitrise de la s�curit� des outils de v�rifications
    def dispo(self=None, compte: str = None):
        """
            V�rifie la disponibilit� d'un num�ro de compte (PKID)

             Si le num�ro n'est pas au format valide, retourne False

             Si le compte est trouv�, retourne le compte

             Si le compte n'existe pas, retourne True
        """
        if not compte or not compte.isdigit() or not len(compte) == 10:
            return False
        else:
            f = Gen.my_open("comptes.txt")
            for line in f.readline():
                if compte in line:
                    return line.split(":")[0]  # Ne r�cup�rer que la premi�re partie
        return True

##########################################  Fonctions Partag�es  ###################################################

##########################################  Fonctions Priv�es  #####################################################


##########################################  Fonctions Sp�ciales  ####################################################

##########################################  Fonctions Magiques  ####################################################
