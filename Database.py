import sqlite3
from Signature import *

class Database:
    default_users = [
        ('mike111', 'mike111'),
        ('rose222', 'rose222'),
        ('alex333', 'alex333')
    ]
    def __init__(self):
        self.connection = sqlite3.connect('./Data/users.sqlite')
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
            username, password = user
            prv, pub = generate_keys()
            prv = prv.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.BestAvailableEncryption(password.encode('utf-8'))
            )
            self.cursor.execute("""
                INSERT OR IGNORE INTO users VALUES
                    (?, ?, ?, ?)
            """, (username, hash_password(password), prv, pub))
        self.connection.commit()

    def verify_user(self, username, password):
        self.cursor.execute("""
            SELECT * FROM users WHERE username = ? AND password_hash = ?
        """, (username, hash_password(password)))
        return self.cursor.fetchone() or []
    
    def add_user(self, username, password):
        prv, pub = generate_keys()
        prv = prv.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(password.encode('utf-8'))
        )
        self.cursor.execute("""
            INSERT INTO users VALUES
                (?, ?, ?, ?)
        """, (username, hash_password(password), prv, pub))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
