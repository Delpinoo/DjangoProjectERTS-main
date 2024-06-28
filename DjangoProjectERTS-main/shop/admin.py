from django.contrib import admin
from .models import Categoria, Contacto, Producto, Carro


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    
class ProductoAdmin(admin.ModelAdmin):
    exclude = ('creado_en', )
    list_display = ('id', 'nombre', 'stock', 'precio', 'creado_en')
    search_fields = ('nombre',)

# Register your models here.
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Contacto)
admin.site.register(Carro)
