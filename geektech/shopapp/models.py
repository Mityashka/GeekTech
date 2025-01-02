from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='products/images/')

    def __str__(self):
        return f"Image for {self.product.product_name}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=80)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    images = models.ManyToManyField(ProductImage, blank=True, related_name='products')
    preview = models.ImageField(upload_to='products/previews/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    stock_quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return f"{self.product_name} ({self.manufacturer})"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username}, продукт {self.product.product_name}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    products = models.ManyToManyField('Product', through='OrderItem')

    def update_total_price(self):
        total = 0
        for item in self.items.all():
            total += item.quantity * item.price
        self.total_price = total
        self.save()

    def __str__(self):
        return f"Заказ №{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Feedback(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    text = models.TextField(max_length=2000)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Автор: {self.author.username} {self.title}'


class Promotion(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField(max_length=2000)

    def __str__(self):
        return f'{self.title}'


class Delivery(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField(max_length=2000)

    def __str__(self):
        return f'{self.title}'


class Contact(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField(max_length=2000)

    def __str__(self):
        return f'{self.title}'
