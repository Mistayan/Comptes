class UndefinedUserError(Exception):
    print("Impossible de créer un compte courant en tout anonymat... Vous devriez le savoir")
    pass

class SoldeError(Exception):
    print("Solde Insuffisant")
    pass
