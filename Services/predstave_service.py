from Data.repository import Repo
from Data.models import *
from typing import List

class PredstaveService:
    def __init__(self) -> None:
        # Potrebovali bomo instanco repozitorija. Po drugi strani bi tako instanco 
        # lahko dobili tudi kot input v konstrukturju.
        self.repo = Repo()

    def dobi_predstave(self) -> List[predstavaDto]:
        return self.repo.dobi_predstave()
