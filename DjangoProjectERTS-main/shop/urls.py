from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:producto_id>', views.detalle, name='detalle'),
    path('stickers', views.stickers, name='stickers'),
    path('llantas', views.llantas, name='llantas'),
    path('accesorios', views.accesorios, name='accesorios'),
    path('contacto', views.contacto, name='contacto'),
    path('tienda', views.tienda, name='tienda'),
    path('carrito/', views.carrito, name='carrito'),
    path('mis_pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('comprar/<int:producto_id>/', views.comprar_producto, name='comprar_producto'),
    path('agregar-producto', views.agregar_producto, name='agregar_producto'),
    path('modificar-producto/<id>/', views.modificar_producto, name='modificar_producto'),
    path('eliminar-producto/<id>/', views.eliminar_producto, name='eliminar_producto'),
    path('registro', views.registro, name='registro'),
]
