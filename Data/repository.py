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
                    p.cena, o.trajanje, p.komentar
            FROM predstava p 
            JOIN operna_hisa oh ON p.id_operne_hise = oh.id
            JOIN opera o ON o.id = p.id_opere
            ORDER BY p.datum, p.cas desc
        """)

        predstave = [predstavaDto.from_dict(t) for t in self.cur.fetchall()] #za vsako vrstico v slovarju, ki ga vrne cursor, naredi objekt dto in te objekte spravi v predstavo
        return predstave
    
    
    def dobi_vloge(self, id_predstave: int) -> List[predstava_vlogaDto]:
        self.cur.execute("""
            SELECT v.ime_vloge, p.ime_pevca, g.fach
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

    
    def dobi_pevce(): # za dropdown seznam
        return
    
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
            INSERT into predstava(id_opere, id_operne_hise, datum, cas, cena, komentar)
            VALUES (%s, %s, %s, %s, %s, %s)
            ''', (#neki iz cookieja,
                  p.id_opere, p.id_operne_hise, p.datum, p.cas, p.cena, p.komentar))
        self.conn.commit()

    def dodaj_vloge_predstavi(self, p: predstava):
        self.cur.execute("""
            INSERT INTO predstava_vloga (id_predstave, id_vloge, id_pevca) (
                         SELECT pr.id, vl.id, NULL
                         FROM predstava pr, vloga vl
                         WHERE pr.id_opere = vl.id_opere
                         AND pr.id_opere = %s AND pr.id_operne_hise= %s AND pr.datum= %s AND pr.cas = %s)
            """, (p.id_opere, p.id_operne_hise, p.datum, p.cas,)) #POZOR! to ni najboljše, ker je načeloma lahko v isti operni hiši ista opera na isti dan ob istem času izvajana dvakrat. Ampak v realnem svetu to verjetno ni zelo, tako da to možnost zanemarimo - žal po nobenih drugih parametrih ne moremo poiskati idja predstave, zato se bomo morali zadovoljiti s tem - pomankljivo začetno načrtovanje
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

# import psycopg2, psycopg2.extensions, psycopg2.extras
# psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
# from Data import auth
# from Data.models import *
# from typing import List

# class Repo:
#     def __init__(self):
#         self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=5432)

#     def dobi_predstave(self) -> List[predstavaDto]:
#         with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
#             cur.execute("""
#                 SELECT o.skladatelj, o.naslov, 
#                        oh.ime AS operna_hisa, oh.naslov AS lokacija, 
#                        p.datum, p.cas, 
#                        p.cena, o.trajanje, p.komentar
#                 FROM predstava p 
#                 JOIN operna_hisa oh ON p.id_operne_hise = oh.id
#                 JOIN opera o ON o.id = p.id_opere
#                 ORDER BY p.datum, p.cas desc
#             """)
#             predstave = [predstavaDto.from_dict(t) for t in cur.fetchall()]
#         return predstave

#     def dobi_vloge(self, id_predstave: int) -> List[predstava_vlogaDto]:
#         with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
#             cur.execute("""
#                 SELECT v.ime_vloge, p.ime_pevca, g.fach
#                 FROM predstava_vloga pv
#                 JOIN vloga v ON v.id = pv.id_vloge
#                 JOIN glas g ON g.id = v.id_glasu
#                 LEFT JOIN pevec p ON p.id = pv.id_pevca
#                 WHERE id_predstave = %s
#             """, (id_predstave,))
#             vloge = [predstava_vlogaDto.from_dict(t) for t in cur.fetchall()]
#         return vloge

#     def dobi_glas(self, fach: str) -> glas:
#         with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
#             cur.execute("""
#                 SELECT id, fach
#                 FROM glas
#                 WHERE fach = %s
#             """, (fach,))
#             result = cur.fetchone()
#             if result:
#                 g = glas.from_dict(result)
#             else:
#                 g = None
#         return g

#     def dobi_pevce(self):
#         # Implementacija, če jo potrebuješ
#         pass

#     def dobi_seznam_oper(self):
#         with self.conn.cursor() as cur:
#             cur.execute("SELECT id, naslov, skladatelj FROM opera")
#             seznam = cur.fetchall()
#         return seznam

#     def dobi_seznam_glasov(self):
#         with self.conn.cursor() as cur:
#             cur.execute("SELECT id, fach FROM glas")
#             seznam = cur.fetchall()
#         return seznam

#     def dobi_opero(self, ime_opere) -> opera:
#         with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
#             cur.execute("""
#                 SELECT id, naslov, skladatelj, trajanje, leto
#                 FROM opera
#                 WHERE naslov = %s
#             """, (ime_opere,))
#             result = cur.fetchone()
#             if result:
#                 o = opera.from_dict(result)
#             else:
#                 o = None
#         return o

#     def dodaj_predstavo(self, p: predstava):
#         with self.conn.cursor() as cur:
#             cur.execute('''
#                 INSERT INTO predstava(id_opere, id_operne_hise, datum, cas, cena, komentar)
#                 VALUES (%s, %s, %s, %s, %s, %s)
#             ''', (p.id_opere, p.id_operne_hise, p.datum, p.cas, p.cena, p.komentar))
#             self.conn.commit()

#     def dodaj_vloge_predstavi(self, p: predstava):
#         with self.conn.cursor() as cur:
#             cur.execute("""
#                 INSERT INTO predstava_vloga (id_predstave, id_vloge, id_pevca)
#                 SELECT pr.id, vl.id, NULL
#                 FROM predstava pr, vloga vl
#                 WHERE pr.id_opere = vl.id_opere
#                 AND pr.id = %s
#             """, (p.id,))
#             self.conn.commit()

#     def dodaj_pevca_predstavi(self, p: pevec, id_vloge: int, id_predstave: int):
#         with self.conn.cursor() as cur:
#             cur.execute("""
#                 UPDATE predstava_vloga SET id_pevca = %s
#                 WHERE id_vloge = %s
#                 AND id_predstave = %s
#             """, (p.id, id_vloge, id_predstave))
#             self.conn.commit()

#     def dodaj_uporabnika(self, uporabnik: uporabnik):
#         with self.conn.cursor() as cur:
#             cur.execute("""
#                 INSERT INTO uporabnik(username, password, id_operne_hise)
#                 VALUES (%s, %s, %s)
#             """, (uporabnik.username, uporabnik.password, uporabnik.id_operne_hise))
#             self.conn.commit()

#     def dobi_uporabnika(self, username: str) -> uporabnik:
#         with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
#             cur.execute("""
#                 SELECT username, password, id_operne_hise
#                 FROM uporabnik
#                 WHERE username = %s
#             """, (username,))
#             result = cur.fetchone()
#             if result:
#                 u = uporabnik.from_dict(result)
#             else:
#                 u = None
#         return u

#     def dobi_operno_hiso(self, id: int) -> operna_hisa:
#         with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
#             cur.execute("""
#                 SELECT id, ime, naslov
#                 FROM operna_hisa
#                 WHERE id = %s
#             """, (id,))
#             result = cur.fetchone()
#             if result:
#                 o = operna_hisa.from_dict(result)
#             else:
#                 o = None
#         return o

#     def dobi_operno_hiso_poimenu(self, ime: str) -> operna_hisa:
#         with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
#             cur.execute("""
#                 SELECT id, ime, naslov
#                 FROM operna_hisa
#                 WHERE ime = %s
#             """, (ime,))
#             result = cur.fetchone()
#             if result:
#                 o = operna_hisa.from_dict(result)
#             else:
#                 o = None
#         return o

#     def dodaj_opero(self, o: opera):
#         with self.conn.cursor() as cur:
#             cur.execute("""
#                 INSERT INTO opera(naslov, skladatelj, trajanje, leto)
#                 VALUES (%s, %s, %s, %s)
#             """, (o.naslov, o.skladatelj, o.trajanje, o.leto))
#             self.conn.commit()

#     def dodaj_vloge(self, dvojice: list, id_opere: int):
#         with self.conn.cursor() as cur:
#             for vloga, id_glasu in dvojice:
#                 cur.execute("""
#                     INSERT INTO vloga (ime_vloge, id_opere, id_glasu)
#                     VALUES (%s, %s, %s)
#                 """, (vloga, id_opere, id_glasu))
#             self.conn.commit()

#     def dodaj_pevca(self, p: pevec):
#         with self.conn.cursor() as cur:
#             cur.execute("""
#                 INSERT INTO pevec(ime, id_glasu)
#                 VALUES (%s, %s)
#             """, (p.ime, p.id_glasu))
#             self.conn.commit()
