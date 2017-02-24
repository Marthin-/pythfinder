#!/usr/bin/env python
import math
import random
import sqlite3
import json

from database import Database


# ############## RECUPERER MODIF CARAC ################
def get_mod(val):
    return math.floor((val - 10) / 2)


# #############CLASSE DE##############
class Dice:
    def __init__(self, value=20, crit=20):
        self.value = value
        self.crit = crit

    def roll(self):
        val = self.value
        crit = self.crit
        r = random.randint(1, val)
        if r >= crit:
            print("critical hit !")
        if r == 1:
            print("fumble !")
        return r

    def __str__(self):
        return "{}({})".format(self.value, self.crit)


# ############# CLASSE ITEM ###########

# TODO Classe Item dont héritent les armes, armures et stuff
# Avec une méthode create_item() pour ajouter les items à la DB correspondante

class Item:
    def __init__(self, i_id=0, place="tete"):
        print("Work in progress")
        self.i_id = i_id
        self.place = "tete"  # TODO à ajuster hein
        # TODO "interface" pour relier un Item à une table de la DB (arme, armure, collier, gants...)


# ############# CLASSE ARME ###########
class Arme():
    def __init__(self, w_id=0):
        # TODO : update quand il y a deux dés de dégâts (cimeterre à deux mains)
        print("toto")
        request = db.get_weapon(w_id)
        crit_data = str(request[4]).split('/')
        if len(crit_data) == 2:
            zone = str(request[4]).split('/')[0]  # split pour récupérer la zone de critique
            mult = str(request[4]).split('/')[1]  # split pour récupérer le multiplicateur de critique
        else:
            zone = 20
            mult = crit_data[0]
        self.name = request[1]
        self.damage = request[2]
        print(request)
        self.nb_dice = request[3]
        self.crit = zone
        self.critmul = mult
        self.hands = request[3] + 1  # It works. arme à deux mains ou à trois mains. Oui oui.

    def __str__(self):
        return "{0} : dégats : {1}d{2} crit : {3}{4} main : {5}".format(self.name, self.nb_dice, self.damage,
                                                                        self.crit, self.critmul, self.hands)


# ############ CLASSE ÉQUIPÉ (OBJETS PORTÉS) ############
# TODO : A modifier : Utiliser un dictionnaire avec les ID des différents objets à chaque emplacement
class Equipe:
    def __init__(self, md=0, armor=0, mg=0, tete=0, front=0, yeux=0, epaules=0, corps=0, torse=0, poignets=0, anneau1=0,
                 anneau2=0, cou=0, taille=0, pieds=0):
        # dictionnaire du stuff équipé
        self.slot = {'tete': tete, 'front': front, 'yeux': yeux, 'epaules': epaules, 'corps': corps, 'torse': torse,
                     'poignets': poignets, 'mg': mg, 'md': md, 'anneau1': anneau1, 'anneau2': anneau2, 'armure': armor,
                     'cou': cou, 'taille': taille, 'pieds': pieds}

    def set_item(self, place, i_id):
        self.slot[place] = i_id

    def print_item(self, place):
        print(self.slot[place])

    def print_all_equiped(self):
        print(self.slot.values())


# ############ CLASSE ARMURE ##########
class Armure:
    # TODO : Ajouter un attribut "catégorie" pour limiter les ports d'armures (ex. mages)
    def __init__(self, a_id):
        request = db.get_armor(a_id)
        self.name = request[1]
        self.value = request[2]
        self.max_dex = request[3]
        self.malus_test = request[4]
        self.echec_sort = request[5]

    def __str__(self):
        return "{} : armure {} dext {}  malus {} echec {}".format(self.name, self.value, self.max_dex,
                                                                  self.malus_test, self.echec_sort)

# ############### CLASSE JsonParser #################
## Classe qui parse un fichier json et ajoute l'objet parsé à la BDD
# TODO implé
# from pprint import pprint
class JsonParser:
    def __init__(self, file):
        self.data = ""
        with open(file) as data_file:
            self.data = json.load(data_file)
        print(self.data)
        # pprint(data)


# ############ CLASSE STUFF (AUTRES OBJETS) #########
# TODO bientôt déprecié
class Stuff:
    def __init__(self, car_mod=None, val=0):
        self.car_mod = car_mod
        self.value = val


# ############ CLASSE PERSONNAGE #############
class Perso:
    def __init__(self, name, race, equip, mlvl=1, mbba=0,
                 forc=10, dex=10, con=10, inte=10, sag=10, cha=10,
                 vig=0, ref=0, vol=0):
        # TODO : demander si perso à charger depuis DB ou si nouveau perso
        self.name = name
        self.race = race
        self.stats = [forc, dex, con, inte, sag, cha]
        self.stats_mod = [0, 0, 0, 0, 0, 0]
        self.lvl = mlvl
        self.bba = mbba
        self.dons = []
        self.defenses = [10, ref, vig, vol]  # CA, ref, vig, vol
        self.stuff = []
        self.equipement = equip
        self.sac = []

    # ajouter un objet au sac
    def add_sac(self, item_id):
        self.sac.append(item_id)

    def wear(self, objet):
        possede = False
        for i in range(0, len(self.sac)):
            if objet.i_id == self.sac[i]:
                possede = True
        if possede is False:
            print("vous ne pouvez pas équiper un objet sans le posséder !")
            return -1
        else:
            self.equipement.set_item(objet.place, objet.i_id)

    def jet_comp(self, comp):
        print("Se préparer à attaquer la partie longue...")
        # penser au mod. Dex limité par l'armure
        # et au malus d'armure

    # calculer et lancer jet d'attaque
    def atk(self, arme, mode=0, other=0):
        bonus = self.bba
        togo = bonus
        if mode == 0:  # pas de don
            bonus += get_mod(self.stats[0] + self.stats_mod[0])
        elif mode == 1:  # attaque en puissance
            bonus += (arme.hands / 2) * (get_mod(self.stats[0] + self.stats_mod[0])) - (self.bba / 4)
        elif mode == 2:  # distance/attaque en finesse
            bonus += get_mod(self.stats[1] + self.stats_mod[1])
        bonus += other
        result = []
        while togo >= 0:
            d = Dice()
            result.append(d.roll() + bonus - 1)  # magic number yolo. It works.
            togo -= 6
            bonus -= 6
        return result

    # resoudre defense
    def defense(self, test=0):  # test : place dans tableau defenses
        d = Dice()
        if test == 0:
            return self.defenses[0]
        elif test == 1:
            return d.roll() + get_mod(self.defenses[test] + self.stats[1])
        elif test == 2:
            return d.roll() + get_mod(self.defenses[test] + self.stats[2])
        elif test == 3:
            return d.roll() + get_mod(self.defenses[test] + self.stats[4])


def shell():
    print("pythfinder shell, enter command (help)")
    while 1:
        rawComm = str(input("~> "))
        comm = rawComm.split()
        if comm[0] == "help":
            print("add_user <char name> <username> <role>")
            print("add_perso <race> <force> <dex> <const> <int> <sag> <cha>")
            print("get_carac <nom perso>")
        elif comm[0] == "add_user":
            if len(comm) is not 4:
                print("error with arguments (usage : " + comm[0] + " <character name> <username> <role>")
            else:
                try:
                    db.add_user(comm[1], comm[2], comm[3])
                except sqlite3.DatabaseError:
                    print("could not add user to database !")

        elif comm[0] == "add_perso":
            if len(comm) is not 9:
                print("error with arguments (usage : " + comm[0] +
                      " <nom_perso> <race> <force> <dexterite> <constitution> <intelligence> <sagesse> <charisme>")
            else:
                try:
                    # TODO prendre race en compte
                    db.add_perso(comm[1], comm[3], comm[4], comm[5], comm[6], comm[7], comm[8])
                except sqlite3.DatabaseError:
                    print("could not add character to database !")

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
                print("perso : %s, arme : %s, mode : %s, bonus : %s" % (comm[1], comm[2], comm[3], comm[4],))

        elif comm[0] == "exit":
            print("Exiting pythfinder shell...")
            break


if __name__ == '__main__':
    print("Welcome to Pythfinder <3")
    update_db = False
    db = Database(update_db)  # !! mettre à True pour drop toute la DB !!

    if update_db:
        db.update_weapons()
        db.update_armors()

    # TODO : créer fonction db.save_perso(self, perso) et db.load_perso(self,nom_perso,perso_dest) pour charger/sauver
    # TODO des profils dans la db

    # pas mal de tests, décommenter en cas de debug
    # db.add_user('fafa', 'lolo', 'testeur')
    # db.add_perso('fafa', 12, 10, 20, 3, 2, 6)
    # db.get_carac('fafa')
    # stuff = Equipe()
    # pj = Perso("fonzie", "nain", stuff, 1, 0, 12, 10, 16, 14, 14, 18, 0, 0, 0)
    # pj.equipement = stuff
    # print(pj.name)
    # print("force : " + str(pj.stats[0]))
    # attack = pj.atk(Arme(15))
    # print("jet d'attaque : " + str(attack))
    # db.get_weapon(15)
    uneArme = Arme(54)
    print(uneArme)
    print("test du morgenstern :")
    print(uneArme.name)
    uneArmure = Armure(7)
    print("Test de l'armure matelassée :")
    print(uneArmure.name)
    print("Test de la flamberge de feu +1000")
    unParser = JsonParser('test.json')
    shell()
