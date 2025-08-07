from Data.repository import Repo
from Data.models import *
from typing import List

class PredstaveService:
    def __init__(self) -> None:
        self.repo = Repo()

    def dobi_predstave(self) -> List[predstavaDto]:
        return self.repo.dobi_predstave()

    def dobi_vloge(self) -> List[predstava_vlogaDto]:
        return self.repo.dobi_vloge()
    
    def ustvari_predstavo(self,  ime_opere : str, datum: datetime, cas : datetime, cena: float, komentar: str ) -> None:

        # potrebujemo id opere
        o = self.repo.dobi_opero(ime_opere) #dobi_opero iz imena pobere ostale podatke

        # objekt za predstavo
        p = predstava(
                id_opere=o.id,
                datum=datum,
                cas=cas,
                cena=cena,
                komentar=komentar
                )
        # zapis v bazo
        self.repo.dodaj_predstavo(p)
        self.repo.dodaj_vloge_predstavi(p)

    def dobi_vse_operne_hise(self) -> List[str]:
        return self.repo.dobi_vse_operne_hise()