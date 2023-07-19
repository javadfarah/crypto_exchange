from django.contrib import admin
from exchange.models import OrderQueue


# Register your models here.
class OrderQueueAdmin(admin.ModelAdmin):
    list_display = ('crypto_name', 'is_deleted', 'total_amount', 'paid_at')


admin.site.register(OrderQueue, OrderQueueAdmin)
