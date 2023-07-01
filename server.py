import socket
import struct

def msg(msg):
    print(msg)


def die(msg):
    #TODO: handle fetching the last error status code.
    err = 1 # errno
    print("[%d] %s" % (err, msg))
    raise SystemExit()


k_max_msg = 4096


def read_full(fd, buf, n, start_index):
    while n > 0:
        data = fd.recv(n)
        rv = len(data)
        if rv <= 0:
            return -1
        assert rv <= n

        n -= rv
        buf[start_index:rv] = data
    # print('here', buf[:20])


def write_all(fd, buf):
    n = len(buf)
    pos = 0
    while n > 0:
        sent = fd.send(buf[pos:])
        if sent == 0:
            return -1 # error

        n -= sent
        pos += sent


def one_request(connfd):
    # 4 bytes header
    rbuf = bytearray(4 + k_max_msg+1)
    try:
        # Read the header
        can = read_full(connfd, rbuf, 4, 0)
        if can == -1: die("EOF")

        # Extract message length from the header
        len_ = struct.unpack("<i", rbuf[:4])[0] # Assume little endian

        if len_ > k_max_msg:
            msg("too long")
            return -1

        # Read the request body
        read_full(connfd, rbuf, len_, 4)

        # Process the request
        request = rbuf[4:4 + len_].decode()
        print("client says:", request)

        # Prepare the reply
        reply = b"world"
        len_ = len(reply)
        wbuf = struct.pack("<i", len_) + reply

        return write_all(connfd, wbuf)
    except Exception as e:
        msg("Error: " + str(e))
        return -1


def main():
    fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if not fd:
        die("socket()")

    # This is needed for most server applications
    val = 1
    fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, val)


    # Bind
    addr = ('', 1234)
    fd.bind(addr)

    # Listen
    fd.listen(socket.SOMAXCONN)

    while True:
        # Accept
        connfd, client_addr = fd.accept()
        _ = client_addr
        if not connfd:
            continue

        while True:
            # Here the server only serves and client connection at once
            err = one_request(connfd)
            if err:
                break

        connfd.close()

if __name__ == "__main__":
    main()
