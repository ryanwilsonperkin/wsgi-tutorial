import json
import socket

from web_application import application

HOST = ''    # Listen on any interface
PORT = 8000  # Listen on port 8000
MAX_SIZE = 1024
CRLF = '\r\n'


def parse_header_line(line):
    key, value = line.split(':', maxsplit=1)
    return (format_header_key(key), value.strip())


def parse_request_line(line):
    return line.split()


def format_header_key(key):
    return 'HTTP_' + key.upper().replace('-', '_').replace(' ', '_')


def parse_http(data):
    request_line, *header_lines = data.split(CRLF)
    method, path, protocol = parse_request_line(request_line)
    headers = dict(
        parse_header_line(line)
        for line in header_lines
    )
    return {
        'PATH_INFO': path,
        'REQUEST_METHOD': method,
        'SERVER_PROTOCOL': protocol,
        **headers,
    }


with socket.socket() as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)
            http_request = conn.recv(MAX_SIZE).decode('utf-8').strip()
            environ = parse_http(http_request)

            # Define a callback for beginning the response
            def start_response(status, headers):
                # Send the status
                conn.sendall(f'HTTP/1.1 {status}{CRLF}'.encode('utf-8'))

                # Send each header
                for (key, value) in headers:
                    conn.sendall(f'{key}: {value}{CRLF}'.encode('utf-8'))

                # Send an extra blank line before the response body
                conn.sendall(CRLF.encode('utf-8'))

            # Run the application code
            response_chunks = application(environ, start_response)

            # Send the response body
            for chunk in response_chunks:
                conn.sendall(chunk)
