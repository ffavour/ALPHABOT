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
        obst = "OB_N"
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
            print(str(dataStr[0]).upper())
            if str(dataStr[0]).upper() in listaShortcut:
                print("dentro if")
                comandiComposti(dataStr[0].upper(), self.bottino, self.conn)
                print("dopo funz")

            else:
                comand = dataStr.split(SEPARATOR)
                comando = comand[0]
                duration = int(comand[1])

                if comando == "-1":
                    print("fine")
                    self.conn.sendall("-1".encode())
                    break

                elif duration <= 0:
                    self.conn.sendall("error".encode())

                else:

                    if comando.lower() == "f":
                        self.bottino.forward()
                        time.sleep(duration)
                        self.bottino.stop()

                        self.conn.sendall("ok".encode())

                    elif comando.lower() == "b":
                        self.bottino.backward()
                        time.sleep(duration)
                        self.bottino.stop()

                        self.conn.sendall("ok".encode())

                    elif comando.lower() == "l":
                        self.bottino.left()
                        time.sleep(duration)
                        self.bottino.stop()

                        self.conn.sendall("ok".encode())

                    elif comando.lower() == "r":
                        self.bottino.right()
                        time.sleep(duration)
                        self.bottino.stop()

                        self.conn.sendall("ok".encode())

                    else:
                        self.conn.sendall("error".encode())


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
            if elemento[0].lower() == "f":
                bottino.forward()
                time.sleep(elemento[1:])
                bottino.stop()

                conn.sendall("ok".encode())

            elif elemento[0].lower() == "b":
                bottino.backward()
                time.sleep(elemento[1:])
                bottino.stop()

                conn.sendall("ok".encode())

            elif elemento[0].lower() == "l":
                bottino.left()
                time.sleep(elemento[1:])
                bottino.stop()

                conn.sendall("ok".encode())

            elif elemento[0].lower() == "r":
                bottino.right()
                time.sleep(elemento[1:])
                bottino.stop()

                conn.sendall("ok".encode())

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
