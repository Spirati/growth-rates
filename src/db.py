import sqlite3

class SqliteContext:
    init: bool
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self, init = False):
        self.init = init

    def __enter__(self):
        self.connection = sqlite3.connect(
            "db/database.db"
        )
        self.cursor = self.connection.cursor()
        if self.init:
            with open("schema.sql") as schema_file:
                schema = schema_file.read()
            self.cursor.executescript(schema)
        return self.cursor
        
    def __exit__(self, type, value, traceback):
        self.cursor.fetchall()
        self.cursor.close()
        self.connection.commit()