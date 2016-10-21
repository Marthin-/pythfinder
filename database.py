import sqlite3


class Database:

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

    # TODO : ajouter race avec race_id
    def add_perso(self, nom_perso="empty", f=10, dex=10, con=10, inte=10, sag=10, cha=10):
        carac = (nom_perso, f, dex, con, inte, sag, cha)

        c = self.db.cursor()
        c.execute("INSERT INTO perso ( nom_perso, force, dexterite, constitution, intelligence, sagesse, charisme)"
                  " VALUES(?,?,?,?,?,?,?)", carac)
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
        for row in conn.execute('SELECT * FROM perso WHERE nom_perso=?', np):
            print(row)
        conn.close()

    def get_db(self):
        """ May be usefull for tests"""
        return self.db
