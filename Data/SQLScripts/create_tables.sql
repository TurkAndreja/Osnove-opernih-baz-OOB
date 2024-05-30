DROP TABLE glas;
CREATE TABLE glas (
    id SERIAL PRIMARY KEY,
    fach TEXT UNIQUE
)

DROP TABLE opera;
CREATE TABLE opera (
    id SERIAL PRIMARY KEY,
    naslov TEXT NOT NULL,
    skladatelj TEXT NOT NULL,
    trajanje INT, --v minutah
    leto INT --krstna izvedba
)

DROP TABLE operna_hisa;
CREATE TABLE operna_hisa (
    id SERIAL PRIMARY KEY,
    ime TEXT NOT NULL,
    naslov TEXT UNIQUE
)

DROP TABLE uporabnik;
CREATE TABLE uporabnik (
    username TEXT PRIMARY KEY,
    password TEXT,
    id_operne_hise INT REFERENCES operna_hisa(id)
)

DROP TABLE pevec;
CREATE TABLE pevec (
    id SERIAL PRIMARY KEY,
    ime TEXT NOT NULL,
    id_glasu INT REFERENCES glas(id)
)

DROP TABLE vloga;
CREATE TABLE vloga (
    id SERIAL PRIMARY KEY,
    ime_vloge TEXT NOT NULL,
    id_opere INT REFERENCES opera(id),
    id_glasu INT REFERENCES glas(id)
)

DROP TABLE predstava;
CREATE TABLE predstava (
    id SERIAL PRIMARY KEY,
    id_opere INT REFERENCES opera(id),
    id_operne_hise INT  REFERENCES operna_hisa(id),
    datum DATE NOT NULL,
    cas TIME NOT NULL,
    cena FLOAT NOT NULL, -- v eur
    komentar TEXT 
)

DROP TABLE predstava_vloga;
CREATE TABLE predstava_vloga (
    id_predstave INT  REFERENCES predstava(id),
    id_vloge INT REFERENCES vloga(id),
    id_pevca INT REFERENCES pevec(id),
    PRIMARY KEY(id_predstave, id_vloge)
)