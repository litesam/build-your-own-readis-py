import socket

HOST = "0.0.0.0"
PORT = 1234

def do_something(connfd):
    rbuf = connfd.recv(64)
    print(f"client says: {rbuf}")

    wbuf = b"world"
    connfd.send(wbuf)


if __name__ == "__main__":
    fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    val = 1
    fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, val)
    fd.bind((HOST, PORT))
    fd.listen()

    while True:
        connfd, client_addr = fd.accept()
        do_something(connfd)
