from Data.repository import Repo
from Data.models import *
from typing import List
from bottle import request
from datetime import datetime


class PredstaveService:
    def __init__(self) -> None:
        self.repo = Repo()

    def dobi_predstave(self) -> List[predstavaDto]:
        return self.repo.dobi_predstave()

    def dobi_vloge(self) -> List[predstava_vlogaDto]:
        return self.repo.dobi_vloge()
    
    def dobi_seznam_oper(self):
        return self.repo.dobi_seznam_oper()
    
    def dobi_seznam_glasov(self) -> List[glas]:
        return self.repo.dobi_seznam_glasov()
    
    def ustvari_predstavo(self,  id_opere : int, datum_str: str, ura_str : str, cena_str: str, komentar: str ) -> None:

        # potrebujemo id opere: to nam obrazez že vrže
        #o = self.repo.dobi_opero(ime_opere) #dobi_opero iz imena pobere ostale podatke

        username = request.get_cookie("uporabnik")  
        # 'uporabnik' je ID operne hiše, zato moramo iz usernama dobiti id_operne hise, ki je zapisan v kukiju
        u = self.repo.dobi_uporabnika(username)

        datum = datetime.strptime(datum_str, "%Y-%m-%d").date() #to je zdaj datum tipa date za v bazo

        ura = datetime.strptime(ura_str, "%H:%M").time()  # datetime.time(14, 30) uro da v tip time za bazo

        cena = float(cena_str)

        # objekt za predstavo
        p = predstava(
                id_opere=id_opere,
                id_operne_hise=u.id_operne_hise,            
                datum=datum,
                cas=ura,
                cena=cena,
                komentar=komentar
                )
        # zapis v bazo
        self.repo.dodaj_predstavo(p)      
        self.repo.dodaj_vloge_predstavi(p)


    def ustvari_opero(self, naslov: str, skladatelj:str, trajanje: int, leto: int) -> None:
       
        # Naredimo objekt za opero
        # Za to potrebujemo številko računa.
        
        # Naredimo objekt za transakcijo
        o = opera(
            naslov=naslov,
            skladatelj=skladatelj,
            trajanje=trajanje,
            leto=leto
            )        
        # uporabimo repozitorij za zapis v bazo
        self.repo.dodaj_opero(o)


    def ustvari_vloge(self, dvojice: List, ime_opere: str) -> None:

        o = self.repo.dobi_opero(ime_opere)
        id_opere = o.id

        nove_dvojice = []           #dvojice, kjer je najprej vloga in potem id glasu, ne pa vloga in tip glasu
        for vloga, fach in dvojice:
            g = self.repo.dobi_glas(fach)
            g_id = g.id
            nove_dvojice.append((vloga, g_id))
        
        self.repo.dodaj_vloge(nove_dvojice, id_opere)


    def ustvari_pevca(self, ime: str, glas_id: int) -> None:

        p = pevec(ime = ime,
                  id_glasu = glas_id)
        self.repo.dodaj_pevca(p)

        
    def dobi_vse_operne_hise(self) -> List[str]:
        return self.repo.dobi_vse_operne_hise()
