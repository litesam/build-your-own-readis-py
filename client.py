import socket
from typing import List

# Assume len to be len_
HOST = "0.0.0.0"
PORT = 1234
k_max_msg = 4096

def msg(m):
    print("\033[1;31;40m", m, sep="")

def query(fd: socket, text: List) -> int:
    len_ = len(text)
    if len_ > k_max_msg:
        return -1
    
    if err := write_all(fd, text, 4+len_):
        return err
    
    # 4 bytes header
    rbuf = ['' * (4 + k_max_msg + 1)]
    errno = 0
    err = read_full(fd, rbuf, 4)
    if err:
        if errno == 0:
            msg("EOF")
        else:
            msg("read() error")
        return err
    
    len_ = len(rbuf) # assume little endian
    if len_ > k_max_msg:
        msg("too long")
        return -1
    
    # reply body
    err = read_full(fd, rbuf, len_)
    if err:
        msg("read() error")
        return err

    # do something
    print(f"server says: {rbuf}")

def read_full(fd: socket, buf: str, n: int) -> int:
    while n > 0:
        rv = fd.recv(n)
        if rv <= 0:
            return -1
        
        n -= rv
        buf += rv
    return 0

def write_all(fd: socket, buf: str, n: int) -> int:
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
    err = query(fd, "hello1")
    if err:
        fd.close()
        quit()
    
    err = query(fd, "hello2")
    if err:
        fd.close()
        quit()
    
    err = query(fd, "hello3")
    if err:
        fd.close()
        quit()

