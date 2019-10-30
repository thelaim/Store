from django.urls import path
from . import views
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('product/', views.find_item, name='find_item'),
    path('product/<int:pk>/', views.item_detail, name='item_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('list_checkout/', views.list_checkout, name='list_checkout'),
    path('list_checkout/no', views.no_list_checkout, name='no_list_checkout'),
    path('cart/', views.cart, name='cart'),
    path('cart/no', views.no_cart, name='no_cart'),
    path('cart/remove/<int:pk>/', views.remove_item, name='remove_item'),
    path('cart/add/<int:pk>/', views.add_cart, name='add_cart'),
    path('account/register', views.register, name='register'),
    path('account/login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)