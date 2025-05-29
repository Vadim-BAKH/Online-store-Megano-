

class AppendSlashMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and not request.path.endswith('/'):
            request.path = request.path + '/'
        return self.get_response(request)
