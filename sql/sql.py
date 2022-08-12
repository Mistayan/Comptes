from pymongo import MongoClient
import Generateurs as Gen
import messages
from comptes import Compte, CompteCourant, CompteEpargne

def sql_get_all():
    pass


def get_by_num_cpt(num_cpt: str):
    mycollection = connect_mongo("comptes")
    mycollection.find_one({"num_compte": num_cpt})


def connect_mongo(item: str):
    client = MongoClient('localhost', 27017)
    if client:
        if client.command("ping"):
            return client.comptes[item]
    return None

def sql_save(compte):
    print("sqlsave")
    if not issubclass(Compte, compte):
        print("invalid data")
        return False
    print("data_ok")
    j_cpt = compte.__to_json__()
    print(j_cpt)
    table = connect_mongo("comptes")
    index = table.insert(j_cpt)
    print(index)

if __name__ == "__main__":
    cpt = CompteCourant(nom="Julie Bois", code=Gen.chaine_aleatoire(4, messages.DIGITS))
    print(cpt.__to_json__())
