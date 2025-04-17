from django.contrib import admin

from payment.models import PaymeOrder, Transaction


# Register your models here.
@admin.register(PaymeOrder)
class PaymeOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_id', 'amount', 'is_paid']



@admin.register(Transaction)
class PaymeTransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'payme_order', 'amount', 'state', 'performed_at', 'canceled_at','created_at', 'updated_at']