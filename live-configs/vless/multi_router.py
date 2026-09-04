import re
import socket, threading

LISTEN = ("127.0.0.1", 8095)
ROUTES = {"/v9efc98": 8102, "/t492cab": 8103, "/s0ac55a": 8104}

def pipe(a, b):
    try:
        while True:
            d = a.recv(65536)
            if not d:
                break
            b.sendall(d)
    except OSError:
        pass
    finally:
        for s in (a, b):
            try:
                s.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            s.close()

def handle(c):
    try:
        c.settimeout(10)
        data = b""
        while b"\r\n\r\n" not in data:
            ch = c.recv(4096)
            if not ch:
                c.close()
                return
            data += ch
            if len(data) > 16384:
                c.close()
                return
        try:
            path = data.split(b" ")[1].decode().split("?")[0]
        except IndexError:
            c.close()
            return
        port = None
        if path == "/sub/moshtari-1day":
            try:
                with open("/data/vless/sub-moshtari.txt", "rb") as f:
                    body = f.read()
                c.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nConnection: close\r\nContent-Length: " + str(len(body)).encode() + b"\r\n\r\n" + body)
            except OSError:
                c.sendall(b"HTTP/1.1 404 Not Found\r\nConnection: close\r\nContent-Length: 0\r\n\r\n")
            c.close()
            return
        for prefix, p in ROUTES.items():
            if path == prefix or path.startswith(prefix + "/"):
                port = p
                break
        if port is None:
            c.sendall(b"HTTP/1.1 404 Not Found\r\nConnection: close\r\nContent-Length: 0\r\n\r\n")
            c.close()
            return
        if b"upgrade" not in data.lower():
            # plain HTTP (probes): force connection close so the tunnel
            # opens a fresh origin connection per request and each one
            # gets routed by path again (no keep-alive glue to one backend)
            data = re.sub(rb"\r\nConnection:[^\r]*", b"", data, flags=re.IGNORECASE)
            data = data.replace(b"\r\n\r\n", b"\r\nConnection: close\r\n\r\n", 1)
        u = socket.create_connection(("127.0.0.1", port), timeout=10)
        u.sendall(data)
        c.settimeout(None)
        threading.Thread(target=pipe, args=(c, u), daemon=True).start()
        pipe(u, c)
    except OSError:
        try:
            c.close()
        except OSError:
            pass

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(LISTEN)
s.listen(128)
print("multi-router on 8095", flush=True)
while True:
    conn, _ = s.accept()
    threading.Thread(target=handle, args=(conn,), daemon=True).start()
