"""
Created by: Mistayan
Project: Comptes-Bancaire
"""
from _md5 import md5


class Override:
    pass


class Encrypt:

    def __init__(self, to_crypt):
        self.to_encrypt = to_crypt
        self.vv = vars()
        print(f"demo helper: {self.vv} => {self.__str__()}")

    def __str__(self):
        return md5(str(self.to_encrypt).encode("utf-8")).hexdigest()
