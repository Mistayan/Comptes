#! encoding:utf-8
""""
Editeur: Mistayan
Projet: Comptes-Bancaires
"""
import messages
from comptes import Compte, CompteCourant, CompteEpargne


##########################################  Classe  #################################################


class Champ(object):
    def __init__(self, *args):
        self._arg = args


class Questionnaire(Compte):
    def __init__(self):
        self._champs = None

    def champs(self, type_compte: any):
        if type(type_compte) is not CompteCourant or type(type_compte) is not CompteEpargne:
            raise ValueError("Questionnaire.champs ne prends que des comptes bancaires")
        if not self._champs:
            self._champs = set()
        for attribut in dir(type_compte):
            valeur = getattr(type_compte, attribut)
            self._champs.insert(attribut, valeur)


if __name__ == '__main__':
    print(messages.EXECUTE)
