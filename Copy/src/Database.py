import sqlite3
from Signature import *

class Database:
    path = '../data/users.sqlite'
    default_users = [
        ('mike111', 'mike111'),
        ('rose222', 'rose222'),
        ('alex333', 'alex333')
    ]
    def __init__(self):
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()
        self.tampered = False
        if not self.verify_hash():
            self.cursor.execute("DROP TABLE IF EXISTS users")
            self.connection.commit()
            self.tampered = True
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
        # for user in self.default_users:
        #     username, password = user
        #     prv, pub = generate_keys()
        #     prv = prv.private_bytes(
        #         encoding=serialization.Encoding.PEM,
        #         format=serialization.PrivateFormat.TraditionalOpenSSL,
        #         encryption_algorithm=serialization.BestAvailableEncryption(password.encode('utf-8'))
        #     )
        #     self.cursor.execute("""
        #         INSERT OR IGNORE INTO users VALUES
        #             (?, ?, ?, ?)
        #     """, (username, hash_password(password), prv, pub))
        # self.connection.commit()
        self.enter_hash()

    def verify_user(self, username, password):
        self.cursor.execute("""
            SELECT * FROM users WHERE username = ? AND password_hash = ?
        """, (username, hash_password(password)))
        user_list = self.cursor.fetchone()
        if user_list is None:
            return []
        else:
            return [user_list[0], password, user_list[2], user_list[3]]
    
    def user_exists(self, username):
        self.cursor.execute("""
            SELECT * FROM users WHERE username = ?
        """, (username,))
        return self.cursor.fetchone() is not None
    
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
        self.enter_hash()

    def get_public_key(self, username):
        self.cursor.execute("""
            SELECT public_key FROM users WHERE username = ?
                            """, (username,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def get_username(self, public_key):
        if public_key == None:
            return "REWARD"
        self.cursor.execute("""
            SELECT username FROM users WHERE public_key = ?
                            """, (public_key,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def compute_hash(self):
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.backends import default_backend
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        self.cursor.execute("""
            SELECT * FROM users WHERE username != 'hash'
        """)
        users = self.cursor.fetchall()
        digest.update(bytes(str(users),'utf8'))
        return digest.finalize()

    def enter_hash(self):
        username = "hash"
        password = self.compute_hash()
        if self.user_exists(username):
            self.cursor.execute("""
                UPDATE users SET password_hash = ? WHERE username = ?
            """, (password, username))
        else:
            prv, pub = None, None
            self.cursor.execute("""
                INSERT OR IGNORE INTO users VALUES
                    (?, ?, ?, ?)
            """, (username, password, prv, pub))
        self.connection.commit()

    def verify_hash(self):
        try:
            self.cursor.execute("""
                SELECT name FROM sqlite_master WHERE type='table' AND name='users'
                        """)
            if self.cursor.fetchone() is None:
                return False
        except:
            import os
            self.cursor.close()
            self.connection.close()
            os.remove(self.path)
            self.connection = sqlite3.connect(self.path)
            self.cursor = self.connection.cursor()
            return False
        self.cursor.execute("""
            SELECT * FROM users WHERE username = 'hash'
        """)
        result = self.cursor.fetchone()
        if result is None:
            return False
        if result[1] == self.compute_hash():
            return True

    def close(self):
        self.cursor.close()
        self.connection.close()
