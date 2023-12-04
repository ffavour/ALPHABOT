from flask import Flask, render_template, request
import sqlite3
import time
import AlphaBot

app = Flask(__name__)


bottino = AlphaBot.AlphaBot()


def comandiDefault(comando=None, duration=2):
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
    # print("sono nel db!")
    # prendo lista di comandi composti
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT Mov_seq FROM Movements WHERE Shortcut = '{comando}'")
    moveSeq = res.fetchall()
    # print(moveSeq[0][0], type(moveSeq))
    con.close()

    if moveSeq:
        # crea lista dal risultato della query con tutti i comandi composti (esempio lista: [F10, L1, B6])
        listaMovimenti = moveSeq[0][0].split(";")

        for elemento in listaMovimenti:
            # esegue i comandi elemento per elemento
            print(elemento[0], elemento[1:])  # elemento[0] = direzione, elemento[1:] = durata
            comandiDefault(elemento[0], elemento[1:])
    else:
        print("ERROR")


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        comandiDefault()

        if 'inputBox' in request.form:
            input_value = request.form['inputBox']
            print('Valore dell\'input: {}'.format(input_value))
            # print(format(input_value), type(format(input_value)))
            comandoDaCercareDB = format(input_value)
            comandiComposti(comandoDaCercareDB)

    elif request.method == 'GET':
        return render_template('index.html')

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
