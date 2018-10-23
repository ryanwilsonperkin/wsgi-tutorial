import socket

HOST = ''    # Listen on any interface
PORT = 8000  # Listen on port 8000

with socket.socket() as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        data = conn.recv(1024)
        print("Received", data)
        conn.sendall(b'Hello World')
