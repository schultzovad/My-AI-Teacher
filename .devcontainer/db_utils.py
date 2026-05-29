import sqlite3
import hashlib

DB_NAME = "tutor_platform.db"

def get_db():
    return sqlite3.connect(DB_NAME)

def hash_pwd(p):
    return hashlib.sha256(p.encode()).hexdigest()
