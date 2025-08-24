import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki
from Data import auth as auth #Data.auth as auth #če je v drugi mapi rabimo Data. ...
import datetime
from datetime import date, time, datetime

from Data import models
from Data.models import * #Data.models import * # Tole naredi pri vseh trans-datotečnih razredih
from typing import List

## V tej datoteki bomo implementirali razred Repo, ki bo vseboval metode za delo z bazo.

class Repo:
    def __init__(self):
        # Ko ustvarimo novo instanco definiramo objekt za povezavo in cursor
        self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=5432)
        #self.conn.set_client_encoding('UTF8')
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        
    def dobi_predstave(self) -> List[predstavaDto]:
        self.cur.execute("""
            SELECT o.skladatelj, o.naslov, 
                    oh.ime AS operna_hisa, oh.naslov AS lokacija, 
                    p.datum, p.cas, 
                    p.cena, o.trajanje, p.komentar,
                    p.id AS id_predstave, oh.id AS id_operne_hise
            FROM predstava p 
            JOIN operna_hisa oh ON p.id_operne_hise = oh.id
            JOIN opera o ON o.id = p.id_opere
            ORDER BY p.datum, p.cas desc
        """)

        predstave = [predstavaDto.from_dict(t) for t in self.cur.fetchall()] #za vsako vrstico v slovarju, ki ga vrne cursor, naredi objekt dto in te objekte spravi v predstavo
        return predstave
    

    def dobi_predstavo(self, id) -> predstavaDto:
        self.cur.execute("""
            SELECT o.skladatelj, o.naslov, 
                    oh.ime AS operna_hisa, oh.naslov AS lokacija, 
                    p.datum, p.cas, 
                    p.cena, o.trajanje, p.komentar,
                    p.id AS id_predstave, oh.id AS id_operne_hise
            FROM predstava p
            JOIN operna_hisa oh ON p.id_operne_hise = oh.id
            JOIN opera o ON o.id = p.id_opere
                WHERE p.id = %s
            ORDER BY p.datum, p.cas desc
        """, (id,))

        predstava = predstavaDto.from_dict(self.cur.fetchall()[0]) #za edino vrstico v slovarju, ki ga vrne cursor, naredi objekt dto in ga spravi v predstavo
        return predstava
    
    
    def dobi_vloge(self, id_predstave: int) -> List[predstava_vlogaDto]:
        self.cur.execute("""
            SELECT v.id AS id_vloge, v.ime_vloge, p.id as id_pevca, p.ime AS ime_pevca, 
                    g.id AS id_glasu, g.fach
            FROM predstava_vloga pv
            JOIN vloga v ON v.id = pv.id_vloge
            JOIN glas g ON g.id = v.id_glasu
            LEFT JOIN pevec p ON p.id = pv.id_pevca
            WHERE id_predstave = %s
        """, (id_predstave,))
        
        vloge = [predstava_vlogaDto.from_dict(t) for t in self.cur.fetchall()]
        return vloge
    
    def dobi_glas(self, fach: str) -> glas:
        self.cur.execute("""
            SELECT id, fach
            FROM glas
            WHERE fach = %s
        """, (fach,))
        
        g = glas.from_dict(self.cur.fetchone())
        return g

    
    def dobi_pevce(self) -> List[pevec]: # za dropdown seznam
        self.cur.execute("""
            SELECT p.id, p.ime, g.id AS id_glasu
            FROM pevec p
            JOIN glas g ON p.id_glasu = g.id
        """)
        
        pevci = [pevec.from_dict(t) for t in self.cur.fetchall()]
        return pevci
    
    
    def dobi_seznam_oper(self): # za dropdown seznam, vrne seznam trojic (opera id, naslov, skladatelj)
        self.cur.execute("""
                         SELECT id, naslov, skladatelj FROM opera
                         """)
        seznam = self.cur.fetchall()
        return seznam
    
    def dobi_seznam_glasov(self): # za dropdown seznam, vrne seznam parov (id, fach)
        self.cur.execute("""
                         SELECT id, fach FROM glas
                         """)
        seznam = self.cur.fetchall()
        return seznam

    def dobi_opero(self, ime_opere) -> opera: # zato da iz imena pridobiš še ostale podatke za vnašanje
        self.cur.execute("""
            SELECT id, naslov, skladatelj, trajanje, leto
            FROM opera
            WHERE naslov = %s
        """, (ime_opere,))
        
        o = opera.from_dict(self.cur.fetchone())
        return o

    
    def dodaj_predstavo(self, p : predstava): #Id je autoincrement
        self.cur.execute('''
            INSERT INTO predstava(id_opere, id_operne_hise, datum, cas, cena, komentar)
            VALUES (%s, %s, %s, %s, %s, %s)
            ''', (p.id_opere, p.id_operne_hise, p.datum, p.cas, p.cena, p.komentar))
        self.conn.commit()


    def posodobi_predstavo(self, id_predstave, datum, ura, cena, komentar):
        self.cur.execute('''
            UPDATE predstava
            SET datum = %s,
                cas = %s,
                cena = %s,
                komentar = %s
            WHERE id = %s         
            ''', (datum, ura, cena, komentar, id_predstave))
        self.conn.commit()


    def posodobi_vlogo(self, id_predstave, id_vloge, id_pevca):
        self.cur.execute('''
            UPDATE predstava_vloga
            SET id_pevca = %s
            WHERE id_predstave = %s
            AND id_vloge = %s          
            ''', (id_pevca, id_predstave, id_vloge))
        self.conn.commit()


    def dodaj_vloge_predstavi(self, p: predstava):
        self.cur.execute("""
            INSERT INTO predstava_vloga (id_predstave, id_vloge, id_pevca) (
                         SELECT pr.id, vl.id, NULL
                         FROM predstava pr, vloga vl
                         WHERE pr.id_opere = vl.id_opere
                         AND pr.id_opere = %s AND pr.id_operne_hise= %s AND pr.datum= %s AND pr.cas = %s)
            """, (p.id_opere, p.id_operne_hise, p.datum, p.cas,))
        self.conn.commit()

    def dodaj_pevca_predstavi(self, p : pevec, id_vloge : int, id_predstave : int):
        self.cur.execute("""
            UPDATE predstava_vloga SET id_pevca = %s
            WHERE id_vloge = %s
            AND id_predstave = %s
            """, (p.id, id_vloge, id_predstave,))
        self.conn.commit()

    def dodaj_uporabnika(self, uporabnik: uporabnik):
        self.cur.execute("""
            INSERT into uporabnik(username, password, id_operne_hise)
            VALUES (%s, %s, %s)
            """, (uporabnik.username, uporabnik.password, uporabnik.id_operne_hise))
        self.conn.commit()


    def dobi_uporabnika(self, username: str) -> uporabnik:
        self.cur.execute("""
            SELECT username, password, id_operne_hise
            FROM uporabnik
            WHERE username = %s
        """, (username,))

        u = uporabnik.from_dict(self.cur.fetchone())
        return u


    def dobi_operno_hiso(self, id: int) -> operna_hisa:
        self.cur.execute("""
            SELECT id, ime, naslov
            FROM operna_hisa
            WHERE id = %s
        """, (id,))
        o = operna_hisa.from_dict(self.cur.fetchone())
        return o
    
    def dobi_operno_hiso_poimenu(self, ime: str) -> operna_hisa:
        self.cur.execute("""
            SELECT id, ime, naslov
            FROM operna_hisa
            WHERE ime = %s
        """, (ime,))
        o = operna_hisa.from_dict(self.cur.fetchone())
        return o

    
    def dodaj_opero(self, o : opera): #Id je autoincrement
        self.cur.execute("""
            INSERT into opera(naslov, skladatelj, trajanje, leto)
            VALUES (%s, %s, %s, %s)
            """, (
                  o.naslov, o.skladatelj, o.trajanje, o.leto))
        self.conn.commit()

        
    def dodaj_vloge(self, dvojice: list, id_opere: int):
        for vloga, id in dvojice:
            self.cur.execute("""
                INSERT INTO vloga (ime_vloge, id_opere, id_glasu)
                VALUES (%s, %s, %s)
                """, (vloga, id_opere, id))
        self.conn.commit()


    def dodaj_pevca(self, p: pevec):
        self.cur.execute("""
            INSERT into pevec(ime, id_glasu)
            VALUES (%s, %s)
            """, (
                  p.ime, p.id_glasu))
        self.conn.commit()

        
    def dobi_vse_operne_hise(self) -> List[str]:
        self.cur.execute("""
            SELECT ime
            FROM operna_hisa
            ORDER BY ime
        """)
        hise = [hisa['ime'] for hisa in self.cur.fetchall()]
        return hise
    
    def je_pevec_prost(self, id_pevca, id_predstave) -> bool:
        self.cur.execute("""
            SELECT *
            FROM predstava_vloga pv
            JOIN predstava p ON pv.id_predstave = p.id
            WHERE pv.id_pevca = %s
            AND pv.id_predstave != %s
            AND p.datum = (SELECT datum FROM predstava WHERE id = %s)
        """, (id_pevca, id_predstave, id_predstave))

        zasedenost = self.cur.fetchall()
        return len(zasedenost) == 0
