from django.http import HttpResponse


def view(request, *args, **kwargs):
    return HttpResponse(f'Hello {request.path}')
