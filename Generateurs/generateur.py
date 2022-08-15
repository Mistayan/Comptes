#!-- coding:utf-8
""""
Editeur: Mistayan
Projet: Comptes-Bancaires
"""
# ################################  IMPORTS  ###################################

import os
import secrets
import re
from datetime import datetime

import messages.static_strings as msgs
import verifications as secu
from comptes import CompteCourant, CompteEpargne


# ###########################  FONCTIONS UTILES  ###############################
def chaine_aleatoire(longueur: int, style: str) -> str:
    """
        Genere une chaine de longueur voulue, contenant les characters de style voulu, selectionnes
        aleatoirement.
        :longueur =>
        La longueur de la chaine voulue
        :style =>
         DIGITS = "0123456789"
         HEXA = DIGITS + "ABCDEF"
         ... et bien d'autres ... (Vous pouvez aussi rentrer une chaine de characters personnalise)
    """
    return ''.join(secrets.choice(style) for _ in range(longueur))


def my_open(fichier: str, mode: str = 'r', encoding: str = "utf-8", rec: int = 0):
    """
        Permet d'ouvrir un fichier avec le mode voulu.
        Si le fichier n'existe pas, de le creer, et de l'ouvrir avec le mode voulu.
    """
    if rec == 5:
        return None
    if not re.search(r"[A-Z]:[\\/]", fichier):  # Path relatif? Petit regex bien pratique.
        dossier_actuel = os.path.abspath('.') + "\\"  # On ajoute le path complet.
    else:
        dossier_actuel = ""
    try:
        fp = open(f"{dossier_actuel}{fichier}", mode=mode, encoding=encoding)
        return fp if fp else None
    except FileNotFoundError:
        fp = my_open(fichier, 'w', encoding, rec + 1)  # Du coup, on cree le fichier.
        fp.close()  # Pas le bon mode, on ferme.
    return my_open(fichier, mode, encoding, rec + 1)  # Verification recursive.


def fraude(compte: str, func: str, arg: str = "") -> None:
    """Enregistre dans le fichier approprie :
    la fraude/tentative de retrait sans solde/... constatee\n
    Cela fonctionne aussi pour les reclamations clients.\n

    :param compte: Le compte mis en defaut, ou reclamant.
    :param func: Nom du fichier d'enregistrement.
    :param arg: La chaine qui aura fait l'erreur ou le message utilisateur.
    """

    fichier = f"Rapports/{func}.log"
    with my_open(fichier, "a+") as f:
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        print(f"{date} {compte} ===> {arg} <===", file=f)
        f.close()
        if msgs.DEBUG:
            print(f"tentative enregistree")
    return


def historique(compte, methode: str, valeur) -> None:
    with my_open(f"Historique/{compte}.log", "a+") as f:
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"{date} /{methode}/ {valeur}", file=f)
        f.close()
        if msgs.DEBUG:
            print("Un evenement vient d'etre historise dans ", f"Historique/{compte}.txt")
    return


def json_en_compte(json: dict) -> any:
    """
    :param json : Un compte au format json
    :return : si le type de compte est valide, le compte,
     avec les informations contenues dans le dictionnaire, sinon None.
    """
    if secu.format_compte(json) is False:  # Double check
        return None
    try:
        match json["type_compte"]:
            case "Epargne":
                return CompteEpargne(nom=json["nom"], interets=json["interets"],
                                     solde_initial=json["solde"], num_compte=json["num_compte"],
                                     code=json["code"], monnaie=json["monnaie"],
                                     force=True, new=False)
            case "Courant":
                return CompteCourant(nom=json["nom"], autorisation=json["autorisation"],
                                     agios=json["agios"], solde_initial=json["solde"],
                                     num_compte=json["num_compte"], code=json["code"],
                                     monnaie=json["monnaie"], force=True, new=False)
            case _:
                return None
    except KeyError:
        print(f"{json}: Aucun type de compte défini")
    return None


def compte_en_json(compte: CompteEpargne | CompteCourant):
    return compte.__to_json__()


# ########################  Fonction test_module  ##############################
if __name__ == '__main__':
    import pprint

    pp = pprint.PrettyPrinter(width=42, compact=True)
    """Je vois pas comment controller l'aleatoire... ? part avec un bon vieux PRINT !"""
    chaine = chaine_aleatoire(style=msgs.BRAIN_FUCK, longueur=2500)
    pp.pprint(chaine)
