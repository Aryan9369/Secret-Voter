from django.contrib import admin
from .models import User, OTPVerification

class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'is_verified', 'is_staff', 'date_joined')
    search_fields = ('phone_number',)

admin.site.register(User, UserAdmin)
admin.site.register(OTPVerification)
