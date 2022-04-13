#!- coding: latin-1 -!#

##########################################  IMPORTS  #####################################################
import Generators.Generateurs as Gen


##########################################  Definition classe  #####################################################


class Verif:  # D�finition d'une classe pour future maitrise de la s�curit� des outils de v�rifications
    """
    Poss�de plusieurs fonctions de v�rification
    dispo: v�rifier la disponibilit� d'un compte
    ... d'autres � venir
    """
    def dispo(self=None, compte: str = None, liste=None): #Annotation tr�s �trange pour rendre statique... pas beau !
        """
            V�rifie la disponibilit� d'un num�ro de compte (UUID)

             Si le num�ro n'est pas au format valide, retourne False

             Si le compte est trouv�, retourne le compte sous forme 'compte':'num_cpt'

             Si le compte n'existe pas, retourne True
        """
        # TODO si json pas accept�: 'nom : numero : solde : monnaie : type : arg1 : arg2''
        if not compte or not compte.isdigit() or not len(compte) == 10:
            return False
        else:
            if not liste:  # En dehors du cadre de l'application
                f = Gen.my_open("comptes.json", 'r+')
                if not f:
                    return False
                for line in f:
                    if compte in line:
                        f.close()
                        return line.split(":")[0]  # Ne retourne que le num�ro de compte...
                f.close()
            else:  # On a re�u une liste
                pass  # TODO faire en liste, pour l'application

def scan_file(numero_en_str: str = None):
    """
    :arg
     Prend une chaine de caracteres;
     Cherche la chaine de caracteres dans le fichier de comptes

    :return
     True si pr�sent
     False si absent
    """

    f = Gen.my_open("comptes.json", "r+")
    for line in f.read():
        if numero_en_str in line:
            print("duplicate found")
            f.close()
            return True
    f.close()
    return False


##########################################  Fonctions Partag�es  ###################################################

##########################################  Fonctions Priv�es  #####################################################


##########################################  Fonctions Sp�ciales  ####################################################

##########################################  Fonctions Magiques  ####################################################
