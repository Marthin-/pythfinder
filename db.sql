drop table if exists arme_perso;
drop table if exists perso;
drop table if exists arme;
drop table if exists joueurs;
drop table if exists race;

create table joueurs (
  joueur_id integer primary key autoincrement,
  nom_perso text not null,
  nom_joueur text not null,
  role text not null
);

create table perso (
  perso_id integer primary key autoincrement,
  nom_perso text not null,
  race integer,
  force integer,
  dexterite integer,
  constitution integer,
  intelligence integer,
  sagesse integer,
  charisme integer,
FOREIGN KEY(race) REFERENCES race(race_id)
 );

create table race (
  race_id integer primary key autoincrement,
  nom text not null
);

create table arme_perso (
  arme_id integer,
  perso_id integer,
  munition integer,
  FOREIGN KEY(perso_id) REFERENCES perso(perso_id)
  FOREIGN KEY(arme_id) REFERENCES arme(arme_id)
);

create table arme (
  arme_id integer primary key autoincrement,
  nom_arme text not null,
  base_degats integer not null,
  mult_degats integer,
  mod_degat text,
  porte text
);