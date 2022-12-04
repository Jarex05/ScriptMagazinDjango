from django.db import models
from products.models import Product, ProductImage
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.1

class Status(models.Model):
    name = models.CharField(max_length=24, blank=True, null=True, default=None)   # Название статуса
    is_active = models.BooleanField(default=True)                                 # Выбор активного статуса
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Статус: %s " % self.name

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)             # Общая цена заказа
    customer_name = models.CharField(max_length=64, blank=True, null=True, default=None)      # Имя клиента
    customer_email = models.EmailField(blank=True, null=True, default=None)                   # Емаил клиента
    customer_phone = models.CharField(max_length=48, blank=True, null=True, default=None)     # Номер телефона клиента
    customer_address = models.CharField(max_length=128, blank=True, null=True, default=None)  # Адрес клиента
    coments = models.TextField(blank=True, null=True, default=None)                           # Коментарий клиента
    status = models.ForeignKey(Status, on_delete=models.CASCADE)                              # Выбор статуса для заказа
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


    def save(self, *args, **kwargs):

        super(Order, self).save(*args, **kwargs)


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, default=None)      # Связанная модель с Ордером
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, default=None)  # Продукт или продукты в заказе
    nmb = models.IntegerField(default=1)                                                                 # Колличество продуктов в заказе
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)                     # Цена за еденицу товара в заказе
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)                        # Общая цена всех товаров в заказе
    is_active = models.BooleanField(default=True)                                                        # Активация товара в заказе
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.product.name)

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'


    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.price_per_item = price_per_item
        self.total_price = int(self.nmb) * price_per_item

        order = self.order
        all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)

        order_total_price = 0
        for item in all_products_in_order:
            order_total_price += item.total_price

        self.order.total_price = order_total_price
        self.order.save(force_update=True)

        super(ProductInOrder, self).save(*args, **kwargs)

def product_in_order_post_save(sender, instance, created, **kwargs):
    order = instance.order
    all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)

    order_total_price = 0
    for item in all_products_in_order:
        order_total_price += item.total_price

    instance.order.total_price = order_total_price
    instance.order.save(force_update=True)

post_save.connect(product_in_order_post_save, sender=ProductInOrder)
    

class ProductInBasket(models.Model):
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None)                  # Ключ сессии
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, default=None)      # Связь с моделью заказов с корзиной
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, default=None)  # Продукты в корзине
    nmb = models.IntegerField(default=1)                                                                 # Колличество продуктов в корзине
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)                     # Цена за еденицу в корзине
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)#price*nmb              # Общая цена продуктов в корзине
    is_active = models.BooleanField(default=True)                                                        # Включение и отключение активной корзины
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'


    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.price_per_item = price_per_item
        self.total_price = int(self.nmb) * price_per_item

        super(ProductInBasket, self).save(*args, **kwargs)