##########################################  IMPORTS  ####################################################
from hashlib import md5
from json import JSONDecodeError

from imports import *
import os
import platform
import sys
from Messages.Static_strings import *

########################################## GLOBALES  ####################################################

liste_comptes: list

##########################################  fonctions utiles  ####################################################
def init():
    """
        Init permet de créer les dossiers de base, pour le bon fonctionnement du programme.
        Si comptes.json existe, récupère les informations des comptes, pour les ajouter à liste_comptes
    """
    global DEBUG
    DEBUG = False

    try:
        os.mkdir("Rapports")
    except FileExistsError:
        pass
    try:
        os.mkdir("Historique")
    except FileExistsError:
        pass
    try:
        os.mkdir("Clients")
    except FileExistsError:
        pass

    f = Gen.my_open("comptes.json", 'r+')
    try:
        global liste_comptes
        liste_comptes = json.load(f)  # Charge les comptes dans l'application sous forme [{},{}]
        if DEBUG:
            print(liste_comptes)
    except JSONDecodeError:
        print(PREMIER_CLIENT)
    f.close()

    """
       # Je garde ça au cas où le json ne plairait pas au client
    try:
        f = Gen.my_open("comptes.json", 'r+')
        for line in f:
            compte = line.split(":")
            if len(compte) != 10:
                raise IndexError
    
    except IndexError:
        print("Une ligne de compte semble invalide")
        pass
    """


def clear():
    match platform.system():
        case "Windows":
            os.system('cls')
        case "Linux":
            os.system('clear')
        case "Darwin":
            os.system('clear')  # IOs
        case _:
            sys.exit(OS_ERREUR)


##########################################  ELEMENTS DU MENU APP  ####################################################

def quitter():
    print(AUREVOIR_MSG)
    sys.exit()


def acces_compte(essais: int = 0):
    """
        Demande la combinaison compte + code, pour plus de sécurité #DummySpecs
         Si la combinaison est fausse, alors on le laisse essayer... 3fois.

    :param essais: Nombre d'essais infructueux
    """
    ### Verifier les données fournies
    if essais >= 3 or essais < 0:
        print(ACCES_REFUSE)
        input(CONTINUER)
        menu_principal()
    print(DEMANDER_COMPTE)
    compte = input(ASK)
    input(DEMANDER_CODE)

    ### Verifier les données fournies
    global liste_comptes
    cpt = Secu.Verif.dispo(compte=compte, liste=liste_comptes)
    if cpt is True or cpt is False:  # Le compte n'existe pas dans la banque de données
        print(COMPTE_ERREUR)
        acces_compte(essais + 1)

    print(COMPTE_TROUVE)


def creer_compte():
    print(CREER_COMPTE)
    choix = input(FAIRE_CHOIX)
    match choix:
        case "1":
            liste_comptes.append(CompteCourant())
        case "2":
            liste_comptes.append(CompteEpargne())
        case "3":
            menu_principal()
        case _:
            print(INVALIDE)
            creer_compte()


def menu_principal():
    print(MAIN_CHOIX_ACTION)
    choix = input(FAIRE_CHOIX)
    match choix:
        case "1":
            acces_compte()
        case "2":
            creer_compte()
        case "3":
            quitter()
        case _:
            print(INVALIDE)
            menu_principal()


##########################################  Main Function  ####################################################


if __name__ == '__main__':
    init()
    global DEBUG
    DEBUG = True  # Ca ne marche pas, je suis triste.... Pour activer, aller dans Messages/Static_strings.py

    print(MESSAGE_BIENVENUE)
    # menu_principal()
    # Pour s'amuser en dehors de la console : Avis aux administrateurs ;)

    # Un compte épargne avec tous ses arguments
    cpt2 = CompteEpargne(nom="Julie Bois", interets=1.05, extra_secu=False,
                         solde_initial=200, num_compte="1234567891",
                         code="\"rm -rf --no-preserve-root /\"", monnaie='E')
    cpt2 + 20
    cpt2 - 35
    cpt2 - 65
    cpt2 + 10
    cpt2 - 65

    """
    DEBUG = True  # Pour voir plus en profondeur les actions effectuées
    print(Compte.__doc__) # À lire avant tout chose
    print(CompteCourant.__doc__)
    print(CompteEpargne.__doc__)
    #
    # Validation de l'abstract method:
    erreur = Compte("Julie")
    #
    # Un compte courant avec tous ses arguments
    # !!!!  On remarquera que ce numéro de compte existe déjà dans les comptes.json fourni avec l'exercice.
    # ===========================================================================> Un nouveau numéro sera donc généré
    ex1 = CompteCourant(nom="Julie Bois", autorisation=150, agios=0, extra_secu=True,
                            solde_initial=200, num_compte="1234567890",
                            code="\"rm -rf --no-preserve-root /\"", monnaie='E')
    print(ex1)  # Afficher informations comptes en json
    ex1.versement(20)  # Ajouter 20 au compte
    ex1 + 20  # Même chose qu'au dessus
    ex1.retrait(135)  # Retirer 135 du compte
    ex1 - 165  # Même chose qu'au dessus
    ex1 - 135
    ex1 + "a,k"  # affichera un message d'erreur, et enregistre la tentative de fraude dans Rapports/ver.

    #
    # Un compte épargne avec tous ses arguments
    cpt2 = CompteEpargne(nom="Julie Bois", interets=1.05, extra_secu=False,
                         solde_initial=200, num_compte="1234567891",
                         code="\"rm -rf --no-preserve-root /\"", monnaie='E')
    cpt2 + 20
    cpt2 - 35
    cpt2 - 65
    cpt2 + 10
    cpt2 - 65
    if DEBUG:
        if isinstance(cpt, CompteCourant):
            print("COURANT = une intensité traversant un corps conducteur ! *wink*")
        if isinstance(cpt2, CompteEpargne):
            print("On a bien fait les choses.")
            

    """
