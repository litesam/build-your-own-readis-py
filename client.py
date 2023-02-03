import socket

HOST = "0.0.0.0"
PORT = 1234

if __name__ == "__main__":
    fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fd.connect((HOST, PORT))

    msg = b"hello"
    fd.send(msg)

    rbuf = fd.recv(64)
    print(f"server says: {rbuf}")

