from django.contrib import admin

from click.models import ClickTransaction

# Register your models here.
@admin.register(ClickTransaction)
class ClickTransactionAdmin(admin.ModelAdmin):
    list_display = ('merchant_prepare_id','click_trans_id', 'state','click_paydoc_id','merchant_trans_id', 'created_at', 'updated_at')