#Vsakič na začetku env\Scripts\activate v terminal napiši

from repository import Repo # če si v mapi Data ni treba Data.repository
from models import *
import Services.auth_service
from Services.auth_service import AuthService

repo = Repo()
auth = AuthService()

# Dobimo vse osebe

predstave = repo.dobi_predstave()


# Jih izpišemo
for p in predstave:
    print(p)

# Izberemo si recimo neko predstavo
p1 = predstave[0]

jaz = auth.dodaj_uporabnika('nejc.skrbec@operabalet-lj.si', 'SNG opera in balet Ljubljana', 'nejc')
print(jaz)

# KAKO ZAČETI:
# python3 -m venv env
# source env/bin/activate
# pip install psycopg2
# pip install dataclasses-json

# Če ti še kaj teži, uporabit chat GPT