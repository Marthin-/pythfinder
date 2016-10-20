#!/usr/bin/env python
import sqlite3
import random
import math

############### RECUPERER MODIF CARAC ################
def get_mod(val):
	return math.floor((val - 10) / 2)


##############CLASSE DE##############
class dice:
	def __init__(self,value=20):
		self.value=value
	def roll(self,times=1):
		val = self.value
		return random.randint(1,val)

############## CLASSE ARME ###########
class arme:
	def __init__(self, damage,crit,nom,main):
		self.name=nom
		self.damage=damage
		self.crit=crit
		self.main=main+1

############# CLASSE ARMURE ##########
class armure:
	def __init__(self,val=0,categorie=0):
		self.categorie=categorie
		self.value=val

############# CLASSE STUFF (AUTRES OBJETS) #########
class stuff:
	def __init__(self,car_mod,val):
		self.car_mod=car_mod
		self.value=val


############# CLASSE PERSONNAGE #############
class perso:

# init
	def __init__(self, name,mbba=0, mlvl=1,forc=10,dex=10,con=10,inte=10,sag=10,cha=10,vig=0,ref=0,vol=0,arme=None,arme2=None,armure=None,armure2=None):
		self.name = name
		self.stats = [forc,dex,con,inte,sag,cha]
		self.stats_mod = [0,0,0,0,0,0]
		self.lvl = mlvl
		self.bba = mbba
		self.dons = []
		self.defenses=[10,0,0,0] #CA, ref, vig, vol
		self.armes = []
		self.armures = []
		self.stuff = []
		if arme != None:
			self.armes.append(arme)
			if arme2 != None:
				self.armes.append(arme)
		if armure != None:
			self.defenses[0]+=armure.value
			self.armures.append(armure)
			if armure2 != None:
				self.defenses[0]+=armure2.value
				self.armures.append(armure2)
#ajouter arme
def add_armes(self,arme):
	self.armes.append(arme)
#ajouter armure
def add_armure(self,armure):
	self.armures.append(armure)
#calculer et lancer jet d'attaque
def atk(self,mode,arme,other):
	bonus=self.bba
	togo = bonus
	if mode == 0 :#pas de don
		bonus+=self.stats[0]+self.stats_mod[0]
	elif mode == 1 :#attaque en puissance
		bonus+=(arme.main / 2) * (self.stats[0] + self.stats_mod[0]) - (self.bba / 4)
	elif mode == 2 :#distance/attaque en finesse
		bonus+=self.stats[1]+self.stats_mod[1]
	bonus+=other
	result=[]
	while togo >= 0:
		result.append(dice.roll()+bonus)
		togo-=6
		bonus-=6
	return result
# resoudre defense
	def defense(self,test=0):#test : place dans tableau defenses
		if test == 0:
			return self.defenses[0]
		elif test == 1:
			return dice.roll()+self.defenses[test]+get_mod(self.stats[1])
		elif test == 2:
			return dice.roll()+self.defenses[test]+get_mod(self.stats[2])
		elif test == 3:
			return dice.roll()+self.defenses[test]+get_mod(self.stats[4])


####################### INITIALISE GAME DATABASE ###########################
class db:
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





db.init_db()
db.add_user('fafa','lolo','testeur',12,10,20,3,2,6)
db.get_carac('fafa')
pj = perso("fonzie", 1,0,12,10,16,14,14,18,0,0,0)
print(pj.name)
print("force : "+str(pj.stats[0]))
