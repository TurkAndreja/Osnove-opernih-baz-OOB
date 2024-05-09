import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki
import Data.auth_public as auth
import datetime

from Data.models import transakcija, oseba, racun, transakcijaDto, Uporabnik
from typing import List

## V tej datoteki bomo implementirali razred Repo, ki bo vseboval metode za delo z bazo.

class Repo:
    def __init__(self):
        # Ko ustvarimo novo instanco definiramo objekt za povezavo in cursor
        self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=5432)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        
    def dobi_predstave_dto(self) -> List[predstavaDto]:
        self.cur.execute("""
            SELECT o.skladatelj, o.naslov, 
                    oh.ime, oh.naslov, 
                    p.datum, p.cas, 
                    p.cena, o.trajanje, p.komentar
            FROM predstava p 
            join operna_hisa oh on p.id_operne_hise  = oh.id
            join opera o on o.id = p.id_opere
            Order by p.datum, p.cas desc
        """)

        predstave = [predstavaDto.from_dict(t) for t in self.cur.fetchall()]
        return predstave