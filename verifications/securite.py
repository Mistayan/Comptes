#! encoding:utf-8 --!#
""""
Editeur: Mistayan
Projet: Comptes-Bancaires
"""
# ##################################  IMPORTS  #################################
import Generateurs as Gen


# ###########################  Definition Fonctions  ###########################


def dispo(num_compte: str = None):
    """
        Verifie la disponibilite d'un numero de compte (UID)

        Si le numero n'est pas au format valide, retourne False
        Si le compte est trouve, retourne "num_cpt"
        Si le compte n'existe pas, retourne True
    """

    if not num_compte or not num_compte.isdigit() or not len(num_compte) == 10:
        return False
    return False if scan_file(num_compte) else True


def scan_file(numero_en_str: str = None):
    """
     Cherche la chaine de caracteres dans le fichier de comptes\n

    :arg numero_en_str:
     Prend une chaine de caracteres NUMERIQUES

    :return:
     True si present;
     False si absent
    """

    with Gen.my_open("comptes.json", "r+") as fp:
        for line in fp.read():
            if numero_en_str in line:
                return True  # Duplicat
    return False  # Unique


def format_compte(dict_compte: dict) -> bool:
    """
    Verifie l'integrite du compte recupere dans un fichier techniquement accessible a l'utilisateur

    :arg dict_compte: un dictionnaire généré par un compte
    :return: True si les donnees sont valides, sinon False
    """
    if not isinstance(dict_compte, dict):
        return False

    champs_compte = ["nom", "type_compte", "solde", "num_compte", "code", "monnaie"]
    try:
        match dict_compte["type_compte"]:
            case "Epargne":
                champs_compte = champs_compte + ["interets"]
            case "Courant":
                champs_compte = champs_compte + ["autorisation", "agios", "pouce"]
            case _:
                return False
        for champ in dict_compte:
            if champ not in champs_compte:
                return False
    except KeyError:
        return False
    return True


if __name__ == "__main__":
    pass
