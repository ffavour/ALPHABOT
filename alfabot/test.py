import sqlite3

username = "gino"
password = "12345678"

con = sqlite3.connect('password.db')
cur = con.cursor()
cur.execute(f"SELECT * FROM Users WHERE Utente = '{username}' AND Password = '{password}'")
rows = cur.fetchall()

print(rows)
