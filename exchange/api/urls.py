from django.urls import path, include
from rest_framework import routers

from product.api.v1.views.feature_crud import FeatureCrud
from product.api.v1.views.product_image import ProductImageCrud
from product.api.v1.views.product_crud import ProductCrud

router = routers.DefaultRouter()
router.register('tags', FeatureCrud, basename='tags')
router.register('images', ProductImageCrud, basename='images')
router.register('products', ProductCrud, basename='products')
product_url_patterns_v1 = [
    path('', include(router.urls)),

]
