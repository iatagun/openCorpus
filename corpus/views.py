"""
Main corpus app views
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from corpus.models import Document, Category, Compilation
from accounts.models import CustomUser


def home(request):
    """
    Home page view - redirect authenticated users to dashboard
    """
    if request.user.is_authenticated:
        return redirect('corpus:dashboard')
    
    context = {
        'total_documents': Document.objects.filter(status=Document.Status.APPROVED).count(),
        'total_categories': Category.objects.filter(is_active=True).count(),
        'total_compilations': Compilation.objects.filter(is_public=True).count(),
        'total_users': CustomUser.objects.filter(is_active=True, is_approved=True).count(),
    }
    return render(request, 'home.html', context)


@login_required
def dashboard(request):
    """
    Role-based user dashboard
    """
    user = request.user
    
    # Base statistics
    context = {
        'user': user,
        'recent_documents': Document.objects.filter(
            uploaded_by=user
        ).order_by('-created_at')[:5] if user.can_edit_corpus() else Document.objects.filter(
            status=Document.Status.APPROVED
        ).order_by('-created_at')[:5],
        'user_compilations': Compilation.objects.filter(
            created_by=user
        ).order_by('-created_at')[:5],
    }
    
    # Role-specific data
    if user.role == user.Role.ADMIN:
        context.update({
            'pending_users': CustomUser.objects.filter(is_approved=False).count(),
            'pending_documents': Document.objects.filter(status=Document.Status.PENDING).count(),
            'total_users': CustomUser.objects.count(),
        })
    elif user.role == user.Role.EDITOR:
        context.update({
            'my_documents': Document.objects.filter(uploaded_by=user).count(),
            'pending_documents': Document.objects.filter(
                status=Document.Status.PENDING
            ).count(),
        })
    elif user.role == user.Role.RESEARCHER:
        context.update({
            'available_compilations': Compilation.objects.filter(is_public=True).count(),
            'total_documents': Document.objects.filter(status=Document.Status.APPROVED).count(),
        })
    
    return render(request, 'dashboard.html', context)
