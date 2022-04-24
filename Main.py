##########################################  IMPORTS  ####################################################
from hashlib import md5
from json import JSONDecodeError

import os
import platform
import sys
import json
import re

#### MODULES PROJET
#
import Generateurs as Gen
import Verifications as Secu
import Message
from Comptes import Compte, CompteCourant, CompteEpargne


#
####

########################################## GLOBALES  ####################################################

##########################################  fonctions utiles  ####################################################
def init() -> list:
    """
        Init permet de créer les dossiers de base, pour le bon fonctionnement du programme.
        Si comptes.json existe, récupère les informations des comptes, pour les ajouter à liste_comptes
    """
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

    liste_comptes = []
    f = Gen.my_open("comptes.json", 'r+')
    try:
        liste_json = json.load(f)  # Charge les comptes dans l'application sous forme [{},{}]
    except JSONDecodeError:
        liste_json = []
        print(Message.PREMIER_CLIENT)
    f.close()

    ### Transformation du json en comptes...
    for j_compte in liste_json:
        if j_compte and Secu.verif_format(j_compte):  # si les infos sont 'valides'
            cpt = Gen.json_en_compte(j_compte)
            if cpt is not None:
                liste_comptes.append(cpt)  # Ajoute le compte à la liste memoire de l'application

    return liste_comptes


def clear():
    """
    Nettoie l'ecran
    """
    match platform.system():
        case "Windows":
            os.system('cls')
        case "Linux":
            os.system('clear')
        case "Darwin":
            os.system('clear')  # IOs
        case _:
            sys.exit(Message.OS_ERREUR)


##########################################  ELEMENTS DU MENU APP  ####################################################

def quitter():
    """Quitter l'interface"""
    print(Message.AUREVOIR_MSG)
    sys.exit()


def gestion_compte(compte, auth=None):
    """Permet de gérer un compte (faire des opérations dessus)
    Prends un compte(Epargne/Courant) en parametre."""
    while True:
        clear()
        print("1: Afficher le solde du compte.")
        print("2: Retirer de l'argent.")
        print("3: Deposer de l'argent.")
        print("4: Faire une réclamation.")
        print("4: Deconnexion")
        choix = input(Message.ASK)
        match choix:
            case "1":
                compte.afficher_solde()
            case "2":
                compte.retrait(input("Combien souhaitez-vous retirer?"))
            case "3":
                compte.versement(input("Combien souhaitez-vous deposer?"))
            case "4":
                return menu_principal(liste_comptes)
            case _:
                pass

    # END while


def ask_code(mode_parano: bool):
    """Demande le code voulu à l'utilisateur, en tenant compte de son choix sur la parano"""
    code = None
    while code is None:
        if mode_parano is True:
            message_dynamique = "(ce que vous voulez, minimum 4 characters)"
        else:
            message_dynamique = "(4 chiffres)"
        code = input("Inserez le code voulu" + message_dynamique + Message.ASK)
        if mode_parano and len(code) >= 4:
            return code
        elif len(code) == 4 and re.match(r'[0-9]{4}', code):
            return code
        if len(code) == 0:
            return ''
        code = None
    return code


def ask_nom(type_compte):
    """Demande son nom à l'utilisateur. S'il souhaite créer un compte Courant, le nom est obligatoire."""
    nom = None
    while nom is None:
        nom = input("votre nom " + "(Obligatoire)" if type_compte == "c" else "" + Message.ASK)
        if len(nom) == 0 and type_compte == "c":
            nom = None
            print("Vous devez rentrer un nom!")
        else:
            return nom


def ask_parano():
    """Demande à l'utilisateur s'il souhaite une securite supplementaire sur son code"""
    parano = None
    while parano is None:
        parano = input("mode securite etendu ? (ceci permet d'utiliser tout type de characters pour le code) [O/n]")
        if re.match(r"^[yYoO]$", parano):
            return True
        elif re.match(r"^[nN]$", parano):
            return False
        parano = None
        print("Valeur éronnée, recommencez")


def ask_decouvert():
    """Demande à l'utilisateur le decouvert qu'il souhaiterait, on controlera les valeurs renseignees"""
    decouvert = None
    while decouvert is None:
        decouvert = input("Combien souhaitez-vous de découvert autorise ?")
        if re.match(r"^[0-9]*\.?[0-9]*$", decouvert):  # Un nombre(, a virgule)?
            return decouvert
        else:
            decouvert = None
            print("Valeur éronnée, recommencez")


def questionnaire_commun(type_compte):
    """Demande les informations de base d'un compte"""
    nom = ask_nom(type_compte)
    parano = ask_parano()
    code = ask_code(parano)
    return [nom, code]


def questionnaire_courant() -> CompteCourant:
    """Assistant à la création d'un compte courant"""
    infos = questionnaire_commun("c")
    infos.append(ask_decouvert())
    return CompteCourant(nom=infos[0], code=infos[1], autorisation=float(infos[2]))


def questionnaire_epargne() -> CompteEpargne:
    """Assistant à la création d'un compte Epargne"""
    infos = questionnaire_commun("e")
    return CompteEpargne(nom=infos[0], code=infos[1])


def acces_compte(liste_comptes, essais: int = 0):
    """
        Demande la combinaison compte + code, pour plus de sécurité #DummySpecs
         Si la combinaison est fausse, alors on le laisse essayer... 3fois.

    :param essais: Nombre d'essais infructueux
    """

    if len(liste_comptes) == 0:
        print("Aucun compte à charger. Veuillez en créer un.")
        creer_compte(liste_comptes)
    ### Controls d'erreurs
    if essais >= 3 or essais < 0:
        print(Message.ACCES_REFUSE)
        input(Message.CONTINUER)
        menu_principal(liste_comptes)

    #  Demande de renseigner les données
    print(Message.DEMANDER_COMPTE)
    compte = input(Message.ASK)
    # md5 sous forme hexa, de input cast en string encodee utf-8
    code_md5 = md5(str(input(Message.DEMANDER_CODE)).encode("utf-8")).hexdigest()

    ### Verifier les données fournies
    # !!!# cpt de type CompteEpargne ou CompteCourant.
    for cpt in liste_comptes:
        # print(f"{type(cpt)}Compte : {cpt}")
        if cpt.connect(compte, code_md5):  # On demande au compte si les valeurs fournies sont correctes
            print(f"Bienvenue sur votre compte.")
            gestion_compte(cpt)
        else:
            pass  # Les donnees du compte ne semblent pas correctes
    acces_compte(liste_comptes, essais + 1)



def creer_compte(liste_comptes):
    """Demande quel type de compte le client souhaite créer"""
    print(Message.CREER_COMPTE)
    choix = input(Message.FAIRE_CHOIX)
    match choix:
        case "1":
            liste_comptes.append(questionnaire_courant())
        case "2":
            liste_comptes.append(questionnaire_epargne())
        case "3":
            menu_principal(liste_comptes)
        case _:
            print(Message.INVALIDE)
            creer_compte(liste_comptes)


def menu_principal(liste_comptes):
    """Menu principal de l'interface utilisateur. Permet d'accéder un compte, ou d'en créer un"""
    print(Message.MAIN_CHOIX_ACTION)
    choix = input(Message.FAIRE_CHOIX)
    match choix:
        case "1":
            acces_compte(liste_comptes)
        case "2":
            creer_compte(liste_comptes)
        case "3":
            quitter()
        case "4":
            if Message.DEBUG:
                print(liste_comptes)
                for cpt in liste_comptes:
                    print(str(cpt))
        case _:
            print(Message.INVALIDE)
    menu_principal(liste_comptes)


##########################################  Main Function  ####################################################


if __name__ == '__main__':
    liste_comptes = init()
    print(Message.MESSAGE_BIENVENUE)
    menu_principal(liste_comptes)
    # Pour s'amuser en dehors de la console : Avis aux administrateurs ;)

    # Pour voir plus en profondeur les actions effectuées #Modifier dans Message/Static_strings.py
    """
    print(Compte.__doc__) # À lire avant tout chose
    print(CompteCourant.__doc__)
    print(CompteEpargne.__doc__)
    #
    # Validation de l'abstract method:
    #erreur = Compte("Julie")
    """
    #
    # Un compte courant avec tous ses arguments
    # !!!!  On remarquera que ce numéro de compte existe déjà dans les comptes.json fourni avec l'exercice.
    # ===========================================================================> Un nouveau numéro sera donc généré
    """ex1 = CompteCourant(nom="Julie Bois", autorisation=150, agios=0, extra_secu=True,
                        solde_initial=200, num_compte="1234567890",
                        code="\"rm -rf --no-preserve-root /\"", monnaie='E')
    #  print(ex1)  # Afficher informations comptes en json
    ex1._recuperer_code()  # Je pensais pas que ça marcherait !
    ex1.versement(20)  # Ajouter 20 au compte
    ex1 + 20  # Même chose qu'au dessus
    ex1.retrait(135)  # Retirer 135 du compte
    ex1 - 165  # Même chose qu'au dessus
    ex1 - 135"""
    #  ex1 + "a,k"  # affichera un message d'erreur, et enregistre la tentative de fraude dans Rapports/versement.

    #
    # Un compte épargne avec tous ses arguments
    """
    cpt2 = CompteEpargne(nom="Julie Bois", interets=1.05, extra_secu=False,
                         solde_initial=200, num_compte="1234567891",
                         code="\"rm -rf --no-preserve-root /\"", monnaie='E')
        cpt2 + 20
        cpt2 - 35
        cpt2 - 65
        cpt2 + 10
        cpt2 - 65
        """

    if Message.DEBUG:
        if isinstance(cpt, CompteCourant):
            print("COURANT = une intensité traversant un corps conducteur ! *wink*")
        if isinstance(cpt2, CompteEpargne):
            print("On a pas si bien fait les choses.... Agilité sera la prochaine étape")
