-- Active: 1709206211024@@baza.fmf.uni-lj.si@5432@sem2024_nezako
INSERT INTO opera (naslov, skladatelj, trajanje, leto)
VALUES ('Cosi fan tutte', 'W. A. Mozart', 195, 1790);

INSERT INTO operna_hisa (ime, naslov)
VALUES ('SNG opera in balet Ljubljana', 'Župančičeva 1, 1000 Ljubljana')

INSERT INTO predstava (id_opere, id_operne_hise, datum, cas, cena, komentar)
VALUES (1, 1, '2024-05-23', NOW(), 15, 'Nič posebega.');