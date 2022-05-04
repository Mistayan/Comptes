#! encoding:utf-8 --!#
""""
Editeur: Mistayan
Projet: Comptes-Bancaires
"""
from string import digits as DIGITS
from string import hexdigits as HEXADECIMAL

DEBUG = False
NO_CODE = False

NOM_BANQUE = "Anno Banque"
MESSAGE_BIENVENUE = f"Bonjour, et bienvenue chez {NOM_BANQUE}.\n" \
                    f"Nous allons vous guider dans vos premier pas avec nous."
EXECUTE = "S'il vous plait, veuillez executer  Main.py, a la racine du projet."
FAIRE_CHOIX = "Faites votre choix :>?"
INVALIDE = "Choix invalide, recommencez"
EXPLICATION_COMPTE_COURANT = "Ce compte vous permet d'avoir un decouvert autorise." \
                             " En contre partie," \
                             " si vous utilisez" \
                             " cet argent, vous serez deduit d'un montant supplementaire," \
                             " conformement aux lois en vigueur"

EXPLICATION_COMPTE_EPARGNE = "Ce compte vous permet de gagner de l'argent."\
                             " Ce taux est susceptible d'evoluer." \
                             " Vous en serez notifie a l'avance via votre" \
                             " application."

CREER_COMPTE = "C'est avec le plus grand plaisir que nous allons vous guider" \
               " pour la creation de votre compte Anno.\n" \
               "Quel type de compte souhaitez vous ouvrir ?\n" \
               f"\t1: Compte Courant:\n\t\t{EXPLICATION_COMPTE_COURANT}\n" \
               f"\t2: Compte Epargne:\n\t\t{EXPLICATION_COMPTE_EPARGNE}\n" \
               f"\t3: Revenir en arriere."

ASK = "?>"
DEMANDER_COMPTE = "Pour acceder a votre compte, nous aurions besoin de votre numero de compte" \
                  " (il se compose de 10 chiffres):"
PREMIER_CLIENT = "Actuellement, aucun fichier de sauvegarde n'existe.\n" \
                 "Felicitations ! vous etes notre premier client !"

DEMANDER_CODE = f"Renseignez votre code{ASK}"
ACCES_REFUSE = "Trop d'essais infructueux; essayez plus tard.\n Vous allez etre" \
               " redirige vers le menu principal...\n"
CONTINUER = "Veuillez appuyer sur ENTREE pour continuer."
OS_ERREUR = "OS  inconnu. Veuillez contacter le support, nous ferons notre possible pour vous servir"

COUP_DE_POUCE = "Vous venez d'utiliser votre coup de pouce.\n" \
                "Votre prochaine tentative de retrait en negatif" \
                " appliquera des frais supplementaires"
POSITIF = "Rien a faire. L'utilisateur est en positif"
ASK_CODE = "Quel est votre code?"
SOLDE_ERROR_MSG = "Impossible de retirer une valeur negative sur le compte!"
NEGATIF_MSG = "Impossible de deposer une valeur negative sur le compte!"
ERREUR_NOMBRES = "Seulement des nombres positifs (et '.') sont acceptes."
MAIN_CHOIX_ACTION = "Veuillez choisir l'action que vous voulez effectuer :\n" \
                    "1: Acceder a un compte deja existant.\n" \
                    "2: Creer un compte.\n" \
                    "3: Quitter l'interface."
ACCES_COMPTE = "Vous Souhaitez acceder a un compte, Renseignez le numero de compte"
COMPTE_ERREUR = "Ce compte n'est pas renseigne dans notre banque de donnee.\n" \
                "L'avez-vous bien renseigne ?"
COMPTE_TROUVE = "Nous avons trouve votre compte; Nous avons maintenant besoin" \
                " de votre code, pour vous connecter"
ACCES_AUTORISE = "L'acces a votre compte autorise"
AUREVOIR_MSG = "Ce fut un plaisir de vous voir, a bientot"

BRAIN_FUCK = "[]><.,+-"



#Alias
def hexa():
    return HEXADECIMAL

def digits():
    return DIGITS
