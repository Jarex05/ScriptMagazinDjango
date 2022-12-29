from django.db import models

# Продукт
class Product(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None) # Название продукта
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)     # Цена за еденицу
    nmb = models.IntegerField(default=0)                                        # Выбор колличества
    quantity_in_stock = models.IntegerField(default=0)                          # Количество товара на складе
    short_descpription = models.TextField(blank=True, null=True, default=None)  # Короткое описание продукта
    description = models.TextField(blank=True, null=True, default=None)         # Полное описание продукта
    is_active = models.BooleanField(default=True)                               # Включение и отключени продукта для отображения на сайте
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s, %s" % (self.price, self.name)

    def main_image(self):
        return self.productimage_set.get(is_main=True, is_active=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

# Картинки продуктов
class ProductImage(models.Model):                                                                       
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, default=None)  # Связанная модель 
    image = models.ImageField(upload_to="products_images/")                                              # Картинка продукта
    is_main = models.BooleanField(default=True)                                                          # Включение продукта из фото для отображения на сайте 
    is_active = models.BooleanField(default=True)                                                        # Включение основной картинки для отображения на продукте
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'