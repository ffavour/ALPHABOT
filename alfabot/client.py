import socket as sck


def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    server_address = ("192.168.1.130", 3464)

    s.connect(server_address)
    print("connesso")

    while True:
        com = input("inserire il comando: ")
        val = input("inserire il valore: ")

        s.sendall(f"{com};{val}".encode())
        data = s.recv(4096)
        stato = s.recv(4096)
        if data.decode() == "-1":
            print(data.decode() + " fine ")
            break
        else:
            print(data.decode())
            print(stato.decode())

    s.close()


if __name__ == "__main__":
    main()
