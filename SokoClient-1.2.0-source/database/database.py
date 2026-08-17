import sqlite3
import os


class Database:

    def __init__(self, file="data/soko.db"):

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.connection = sqlite3.connect(file)

        self.create_tables()


    def create_tables(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY,
                name TEXT,
                version TEXT,
                loader TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mods (
                id INTEGER PRIMARY KEY,
                name TEXT,
                version TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS modpacks (
                id INTEGER PRIMARY KEY,
                name TEXT,
                version TEXT
            )
        """)

        self.connection.commit()


    def execute(self, query, values=()):

        cursor = self.connection.cursor()

        cursor.execute(
            query,
            values
        )

        self.connection.commit()


    def fetch(self, query, values=()):

        cursor = self.connection.cursor()

        cursor.execute(
            query,
            values
        )

        return cursor.fetchall()