from django.shortcuts import redirect
from .models import Cart

def Cart_count(get_response):
    def middleware(request):
        if not request.session.get('user'):
            pass
        else:
            cart_count = Cart.objects.filter(user = request.user).count()
            request.session['cart_count'] = cart_count
        response = get_response(request)
        return response
    return middleware

def auth_middleware(get_response):
    def middleware(request):
        # Code to be executed for each request before
        # # the view (and later middleware) are called.
        return_url = request.META['PATH_INFO']
        if not request.session.get('user'):
            return redirect(f'account/login/?next={return_url}')
        response = get_response(request)
        return response
    return middleware
