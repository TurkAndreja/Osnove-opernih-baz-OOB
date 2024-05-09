from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime


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
    password : str = field(default="") 
    id_operne_hise : int = field(default=0)
    
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
    datum : datetime = field(default=datetime.now()) 
    ura: datetime = field(default=datetime.now()) 
    cena : float = field(default=0)
    trajanje : int = field(default=0)
    komentar: str = field(default="") 
     
@dataclass_json
@dataclass
class predstava_vlogaDto:
    ime_vloge : str = field(default="") 
    ime_pevca : str = field(default="") 
    fach : str = field(default="")
    
    
