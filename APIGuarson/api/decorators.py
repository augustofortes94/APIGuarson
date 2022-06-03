from functools import wraps
from django.http import JsonResponse
import jwt

def api_login_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        token = request.request.COOKIES.get('jwt')
        if token == None:
            return JsonResponse({'message':"Error: Unauthenticated..."})
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])     #if the token can be decoded, it is a valid token
        except Exception: #jwt.ExpiredSignatureError:
            return JsonResponse({'message':"Error: Unauthenticated..."})    #if the token is expired or something else, refuse
        return function(request, *args, **kwargs)
    return wrap