from django.contrib import admin

from Uzum.models import UzumbankTransaction


# Register your models here.

@admin.register(UzumbankTransaction)
class UzumbankTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'state','created_at', 'updated_at')