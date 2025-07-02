from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import UserSession, UserProfile


def login_view(request):
    """Custom login view with session tracking"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if user has profile and is active staff
            try:
                profile = user.profile
                if not profile.is_active_staff:
                    messages.error(request, 'Your account has been deactivated. Please contact administrator.')
                    return render(request, 'authentication/login.html')
            except UserProfile.DoesNotExist:
                messages.error(request, 'User profile not found. Please contact administrator.')
                return render(request, 'authentication/login.html')
            
            # Log the user in
            login(request, user)
            
            # Create session record for audit
            UserSession.objects.create(
                user=user,
                session_key=request.session.session_key or '',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                is_active=True
            )
            
            messages.success(request, f'Welcome back, {profile.full_name}!')
            
            # Redirect to next URL or dashboard
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'authentication/login.html')


@login_required
def logout_view(request):
    """Custom logout view with session cleanup"""
    # Update session record
    try:
        session = UserSession.objects.filter(
            user=request.user,
            session_key=request.session.session_key,
            is_active=True
        ).first()
        
        if session:
            session.logout_time = timezone.now()
            session.is_active = False
            session.save()
    except Exception:
        pass  # Don't fail logout if session update fails
    
    username = request.user.username
    logout(request)
    messages.success(request, f'You have been logged out successfully.')
    return redirect('login')


@login_required
def profile_view(request):
    """View user profile and recent sessions"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profile not found. Please contact administrator.')
        return redirect('dashboard')
    
    # Get recent sessions
    recent_sessions = UserSession.objects.filter(
        user=request.user
    ).order_by('-login_time')[:10]
    
    context = {
        'profile': profile,
        'recent_sessions': recent_sessions,
    }
    
    return render(request, 'authentication/profile.html', context)


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
