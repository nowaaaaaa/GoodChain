import sqlite3
from Backend.Signature import *

class Database:
    default_users = [
        ('mike111', 'mike111'),
        ('rose222', 'rose222'),
        ('alex333', 'alex333')
    ]
    def __init__(self):
        self.connection = sqlite3.connect('./Data/users.db')
        self.cursor = self.connection.cursor()
        self.setup_tables()
        
    def setup_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY, 
                password_hash BLOB,
                private_key BLOB,
                public_key BLOB                
            )
        """)
        for user in self.default_users:
            prv, pub = generate_keys()
            prv = prv.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
            self.cursor.execute("""
                INSERT OR IGNORE INTO users VALUES
                    (?, ?, ?, ?)
            """, (user[0], hash_password(user[1]), prv, pub))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
