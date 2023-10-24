import sqlite3


def main():
    a = "F12"
    shortCut = "y".upper()

    # prendo lista di comandi composti
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT Mov_seq FROM Movements WHERE Shortcut = '{shortCut}'")
    moveSeq = res.fetchall()
    # print(moveSeq[0][0], type(moveSeq))
    con.close()

    # prendo lista di scorciatoie
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT Shortcut FROM Movements")
    sC = res.fetchall()
    # print(sC, type(sC))
    con.close()

    listaSc = []
    for i in range(len(sC)):
        listaSc.append(sC[i][0])
    print(listaSc)

    dizComandiBase = {"f": "avanti", "b": "indietro", "r": "derecha", "l": "izquierda"}

    if moveSeq:
        listaMovimenti = moveSeq[0][0].split(";")

        for elemento in listaMovimenti:
            print(dizComandiBase[elemento[0].lower()], elemento[1:])

    else:
        print("cueri vuota")


if __name__ == "__main__":
    main()