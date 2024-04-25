CREATE TABLE glas (
    id INT PRIMARY KEY,
    fach TEXT UNIQUE
)

CREATE TABLE opera (
    id INT PRIMARY KEY,
    naslov TEXT NOT NULL,
    skladatelj TEXT NOT NULL,
    trajanje INT, --v minutah
    leto INT --krstna izvedba
)

CREATE TABLE operna_hisa (
    id INT PRIMARY KEY,
    ime TEXT NOT NULL,
    naslov TEXT UNIQUE
)

CREATE TABLE uporabnik (
    username TEXT PRIMARY KEY,
    password TEXT,
    id_operne_hise INT REFERENCES operna_hisa(id)
)

CREATE TABLE pevec (
    id INT PRIMARY KEY,
    ime TEXT NOT NULL,
    id_glasu INT REFERENCES glas(id)
)

CREATE TABLE vloga (
    id INT PRIMARY KEY,
    ime_vloge TEXT NOT NULL,
    id_opere INT REFERENCES opera(id),
    id_glasu INT REFERENCES glas(id)
)

CREATE TABLE predstava (
    id INT PRIMARY KEY,
    id_opere INT REFERENCES opera(id),
    id_operne_hise INT  REFERENCES operna_hisa(id),
    datum DATE NOT NULL,
    cas TIME NOT NULL,
    cena FLOAT NOT NULL, -- v eur
    komentar TEXT 
)

CREATE TABLE predstava_vloga (
    id_predstave INT  REFERENCES predstava(id),
    id_vloge INT REFERENCES vloga(id),
    id_pevca INT REFERENCES pevec(id),
    PRIMARY KEY(id_predstave, id_vloge)
)