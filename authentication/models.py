from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserProfile(models.Model):
    """Расширенный профиль пользователя для медицинского персонала"""
    
    ROLE_CHOICES = [
        ('doctor', 'Врач'),
        ('nurse', 'Медсестра'),
        ('admin', 'Администратор'),
        ('researcher', 'Исследователь'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Пользователь")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='nurse', verbose_name="Роль")
    license_number = models.CharField(max_length=50, blank=True, null=True, 
                                    help_text="Номер медицинской лицензии для врачей", verbose_name="Номер лицензии")
    department = models.CharField(max_length=100, blank=True, null=True,
                                help_text="Отделение или специальность", verbose_name="Отделение")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    is_active_staff = models.BooleanField(default=True,
                                        help_text="Является ли этот сотрудник активным в настоящее время", verbose_name="Активный сотрудник")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    
    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"
        
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
    """Отслеживание пользовательских сессий для аудита"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions_log', verbose_name="Пользователь")
    session_key = models.CharField(max_length=40, verbose_name="Ключ сессии")
    login_time = models.DateTimeField(auto_now_add=True, verbose_name="Время входа")
    logout_time = models.DateTimeField(null=True, blank=True, verbose_name="Время выхода")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP адрес")
    user_agent = models.TextField(blank=True, null=True, verbose_name="User Agent")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    
    class Meta:
        verbose_name = "Сессия пользователя"
        verbose_name_plural = "Сессии пользователей"
        ordering = ['-login_time']
        
    def __str__(self):
        return f"{self.user.username} - {self.login_time.strftime('%Y-%m-%d %H:%M')}"
