#!-- coding:latin-1 --!#


##########################################  IMPORTS  #####################################################

import random
from datetime import datetime
import os
import re
import Message


##########################################  SNIPPETS  #####################################################


##########################################  SNIPPETS  #####################################################


def chaine_aleatoire(longueur: int, style: str) -> str:
    """
        Genere une chaine de longueur voulue, contenant les characters de style voulu, s�lectionnes aleatoirement.

        :longueur =>
        La longueur de la chaine g�n�r�e

        :style =>
         DIGITS = "0123456789"

         HEXA = DIGITS + "ABCDEF"

         ... et bien d'autres ... (Vous pouvez aussi rentrer une chaine de characters personnalise)
    """

    # .... sinon c'est un simple:
    #   return ''.join(random.choice(style) for i in range(longueur))

    def _choix_aleatoire():  # Fonction imbriqu�e (et donc priv�e ?), utilisable uniquement au sein de cette fonction.
        for _ in range(longueur):  # Le petit _ pour dire 'pas important'
            # Yield est un return � m�moire. Retourne un generateur it�rable.
            yield random.choice(style)
        # ^^^^^^^^ Au prochain appel de la fonction, reprendra � cette ligne

    ret = ''.join(elem for elem in _choix_aleatoire())
    return ret


def chaine_vers_json(chaine: str):
    print(chaine)


def my_open(fichier: str, mode: str = 'r', encoding: str = "utf-8"):
    """
        Permet d'ouvrir un fichier avec le mode voulu.
        Si le fichier n'existe pas, de le creer, et de l'ouvrir avec le mode voulu.
    """
    if not re.search(r":[\\]|[/]", fichier):  # Path relatif d?tect?. Petit regex bien pratique.
        dossier_actuel = os.path.abspath('.') + "\\"  # On ajoute le path complet.
    else:
        dossier_actuel = ""
    try:
        f = open(f"{dossier_actuel}{fichier}", mode=mode, encoding=encoding)
        return f if f else None
    except FileNotFoundError as e:
        f = open(fichier, 'w')  # Du coup, on cr?e le fichier.
        f.close()  # Pas le bon mode, on ferme.
    return my_open(fichier, mode=mode, encoding=encoding)  # Bouclage des verifications de securite.


def fraude(compte: str, func: str, arg: str = "") -> None:
    """Enregistre dans le fichier approprie:
    la fraude/tentative de retrait sans solde/... constatee

    :compte =>
    Le compte mis en defaut

    :func =>
    Quelle action l'utilisateur essayait a ce moment.

    :arg =>
    Une valeur indicative associee a l'action enregistree
    """

    fichier = f"Rapports/{func}.txt"
    with my_open(fichier, "a+") as f:
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"{compte} ; {date} ===> {arg} <===", file=f)
        f.close()
        if Message.DEBUG:
            print(f"tentative enregistr?e")
    return


def historique(compte, valeur) -> None:
    with my_open(f"Historique/{compte}.txt", "a+") as f:
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"{date} // {valeur}", file=f)
        f.close()
        if Message.DEBUG:
            print("Un evenement vient d'etre historise dans ", f"Historique/{compte}.txt")
    return


##########################################  Fonction test_module  ####################################################
if __name__ == '__main__':
    import pprint

    pp = pprint.PrettyPrinter(width=42, compact=True)
    """Je vois pas comment controller l'aleatoire... ? part avec un bon vieux PRINT !"""
    chaine = chaine_aleatoire(style=BRAIN_FUCK, longueur=2500)
    pp.pprint(chaine)
