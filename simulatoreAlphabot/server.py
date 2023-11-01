import socket as sck
import turtle
import sqlite3


def comandiComposti(comando, bottino, conn):
    print("sono nel db!")

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
            comando = str(elemento[0]).lower()
            duration = int(elemento[1:])

            print(comando, duration, type(comando), type(duration))
            comandiDefault(comando, duration, bottino, conn)
    else:
        print("cueri vuota")


def comandiDefault(comando, duration, t, conn):
    if duration <= 0:
        conn.sendall("error".encode())
    else:

        if comando == "f":
            t.forward(duration)
            conn.sendall("ok".encode())
        elif comando == "b":
            t.backward(duration)
            conn.sendall("ok".encode())
        elif comando == "l":
            t.left(duration)
            conn.sendall("ok".encode())

        elif comando == "r":
            t.right(duration)
            conn.sendall("ok".encode())

        else:
            conn.sendall("error".encode())


def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    my_address = ("127.0.0.1", 8000)
    s.bind(my_address)
    s.listen()

    t = turtle.Turtle()
    conn, address = s.accept()

    while True:
        data = conn.recv(4096)
        print(f"ricevuto {data} da {address}")

        dataStr = data.decode()

        # prendo lista di scorciatoie da db
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        res = cur.execute(f"SELECT Shortcut FROM Movements")
        Shortcut = res.fetchall()
        con.close()

        listaShortcut = []
        for i in range(len(Shortcut)):
            listaShortcut.append(Shortcut[i][0])

        print("fuori if")
        comandoCercatoDB = str(dataStr[0]).upper()
        print(comandoCercatoDB)

        if comandoCercatoDB in listaShortcut:
            print("dentro if")
            comandiComposti(comandoCercatoDB, t, conn)
            print("dopo funz")

        else:
            comand = dataStr.split(";")
            comando = comand[0]
            duration = int(comand[1])

            if comando == "-1":
                print("fine")
                conn.sendall("-1".encode())
                break
            else:
                comandiDefault(comando, duration, t, conn)
        print("uscito")

    conn.close()
    turtle.done()


if __name__ == "__main__":
    main()
