from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .models import ProductInBasket, Order, ProductInOrder
from products.models import Product
from django.shortcuts import render
from .forms import CheckoutContactForm
from django.contrib.auth.models import User
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse


def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    print (request.POST)
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")
    quantity = data.get("quantity")
    quantity = int(quantity) - int(nmb)
    print("Колличество " + str(quantity))
    is_delete = data.get("is_delete")

    if is_delete == 'true':
        ProductInBasket.objects.filter(id=product_id).update(is_active=False)
    else:
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id, is_active=True, defaults={"nmb": nmb})
        Product.objects.filter(name=new_product.product.name).update(nmb=quantity)
        if not created:
            print("not created")
            new_product.nmb += int(nmb)
            new_product.save(force_update=True)
            new_product.product.nmb -= int(nmb)
            Product.objects.filter(name=new_product.product.name).update(nmb=new_product.product.nmb)

            if new_product.nmb > new_product.product.quantity_in_stock:
                new_product.nmb = new_product.product.quantity_in_stock
                new_product.save(force_update=True)

            if new_product.product.nmb < 0:
                new_product.product.nmb = 0
                Product.objects.filter(name=new_product.product.name).update(nmb=new_product.product.nmb)

    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    products_total_nmb = products_in_basket.count()
    all_products_in_order = products_in_basket
    order_total_price = 0
    for item in all_products_in_order:
        order_total_price += item.total_price

    return_dict["products_total_nmb"] = products_total_nmb
    return_dict["order_total_price"] = order_total_price

    return_dict["products"] = list()

    for item in products_in_basket:
        product_dict = dict()
        product_dict["id"] = item.id
        product_dict["image"] = item.product.main_image().image.url
        product_dict["name"] = item.product.name
        product_dict["price_per_item"] = item.price_per_item
        product_dict["nmb"] = item.nmb
        product_dict["quantity"] = item.product.nmb
        product_dict["total_price"] = item.total_price
        return_dict["products"].append(product_dict)

    return JsonResponse(return_dict)


def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    form = CheckoutContactForm(request.POST or None)
    if request.POST:
        print(request.POST)
        if form.is_valid():
            print("yes")
            data = request.POST
            name = data.get("name", "3423453")
            phone = data["phone"]
            user, created = User.objects.get_or_create(username=phone, defaults={"first_name": name})

            order = Order.objects.create(user=user, customer_name=name, customer_phone=phone, status_id=1)

            for name, value in data.items():
                if name.startswith("product_in_basket_"):
                    product_in_basket_id = name.split("product_in_basket_")[1]
                    product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)
                    quantity = product_in_basket.product.quantity_in_stock

                    product_in_basket.nmb = value
                    product_in_basket.order = order
                    product_in_basket.save(force_update=True)
                    ProductInOrder.objects.create(product=product_in_basket.product, nmb = product_in_basket.nmb,
                                                  price_per_item=product_in_basket.price_per_item,
                                                  total_price = product_in_basket.total_price,
                                                  order=order)
                    ProductInBasket.objects.filter(product=product_in_basket.product).update(is_active=False)
                    quantity_stock = int(quantity) - int(product_in_basket.nmb)
                    print(quantity_stock)
                    Product.objects.filter(name=product_in_basket.product.name).update(quantity_in_stock=quantity_stock)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            print("no")
    return render(request, 'orders/checkout.html', locals())



def product_remove_checkout(request, product_id):
    product_in_basket = get_object_or_404(ProductInBasket, id=product_id)
    product_in_basket.delete()
    return redirect('checkout')