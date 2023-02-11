import socket
from typing import List
from typing import Any

# Always use list mutate the data wherever possible
# Assume len to be len_
HOST = "0.0.0.0"
PORT = 1234
k_max_msg = 4096


def query(fd: socket.socket, text: List) -> int:
    len_ = len(text)
    if len_ > k_max_msg:
        return -1

    wbuf = ['' * (1 + k_max_msg)]
    wbuf[0] = str(len_)
    wbuf[1:] = list(text)
    if err := write_all(fd, wbuf, 1 + len_):  # 1 is the length of the header, and the rest is the length
        return int(err)

    # 4 bytes header
    rbuf = [b'' * (k_max_msg + 1)]
    errno = 0
    err = read_full(fd, rbuf, 1)
    if err:
        if errno == 0:
            print("EOF")
        else:
            print("read() error")
        return int(err)

    len_ = int(b''.join(rbuf))  # assume little endian
    if len_ > k_max_msg:
        print("too long")
        return -1

    # reply body
    err = read_full(fd, rbuf, len_)
    if err:
        print("read() error")
        return int(err)

    # do something
    print(f"server says: {rbuf[2:]}")
    return 0


def read_full(fd: socket.socket, buf: List, n: int) -> int:
    while n > 0:
        rv = fd.recv(n)
        if type(rv) is int and rv <= 0:
            return -1
        n -= len(rv)
        buf += [rv]
    return 0


def write_all(fd: socket.socket, buf: Any, n: int) -> int:
    buf = ''.join(buf)
    buf = bytes(buf, 'utf-8')
    while n > 0:
        rv = fd.send(buf)
        if rv <= 0:
            return -1

        n -= rv
        rv = bytes(str(rv), 'utf-8')
        buf += rv
    return 0


if __name__ == "__main__":
    fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fd.connect((HOST, PORT))

    # multilple requests
    err = query(fd, list("hello1"))
    if err:
        fd.close()
        quit()

    err = query(fd, list("hello2"))
    if err:
        fd.close()
        quit()

    err = query(fd, list("hello3"))
    if err:
        fd.close()
        quit()

    fd.close()
