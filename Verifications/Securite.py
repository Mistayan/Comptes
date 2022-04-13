#!- coding: latin-1 -!#

##########################################  IMPORTS  #####################################################
import Generators.Generateurs as Gen


##########################################  Definition classe  #####################################################


class Verif:  # Définition d'une classe pour future maitrise de la sécurité des outils de vérifications
    """
    Possède plusieurs fonctions de vérification
    dispo: vérifier la disponibilité d'un compte
    ... d'autres à venir
    """
    def dispo(self=None, compte: str = None, liste=None): #Annotation très étrange pour rendre statique... pas beau !
        """
            Vérifie la disponibilité d'un numéro de compte (UUID)

             Si le numéro n'est pas au format valide, retourne False

             Si le compte est trouvé, retourne le compte sous forme 'compte':'num_cpt'

             Si le compte n'existe pas, retourne True
        """
        # TODO si json pas accepté: 'nom : numero : solde : monnaie : type : arg1 : arg2''
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
                        return line.split(":")[0]  # Ne retourne que le numéro de compte...
                f.close()
            else:  # On a reçu une liste
                pass  # TODO faire en liste, pour l'application

def scan_file(numero_en_str: str = None):
    """
    :arg
     Prend une chaine de caracteres;
     Cherche la chaine de caracteres dans le fichier de comptes

    :return
     True si présent
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


##########################################  Fonctions Partagées  ###################################################

##########################################  Fonctions Privées  #####################################################


##########################################  Fonctions Spéciales  ####################################################

##########################################  Fonctions Magiques  ####################################################
