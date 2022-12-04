from django.shortcuts import redirect, render
from products.models import ProductImage
from django.views.generic import View



class Home(View):
    def get(self, request):
        products_images = ProductImage.objects.filter(is_active=True, is_main=True)

        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
    
        print(request.session.session_key)

        return render(request, 'blog/home.html', context={'products_images': products_images})





# def home(request):
#     products_images = ProductImage.objects.filter(is_active=True, is_main=True)
    
#     session_key = request.session.session_key
#     if not session_key:
#         request.session.cycle_key()
    
#     print(request.session.session_key)
    
#     return render(request, 'blog/home.html', context={'products_images': products_images})



