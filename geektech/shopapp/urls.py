from django.urls import path, include

from .views import (ShopIndexView, ReviewsView, PromotionsView, DeliveryView,
                    ContactsView, CategoryDetailsView, cart_view, ProductDetailsView, cart_add, cart_delete, cart_decrease, order_create, FeedBackView)


app_name = 'shopapp'

urlpatterns = [
    path('', ShopIndexView.as_view(), name='index'),
    path('reviews/', ReviewsView.as_view(), name='reviews'),
    path('promotions/', PromotionsView.as_view(), name='promotions'),
    path('delivery/', DeliveryView.as_view(), name='delivery'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('category/<slug:slug>/', CategoryDetailsView.as_view(), name='category-detail'),
    path('product/<int:pk>/', ProductDetailsView.as_view(), name='product-details'),
    path('cart/', cart_view, name='cart'),
    path('cart/cart-add/<int:product_id>/', cart_add, name='cart-add'),
    path('cart/cart-delete/<int:product_id>/', cart_delete, name='cart-delete'),
    path('cart/cart-decrease/<int:product_id>/', cart_decrease, name='cart-decrease'),
    path('order/create/', order_create, name='order-create'),
    path('reviews/feedback', FeedBackView.as_view(), name='feedback'),

]
