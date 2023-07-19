from django.urls import path
from exchange.api.v1.views import SetOrderView

exchange_url_patterns_v1 = [
    path('set_orders/', SetOrderView.as_view(), name='set-order'),

]
