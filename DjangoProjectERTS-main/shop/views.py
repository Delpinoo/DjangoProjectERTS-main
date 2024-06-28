from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from .forms import ContactoForm, ProductoForm, CustomUserCreationForm
from .models import Producto, Carro
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from shop.carro import Carrito
from django.contrib.auth.decorators import login_required
# Create your views here.


@permission_required('shop.view_producto')
def index (request):
    productos = Producto.objects.all()
    page = request.GET.get('page', 1)
    
    try:
        paginator = Paginator(productos, 10)
        productos = paginator.page(page)
    except:
        raise Http404
    
    data = {
        'entity': productos,
        'paginator': paginator,
        
    }
    return render(
        request,
        'index.html',
        context={
            'productos': productos,
            'paginator': paginator}
    )



def detalle(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto = Producto.objects.get(id=producto_id)
        
    return render(
        request, 
        'detalle.html', 
        context= {'producto': producto})
    

    
def stickers(request):
    productos = Producto.objects.filter(categoria_id=1)
    return render(request, 'stickers.html', {'productos': productos})

def llantas(request):
    productos = Producto.objects.filter(categoria_id=2)
    return render(request, 'llantas.html', {'productos': productos})

def accesorios(request):
    productos = Producto.objects.filter(categoria_id=3)
    return render(request, 'accesorios.html', {'productos': productos})

def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/shop/contacto')  
    else:
        form = ContactoForm()

    data = {
        'contacto_form': form
    }
    return render(request, 'contacto.html', data)

def tienda(request):

    return render(request, 'tienda.html')




@permission_required('shop.add_producto')
def agregar_producto (request):
    data= {
        'form': ProductoForm()
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Agregado Correctamente")
        else:
            data["form"] = formulario
    
    return render(request,'producto/agregar.html', data)



@permission_required('shop.change_producto')
def modificar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    data = {
        'form' : ProductoForm(instance=producto)
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return HttpResponseRedirect('/shop')
        else:
            data["form"] = formulario
    
    return render(request, 'producto/modificar.html',data)



@permission_required('shop.delete_producto')
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "Eliminado Correctamente")
    return HttpResponseRedirect('/shop')
    
    
def registro (request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username= formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Registrado Correctamente")
            return redirect(to="inicio")
        data['form'] = formulario
    return render(request, 'registration/registro.html', data)


@login_required
def agregar_producto_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = Carrito(request)
    carrito.agregar(producto)
    
    messages.success(request, f"Producto {producto.nombre} agregado al carrito.")
    return redirect('tienda')
@login_required
def agregar_producto_carrito_otro(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = Carrito(request)
    carrito.agregar(producto)
    return redirect('carrito')
@login_required
def eliminar_producto_carrito(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect("tienda")
@login_required
def restar_producto_carrito(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect("carrito")
@login_required
def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("carrito")

def iniciar_carrito(request):
    if 'carrito' not in request.session:
        request.session['carrito'] = {}


def carrito(request):
    return render(request, 'carrito.html')

def comprar_producto(request):
    if 'carrito' in request.session:
        carrito = request.session['carrito']
        productos = Producto.objects.filter(id__in=carrito)
        
        for producto in productos:
            carro_item, created = Carro.objects.get_or_create(
                usuario=request.user,
                producto=producto.nombre,
                defaults={
                    
                'producto': producto.nombre,
                'cantidad': 1,
                'precio': producto.precio,
                'comprado': True
                }
            )
            if not created:
                carro_item.cantidad += 1
                carro_item.comprado = True
                carro_item.save()
        
        request.session['carrito'] = []
        
        return render(request, 'mis_pedidos.html')
    else:
        messages.info(request, "No tienes productos en el carrito.")
        return redirect('tienda')


def mis_pedidos(request):
    productos_carrito = Carro.objects.filter(usuario=request.user, comprado=True)
    
    context = {
        'productos_carrito': productos_carrito
    }
    return render(request, 'mis_pedidos.html', context)
