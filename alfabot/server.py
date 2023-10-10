import socket as sck
import time

import AlphaBot
SEPARATOR = ";"


def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    my_address = ("0.0.0.0", 8000)
    s.bind(my_address)
    s.listen()

    bottino = AlphaBot.AlphaBot()
    conn, address = s.accept()

    while True:
        data = conn.recv(4096)
        print(f"ricevuto {data} da {address}")

        dataStr = data.decode()
        comand = dataStr.split(SEPARATOR)
        comando = comand[0]
        duration = int(comand[1])

        if comando == "-1":
            print("fine")
            conn.sendall("-1".encode())
            break

        elif duration <= 0:
            conn.sendall("error".encode())

        else:

            if comando.lower() == "f":
                bottino.forward()
                time.sleep(duration)
                bottino.stop()

                conn.sendall("ok".encode())

            elif comando.lower() == "b":
                bottino.backward()
                time.sleep(duration)
                bottino.stop()

                conn.sendall("ok".encode())

            elif comando.lower() == "l":
                bottino.left()
                time.sleep(duration)
                bottino.stop()

                conn.sendall("ok".encode())

            elif comando.lower() == "r":
                bottino.right()
                time.sleep(duration)
                bottino.stop()

                conn.sendall("ok".encode())

            else:
                conn.sendall("error".encode())

    print("uscito")
    conn.close()


if __name__ == "__main__":
    main()
