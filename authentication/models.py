from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserProfile(models.Model):
    """Extended user profile for medical practice staff"""
    
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('admin', 'Administrator'),
        ('researcher', 'Researcher'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='nurse')
    license_number = models.CharField(max_length=50, blank=True, null=True, 
                                    help_text="Medical license number for doctors")
    department = models.CharField(max_length=100, blank=True, null=True,
                                help_text="Department or specialty")
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_active_staff = models.BooleanField(default=True,
                                        help_text="Whether this staff member is currently active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"
    
    def clean(self):
        """Validate license number for doctors"""
        if self.role == 'doctor' and not self.license_number:
            raise ValidationError({'license_number': 'License number is required for doctors'})
    
    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username
    
    @property
    def can_manage_users(self):
        """Check if user can manage other users"""
        return self.role in ['admin', 'doctor']
    
    @property
    def can_view_all_patients(self):
        """Check if user can view all patients"""
        return self.role in ['admin', 'doctor', 'researcher']
    
    @property
    def can_edit_patients(self):
        """Check if user can edit patient data"""
        return self.role in ['admin', 'doctor', 'nurse']
    
    @property
    def can_delete_data(self):
        """Check if user can delete data"""
        return self.role in ['admin', 'doctor']
    
    @property
    def can_view_analytics(self):
        """Check if user can view group analytics and z-scores"""
        return self.role in ['admin', 'doctor', 'researcher']


class UserSession(models.Model):
    """Track user sessions for audit purposes"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions_log')
    session_key = models.CharField(max_length=40)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "User Session"
        verbose_name_plural = "User Sessions"
        ordering = ['-login_time']
        
    def __str__(self):
        return f"{self.user.username} - {self.login_time.strftime('%Y-%m-%d %H:%M')}"
