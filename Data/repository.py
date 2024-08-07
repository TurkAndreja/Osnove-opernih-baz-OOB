import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki
import Data.auth as auth #ker je v drugi mapi rabimo Data. ...
import datetime

from Data.models import * # Tole naredi pri vseh trans-datotečnih razredih
from typing import List

## V tej datoteki bomo implementirali razred Repo, ki bo vseboval metode za delo z bazo.

class Repo:
    def __init__(self):
        # Ko ustvarimo novo instanco definiramo objekt za povezavo in cursor
        self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=5432)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        
    def dobi_predstave(self) -> List[predstavaDto]:
        self.cur.execute("""
            SELECT o.skladatelj, o.naslov, 
                    oh.ime AS operna_hisa, oh.naslov AS lokacija, 
                    p.datum, p.cas, 
                    p.cena, o.trajanje, p.komentar
            FROM predstava p 
            JOIN operna_hisa oh ON p.id_operne_hise = oh.id
            JOIN opera o ON o.id = p.id_opere
            ORDER BY p.datum, p.cas desc
        """)

        predstave = [predstavaDto.from_dict(t) for t in self.cur.fetchall()]
        return predstave
    
    def dobi_vloge(self, id_predstave: int) -> List[predstava_vlogaDto]:
        self.cur.execute("""
            SELECT v.ime_vloge, p.ime_pevca, g.fach
            FROM predstava_vloga pv
            JOIN vloga v ON v.id = pv.id_vloge
            JOIN glas g ON g.id = v.id_glasu
            LEFT JOIN pevec p ON p.id = pv.id_pevca
            WHERE id_predstave = %s
        """, (id_predstave))
        
        vloge = [predstava_vlogaDto.from_dict(t) for t in self.cur.fetchall()]
        return vloge
    
    def dobi_pevca():
        return
    
    def dobi_opero():
        return
    
    def dodaj_predstavo(self, p : predstava):
        self.cur.execute("""
            INSERT into predstava(id_opere, id_operne_hise, datum
            cas, cena, komentar)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (p.id, #neki iz cookieja,
                  p.datum, p.cas, p.cena, p.komentar))
        self.conn.commit()
        
    def dodaj_pevca(self, p : pevec, id_vloge : int, id_predstave : int):
        self.cur.execute("""
            UPDATE predstava_vloga SET id_pevca = %s
            WHERE id_vloge = %s
            AND id_predstave = %s
            """, (p.id, id_vloge, id_predstave))
        self.conn.commit()

    
