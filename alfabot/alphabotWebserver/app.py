from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import time
import AlphaBot
import string
import random
import hashlib

app = Flask(__name__)

bottino = AlphaBot.AlphaBot()
hash_algorithm = hashlib.sha256()


# genera stringa alfanumerica casuale per il token della pagina utente
def generaStringaRandom(lunghezza=40):
    caratteri = string.ascii_letters + string.digits  # lettere e numeri
    stringa_alfanumerica = ''.join(random.choice(caratteri) for _ in range(lunghezza))
    return stringa_alfanumerica


def comandiDefault(comando=None, duration=2):
    # gestione dei comandi inviati dall'utente [AVANTI, INDIETRO,ecc sono i vari valori dei bottoni,
    # str(comando).lower() per i comandi composti]
    if request.form.get('avanti') == 'AVANTI' or str(comando).lower() == "f":  # name == value
        print("vado avanti", duration)
        bottino.forward()
        time.sleep(duration)
        bottino.stop()
    elif request.form.get('indietro') == 'INDIETRO' or str(comando).lower() == "b":
        print("vado indietro", duration)
        bottino.backward()
        time.sleep(duration)
        bottino.stop()
    elif request.form.get('destra') == 'DESTRA' or str(comando).lower() == "r":
        print("vado a dx", duration)
        bottino.right()
        time.sleep(duration)
        bottino.stop()
    elif request.form.get('sinistra') == 'SINISTRA' or str(comando).lower() == "l":
        print("vado a sx", duration)
        bottino.left()
        time.sleep(duration)
        bottino.stop()


def comandiComposti(comando):
    # apertura db
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT Mov_seq FROM Movements WHERE Shortcut = '{comando}'")
    moveSeq = res.fetchall()
    con.close()

    if moveSeq:
        # crea lista dal risultato della query con tutti i comandi composti (esempio lista: [F10, L1, B6])
        listaMovimenti = moveSeq[0][0].split(";")

        for elemento in listaMovimenti:
            # esegue i comandi elemento per elemento
            print(elemento[0], elemento[1:])  # elemento[0] = direzione, elemento[1:] = durata
            comandiDefault(elemento[0], int(elemento[1:]))
    else:
        print("ERROR")


def check_password(hashed_password, user_password):
    return hashed_password == user_password


def validate(username, password):
    completion = False
    con = sqlite3.connect('password.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM Users")
    rows = cur.fetchall()
    for row in rows:
        dbUser = row[0]
        dbPass = row[1]
        if dbUser == username:
            hash_algorithm = hashlib.sha256()  # Crea una nuova istanza di hash
            hash_algorithm.update(password.encode('utf-8'))
            hashed_password = hash_algorithm.hexdigest()
            completion = check_password(dbPass, hashed_password)
            print(dbPass, hashed_password)
    return completion



"""
Per testare pagina login
utenti  |  password in chiaro
gino        12345678
pinco       palla
"""

token = generaStringaRandom()


@app.route(f"/{token}", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        comandiDefault()

        # controlla che la casella per eseguire i comandi sia nella pagina
        if 'inputBox' in request.form:
            input_value = request.form['inputBox']
            print('Valore dell\'input: {}'.format(input_value))
            comandoDaCercareDB = format(input_value)
            comandiComposti(comandoDaCercareDB)

    elif request.method == 'GET':
        return render_template('index.html')

    return render_template("index.html")


@app.route("/", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':

        # controlla che la casella per eseguire i comandi sia nella pagina
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            completion = validate(username, password)
            if not completion:
                error = 'Invalid Credentials. Please try again.'
            else:
                return redirect(url_for('index'))
    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
