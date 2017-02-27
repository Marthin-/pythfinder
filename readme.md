# Pythfinder

__Utilitaire en python pour porter le système de Pathfinder sur PC et automatiser (entre autres) les feuilles de personnage, les jets de dés, etc...__

[![Build Status](https://travis-ci.org/Marthin-/pythfinder.png)](https://travis-ci.org/Marthin-/pythfinder)

## Étape 1 : portage du système
* Mini shell pour debug [ ✔]
* DB avec sqlite3 [ ✔]
* Import des armes et armures depuis Pathfinder-wiki.fr [ ✔]
* Implé personnage [ ❌ ]
* Implé jet d'attaque [ ✔]
* Implé jets de compétences [ ❌ ]
* Implé montée de niveau [ ❌ ]
* GUI [ __x__]
* Plein d'autres trucs [ ❌ ]

## Étape 2 : jeu en ligne
* Serveur [ ❌ ]
* Client [ ❌ ]

---

## Détails implémentation

* Personnages :
  * Objet Sorts
    * Méthode d'ajout de sorts
    * Ajout à BDD
    * Objet Grimoire sur perso
  * Dons
    * Méthode ajouts de dons
    * Ajout à BDD
    * table de dons sur perso
      * flag "compétence" pour en tenir compte pour les jets
      * variable modifiée par le don : à choisir dans 
      * à cocher ou décocher pour en tenir compte (selon situation)
  * Perso
    * tenir compte effets de sorts
    * tenir compte des dons
      * pour ça : au moment du lancer de dé mettre une popup avec les différents bonus qui pourraient s'appliquer
    
* Objets
  * Armes / Armures magiques
    * Méthode ajout objets persos à BDD
  * Objets magiques
    * champ pour différents objets en fonction d'emplacement
  * Possibilité de créer ses objets en éditant un fichier json [ ✔]
  
* GUI
  * premier jet en curses
  * voir gui.txt
