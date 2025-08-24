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
    
    def dobi_predstavo(self,id) -> predstavaDto:
        return self.repo.dobi_predstavo(id)

    def dobi_vloge(self,id_predstave) -> List[predstava_vlogaDto]:
        return self.repo.dobi_vloge(id_predstave)
    
    def dobi_pevce(self):
        return self.repo.dobi_pevce()
    
    def dobi_seznam_oper(self):
        return self.repo.dobi_seznam_oper()
    
    def dobi_seznam_glasov(self) -> List[glas]:
        return self.repo.dobi_seznam_glasov()
    
    def id_uporabnika(self):
        username = request.get_cookie("uporabnik")  
        # Iz usernama moramo dobiti id_operne_hise, ki je zapisan v kukiju
        u = self.repo.dobi_uporabnika(username)
        return u.id_operne_hise

    def ustvari_predstavo(self,  id_opere : int, datum_str: str, ura_str : str, cena_str: str, komentar: str ) -> None:

        username = request.get_cookie("uporabnik") 

        # Iz usernama moramo dobiti id_operne_hise, ki je zapisan v cookie-ju
        u = self.repo.dobi_uporabnika(username)

        datum = datetime.strptime(datum_str, "%Y-%m-%d").date() # Datum tipa date za v bazo
        ura = datetime.strptime(ura_str, "%H:%M").time()  # Ura tipa time za v bazo
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

    def posodobi_predstavo(self, id_predstave, datum_str, ura_str, cena_str, komentar):
        
        datum = datetime.strptime(datum_str, "%Y-%m-%d").date()
        ura = datetime.strptime(ura_str, "%H:%M").time()
        cena = float(cena_str)
        
        self.repo.posodobi_predstavo(id_predstave, datum, ura, cena, komentar)

    def posodobi_vlogo(self, id_predstave, id_vloge, id_pevca):
        self.repo.posodobi_vlogo(id_predstave, id_vloge, id_pevca)


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
    
    def je_pevec_prost(self, id_pevca, id_predstave):
        return self.repo.je_pevec_prost(id_pevca, id_predstave)
