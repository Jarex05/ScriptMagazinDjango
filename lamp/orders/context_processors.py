from .models import ProductInBasket


def getting_basket_info(request):

    session_key = request.session.session_key
    if not session_key:
        #workaround for newer Django versions...
        request.session["session_key"] = 123
        #re-apply value
        request.session.cycle_key()

    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    products_total_nmb = products_in_basket.count()
    all_products_in_order = products_in_basket
    order_total_price = 0
    for item in all_products_in_order:
        order_total_price += item.total_price
    
        
    return locals()