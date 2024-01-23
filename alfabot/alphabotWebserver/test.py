import sqlite3
username = 'prova'
password = '1234'

con = sqlite3.connect("password.db")
cur = con.cursor()
res = cur.execute(f"SELECT Tipo FROM Users WHERE Utente = '{username}'")
moveSeq = res.fetchall()
con.close()

tipo = moveSeq[0][0]
print(tipo)
