import sqlite3
import os

class Database:
    def __init__(self, db_path="beer.db"):
        self.create_database(db_path)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def create_database(self, db_path):
        db_path = os.path.abspath(db_path)
        if os.path.exists(db_path):
            os.remove(db_path)
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute('''
            CREATE TABLE breweries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
        ''')

        c.execute('''
            CREATE TABLE beers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                brewery_id INTEGER,
                FOREIGN KEY (brewery_id) REFERENCES breweries (id),
                UNIQUE (name, brewery_id)
            )
        ''')

        c.execute('''
            CREATE TABLE checkins (
                id TEXT PRIMARY KEY,
                beer_id INTEGER,
                rating_score REAL,
                timestamp TEXT,
                description TEXT,
                image TEXT,
                FOREIGN KEY (beer_id) REFERENCES beers (id)
            )
        ''')

        conn.commit()
        conn.close()

    def create_brewery_if_not_exists(self, brewery_name):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id
            FROM breweries
            WHERE name = ?""",
            (brewery_name,))
        brewery = cursor.fetchone()
        if brewery:
            return brewery[0]
        else:
            cursor.execute("""
                INSERT INTO breweries (name)
                VALUES (?)""",
                (brewery_name,))
            self.conn.commit()
            return cursor.lastrowid

    def create_beer_if_not_exists(self, beer_name, brewery_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id FROM beers
            WHERE name = ? AND brewery_id = ?""",
            (beer_name, brewery_id))
        beer = cursor.fetchone()
        if beer:
            return beer[0]
        else:
            cursor.execute("""
                INSERT INTO beers (name, brewery_id)
                VALUES (?, ?)""",
                (beer_name, brewery_id))
            self.conn.commit()
            return cursor.lastrowid
    
    def create_checkin(
        self, checkin_id, beer_id, rating_score, timestamp,
        description, image
    ):
        cursor = self.conn.cursor()
        cursor.execute("""
                INSERT INTO checkins (id, beer_id, rating_score, timestamp, description, image)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (checkin_id, beer_id, rating_score, timestamp, description, image))
        self.conn.commit()
        return True

    def get_checkins(self):
        c = self.conn.cursor()
        c.execute("""
            SELECT
                c.id as checkin_id,
                c.rating_score,
                c.timestamp,
                c.description,
                c.image,
                b.name as beer_name,
                br.name as brewery_name
            FROM checkins c
            JOIN beers b ON c.beer_id = b.id
            JOIN breweries br ON b.brewery_id = br.id
            ORDER BY c.timestamp DESC
        """)
        return c.fetchall()
    
    def get_beers(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM beers")
        return c.fetchall()

    def get_breweries(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM breweries")
        return c.fetchall()

    def get_brewery(self, brewery_id):
        c = self.conn.cursor()
        c.execute("SELECT * FROM breweries WHERE id = ?", (brewery_id,))
        return c.fetchone()

    def get_checkins_for_beer(self, beer_id):
        c = self.conn.cursor()
        c.execute("""
            SELECT
                c.id as checkin_id,
                c.rating_score,
                c.timestamp,
                c.description,
                c.image,
                b.name as beer_name,
                br.name as brewery_name
            FROM checkins c
            JOIN beers b ON c.beer_id = b.id
            JOIN breweries br ON b.brewery_id = br.id
            WHERE c.beer_id = ?
            ORDER BY c.timestamp DESC
        """, (beer_id,))
        return c.fetchall()

    def get_beers_for_brewery(self, brewery_id):
        c = self.conn.cursor()
        c.execute("""
            SELECT b.name, b.id
            FROM beers b
            WHERE b.brewery_id = ?
        """, (brewery_id,))
        return c.fetchall()

    def close(self):
        self.conn.close()
