def application(environ, start_response):
    path = environ['PATH_INFO']
    response = process_request(path)
    content_length = len(response)

    start_response('200 OK', [
        ('Content-Length', str(len(response))),
        ('Content-Type', 'text/html'),
    ])
    return [response.encode('utf-8')]


def process_request(path):
    return f'Hello {path}'
