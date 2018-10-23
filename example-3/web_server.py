import json
import socket

HOST = ''    # Listen on any interface
PORT = 8000  # Listen on port 8000
MAX_SIZE = 1024
CRLF = '\r\n'


def parse_header_line(line):
    key, value = line.split(':', maxsplit=1)
    return (key, value.strip())


def parse_request_line(line):
    return line.split()


def parse_http(data):
    request_line, *header_lines = data.split(CRLF)
    method, path, protocol = parse_request_line(request_line)
    headers = dict(
        parse_header_line(line)
        for line in header_lines
    )

    return {
        'method': method,
        'path': path,
        'protocol': protocol,
        'headers': headers,
    }


def process_request(request):
    print(json.dumps(request, indent=4))
    return f'Hello {request["path"]}'


def process_response_headers(response):
    content_length = len(response)
    return CRLF.join([
        'HTTP/1.1 200 OK',
        f'Content-Length: {content_length}',
        'Content-Type: text/html',
        # Include a blank line at the end
        '',
        '',
    ])


with socket.socket() as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)
            http_request = conn.recv(MAX_SIZE).decode('utf-8').strip()
            request = parse_http(http_request)
            response = process_request(request)
            response_headers = process_response_headers(response)

            # Send HTTP response
            conn.sendall(response_headers.encode('utf-8'))
            conn.sendall(response.encode('utf-8'))
