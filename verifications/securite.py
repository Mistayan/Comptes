#! encoding:utf-8 --!#
""""
Editeur: Mistayan
Projet: Comptes-Bancaires
"""
##########################################  IMPORTS  ###############################################
import Generateurs as Gen


##########################################  Definition classe  #####################################


def dispo(compte: str = None, code: str = None, ):
    """
        Verifie la disponibilite d'un numero de compte (UID)

         Si le numero n'est pas au format valide, retourne False

         Si le compte est trouve, retourne le compte sous forme False

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
                return line.split(":")[1]  # Retourne le numero du compte.
        f.close()
    return True


def scan_file(numero_en_str: str = None):
    """
    :arg
     Prend une chaine de caracteres;
     Cherche la chaine de caracteres dans le fichier de comptes

    :return
     True si present
     False si absent
    """

    f = Gen.my_open("comptes.json", "r+")
    for line in f.read():
        if numero_en_str in line:
            # print("duplicate found")
            f.close()
            return True
    f.close()
    return False


def verif_format(dict_compte):
    """
    arg: un dictionnaire de comptes
    Verifie l'integrite du compte recupere dans un fichier techniquement accessible a l'utilisateur.

    Retourne un compte du type voulu si les donnees sont valides, sinon False.
    """
    champs_compte = ["nom", "type_compte", "solde", "num_compte", "code", "monnaie"]
    champs_compte_courant = ["autorisation", "agios"]
    champs_compte_epargne = ["interets"]

    if not type(dict_compte) is dict:
        return False
    for c in champs_compte:
        if c not in dict_compte:
            return False  # Un des champs n'existe pas.

    if dict_compte["type_compte"] == "Epargne":
        for c in champs_compte_epargne:
            if c not in dict_compte:
                return False  # Un des champs n'existe pas.
        return True  # Les champs sont 'valides'

    elif dict_compte["type_compte"] == "Courant":
        for c in champs_compte_courant:
            if c not in dict_compte:
                return False  # Un des champs n'existe pas.
        return True  # Les champs sont 'valides'

    return False  # Les champs sont presents ET valides


if __name__ == "__main__":
    pass
