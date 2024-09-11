-- Active: 1709206211024@@baza.fmf.uni-lj.si@5432@sem2024_nezako
INSERT INTO opera (naslov, skladatelj, trajanje, leto)
VALUES ('Cosi fan tutte', 'W. A. Mozart', 195, 1790);

INSERT INTO operna_hisa (ime, naslov)
VALUES ('SNG opera in balet Ljubljana', 'Župančičeva 1, 1000 Ljubljana')

INSERT INTO predstava (id_opere, id_operne_hise, datum, cas, cena, komentar)
VALUES (1, 1, '2024-05-23', NOW(), 15, 'Nič posebega.');

INSERT INTO opera (naslov, skladatelj, trajanje, leto) VALUES ('Carmen', 'Georges Bizet', 190, 1875);

INSERT INTO operna_hisa (ime, naslov)
VALUES ('SNG Maribor', 'Slovenska ulica 27, 2000 Maribor');

INSERT INTO vloge (ime_vloge, id_opere, id_glasu) VALUES ('Carmen', 2, 2),('Don José', 2, 3), ('Micaëla',2,1), ('Escamillo',2,4),('Zuniga',2,5),('Moralès',2,4),('Frasquita',2,1),('Mercédès',2,2);

INSERT INTO opera (naslov, skladatelj, trajanje, leto) VALUES ('La Traviata', '	Giuseppe Verdi',160, 1853);

INSERT INTO vloge (ime_vloge, id_opere, id_glasu) VALUES ('Violetta Valéry', 3, 1),('Alfredo Germont', 3, 3), ('Giorgio Germont',3,4), ('Marchese Obigny',3,5),('Flora Bervoix',3,2),('Dottore Grenvil',3,5),('Gastone',3,3),('Barone Douphol',3,4),('Annina',3,1),('Giuseppe',3,3);

INSERT INTO pevec (ime, id_glasu) VALUES ('Diana Damrau',1),('Anna Netrebko',1),('Sabine Devieilhe',1),('Kathleen Battle',1),('Mirella Freni',1),('Elina Garanca',2),('Cecilia Bartoli',2),('Joyce DiDonato',2),('Luciano Pavarotti',3),('Philippe Jaroussky',3),('Plácido Domingo',3),('Jonas Kaufmann',3),('José Carreras',3),('Dmitri Hvorostovsky',4),('Bryn Terfel',4),('Thomas Hampson',4),('Detlef Roth',5),('Bryn Terfel',5),('Ferruccio Furlanetto',5),('Ruggero Raimondi',5),('Ildebrando Arcangelo',5);