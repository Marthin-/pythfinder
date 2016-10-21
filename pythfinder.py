#!/usr/bin/env python
import sqlite3
import random
import math
from database import Database


############### RECUPERER MODIF CARAC ################
def get_mod(val):
    return math.floor((val - 10) / 2)


##############CLASSE DE##############
class dice:
    def __init__(self, value=20, crit=20):
        self.value = value
        self.crit = crit

    def roll(self):
        val = self.value
        crit = self.crit
        r = random.randint(1,val)
        if r >= crit:
            print("critical hit !")
        if r == 1:
            print("fumble !")
        return r


############## CLASSE ARME ###########
class arme:
    def __init__(self, damage=6, nbd=1, crit=20, critmul=2, nom="epee", main=1):
        self.name = nom
        self.damage = damage
        self.nb_dice = nbd
        self.crit = crit
        self.crit_mul = critmul
        self.main = main+1


############# CLASSE ARMURE ##########
class armure:
    def __init__(self, val=0, categorie=0):
        self.categorie = categorie
        self.value = val


############# CLASSE STUFF (AUTRES OBJETS) #########
class stuff:
    def __init__(self, car_mod=None, val=0):
        self.car_mod = car_mod
        self.value = val


############# CLASSE PERSONNAGE #############
class perso:

# init
    def __init__(self, name, mbba=0, mlvl=1,
                 forc=10, dex=10, con=10, inte=10, sag=10, cha=10,
                 vig=0, ref=0, vol=0,
                 arme=None, arme2=None, armure=None, armure2=None):
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
        if arme is not None:
            self.armes.append(arme)
            if arme2 is not None:
                self.armes.append(arme)
        if armure is not None:
            self.defenses[0]+=armure.value
            self.armures.append(armure)
            if armure2 is not None:
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




def shell():
    print("pythfinder shell, enter command (help)")
    while 1:
        rawComm = str(input("~> "))
        comm = rawComm.split()
        if comm[0] == "help":
            print("It works !")
        elif comm[0] == "add_user":
            if len(comm) is not 4:
                print("error with arguments (usage : "+comm[0]+" <character name> <username> <role>")
            else:
                try:
                    db.add_user(comm[1],comm[2],comm[3])
                except sqlite3.DatabaseError:
                    print("could not add user to database !")

        elif comm[0] == "add_perso":
            if len(comm) is not 9:
                print("error with arguments (usage : " + comm[0] + " <nom_perso> <race> <force> <dexterite> <constitution> <intelligence> <sagesse> <charisme>")
            else:
                try:
                    #TODO prendre race en compte
                    db.add_perso(comm[1],comm[3],comm[4],comm[5],comm[6],comm[7],comm[8])
                except sqlite3.DatabaseError:
                    print("could not add character to database !")

        elif comm[0] == "init_db":
            pass
            # db.init_db()

        elif comm[0] == "get_carac":
            if len(comm) is not 2:
                print("error with arguments (usage : " + comm[0] + " <nom_perso>")
            else:
                db.get_carac(comm[1])
        elif comm[0] == "atk":
            if len(comm) > 5:
                print("error with arguments : usage : atk -p=<perso> -a=<arme> -m=<mode> -b=<bonus/malus>")
            else:
                print("en cours d'implé")
                print("perso : %s, arme : %s, mode : %s, bonus : %s" %(comm[1],comm[2],comm[3],comm[4],))

        elif comm[0] == "exit":
            print("Exiting pythfinder shell...")
            break

db = Database(True)
db.add_user('fafa','lolo','testeur')
db.add_perso('fafa',12,10,20,3,2,6)
db.get_carac('fafa')
pj = perso("fonzie", 1,0,12,10,16,14,14,18,0,0,0)
print(pj.name)
print("force : "+str(pj.stats[0]))
attack = pj.atk(arme())
print("jet d'attaque : " + str(attack))
shell()