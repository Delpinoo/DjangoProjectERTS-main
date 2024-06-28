"""endlessride URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from shop.forms import CustomAuthenticationForm
from . import views
from django.conf import settings
from django.conf.urls.static import static
from shop.views import agregar_producto_carrito,agregar_producto_carrito_otro , eliminar_producto_carrito, restar_producto_carrito, limpiar_carrito, tienda, carrito, comprar_producto, mis_pedidos
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('tienda', tienda, name='tienda'),
    path('carrito', carrito, name='carrito'),
    path('mis_pedidos/', mis_pedidos, name='mis_pedidos'),
    path('comprar/<int:producto_id>/', comprar_producto, name='comprar_producto'),
    path('admin/', admin.site.urls),
    path('shop/', include('shop.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(authentication_form=CustomAuthenticationForm), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('agregar/<int:producto_id>/', agregar_producto_carrito, name="agregar"),
    path('agregar_otro/<int:producto_id>/', agregar_producto_carrito_otro, name="agregar_otro"),
    path('eliminar/<int:producto_id>/', eliminar_producto_carrito, name="eliminar"),
    path('restas/<int:producto_id>/', restar_producto_carrito, name="restar"),
    path('limpiar/', limpiar_carrito, name="limpiar"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)