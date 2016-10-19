#!/usr/bin/env python
import sqlite3


def init_db():
	conn = sqlite3.connect('pf.db')
	c=conn.cursor()
	try:
		c.execute("CREATE table joueurs(nom_perso text, nom_joueur text,role text)")
		com=[('earlinde','soline','dps'),('gunnar','romain','tank'),('fonzie','martin','element comique'),]
		c.executemany("INSERT INTO joueurs VALUES(?,?,?)",com)
		conn.commit()
	except sqlite3.DatabaseError:
		print("error : database already exists")
	for row in conn.execute("select * from joueurs"):
		print(row)
	conn.close()


#
# conn = sqlite3.connect('test.db')
# c = conn.cursor()
#
# c.execute("INSERT INTO test VALUES('tata','toto',10,12)")
# conn.commit()
# conn.close()
#
# conn=sqlite3.connect('test.db')
# c=conn.cursor()
# c.execute("select * from test")
# while (1):
# 	toto = c.fetchone()
# 	if toto is not None:
# 		print(toto)
# 	else:
# 		break
# conn.close()
