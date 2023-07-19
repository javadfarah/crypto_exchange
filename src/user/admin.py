from django.contrib import admin
from .models import User, Order, Balance


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'crypto_name', 'crypto_amount', 'is_deleted', 'processed')


class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')


admin.site.register(User)
admin.site.register(Order, OrderAdmin)
admin.site.register(Balance, BalanceAdmin)
