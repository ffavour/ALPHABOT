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
        dizComandiBase = {"f": self.bottino.forward(), "b": self.bottino.backward(), "r": self.bottino.right(),
                          "l": self.bottino.forward()}
        while True:
            self.bottino.get_sensors()
            data = self.conn.recv(4096)
            print(f"ricevuto {data} da {self.address}")

            dataStr = data.decode()

            comand = dataStr.split(SEPARATOR)
            comando = comand[0]
            duration = int(comand[1])

            # prendo lista di comandi composti
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            res = cur.execute(f"SELECT Mov_seq FROM Movements WHERE Shortcut = '{dataStr}'")
            moveSeq = res.fetchall()
            print(moveSeq, type(moveSeq))
            con.close()

            if moveSeq:
                listaMoveSeq = str(moveSeq).split(";")
                listaMovimenti = []

                for elemento in listaMoveSeq:
                    a = elemento.replace("[('", "").replace("',)]", "")
                    print(a)
                    listaMovimenti.append(a)
                print(listaMovimenti)

                for elemento in listaMovimenti:
                    print(dizComandiBase[elemento[0].lower()], elemento[1:])


            else:
                print("cueri vuota")

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


def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    my_address = ("0.0.0.0", 3464)
    s.bind(my_address)

    s.listen()
    conn, address = s.accept()
    bottino = AlphaBot.AlphaBot()

    client = ClientThread(conn, address, bottino)
    statoSensori = InvioContinuo(conn, address, bottino)

    while True:
        client.start()
        statoSensori.start()


if __name__ == "__main__":
    main()
