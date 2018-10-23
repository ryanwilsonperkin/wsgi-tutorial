import socket

HOST = ''    # Listen on any interface
PORT = 8000  # Listen on port 8000
MAX_SIZE = 1024


def process_request(request):
    print("Received", request)
    return 'Hello World'


with socket.socket() as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)
            data = conn.recv(MAX_SIZE)
            response = process_request(data)
            conn.sendall(response.encode('utf-8'))
