from django.http import JsonResponse

class Response(JsonResponse):
    def __init__(self, success, message, status=None, **kwargs):
        data = kwargs
        data.update({
            "success": success,
            "message": message
        })
        super().__init__(data, status=status)


class SuccessResponse(Response):
    def __init__(self, message, status=None, **kwargs):
        status = 200 if (status == None) else status 
        super().__init__(success=True, message=message, status=status, **kwargs)


class ErrorResponse(Response):
    def __init__(self, message, status=None, **kwargs):
        super().__init__(success=False, message=message, status=status, **kwargs)


class Http400Response(ErrorResponse):
    def __init__(self, message, **kwargs):
        super().__init__(message=message, status=400, **kwargs)


class Http404Response(ErrorResponse):
    def __init__(self, message, **kwargs):
        super().__init__(message=message, status=404, **kwargs)


class Http500Response(ErrorResponse):
    def __init__(self, message, **kwargs):
        super().__init__(message=message, status=500, **kwargs)
    

class Http403Response(ErrorResponse):
    def __init__(self, message, **kwargs):
        super().__init__(message=message, status=403, **kwargs)