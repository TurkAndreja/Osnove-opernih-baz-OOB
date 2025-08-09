from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import date, time, datetime


@dataclass_json
@dataclass
class glas:
    id : int = field(default=0)
    fach : str = field(default="")
    
@dataclass_json
@dataclass
class opera:
    id : int = field(default=0)
    naslov : str = field(default="")   
    skladatelj : str = field(default="")   
    trajanje : int = field(default=0)
    leto : int = field(default=0)

@dataclass_json
@dataclass
class operna_hisa:
    id : int = field(default=0)
    ime : str = field(default="")   
    naslov : str = field(default="")   


@dataclass_json
@dataclass
class uporabnik:
    username : str = field(default="")   
    password : str = field(default="") # v bazi je samo password
    id_operne_hise : int = field(default=0)

@dataclass
class uporabnikDto:
    ime_operne_hise : str = field(default="")
    username: str = field(default="")
    
@dataclass_json
@dataclass
class pevec:
    id : int = field(default=0)
    ime : str = field(default="")   
    id_glasu : int = field(default=0)
    
@dataclass_json
@dataclass
class vloga:
    id : int = field(default=0) 
    ime_vloge : str = field(default="")   
    id_opere : int = field(default=0)
    id_glasu : int = field(default=0)     
    
@dataclass_json
@dataclass
class predstava:
    id : int = field(default=0)
    id_opere : int = field(default=0)
    id_operne_hise : int = field(default=0) 
    datum : datetime = field(default=datetime.now()) 
    cas: datetime = field(default=datetime.now())   
    cena : float = field(default=0)
    komentar: str = field(default="") 
    

    
@dataclass_json
@dataclass
class predstava_vloga:
    id_predstave : int = field(default=0)  
    id_vloge : int = field(default=0)
    id_pevca : int = field(default=0)   
    


@dataclass_json
@dataclass
class predstavaDto:
    skladatelj : str = field(default="") 
    naslov : str = field(default="")
    operna_hisa : str = field(default="")   
    lokacija : str = field(default="")  
    datum : date = field(default_factory=date.today)  # pravi datum
    cas: time = field(default_factory=lambda: datetime.now().time())  # pravi čas 
    cena : float = field(default=0)
    trajanje : int = field(default=0)
    komentar: str = field(default="") 


# Tvoj problem je, da v predstavaDto definiraš datum in ura kot:

# python
# Kopiraj
# Uredi
# datum : datetime.date = field(default=datetime.now())
# ura: datetime.time = field(default=datetime.now())
# Kot sem prej omenil, tukaj se:

# datetime.now() vrne celoten datetime objekt, ne samo date ali time.

# In ker je to default, se ta vrednost izračuna ena sama pot ob definiciji razreda, ne ob vsakem klicu.

# Poleg tega ni pretvorbe iz vrednosti iz baze (verjetno tip tuple ali dict z vrednostmi) v date in time, zato from_dict v dataclasses_json uporabi default (trenutni datum/čas).
     


@dataclass_json
@dataclass
class predstava_vlogaDto:
    ime_vloge : str = field(default="") 
    ime_pevca : str = field(default="") 
    fach : str = field(default="")
    
    
