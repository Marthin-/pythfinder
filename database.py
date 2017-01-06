import sqlite3


class Database:
#TODO possibilité de rajouter des objets à la DB (ex. Armes magiques) : En entrant les dégâts, le type d'arme, et les effets supplémentaires.
#TODO (Je le met ici pour penser à modifier un peu le code de la gestion de DB pour ne pas effacer à chaque fois les objets "personnalisés")
    def __init__(self, reset=True, db_filname="pf.db"):
        self.db = sqlite3.connect(db_filname)

        try:
            if reset:
                with open('db.sql', mode='r') as f:
                    self.db.cursor().executescript(f.read())
                self.db.commit()

                with open('populate.sql', mode='r') as f:
                    self.db.cursor().executescript(f.read())
                self.db.commit()

        except sqlite3.DatabaseError as error:
            print("Error creating sql database {}".format(error))

    def __del__(self):
        self.db.close()

    def add_user(self, nom_perso="empty", nom_joueur="nobody", role="useless"):
        info = (nom_perso, nom_joueur, role)
        conn = self.db
        c = conn.cursor()
        c.execute("INSERT INTO joueurs (nom_joueur, nom_perso, role) VALUES(?,?,?)", info)
        conn.commit()

    def add_perso(self, nom_perso="empty", f=10, dex=10, con=10, inte=10, sag=10, cha=10, race="Nain"):

        c = self.db.cursor()
        race_id = int(c.execute('SELECT race_id FROM race WHERE nom=?', (race, )).fetchone()[0])

        carac = (nom_perso, f, dex, con, inte, sag, cha, race_id)

        c.execute("INSERT INTO perso "
                  "( nom_perso, force, dexterite, constitution, intelligence, sagesse, charisme, race)"
                  " VALUES(?,?,?,?,?,?,?,?)", carac)
        self.db.commit()

    def add_stuff(self, nom_perso="empty", categorie="stuff", nom="empty"):
        info = (nom_perso, categorie, nom)
        conn = self.db
        c = conn.cursor()
        c.execute("INSERT INTO stuff_perso VALUES(?,?,?)", info)
        conn.commit()

    def get_player(self, nom_perso):
        conn = self.db
        np = (nom_perso,)
        for row in conn.execute('SELECT * FROM joueurs WHERE nom_perso=?', np):
            print(row)

    def get_carac(self, nom_perso):
        conn = self.db

        np = (nom_perso,)
        for row in conn.execute('SELECT * FROM perso INNER JOIN race ON race.race_id=perso.race WHERE nom_perso=?', np):
            print(row)

    def get_db(self):
        """ May be usefull for tests"""
        return self.db

    def get_weapon(self, w_id):
        conn = self.db
        arme_id = (w_id,)
        print("getting weapon with id "+str(w_id))
        c = conn.cursor()
        c.execute('SELECT * FROM arme WHERE arme_id=?', arme_id)
        return c.fetchone()

    def get_armor(self,a_id):
        conn = self.db
        armor_id = (a_id,)
        print("getting armor with id "+str(a_id))
        c = conn.cursor()
        c.execute('SELECT * FROM armure WHERE armure_id=?', armor_id)
        return c.fetchone()

    def update_weapons(self):
        from bs4 import BeautifulSoup
        import requests

        def insert_arm_in_db(data):
            conn = self.db
            c = conn.cursor()
            tmp = data[3].split('d')

            if len(tmp) == 1:  # ammunition
                tmp = [0, 0]
            else:  # hack for staff
                tmp = [tmp[0], tmp[1].split('/')[0]]

            c.execute("INSERT INTO arme(nom_arme, base_degats, mult_degats, mod_degat, porte)"
                      "VALUES (?, ?, ?, ?, ?)", (data[0], tmp[1], tmp[0], data[4], data[5]))
            conn.commit()

        page = requests.get(
            'http://www.pathfinder-fr.org/Wiki/Pathfinder-RPG.Tableau%20r%c3%a9capitulatif%20des%20armes.ashx')
        soup = BeautifulSoup(page.content, 'html.parser')

        for elem in soup.find_all('table', class_='tablo'):
            for entry in elem.find_all('tr'):

                col = entry.find_all('td')
                col = [ele.text.strip() for ele in col]

                if len(col) == 9 and col[1] != "Prix":
                    insert_arm_in_db(col)

        print("Successfully import weapons")

    def update_armors(self):
        from bs4 import BeautifulSoup
        import requests

        def insert_arm_in_db(data):
            conn = self.db
            c = conn.cursor()
            data[2] = data[2][1] if len(data[2]) == 2 else '0'
            data[3] = data[3][1] if len(data[3]) == 2 else '0'
            data[4] = data[4][1] if len(data[4]) == 2 else '0'
            data[5] = data[5].split('%')[0]

            c.execute("INSERT INTO armure(nom_armure, bonus_armure, bonus_max_dex, malus_test, echec_sort)"
                      "VALUES (?, ?, ?, ?, ?)", (data[0], data[2], data[3], data[4], data[5]))
            conn.commit()

        page = requests.get(
            'http://www.pathfinder-fr.org/Wiki/Pathfinder-RPG.Tableau%20r%c3%a9capitulatif%20des%20armures.ashx')
        soup = BeautifulSoup(page.content, 'html.parser')

        for elem in soup.find_all('table', class_='tablo'):
            for entry in elem.find_all('tr'):

                col = entry.find_all('td')
                col = [ele.text.strip() for ele in col]

                if len(col) == 10:  # and col[1] != "Prix":
                    insert_arm_in_db(col)

        print("Successfully import armors")
