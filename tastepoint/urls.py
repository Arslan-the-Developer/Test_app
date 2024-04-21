from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from tastepointapp import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('tastepointapp.urls')),
    path('auth',include('authentication.urls')),
    path('about',views.about, name='about'),
    path('products',views.products, name='products'),
    path('product/<int:pk>/',views.product_detail,name='product_detail'),
    path('cart',views.user_cart,name='user_cart'),
    path('update_cart_quantity',views.update_quantity,name='update_quantity'),
    path('clear-cart',views.clear_cart,name='clear_cart'),
    path('checkout',views.handle_checkout,name='handle_checkout'),
    path('payment',views.handle_payment,name='handle_payment'),
    path('order_success',views.order_success,name='order_success')
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)