from django.urls import path
from .views import basket_adding, checkout, product_remove_checkout

urlpatterns = [
    path('basket_adding/', basket_adding, name='basket_adding'),
    path('checkout/', checkout, name='checkout'),
    path('remove/<int:product_id>/', product_remove_checkout, name='product_remove_checkout'),
]
