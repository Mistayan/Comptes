#! encoding:utf-8 --!#
""""
Editeur: Mistayan
Projet: Comptes-Bancaires
"""

##########################################  IMPORTS  ###############################################
import json
import logging
import math
import os
import platform
import re
import sys

from hashlib import md5
from json import JSONDecodeError

#### MODULES PROJET
#
import Generateurs as Gen
import messages as msgs
import verifications as Secu
from comptes import CompteCourant, CompteEpargne, Compte


##########################################  fonctions utiles  ######################################
def folders_init():
    try:
        os.mkdir("Rapports")
    except FileExistsError:
        pass
    try:
        os.mkdir("Historique")
    except FileExistsError:
        pass
    try:
        os.mkdir("clients")
    except FileExistsError:
        pass


def init_with_file() -> list[CompteCourant | CompteEpargne]:
    """
        Init permet de creer les dossiers de base, pour le bon fonctionnement du programme.
        Si comptes.json existe, recupere les informations des comptes,
         pour les ajouter à liste_comptes
    """
    liste_comptes = []
    print("Chargement des comptes à partir du fichier comptes.json")

    try:
        with Gen.my_open("comptes.json", 'r+') as fp:
            liste_json = json.load(fp)  # Charge les comptes dans l'application sous forme [{},{}]
    except JSONDecodeError:
        liste_json = []
        print(msgs.PREMIER_CLIENT)

    # Transformation du fichier en comptes...
    for j_compte in liste_json:
        if j_compte and Secu.verif_format(j_compte):  # si les infos sont 'valides'
            cpt = Gen.json_en_compte(j_compte)
            if cpt:
                liste_comptes.append(cpt)  # Ajoute le compte à la liste memoire de l'application

    return liste_comptes


def init_with_mongo() -> list:
    # Importing required modules
    from pymongo import MongoClient

    # Connecting to MongoDB server
    # client = MongoClient('host_name', 'port_number')
    client = MongoClient('localhost', 27017)
    # Connecting to the database named comptes
    db = client.comptes
    # Accessing the collection named comptes
    mycollection = db.comptes
    # Now creating a Cursor instance using find() function
    # Gather every occurrence
    cursor = mycollection.find()
    # Converting cursor to the list of dictionaries
    list_cur = list(cursor)

    # Transformation du json en comptes...
    liste_comptes = []
    for j_compte in list_cur:
        if j_compte and Secu.verif_format(j_compte):  # si les infos sont 'valides'
            cpt = Gen.json_en_compte(j_compte)
            if cpt:
                liste_comptes.append(cpt)  # Ajoute le compte à la liste memoire de l'application
    return liste_comptes


def clear():
    """Nettoie l'ecran"""
    match platform.system():
        case "Windows":
            os.system('cls')
        case "Linux":
            os.system('clear')
        case "Darwin":
            os.system('clear')  # IOs
        case _:
            sys.exit(msgs.OS_ERREUR)


# #####################  ELEMENTS DU MENU APP  #################################

def quitter():
    """ Quitter l'interface"""
    print(msgs.AUREVOIR_MSG)
    sys.exit()


def print_ticket(num_cpt, old, new):
    """ Imprime le ticket de transaction dans la console"""
    old = round(old, 2)
    new = round(new, 2)
    ticket = f"Compte: {num_cpt}\n" \
             f"Solde avant opération: {old}\n" \
             f"Nouveau Solde: {new}" if old != new else "Solde Insuffisant"
    print("-" * 20)
    print(ticket)
    print("-" * 20)


def gestion_compte(compte, solde=math.pi):
    """ Permet de gerer un compte (faire des operations dessus)
    Prends un compte(Epargne/Courant) en parametre."""
    clear()
    if not solde == math.pi:
        compte.afficher_solde()
    while True:
        print("\n".join(msgs.MENU_GESTION))
        choix = input(msgs.ASK)
        match choix:
            case "1":
                return gestion_compte(compte, 0)
            case "2":
                old = compte.get_solde()
                new = compte.retrait(input("Combien souhaitez-vous retirer? (0 pour annuler)"))
                print_ticket(compte.get_num(), old, new)
            case "3":
                old = compte.get_solde()
                new = compte.versement(input("Combien souhaitez-vous deposer? (0 pour annuler)"))
                print_ticket(compte.get_num(), old, new)
            case "4":
                user_msg = input("Votre message ? (nous reviendrons vers vous au plus vite)\n?>")
                Gen.fraude(compte.get_num(), "reclamation", user_msg)
                print("Merci pour votre participation.")
            case "5":
                print()
                print(compte.__to_json__())
                return gestion_compte(liste_comptes)
            case "6":
                print("A bientot !")
                return menu_principal(liste_comptes)
            case _:
                pass
    # END while


def ask_nom(type_compte):
    """Demande son nom à l'utilisateur. S'il souhaite creer un compte Courant,
     le nom est obligatoire."""
    nom = None
    clear()
    while nom is None:
        nom = input("votre nom:" + ("(Obligatoire)" if type_compte == "c" else "") + msgs.ASK)
        if len(nom) == 0 and type_compte == "c":
            nom = None
            print("Vous devez rentrer un nom!")
        else:
            return nom


def ask_parano():
    """Demande à l'utilisateur s'il souhaite une securite supplementaire sur son code"""
    parano = None
    clear()
    while parano is None:
        parano = input("mode securite etendu ?"
                       " (ceci permet d'utiliser tout type de characters pour le code) [O/n]")
        if re.match(r"^[yYoO]$", parano):
            return True
        elif re.match(r"^[nN]$", parano):
            return False
        parano = None
        print("Valeur eronnee, recommencez")


def ask_decouvert():
    """Demande à l'utilisateur le decouvert qu'il souhaiterait, on controlera les valeurs
    renseignees"""
    decouvert = None
    clear()
    while decouvert is None:
        decouvert = input("Combien souhaitez-vous de decouvert autorise ?")
        if re.match(r"^\d*[.|,]?\d*$", decouvert):  # Un nombre(, a virgule)?
            return decouvert
        else:
            decouvert = None
            print("Valeur eronnee, recommencez")


def questionnaire_commun(type_compte):
    """Demande les informations de base d'un compte"""
    nom = ask_nom(type_compte)
    parano = ask_parano()
    return [nom, parano]


def questionnaire_courant() -> CompteCourant:
    """Assistant à la creation d'un compte courant"""
    clear()
    infos = questionnaire_commun("c")
    infos.append(ask_decouvert())
    try:
        num = float(infos[2])
    except ValueError:
        num = 0
    return CompteCourant(nom=infos[0], extra_secu=infos[1], autorisation=num, new=True)


def questionnaire_epargne() -> CompteEpargne:
    """Assistant à la creation d'un compte Epargne"""
    clear()

    infos = questionnaire_commun("e")
    cpt = CompteEpargne(nom=infos[0], extra_secu=infos[1], new=True)

    return cpt


def acces_compte(liste_comptes, essais: int = 0):
    """
        Demande la combinaison compte + code, pour plus de securite #DummySpecs
         Si la combinaison est fausse, alors on le laisse essayer... 3fois.

    :param essais: Nombre d'essais infructueux
    """

    if len(liste_comptes) == 0:
        print("Aucun compte à charger. Veuillez en creer un.")
        creer_compte(liste_comptes)
    ### Controls d'erreurs
    if essais >= 3 or essais < 0:
        print(msgs.ACCES_REFUSE)
        input(msgs.CONTINUER)
        menu_principal(liste_comptes)

    #  Demande de renseigner les donnees
    print(msgs.DEMANDER_COMPTE)
    compte = input(msgs.ASK)
    if len(compte) != 10:
        acces_compte(liste_comptes, essais)
    # md5 sous forme hexa, de input cast en string encodee utf-8
    code_md5 = md5(str(input(msgs.DEMANDER_CODE)).encode("utf-8")).hexdigest()

    # ## Verifier les donnees fournies
    # !!!# cpt de type compteEpargne ou CompteCourant.
    for cpt in liste_comptes:
        # print(f"{type(cpt)}Compte : {cpt}")
        # On demande au compte si les valeurs fournies sont correctes
        if cpt.connect(compte,
                       code_md5, with_db=False):
            print(f"Bienvenue sur votre compte.")
            gestion_compte(cpt)
        else:
            pass  # Les donnees du compte ne semblent pas correctes
    acces_compte(liste_comptes, essais + 1)


def creer_compte(liste_comptes):
    """Demande quel type de compte le client souhaite creer"""
    clear()
    print(msgs.ACTIONS_CREER_COMPTE)
    choix = input(msgs.FAIRE_CHOIX)
    match choix:
        case "1":
            liste_comptes.append(questionnaire_courant())
        case "2":
            liste_comptes.append(questionnaire_epargne())
        case "3":
            menu_principal(liste_comptes)
        case _:
            print(msgs.INVALIDE)
            creer_compte(liste_comptes)


def menu_principal(liste_comptes):
    """
    Menu principal de l'interface utilisateur.
    Permet d'acceder un compte, ou d'en creer un
    """
    print(msgs.ACTIONS_MENU_PRINCIPAL)
    choix = input(msgs.FAIRE_CHOIX)
    match choix:
        case "1":
            acces_compte(liste_comptes)
        case "2":
            creer_compte(liste_comptes)
        case "3":
            quitter()
        case "4":
            for cpt in liste_comptes:
                print(cpt.__to_json__())
        case _:
            print(msgs.INVALIDE)
    menu_principal(liste_comptes)


# ##########################  Main Function  ###################################
if __name__ == '__main__':
    # liste_comptes = init_with_mongo()
    folders_init()
    liste_comptes = init_with_file()
    print("liste des comptes d'essai pré-construits (mdp: \"rm -rf --no-preserve-root /\")")
    [print(cpt.__str__()) for cpt in liste_comptes]
    # Pour s'amuser en dehors de la console : Avis aux administrateurs ;)
    # Pour voir plus en profondeur les actions effectuees
    # Modifier DEBUG dans messages/static_strings.py
    print("\n\nDocumentation de Compte :")
    print(Compte.__doc__)  # À lire avant tout chose
    print("\n\nDocumentation de CompteCourant :")
    print(CompteCourant.__doc__)
    print("\n\nDocumentation de CompteEpargne :")
    print(CompteEpargne.__doc__)
    #
    # Validation de l'abstract method:
    print("\n\nvalidation de l'abstract methode de Compte :")
    try:
        erreur = Compte("Julie")  # Erreur bloquante de type TypeError
    except TypeError as err:
        print(err)
    #
    # Un compte courant avec tous ses arguments
    # !!!!  On remarquera que ce numero de compte existe dejà dans les comptes.json
    # fourni avec l'exercice.
    # ===============================================> Un nouveau numero sera donc genere
    ex1 = CompteCourant(nom="Julie Bois", autorisation=150, agios=0, extra_secu=True,
                        solde_initial=200, num_compte="1234567890",
                        code="\"rm -rf --no-preserve-root /\"", monnaie='E', new=True)
    #  print(ex1)  # Afficher informations comptes en json
    ex1._recuperer_code()  # Je pensais pas que ça marcherait !
    ex1.versement(20)  # Ajouter 20 au compte
    ex1.afficher_solde()
    ex1 + 20  # Même chose qu'au dessus
    ex1.afficher_solde()
    ex1.retrait(135)  # Retirer 135 du compte
    ex1.afficher_solde()
    ex1 - 165  # Même chose qu'au dessus
    ex1.afficher_solde()
    ex1 - 135
    liste_comptes.append(ex1)
    try:
        # affichera un message d'erreur, enregistre la tentative de fraude dans Rapports/versement.
        ex1 + "a,k"
    except ValueError as err:
        logging.warning(err)
    try:
        # affichera un message d'erreur, enregistre la tentative de fraude dans Rapports/versement.
        ex1 + "-12"
    except ValueError as err:
        logging.warning(err)

    # Un compte epargne avec tous ses arguments
    cpt2 = CompteEpargne(nom="Julie Bois", interets=1.05, extra_secu=False,
                         solde_initial=200, num_compte="1234567891",
                         code='"rm -rf --no-preserve-root /"', monnaie='E', new=True)
    cpt2 + 20
    cpt2 - 35
    cpt2 - 65
    cpt2 + 10
    cpt2 - 65
    liste_comptes.append(cpt2)
    if isinstance(ex1, CompteCourant):
        print("COURANT = une intensite traversant un corps conducteur ! *wink*")

    print("\n" * 5 + "Fin de la démonstration... à votre tour de vous amuser !")
    menu_principal(liste_comptes)
