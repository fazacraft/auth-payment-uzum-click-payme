from django.contrib import admin

from payment.models import PaymeOrder


# Register your models here.
@admin.register(PaymeOrder)
class PaymeOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_id', 'amount', 'is_paid']