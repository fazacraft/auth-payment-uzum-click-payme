from django.contrib import admin

from authentication.models import User, OTP


# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'is_verified')



@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'otp_key', 'otp_code')
