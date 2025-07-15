from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from food_items import views

urlpatterns = [
    path('', views.menupage, name='menupage'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('admin/', admin.site.urls),
]

# 👇 Ye zaruri hai image (MEDIA files) dikhane ke liye:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
