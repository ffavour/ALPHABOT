import socket as sck
import time
import AlphaBot
import threading
import sqlite3
import RPi.GPIO as GPIO

SEPARATOR = ";"


class InvioContinuo(threading.Thread):
    def __init__(self, conn, address, bottino):
        super().__init__()
        self.conn = conn
        self.address = address
        self.bottino = bottino

    def run(self):
        obst = "OB_N"  # ostacolo nullo = no ostacoli
        while True:
            sens = self.bottino.get_sensors()

            if obst != sens:
                if sens == "OB_R" and obst != "OB_R":
                    self.conn.sendall("ostacolo a destra".encode())
                    self.bottino.stop()
                if sens == "OB_L" and obst != "OB_L":
                    self.conn.sendall("ostacolo a sinistra".encode())
                    self.bottino.stop()
                if sens == "OB_ALL" and obst != "OB_ALL":
                    self.conn.sendall("ostacoli ovunque!".encode())
                    self.bottino.stop()


class ClientThread(threading.Thread):
    def __init__(self, conn, address, bottino):
        super().__init__()
        self.conn = conn
        self.address = address
        self.bottino = bottino

    def run(self):
        while True:
            self.bottino.get_sensors()
            data = self.conn.recv(4096)
            print(f"ricevuto {data} da {self.address}")

            dataStr = data.decode()

            # prende lista di scorciatoie da db
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            res = cur.execute(f"SELECT Shortcut FROM Movements")
            Shortcut = res.fetchall()
            con.close()

            # crea liste con tutte le scorciatoie
            listaShortcut = []
            for i in range(len(Shortcut)):
                listaShortcut.append(Shortcut[i][0])

            print("fuori if")
            print(str(dataStr[0]).upper())
            comandoCercatoDB = str(dataStr[0]).upper()

            # controlla se comando si trova nella lista
            if comandoCercatoDB in listaShortcut:
                print("dentro if")
                # esegue comandi composti
                comandiComposti(comandoCercatoDB, self.bottino, self.conn)
                print("dopo funz")

            # esegue comandi di default (f, b, l, r)
            else:
                comand = dataStr.split(SEPARATOR)
                comando = comand[0]
                duration = int(comand[1])

                if comando == "-1":
                    print("fine")
                    self.conn.sendall("-1".encode())
                    break
                else:
                    comandiDefault(comando, duration, self.bottino, self.conn)


def comandiDefault(comando, duration, bottino, conn):
    if duration <= 0:
        conn.sendall("error".encode())
    elif comando == "f":
        bottino.forward()
        time.sleep(duration)
        bottino.stop()

        conn.sendall("ok".encode())

    elif comando == "b":
        bottino.backward()
        time.sleep(duration)
        bottino.stop()

        conn.sendall("ok".encode())

    elif comando == "l":
        bottino.left()
        time.sleep(duration)
        bottino.stop()

        conn.sendall("ok".encode())

    elif comando == "r":
        bottino.right()
        time.sleep(duration)
        bottino.stop()

        conn.sendall("ok".encode())
    else:
        conn.sendall("error".encode())


def comandiComposti(comando, bottino, conn):
    print("sono nel db!")

    # prendo lista di comandi composti
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT Mov_seq FROM Movements WHERE Shortcut = '{comando}'")
    moveSeq = res.fetchall()
    # print(moveSeq[0][0], type(moveSeq))
    con.close()

    # in teoria questo controllo è inutile
    if moveSeq:
        # crea lista dal risultato della query con tutti i comandi composti (esempio lista: [F10, L1, B6])
        listaMovimenti = moveSeq[0][0].split(";")

        for elemento in listaMovimenti:
            # esegue i comandi elemento per elemento
            print(elemento[0], elemento[1:])  # elemento[0] = direzione, elemento[1:] = durata
            comando = str(elemento[0]).lower()
            duration = int(elemento[1:])
            comandiDefault(comando, duration, bottino, conn)

    else:
        print("cueri vuota")


def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    my_address = ("0.0.0.0", 3465)
    s.bind(my_address)

    s.listen()
    while True:
        conn, address = s.accept()
        bottino = AlphaBot.AlphaBot()

        client = ClientThread(conn, address, bottino)
        statoSensori = InvioContinuo(conn, address, bottino)

        client.start()
        statoSensori.start()


if __name__ == "__main__":
    main()
