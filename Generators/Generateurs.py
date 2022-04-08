#!-- coding:utf-8 --!#


##########################################  IMPORTS  #####################################################

import random
from datetime import datetime
from string import digits as DIGITS
from string import hexdigits as HEXA
import os

##########################################  SCRIPTS  #####################################################
def random_string(longueur: int, style: str) -> str:
    """
        Génère une chaine de longueur voulue, contenant une chaine aléatoire des characters voulus.
        :longueur:
        La longueur de la chaine générée

        :style:
        DIGITS = "0123456789"
        HEXA = DIGITS + "ABCDEF"
    """
    return ''.join(random.choice(style) for i in range(longueur))


def my_open(fichier: str, mode: str = 'r+'):
    """
        Permet d'ouvrir un fichier avec le mode voulu.
        Si le fichier n'existe pas, de le créer, et de l'ouvrir avec le mode voulu.
    """
    try:
        return open(fichier, mode)
    except FileNotFoundError as e:
        f = open(fichier, 'w+')
        f.close()
    return open(fichier, mode)


def fraude(compte: str, func: str):
    """Enregistre dans le fichier approprié:
    la fraude/tentative de retrait sans solde/... constatée

    :compte
    Le compte mis en défaut

    :func
    Quelle action l'utilisateur essayait à ce moment.
    """
    fichier = f"./Rapports/{func}.txt"
    print(f"tentative d'enregistrer: {fichier}")
    with my_open(fichier, "a+") as f:
        date = datetime.now.strftime("%d/%m/%Y %H:%M:%S")   # annotation batarde à revoir
        f.write(f"{compte} => {func} <= {date}\n")
        f.close()
