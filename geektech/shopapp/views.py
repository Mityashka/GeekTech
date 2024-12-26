import slug
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request
from django.views import View
from django.views.generic import ListView, DetailView
from django.db import models

from .models import Product, Category, Cart, Feedback, Promotion, Delivery, Contact


# Create your views here.

class ShopIndexView(View):
    def get(self, request):
        products = Product.objects.all()
        categories = Category.objects.all()
        return render(request, 'geektech.html', {'products': products, 'categories': categories})

class ReviewsView(View):
    def get(self, request: HttpRequest):
        feedbacks = Feedback.objects.all().order_by('-created_timestamp')
        return render(request, 'reviews.html', {'feedbacks': feedbacks})

class PromotionsView(View):
    def get(self, request: HttpRequest):
        promotions = Promotion.objects.all()
        return render(request, 'promotions.html', {'promotions':promotions})

class DeliveryView(View):
    def get(self, request: HttpRequest):
        deliveries = Delivery.objects.all()
        return render(request, 'delivery.html', {'deliveries':deliveries})

class ContactsView(View):
    def get(self, request: HttpRequest):
        contacts = Contact.objects.all()
        return render(request, 'contacts.html', {'contacts':contacts})

class ProductListView(View):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class CategoryDetailsView(ListView):
    template_name = 'category.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Product.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        return context

class CategoryPreviewView(View):
    def get(self, request, slug):
        category = Category.objects.get(slug=slug)
        return render(request, 'category.html', {'category': category})


class ProductDetailsView(DetailView):
    model = Product
    template_name = 'product-details.html'
    context_object_name = 'product'

@login_required
def cart_view(request: HttpRequest):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    for item in cart_items:
        item.total_price = item.quantity * item.product.price
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


def cart_add(request: HttpRequest, product_id: int):
    current_page = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.filter(user=request.user, product=product)
    if not cart.exists():
        Cart.objects.create(user=request.user, product=product, quantity=1)
        return HttpResponseRedirect(current_page)
    else:
        cart = cart.first()
        cart.quantity += 1
        cart.save()
        return HttpResponseRedirect(current_page)

def cart_delete(request: HttpRequest, product_id: int):
    cart = Cart.objects.get(id=product_id)
    cart.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def cart_decrease(request, product_id: int):
    cart_item = Cart.objects.get(product__id=product_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    products = models.ManyToManyField(Product, through='OrderItem')

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



    def __str__(self):
        return f"{self.product.product_name} - {self.quantity} шт"

def order_create(request):
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=request.user)
        order = Order.objects.create(user=request.user)
        total_price = 0

        for item in cart_items:
            if item.product.stock_quantity >= item.quantity:
                order_item = OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
                item.product.stock_quantity -= item.quantity
                item.product.save()
                total_price += item.product.price * item.quantity
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Недостаточно товара {item.product.product_name} на складе.'
                })

        order.total_price = total_price
        order.save()
        cart_items.delete()

        return JsonResponse({
            'status': 'success',
            'order_number': order.id
        })

class FeedBackView(View):
    def get(self, request: HttpRequest):
        feedbacks = Feedback.objects.all().order_by('-created_timestamp')
        return render(request, 'feedback.html')

    def post(self, request: HttpRequest):
        text = request.POST.get('text', '')
        title = request.POST.get('title', '')
        if not request.user.is_authenticated:
            return HttpResponse("Вы должны быть авторизованы, чтобы оставить отзыв", status=403)

        if text and title:
            Feedback.objects.create(
                title=title,
                text=text,
                author=request.user
            )
        return redirect('shopapp:reviews')



