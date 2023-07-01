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


def write_all(fd, buf):
    n = len(buf)
    pos = 0
    while n > 0:
        sent = fd.send(buf[pos:])
        if sent == 0:
            return -1 # error
        n -= sent
        pos += sent


def query(fd, text):
    length = len(text)
    if length > k_max_msg:
        return -1

    # total data
    wbuf = struct.pack("<i", length) + text.encode()
    if write_all(fd, wbuf):
        return -1

    # code to read from server.
    # 4 bytes header
    rbuf = bytearray(4 + k_max_msg+1)
    try:
        # Read the header
        read_full(fd, rbuf, 4, 0)

        len_ = struct.unpack("<i", rbuf[:4])[0] # Assume little endian

        if len_ > k_max_msg:
            msg("too long")
            return -1

        # Read the reply body
        read_full(fd, rbuf, len_, 4)

        # Process the reply
        reply = rbuf[4:4+len_].decode()
        print("Server says:", reply)

        return 0
    except Exception as e:
        msg("Error: " + str(e))
        return -1


def main():
    fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if not fd:
        die("socket()")

    addr = ("127.0.0.1", 1234)
    try:
        fd.connect(addr)
    except Exception as e:
        die("connect " + str(e))

    # Multiple requests
    err = query(fd, "hello1")
    if err:
        fd.close()
        return
    err = query(fd, "hello2")
    if err:
        fd.close()
        return
    err = query(fd, "hello3")
    if err:
        fd.close()
        return

if __name__ == "__main__":
    main()
