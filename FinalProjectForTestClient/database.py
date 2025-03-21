import sqlite3
import os
import time
from cryptography.hazmat.primitives import serialization

#Here is a path definition to the SQLite DB file within the project's root folder
DB_FILE = os.path.join(os.getcwd(), "totally_not_my_privateKeys.db")

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    #Database gets initialized and the keys table gets created
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS keys(
            kid INTEGER PRIMARY KEY AUTOINCREMENT,
            key BLOB NOT NULL,
            exp INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_key(private_key, exp):
    #Here the RSA private key is serialized to PEM format to store it inside of the DB
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO keys (key, exp) VALUES (?, ?)", (pem, exp))  
    kid = cursor.lastrowid
    conn.commit()
    conn.close()
    return kid

def get_key(expired=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = int(time.time())
    if expired:
        #Gets an expired key for testing
        cursor.execute("SELECT * FROM keys WHERE exp <= ? ORDER BY exp DESC LIMIT 1", (now,))  
    else:
        #Gets the first unexpired key
        cursor.execute("SELECT * FROM keys WHERE exp > ? ORDER BY exp ASC LIMIT 1", (now,))   
    row = cursor.fetchone()
    conn.close()
    return row

def get_all_valid_keys():
    now = int(time.time())
    conn = get_db_connection()
    cursor = conn.cursor()

    #I utilized a parameterized query to prevent an SQL injection attack
    cursor.execute("SELECT * FROM keys WHERE exp > ?", (now,))  
    rows = cursor.fetchall()
    conn.close()
    return rows
