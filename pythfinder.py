#!/usr/bin/env python
import sqlite3


def init_db():
	conn = sqlite3.connect('pf.db')
	c=conn.cursor()
	try:
		c.execute("CREATE table joueurs(nom_perso text, nom_joueur text,role text)")
		conn.commit()
	except sqlite3.DatabaseError:
		print("error : database already exists")
	for row in conn.execute("select * from joueurs"):
		print(row)
	conn.close()

def add_users(nom_perso="",nom_joueur="",role=""):
	info=(nom_perso,nom_joueur,role)
	conn = sqlite3.connect('pf.db')
	c=conn.cursor()
	c.execute("INSERT INTO joueurs VALUES(?,?,?)",info)
	conn.close()

def get_player(nom_perso):
	conn = sqlite3.connect('pf.db')
	c=conn.cursor()
	np=(nom_perso,)
	# c.execute("SELECT * FROM joueurs WHERE nom_perso=?",nom_perso)
	for row in conn.execute('SELECT * FROM joueurs WHERE nom_perso=?',np):
		print(row)
	conn.close()

get_player('earlinde')
