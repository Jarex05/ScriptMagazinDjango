from django.shortcuts import render
from .models import Product, ProductImage


def product(request, product_id):
    product_image = ProductImage.objects.filter(is_active=True, is_main=True)
    product = Product.objects.get(id=product_id)

    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()
    
    print(request.session.session_key)

    return render(request, 'products/product.html', {'products_images': product_image, 'product': product})
