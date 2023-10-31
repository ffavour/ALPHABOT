import sqlite3

"""dizComandiBase = {"f": self.bottino.forward(), "b": self.bottino.backward(), "r": self.bottino.right(),
                          "l": self.bottino.forward()}"""


def main():
    dizComandiBase = {"f": "avanti", "b": "indietro", "r": "derecha", "l": "izquierda"}
    comando = "z".upper()

    # prendo lista di scorciatoie
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT Shortcut FROM Movements")
    Shortcut = res.fetchall()
    # print(Shortcut, type(Shortcut))
    con.close()

    listaShortcut = []
    for i in range(len(Shortcut)):
        listaShortcut.append(Shortcut[i][0])
    # print(listaSc)

    if comando in listaShortcut:
        # prendo lista di comandi composti
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        res = cur.execute(f"SELECT Mov_seq FROM Movements WHERE Shortcut = '{comando}'")
        moveSeq = res.fetchall()
        # print(moveSeq[0][0], type(moveSeq))
        con.close()

        if moveSeq:
            listaMovimenti = moveSeq[0][0].split(";")

            for elemento in listaMovimenti:
                print(elemento[0], elemento[1:])  # elemento[0] = direzione, elemento[1:] = durata
                if elemento[0].lower() == "f":
                    self.bottino.forward()
                    time.sleep(elemento[1:])
                    self.bottino.stop()

                    self.conn.sendall("ok".encode())

                elif elemento[0].lower() == "b":
                    self.bottino.backward()
                    time.sleep(elemento[1:])
                    self.bottino.stop()

                    self.conn.sendall("ok".encode())

                elif elemento[0].lower() == "l":
                    self.bottino.left()
                    time.sleep(elemento[1:])
                    self.bottino.stop()

                    self.conn.sendall("ok".encode())

                elif elemento[0].lower() == "r":
                    self.bottino.right()
                    time.sleep(elemento[1:])
                    self.bottino.stop()

                    self.conn.sendall("ok".encode())

        else:
            print("cueri vuota")


if __name__ == "__main__":
    main()
