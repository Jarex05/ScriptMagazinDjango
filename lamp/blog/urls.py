from django.urls import path

from .views import Home

urlpatterns = [
    path('', Home.as_view(), name='home'),
]

# from blog import views
# path('', views.home, name='home'),