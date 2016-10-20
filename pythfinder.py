#!/usr/bin/env python
import sqlite3
import random
import math

############### RECUPERER MODIF CARAC ################
def get_mod(val):
	return math.floor((val - 10) / 2)


##############CLASSE DE##############
class dice:
	def __init__(self,value=20,crit=20):
		self.value=value
		self.crit=crit
	def roll(self):
		val = self.value
		crit= self.crit
		r = random.randint(1,val)
		if r >= crit:
			print("critical hit !")
		if r == 1:
			print("fumble !")
		return r

############## CLASSE ARME ###########
class arme:
	def __init__(self, damage=6,nbd=1,crit=20,critmul=2,nom="epee",main=1):
		self.name=nom
		self.damage=damage
		self.nb_dice=nbd
		self.crit=crit
		self.crit_mul=critmul
		self.main=main+1

############# CLASSE ARMURE ##########
class armure:
	def __init__(self,val=0,categorie=0):
		self.categorie=categorie
		self.value=val

############# CLASSE STUFF (AUTRES OBJETS) #########
class stuff:
	def __init__(self,car_mod=None,val=0):
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
	def atk(self,arme,mode=0,other=0):
		bonus=self.bba
		togo = bonus
		if mode == 0 :#pas de don
			bonus+=get_mod(self.stats[0]+self.stats_mod[0])
		elif mode == 1 :#attaque en puissance
			bonus+=(arme.main / 2) * (get_mod(self.stats[0] + self.stats_mod[0])) - (self.bba / 4)
		elif mode == 2 :#distance/attaque en finesse
			bonus+=get_mod(self.stats[1]+self.stats_mod[1])
		bonus+=other
		result=[]
		while togo >= 0:
			d=dice()
			result.append(d.roll()+bonus-1)#magic number yolo. It works.
			togo-=6
			bonus-=6
		return result
	# resoudre defense
		def defense(self,test=0):#test : place dans tableau defenses
			d=dice()
			if test == 0:
				return self.defenses[0]
			elif test == 1:
				return d.roll()+get_mod(self.defenses[test]+self.stats[1])
			elif test == 2:
				return d.roll()+get_mod(self.defenses[test]+self.stats[2])
			elif test == 3:
				return d.roll()+get_mod(self.defenses[test]+self.stats[4])


####################### INITIALISE GAME DATABASE ###########################
class db:
	def init_db():
		conn = sqlite3.connect('pf.db')
		c=conn.cursor()
		try:
			c.execute("CREATE table joueurs(nom_perso text, nom_joueur text,role text)")
			conn.commit()
		except sqlite3.DatabaseError:
			print("did not create : table joueurs already exists")
		try:
			c.execute("CREATE table carac_perso(nom_perso text, for real, dex real, con real, int real, sag real, cha real)")
			conn.commit()
		except sqlite3.DatabaseError:
			print("did not create : table carac_perso already exists")
		try:
			c.execute("CREATE table stuff_perso(nom_perso text, for real, dex real, con real, int real, sag real, cha real)")
			conn.commit()
		except sqlite3.DatabaseError:
			print("did not create : table stuff_perso already exists")
		conn.close()

	def add_user(nom_perso="empty",nom_joueur="nobody",role="useless",f=10,dex=10,con=10,inte=10,sag=10,cha=10):
		info=(nom_perso,nom_joueur,role)
		carac=(nom_perso,f,dex,con,inte,sag,cha)
		conn = sqlite3.connect('pf.db')
		c=conn.cursor()
		c.execute("INSERT INTO joueurs VALUES(?,?,?)",info)
		c.execute("INSERT INTO carac_perso VALUES(?,?,?,?,?,?,?)",carac)
		conn.commit()
		conn.close()

	def add_stuff(nom_perso="empty",categorie="stuff",nom="empty"):
		info=(nom_perso,categorie,nom)
		conn = sqlite3.connect('pf.db')
		c=conn.cursor()
		c.execute("INSERT INTO stuff_perso VALUES(?,?,?)",info)
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
attack = pj.atk(arme())
print("jet d'attaque : " + str(attack))