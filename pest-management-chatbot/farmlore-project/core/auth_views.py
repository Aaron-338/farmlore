from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["GET", "POST"])
def custom_logout(request):
    """
    Custom logout view that handles both GET and POST requests.
    This is more flexible than Django's built-in LogoutView.
    """
    logout(request)
    return redirect('core:home')
