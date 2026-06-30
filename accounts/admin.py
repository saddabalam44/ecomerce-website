from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Address

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'phone_number', 'is_email_verified', 'is_staff']
    search_fields = ['email', 'username']
    ordering = ['email']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'profile_picture', 'is_email_verified', 'email_verification_token')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'phone_number', 'profile_picture', 'is_email_verified')}),
    )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'city', 'state', 'postal_code', 'is_default']
    list_filter = ['is_default', 'state', 'country']
    search_fields = ['full_name', 'address_line1', 'city']

admin.site.register(CustomUser, CustomUserAdmin)
