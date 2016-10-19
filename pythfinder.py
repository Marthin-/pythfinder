#!/usr/bin/env python
import sqlite3


def init_db():
	conn = sqlite3.connect('pf.db')
	c=conn.cursor()
	try:
		c.execute("CREATE table joueurs(nom_perso text, nom_joueur text,role text)")
		conn.commit()
	except sqlite3.DatabaseError:
		print("error : table joueurs already exists")
	try:
		c.execute("CREATE table carac_perso(nom_perso text, for real, dex real, con real, int real, sag real, cha real)")
		conn.commit()
	except sqlite3.DatabaseError:
		print("error : table carac_perso already exists")

	conn.close()

def add_user(nom_perso="",nom_joueur="",role="",f=10,dex=10,con=10,inte=10,sag=10,cha=10):
	info=(nom_perso,nom_joueur,role)
	carac=(nom_perso,f,dex,con,inte,sag,cha)
	conn = sqlite3.connect('pf.db')
	c=conn.cursor()
	c.execute("INSERT INTO joueurs VALUES(?,?,?)",info)
	c.execute("INSERT INTO carac_perso VALUES(?,?,?,?,?,?,?)",carac)
	conn.commit()
	conn.close()

def get_player(nom_perso):
	conn = sqlite3.connect('pf.db')
	c=conn.cursor()
	np=(nom_perso,)
	for row in conn.execute('SELECT * FROM joueurs WHERE nom_perso=?',np):
		print(row)
	conn.close()

def get_carac(nom_perso):
	conn = sqlite3.connect('pf.db')
	c=conn.cursor()
	np=(nom_perso,)
	for row in conn.execute('SELECT * FROM carac_perso WHERE nom_perso=?',np):
		print(row)
	conn.close()


init_db()
add_user('fafa','lolo','testeur',12,10,20,3,2,6)
get_carac('fafa')
