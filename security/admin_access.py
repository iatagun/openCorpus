"""
Admin access control middleware
"""
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import resolve


class AdminAccessMiddleware:
    """
    Middleware to restrict admin panel access to ADMIN role only
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if accessing admin panel
        if request.path.startswith('/admin/') and not request.path.startswith('/admin/login'):
            # Allow access only if user is authenticated and has ADMIN role
            if request.user.is_authenticated:
                if not (request.user.is_superuser or request.user.role == 'ADMIN'):
                    messages.error(request, 'Bu alana erisim yetkiniz bulunmamaktadir.')
                    return redirect('corpus:dashboard')
        
        response = self.get_response(request)
        return response
