from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from .models import UserProfile


def role_required(roles):
    """
    Decorator that requires user to have one of the specified roles
    Usage: @role_required(['doctor', 'admin'])
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            try:
                profile = request.user.profile
                if not profile.is_active_staff:
                    messages.error(request, 'Your account has been deactivated. Please contact administrator.')
                    return redirect('login')
                
                if profile.role not in roles:
                    messages.error(request, f'Access denied. This page requires {" or ".join(roles)} role.')
                    return redirect('dashboard')
                
                return view_func(request, *args, **kwargs)
            except UserProfile.DoesNotExist:
                messages.error(request, 'User profile not found. Please contact administrator.')
                return redirect('login')
        return _wrapped_view
    return decorator


def can_manage_users_required(view_func):
    """Decorator that requires user management permissions"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        try:
            profile = request.user.profile
            if not profile.can_manage_users:
                messages.error(request, 'Access denied. User management permissions required.')
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        except UserProfile.DoesNotExist:
            messages.error(request, 'User profile not found. Please contact administrator.')
            return redirect('login')
    return _wrapped_view


def can_view_all_patients_required(view_func):
    """Decorator that requires permission to view all patients"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        try:
            profile = request.user.profile
            if not profile.can_view_all_patients:
                messages.error(request, 'Access denied. Full patient access required.')
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        except UserProfile.DoesNotExist:
            messages.error(request, 'User profile not found. Please contact administrator.')
            return redirect('login')
    return _wrapped_view


def can_edit_patients_required(view_func):
    """Decorator that requires permission to edit patient data"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        try:
            profile = request.user.profile
            if not profile.can_edit_patients:
                messages.error(request, 'Access denied. Patient editing permissions required.')
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        except UserProfile.DoesNotExist:
            messages.error(request, 'User profile not found. Please contact administrator.')
            return redirect('login')
    return _wrapped_view


def can_delete_data_required(view_func):
    """Decorator that requires permission to delete data"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        try:
            profile = request.user.profile
            if not profile.can_delete_data:
                messages.error(request, 'Access denied. Data deletion permissions required.')
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        except UserProfile.DoesNotExist:
            messages.error(request, 'User profile not found. Please contact administrator.')
            return redirect('login')
    return _wrapped_view


def can_view_analytics_required(view_func):
    """Decorator that requires permission to view analytics"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        try:
            profile = request.user.profile
            if not profile.can_view_analytics:
                messages.error(request, 'Access denied. Analytics viewing permissions required.')
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        except UserProfile.DoesNotExist:
            messages.error(request, 'User profile not found. Please contact administrator.')
            return redirect('login')
    return _wrapped_view


def active_staff_required(view_func):
    """Decorator that requires user to be active staff"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        try:
            profile = request.user.profile
            if not profile.is_active_staff:
                messages.error(request, 'Your account has been deactivated. Please contact administrator.')
                return redirect('login')
            return view_func(request, *args, **kwargs)
        except UserProfile.DoesNotExist:
            # Create default profile for users without one
            profile = UserProfile.objects.create(
                user=request.user,
                role='nurse' if not request.user.is_superuser else 'admin',
                is_active_staff=True
            )
            messages.info(request, 'User profile created. Please update your profile information.')
            return view_func(request, *args, **kwargs)
    return _wrapped_view