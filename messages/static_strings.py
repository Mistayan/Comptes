#! encoding:utf-8 --!#
""""
Editeur: Mistayan
Projet: Comptes-Bancaires
"""
from string import digits as string_digits
from string import hexdigits as hexadecimal

DEBUG = False
NO_CODE = True  # vérification une fois connecté, à chaque action utilisateur ?

NOM_BANQUE = "Anno Banque"
MESSAGE_BIENVENUE = f"Bonjour, et bienvenue chez {NOM_BANQUE}.\n" \
                    f"Nous allons vous guider dans vos premier pas avec nous."
ASK = "?>"
EXECUTE = "S'il vous plait, veuillez executer  Main.py, a la racine du projet."
INVALIDE = "Choix invalide, recommencez"
EXPLICATION_COMPTE_COURANT = "Ce compte vous permet d'avoir un decouvert autorise." \
                             " En contre partie, si vous utilisez" \
                             " cet argent, vous serez deduit d'un montant supplementaire," \
                             " conformement aux lois en vigueur"
EXPLICATION_COMPTE_EPARGNE = "Ce compte vous permet de gagner de l'argent." \
                             " Ce taux est susceptible d'evoluer." \
                             " Vous en serez notifie a l'avance via votre" \
                             " application."

DEMANDER_COMPTE = "Pour acceder a votre compte, nous aurions besoin de votre numero de compte" \
                  " (il se compose de 10 chiffres):"
PREMIER_CLIENT = "Actuellement, aucun fichier de sauvegarde n'existe.\n" \
                 "Felicitations ! vous etes notre premier client !"

FAIRE_CHOIX = f"Faites votre choix {ASK}"
DEMANDER_CODE = f"Renseignez votre code{ASK}"
ACCES_REFUSE = "Trop d'essais infructueux; essayez plus tard.\n Vous allez etre" \
               " redirige vers le menu principal...\n"
CONTINUER = "Veuillez appuyer sur ENTREE pour continuer."
OS_ERREUR = "OS  inconnu. Veuillez contacter le support," \
            " nous ferons notre possible pour vous servir"

COUP_DE_POUCE = "Vous venez d'utiliser votre coup de pouce.\n" \
                "Votre prochaine tentative de retrait en negatif" \
                " appliquera des frais supplementaires"
ASK_CODE = "Quel est votre code?"
ERREUR_NOMBRES = "Seulement des nombres positifs (et '.') sont acceptes."
AUREVOIR_MSG = "Ce fut un plaisir de vous voir, a bientot"
BRAIN_FUCK = "[]><.,+-"

ACTIONS_CREER_COMPTE = "C'est avec le plus grand plaisir que nous allons vous guider" \
               " pour la creation de votre compte Anno.\n" \
               "Quel type de compte souhaitez vous ouvrir ?\n" \
               f"\t1: Compte Courant:\n\t\t{EXPLICATION_COMPTE_COURANT}\n" \
               f"\t2: Compte Epargne:\n\t\t{EXPLICATION_COMPTE_EPARGNE}\n" \
               f"\t3: Revenir en arriere."
ACTIONS_MENU_PRINCIPAL = "Veuillez choisir l'action que vous voulez effectuer :\n" \
                    "1: Acceder a un compte deja existant.\n" \
                    "2: Creer un compte.\n" \
                    "3: Quitter l'interface."
MENU_GESTION = [
    "1: informations du compte.", "2: Retirer de l'argent.",
    "3: Deposer de l'argent.", "4: Faire une reclamation.",
    "5: Deconnexion"
]


# Alias
def digits():
    return string_digits


def hexa():
    return hexadecimal
