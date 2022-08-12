#!-- coding:utf-8
""""
Editeur: Mistayan
Projet: Comptes-Bancaires
"""
##########################################  IMPORTS  ###############################################

import os
import secrets
import re
from datetime import datetime
import messages.static_strings as Message
import vertifications as Verif
from comptes import CompteCourant, CompteEpargne


##########################################  SNIPPETS  ##############################################
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
    """
        # Fonction wrapped (et donc privee ?), utilisable uniquement au sein de cette fonction.
        def _choix_aleatoire():
            for _ in range(longueur):  # _ veut dire 'pas important'
                # Yield est un return a memoire. Retourne un generateur iterable.
                yield secrets.choice(style)
            # ^^^^^^^^ Au prochain appel de la fonction, reprendra ici.

        ret = ''.join(elem for elem in _choix_aleatoire())
        return ret
        """
    return ''.join(secrets.choice(style) for _ in range(longueur))


def my_open(fichier: str, mode: str = 'r', encoding: str = "utf-8", rec: int = 0):
    """
        Permet d'ouvrir un fichier avec le mode voulu.
        Si le fichier n'existe pas, de le creer, et de l'ouvrir avec le mode voulu.
    """
    if rec == 5:
        return None
    if not re.search(r"[A-Z]:[\\]|[/]", fichier):  # Path relatif? Petit regex bien pratique.
        dossier_actuel = os.path.abspath('.') + "\\"  # On ajoute le path complet.
    else:
        dossier_actuel = ""
    try:
        fp = open(f"{dossier_actuel}{fichier}", mode=mode, encoding=encoding)
        return fp if fp else None
    except FileNotFoundError as e:
        fp = my_open(fichier, 'w', encoding, rec + 1)  # Du coup, on cree le fichier.
        fp.close()  # Pas le bon mode, on ferme.
    return my_open(fichier, mode, encoding, rec + 1)  # Verification recursive.


def fraude(compte: str, func: str, arg: str = "") -> None:
    """Enregistre dans le fichier approprie:
    la fraude/tentative de retrait sans solde/... constatee
    Cela fonctionne aussi pour les reclamations clients.
    :param compte: Le compte mis en defaut, ou reclamant.
    :param func: Quelle action l'utilisateur essayait a ce moment.
    :param arg: La chaine qui aura fait l'erreur.
    """

    fichier = f"Rapports/{func}.txt"
    with my_open(fichier, "a+") as f:
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"{compte} ; {date} ===> {arg} <===", file=f)
        f.close()
        if Message.DEBUG:
            print(f"tentative enregistree")
    return


def historique(compte, methode: str, valeur) -> None:
    with my_open(f"Historique/{compte}.txt", "a+") as f:
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"{date} /{methode}/ {valeur}", file=f)
        f.close()
        if Message.DEBUG:
            print("Un evenement vient d'etre historise dans ", f"Historique/{compte}.txt")
    return


def json_en_compte(json: dict) -> any:
    """
    :param json : Un compte au format json
    :return : si le type de compte est valide, le compte,
     avec les informations contenues dans le dictionnaire, sinon None.
    """
    if Verif.verif_format(json) is False:  # Double check
        return None
    if json["type_compte"] == "Epargne":
        return CompteEpargne(nom=json["nom"], interets=json["interets"],
                             solde_initial=json["solde"], num_compte=json["num_compte"],
                             code=json["code"], monnaie=json["monnaie"], force=True)
    if json["type_compte"] == "Courant":
        return CompteCourant(nom=json["nom"], autorisation=json["autorisation"],
                             agios=json["agios"], solde_initial=json["solde"],
                             num_compte=json["num_compte"], code=json["code"],
                             monnaie=json["monnaie"], force=True)
    return None


def compte_en_json(compte):
    return compte.__repr__()


def compte_en_json(compte: CompteEpargne):
    return compte.__repr__()


##########################################  Fonction test_module  ##################################
if __name__ == '__main__':
    import pprint

    pp = pprint.PrettyPrinter(width=42, compact=True)
    """Je vois pas comment controller l'aleatoire... ? part avec un bon vieux PRINT !"""
    chaine = chaine_aleatoire(style=Message.BRAIN_FUCK, longueur=2500)
    pp.pprint(chaine)
