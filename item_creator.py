#!/usr/bin/env python3

import os
from random import randint  # pour générer le nom de fichier
from subprocess import *

if __name__ == "__main__":
    print("Bienvenue dans l\"éditeur d\"objets de pythfinder")
    print("Choisissez le nom de votre objet")
    nom = str(input(">>> "))
    print("Choisissez le type (l\"emplacement) d\"objet dans la liste :")
    print("1 : Arme")
    print("2 : Armure")
    print("3 : Tête (casque...)")
    print("4 : Front (bandeau, couronne)")
    print("5 : Yeux (lunettes)")
    print("6 : Epaules (spallières ?)")
    print("7 : Corps (Vêtements)")
    print("8 : Torse (chemise mâgîque)")
    print("9 : Poignets (bracelets)")
    print("10 : Anneau")
    print("11 : Cou (cape, amulette, collier)")
    print("12 : Taille (ceinture)")
    print("13 : Pieds (bottes)")

    choix = str(input(">>> "))

    if choix == "1":
        place = "main"
        print("Une ou deux mains ? (1/2)")
        mains = str(input(">>> "))
        print("Dommages (4,6,8,10,12,20...)")
        damage = str(input(">>> "))
        print("Nombre de dés de dégâts")
        nb_dice = str(input(">>> "))
        print("Bonus à l\"attaque :")
        bonus_attaque = str(input(">>> "))
        print("Bonus aux dégâts :")
        bonus_degats = str(input(">>> "))
        print("Zone de critique (ex : 18 pour critique sur 18-20)")
        critique = str(input(">>> "))
        print("Multiplicateur de critique (ex. 3 pour critique x3)")
        multi_critique = str(input(">>> "))
    elif choix == "2":
        place = "armure"
        print("bonus de CA (base + bonus d\"alteration)")
        bonus_ca = str(input(">>> "))
        print("mod. dex. maximal (Ex. : 2)")
        max_dex = str(input(">>> "))
        print("malus aux tests (discretion, etc... Ex. : 2)")
        malus_tests = str(input(">>> "))
        print("echec de lancement des sorts profanes (ex. : 15")
        echec_sort = str(input(">>> "))
    elif choix == "3":
        place = "tete"
    elif choix == "4":
        place = "front"
    elif choix == "5":
        place = "yeux"
    elif choix == "6":
        place = "epaules"
    elif choix == "7":
        place = "corps"
    elif choix == "8":
        place = "torse"
    elif choix == "9":
        place = "poignets"
    elif choix == "10":
        place = "anneau"
    elif choix == "11":
        place = "cou"
    elif choix == "12":
        place = "taille"
    elif choix == "13":
        place = "pieds"
    else:
        print("Pas d\"emplacement valide")
        exit()

    print("nombre de bonus aux caractéristiques (1,2,3...)")
    imax = int(input(">>> "))

    bonus_string = "\"bonus_carac\": [\n"
    for i in range(0, imax):
        print("caractéristique (for, dex, con, int, sag, cha)")
        carac = str(input(">>> "))
        print("bonus : (1,2...)")
        bonus = str(input(">>> "))
        bonus_string = bonus_string + "{\"carac\": \"" + carac + "\", \"bonus\": \"" + bonus + "\"}"
        if i < imax - 1:
            bonus_string = bonus_string + ",\n"
    bonus_string = bonus_string + "],\n"
    print("Description (effet)")
    effet = str(input(">>> "))

    filename = str(nom.split(' ')[0]) + str(randint(1, 512)) + ".json"
    print(filename)

    commande = ["touch", "data/"+str(filename)]
    out = Popen(commande, stdout=PIPE)
    (sout, serr) = out.communicate()
    print(sout)

    os.chmod("data/"+filename, 502)

    file = open("data/"+filename, 'w')
    file.write("{\n")
    file.write("\"objet\": {")
    file.write("\"place\": \""+place+"\",\n")
    file.write("\"nom\": \""+nom+"\",\n")
    file.write("\"carac_arme\": {\n")
    if choix == "1":
        file.write("\"damage\": \""+damage+"\",\n")
        file.write("\"nb_dice\": \""+nb_dice+"\",\n")
        file.write("\"bonus_attaque\": \""+bonus_attaque+"\",\n")
        file.write("\"bonus_degats\": \""+bonus_degats+"\",\n")
        file.write("\"critique\": \""+critique+"\",\n")
        file.write("\"multi_critique\": \""+multi_critique+"\"\n")
    file.write("},\n")
    file.write("\"carac_armure\": {\n")
    if choix == "2":
        file.write("\"CA\": \""+bonus_ca+"\",\n")
        file.write("\"max_dex\": \""+max_dex+"\",\n")
        file.write("\"malus_tests\": \""+malus_tests+"\",\n")
        file.write("\"echec_sort\": \""+echec_sort+"\"\n},")
    file.write("},\n")
    file.write(bonus_string)
    file.write("\"effet\": \""+effet+"\"\n}\n}")
