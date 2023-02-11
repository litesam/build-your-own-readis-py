import socket
from typing import List
from typing import Any

HOST = "0.0.0.0"
PORT = 1234
k_max_msg = 4096


def one_request(connfd: socket.socket):
    # 4 bytes header
    rbuf = ['' * (4 + k_max_msg + 1)]
    print('here1')
    errno = 0
    err = read_full(connfd, rbuf, 4)
    if err:
        if errno == 0:
            print("EOF")
        else:
            print("read() error")
        return err

    print('here2')
    len_ = len(rbuf)
    if len_ > k_max_msg:  # assume little endian
        print("too long")
        return -1

    # request body
    err = read_full(connfd, rbuf, len_)
    if err:
        print("read() error")
        return err

    print("here3")
    # do something
    # CPP sets the end position of the rbuf to '\0' escape sequence
    print(f"client says {rbuf}")

    # reply using the same protocol
    reply = "world"
    len_ = len(reply)
    return write_all(connfd, reply, 4 + len_)


def read_full(fd: socket.socket, buf: List, n: Any) -> int:
    while n > 0:
        rv = fd.recv(n)
        print(f"here: {rv}")
        try:
            rv = int(rv)
        except:
            pass
        if type(rv) is int and rv <= 0:
            return -1

        try:
            n -= rv
        except:
            buf += [str(rv)]
    return 0


def write_all(fd: socket.socket, buf: Any, n: int) -> int:
    while n > 0:
        rv = fd.send(buf)
        if rv <= 0:
            return -1

        n -= rv
        buf += rv
    return 0


if __name__ == "__main__":
    fd: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    val: int = 1
    fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, val)
    fd.bind((HOST, PORT))
    fd.listen()

    while True:
        # accept
        connfd, client_addr = fd.accept()

        while True:
            err = one_request(connfd)
            if err:
                break
        connfd.close()
