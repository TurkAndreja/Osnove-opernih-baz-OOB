from Data.repository import Repo
from Data.models import *
from typing import List, Union
import bcrypt
from datetime import date


class AuthService:
    repo : Repo
    def __init__(self):
         self.repo = Repo()

    def obstaja_uporabnik(self, uporabnik: str) -> bool:
        try:
            user = self.repo.dobi_uporabnika(uporabnik)
            return True
        except:
            return False

    def prijavi_uporabnika(self, uporabnik : str, geslo: str) -> Union[uporabnikDto, bool]:

        user = self.repo.dobi_uporabnika(uporabnik)
        geslo_bytes = geslo.encode('utf-8')

        succ = bcrypt.checkpw(geslo_bytes, user.password.encode('utf-8'))

        if succ:
            hisa = self.repo.dobi_operno_hiso(user.id_operne_hise)
            return uporabnikDto(username=user.username, ime_operne_hise=hisa.ime)

        return False

    def dodaj_uporabnika(self, uporabnisko_ime: str, ime_operne_hise: str, geslo: str) -> uporabnikDto:

        bytes = geslo.encode('utf-8')
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(bytes, salt)
        password = password_hash.decode('utf-8')

        hisa = self.repo.dobi_operno_hiso_poimenu(ime_operne_hise)
        if hisa is None:
            raise Exception("Operna hiša s tem imenom ne obstaja.")

        u = uporabnik(
            username=uporabnisko_ime,
            password=password,
            id_operne_hise=hisa.id
        )
        self.repo.dodaj_uporabnika(u)

        return uporabnikDto(username=uporabnisko_ime, ime_operne_hise=ime_operne_hise)