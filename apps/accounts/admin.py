from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .admin_forms import EmailAuthenticationForm
from .models import FriendRequest

User = get_user_model()

admin.site.login_form = EmailAuthenticationForm


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active')

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('profile_picture', 'bio', 'last_seen')
        }),
    )
    
@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'created_at')