#!-- coding:latin-1 --!#


##########################################  IMPORTS  #####################################################

# from imports import *
import random
from datetime import datetime
import os
import re
import Messages.Static_strings as Message

##########################################  SNIPPETS  #####################################################


##########################################  SNIPPETS  #####################################################


def chaine_aleatoire(longueur: int, style: str) -> str:
    """
        Génère une chaine de longueur voulue, contenant les characters de style voulu, sélectionnés aléatoirement.

        :longueur =>
        La longueur de la chaine générée

        :style =>
         DIGITS = "0123456789"

         HEXA = DIGITS + "ABCDEF"

         ... et bien d'autres ... (Vous pouvez aussi rentrer une chaine de characters personnalisé)
    """
    # Aller, c'est bien parce qu'on a vu yield que je fais ça.... sinon c'est un simple:
    #   return ''.join(random.choice(style) for i in range(longueur))

    def _choix_aleatoire():  # Fonction imbriquée (et donc privée ?), utilisable uniquement au sein de cette fonction.
        for _ in range(longueur):  # Le petit _ pour dire osef
            yield random.choice(style)  # Yield est un return à mémoire. Retourne un generateur itérable.

    ret = ""
    for bout_de_code in _choix_aleatoire():
        ret += bout_de_code
    return ret



def my_open(fichier: str, mode: str = 'r', encoding: str = "utf-8"):
    """
        Permet d'ouvrir un fichier avec le mode voulu.
        Si le fichier n'existe pas, de le créer, et de l'ouvrir avec le mode voulu.
    """
    if not re.search(r":[\\]|[/]", fichier):  # Path relatif détecté. Petit regex bien pratique.
        dossier_actuel = os.path.abspath('.') + "\\"  # On ajoute le path complet.
    else:
        dossier_actuel = ""
    try:
        f = open(f"{dossier_actuel}{fichier}", mode=mode, encoding=encoding)
        return f if f else None
    except FileNotFoundError as e:
        f = open(fichier, 'w')  # Du coup, on crée le fichier.
        f.close()           # Pas le bon mode, on ferme.
    return my_open(fichier, mode=mode, encoding=encoding)  # Bouclage des vérifications de sécurité.


def fraude(compte: str, func: str, arg: str = "") -> None:
    """Enregistre dans le fichier approprié:
    la fraude/tentative de retrait sans solde/... constatée

    :compte =>
    Le compte mis en défaut

    :func =>
    Quelle action l'utilisateur essayait à ce moment.

    :arg =>
    Une valeur indicative associée à l'action enregistrée
    """

    fichier = f"Rapports/{func}.txt"
    with my_open(fichier, "a+") as f:
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"{compte} ; {date} ===> {arg} <===", file=f)
        f.close()
        if Message.DEBUG:
            print(f"tentative enregistrée")
    return


def historique(compte, valeur) -> None:
    with my_open(f"Historique/{compte}.txt", "a+") as f:
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"{date} // {valeur}", file=f)
        f.close()
        if Message.DEBUG:
            print("Un évènement vient d'être historisé dans ", f"Historique/{compte}.txt")
    return

##########################################  Fonction test_module  ####################################################
if __name__ == '__main__':
    import pprint
    pp = pprint.PrettyPrinter(width=42, compact=True)
    """Je vois pas comment controller l'aléatoire... à part avec un bon vieux PRINT !"""
    chaine = chaine_aleatoire(style=BRAIN_FUCK, longueur=2500)
    pp.pprint(chaine)


