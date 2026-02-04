"""
Custom authentication views for academic platform
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import AuditLog


def login_view(request):
    """
    Custom login page with academic design
    """
    if request.user.is_authenticated:
        return redirect('corpus:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_approved:
                login(request, user)
                
                # Log the login
                AuditLog.objects.create(
                    user=user,
                    action=AuditLog.ActionType.LOGIN,
                    resource_type='AUTH',
                    description=f'User logged in successfully',
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
                )
                
                return redirect('corpus:dashboard')
            else:
                messages.error(request, 'Hesabiniz henuz onaylanmamis. Lutfen yonetici ile iletisime gecin.')
        else:
            messages.error(request, 'Kullanici adi veya sifre hatali.')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    """
    Logout view
    """
    if request.user.is_authenticated:
        # Log the logout
        AuditLog.objects.create(
            user=request.user,
            action=AuditLog.ActionType.LOGOUT,
            resource_type='AUTH',
            description=f'User logged out',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
        )
    
    logout(request)
    messages.success(request, 'Basariyla cikis yaptiniz.')
    return redirect('accounts:login')


def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
