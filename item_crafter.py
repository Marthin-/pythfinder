#!/usr/bin/env python3

from random import randint  # pour générer le nom de fichier
from subprocess import *
import json
import os

if __name__ == "__main__":

    objet = {
        "place": "",
        "nom": "",
        "carac_arme": {},
        "carac_armure": {},
        "bonus_carac": {},
        "effet": ""
    }

    print("Bienvenue dans l\"éditeur d\"objets de pythfinder")
    print("Choisissez le nom de votre objet")
    objet["nom"] = str(input(">>> "))
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
        objet["place"] = "main"
        print("Une ou deux mains ? (1/2)")
        objet['carac_arme']['main'] = str(input(">>> "))
        print("Dommages (4,6,8,10,12,20...)")
        objet['carac_arme']['damage'] = str(input(">>> "))
        print("Nombre de dés de dégâts")
        objet['carac_arme']['nb_dice'] = str(input(">>> "))
        print("Bonus à l\"attaque :")
        objet['carac_arme']['bonus_attaque'] = str(input(">>> "))
        print("Bonus aux dégâts :")
        objet['carac_arme']['bonus_degats'] = str(input(">>> "))
        print("Zone de critique (ex : 18 pour critique sur 18-20)")
        objet['carac_arme']['critique'] = str(input(">>> "))
        print("Multiplicateur de critique (ex. 3 pour critique x3)")
        objet['carac_arme']['multi_critique'] = str(input(">>> "))
    elif choix == "2":
        objet['place'] = "armure"
        print("bonus de CA (base + bonus d\"alteration)")
        objet['carac_armure']['bonus_ca'] = str(input(">>> "))
        print("mod. dex. maximal (Ex. : 2)")
        objet['carac_armure']['max_dex'] = str(input(">>> "))
        print("malus aux tests (discretion, etc... Ex. : 2)")
        objet['carac_armure']['malus_tests'] = str(input(">>> "))
        print("echec de lancement des sorts profanes (ex. : 15")
        objet['carac_armure']['echec_sort'] = str(input(">>> "))
    elif choix == "3":
        objet['place'] = "tete"
    elif choix == "4":
        objet['place'] = "front"
    elif choix == "5":
        objet['place'] = "yeux"
    elif choix == "6":
        objet['place'] = "epaules"
    elif choix == "7":
        objet['place'] = "corps"
    elif choix == "8":
        objet['place'] = "torse"
    elif choix == "9":
        objet['place'] = "poignets"
    elif choix == "10":
        objet['place'] = "anneau"
    elif choix == "11":
        objet['place'] = "cou"
    elif choix == "12":
        objet['place'] = "taille"
    elif choix == "13":
        objet['place'] = "pieds"
    else:
        print("Pas d\"emplacement valide")
        exit()

    print("nombre de bonus aux caractéristiques (1,2,3...)")
    imax = int(input(">>> "))

    for i in range(0, imax):
        print("caractéristique (for, dex, con, int, sag, cha)")
        carac = str(input(">>> "))
        objet['bonus_carac'][carac] = str(input("bonus: (1,2...)\n>>> "))

    print("Description (effet)")
    objet['effet'] = str(input(">>> "))

    filename = str(objet['nom'].split(' ')[0]) + str(randint(1, 512)) + ".json"
    os.chdir("data")
    print("Objet sauvegardé à l'emplacement : " + os.getcwd() + "/" + filename)
    commande = ["touch", str(filename)]
    out = Popen(commande, stdout=PIPE)
    (sout, serr) = out.communicate()
    os.chmod(filename, 502)
    with open(filename, 'w') as outputFile:
        json.dump(objet, outputFile)
