
from django.shortcuts import render,redirect
from django.db.models import Q,Prefetch
from django.forms import modelform_factory
from .models import *
from .forms import *
from django.db.models import Sum
from django.contrib import messages

# Create your views here.

def inicio(request):
    return render(request, 'Padre.html')

def pagina_de_enlaces(request):
    return render(request, 'enlaces.html')

def busqueda_avanzada(request):
    query = request.GET.get('query', '')  # Recupera el término de búsqueda
    tipo_busqueda = request.GET.get('tipo_busqueda', 'usuario')  # Recupera el tipo de búsqueda (usuario o curso)

    usuarios = []

    if query:
        if tipo_busqueda == 'usuario':
            usuarios = Usuario.objects.filter(nombre__icontains=query)
    
    # Devuelve los resultados a un template dentro de la carpeta 'formulario'
    return render(request, 'formulario/busqueda_resultado.html', {
        'usuarios': usuarios,
    })
    
def promocion_Form (request):
    if request.method == 'POST':
        formulario = PromocionForm(request.POST)
        if formulario.is_valid():
            try:
                # Guarda el usuario en la base de datos
                formulario.save()
                return redirect('filtros_avanzados_promociones')
            except Exception as error:
                print(error)
    else:
        formulario = PromocionForm()
        
    return render(request, 'formulario/promocionFormulario.html', {"formulario": formulario})

def filtros_avanzados_promociones(request):
    formulario = BusquedaAvanzadaPromocion(request.GET)
    promociones = Promocion.objects.all()
    usuarios = Usuario.objects.all()
    productos = Producto.objects.all()

    if request.GET:  # Si hay datos enviados por GET
        if formulario.is_valid():
            nombre = formulario.cleaned_data.get('nombre')
            descripcion = formulario.cleaned_data.get('descripcion')
            fecha_fin_inicio = formulario.cleaned_data.get('fecha_fin')
            fecha_fin_final = formulario.cleaned_data.get('fecha_fin')
            descuento = formulario.cleaned_data.get('descuento')
            usuario = formulario.cleaned_data.get('usuario')
            producto = formulario.cleaned_data.get('producto')

            # Aplicamos los filtros
            if nombre:
                promociones = promociones.filter(nombre__icontains=nombre)
            if descripcion:
                promociones = promociones.filter(descripcion__icontains = descripcion)
            if fecha_fin_inicio:
                promociones = promociones.filter(fecha_fin__gte=fecha_fin_inicio)
            if fecha_fin_final:
                promociones = promociones.filter(fecha_fin__lte=fecha_fin_final)
            if descuento:
                promociones = promociones.filter(descuento=descuento)
            if usuario:
                promociones = promociones.filter(usuario=usuario)
            if producto:
                promociones = promociones.filter(producto=producto)
        else:
            # Si el formulario no es válido, mostramos los errores
            return render(request, 'filtros_avanzados_promociones.html', {
                'formulario': formulario,
                'promociones':[],
                'usuarios': usuarios,
                'productos': productos,
                
            })

    # Siempre renderiza un HttpResponse
    return render(request, 'formulario/filtros_avanzados_promociones.html', {
        'formulario': formulario,
        'promociones':promociones,
        'usuarios': usuarios,
        'productos': productos,
    })
    
def promocion_modificar(request,promocion_id):
    promocion = Promocion.objects.get(id=promocion_id)

    datosFormulario = None

    if request.method == "POST":
        datosFormulario = request.POST


    formulario = PromocionForm(datosFormulario,instance = promocion)

    if (request.method == "POST"):

        if formulario.is_valid():
            try:
                formulario.save()
                messages.success(request, 'Se ha editado la Promocion '+formulario.cleaned_data.get('nombre')+" correctamente")
                return redirect('filtros_avanzados_promociones')
            except Exception as error:
                print(error)
    return render(request, 'formulario/promocion_modificar.html',{"formulario":formulario,"promocion":promocion})

def eliminar_promocion(request,promocion_id):
    promocion = Promocion.objects.get(id=promocion_id)
    try:
        promocion.delete()
        messages.success(request, "Se ha elimnado el promocion "+promocion.nombre+" correctamente")
    except Exception as error:
        print(error)
    return redirect('filtros_avanzados_promociones')