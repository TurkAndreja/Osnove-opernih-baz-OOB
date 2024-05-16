#Vsakič na začetku env\Scripts\activate v terminal napiši

from Data.repository import Repo
from Data.models import *


repo = Repo()

# Dobimo vse osebe

predstave = repo.dobi_predstave()


# Jih izpišemo
for p in predstave:
    print(p)

# Izberemo si recimo neko predstavo
p1 = predstave[0]

