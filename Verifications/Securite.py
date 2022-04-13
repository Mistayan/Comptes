#!- coding: latin-1 -!#

##########################################  IMPORTS  #####################################################
import Generateurs as Gen
import json
from json import JSONDecodeError


##########################################  Definition classe  #####################################################


def dispo(compte: str = None, code: str = None):
    """
        V�rifie la disponibilit� d'un num�ro de compte (UID)

         Si le num�ro n'est pas au format valide, retourne False

         Si le compte est trouv�, retourne le compte sous forme False

             Si le compte n'existe pas, retourne True
    """

    if not compte or not compte.isdigit() or not len(compte) == 10:
        return False
    else:
        f = Gen.my_open("comptes.json", 'r+')
        if not f:
            return False
        for line in f:
            if compte in line:
                f.close()
                return line.split(":")[0]  # Ne retourne que le num�ro de compte...
        f.close()


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
