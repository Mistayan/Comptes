#! coding:utf-8
"""
Auteur: Misatayan
Projet : Compte-Bancaire
"""


class ErreurUtilisateurNonDefini(Exception):
    # print("Impossible de creer un compte courant en tout anonymat... Vous devriez le savoir")
    pass


class ErreurSolde(Exception):
    # print("Solde Insuffisant")
    pass
