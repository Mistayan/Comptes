#! encoding:utf-8 --!#
""""
Init des packages de verifications
Editeur: Mistayan
Projet: Comptes-Bancaires
"""
from .ErrorsHandling import ErreurUtilisateurNonDefini, ErreurSolde
from .securite import dispo, scan_file, verif_format
