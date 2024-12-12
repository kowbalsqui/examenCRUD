from django import forms
from datetime import datetime
from django.forms import ModelForm
from .models import *
from django.utils.timezone import now
from datetime import date, timedelta
from datetime import datetime

class PromocionForm(ModelForm):
    class Meta:
        model = Promocion
        fields = ['nombre', 'descripcion', 'producto', 'usuario', 'descuento', 'fecha_inicio', 'fecha_fin']
        labels = {
            "Nombre": ("Nombre de la promocion"),
            "Descripcion": ("Descripcion"),
            "Producto": ("Producto"),
            "Usuario": ("Usuario"),
            "Descuento": ("Descuento"),
            "Fecha_de_inicio": ("Fecha de inicio"),
            "Fecha_de_fin": ("Fecha de fin"),
        }
        widgets = {
            "Fecha_de_inicio":forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "Fecha_de_fin":forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "Producto": forms.Select(attrs={'class': 'form-control'}),
            "Usuario": forms.Select(attrs={'class': 'form-control'}),
            "Descuento": forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def clean (self):
        
        super().clean()
        
        #Primero obtenemos los campos necesarios
        
        nombre = self.cleaned_data.get('nombre')
        descripcion = self.cleaned_data.get('descripcion')
        producto = self.cleaned_data.get('producto')
        usuario = self.cleaned_data.get('usuario')
        descuento = self.cleaned_data.get('desceuento')
        fecha_de_inicio = self.cleaned_data.get('fecha_inicio')
        fecha_de_fin = self.cleaned_data.get('fecha_fin')
        

        if len(nombre) < 3:
            self.add_error('nombre', 'El nombre debe tener al menos 3 o más caracteres')
        
        
        if len(descripcion) > 100:
            self.add_error('descripcion', 'La descripcion es demasiado larga')
        
        
        if not producto:
            self.add_error('producto', 'debes elejir un producto')
        
        
        if not usuario:
            self.add_error('usuario', 'debes elejir un usuario')
            
        if descuento is not None and descuento < 0:
            self.add_error('descuento', 'El descuento debe ser mayor que 0.')
        
        if descuento is not None and descuento > 10:
            self.add_error('descuento', 'El descuento debe ser menor que 10.')
        
        
        if fecha_de_inicio > fecha_de_fin :
            self.add_error('fecha_de_inicio', 'La fecha de inicio debe ser menor a la de fin')
            
        if fecha_de_fin < fecha_de_inicio:
            self.add_error('fecha_de_fin', 'La fecha de fin debe ser mayor a la de inicio')
        
        return self.cleaned_data
    
class BusquedaAvanzadaPromocion(forms.Form):
     nombre = forms.CharField(
        max_length=50, 
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'nombre de promocion',
        })
    )
     
     descripcion = forms.CharField(
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'descripcion de la promocion',
        })
    )
     
     fecha_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        })
    )
     
     descuento = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'desceunto'
        })
    )
     
     usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
     
     producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

def clean(self):
        super().clean()

        nombre = self.cleaned_data.get('nombre')
        descripcion = self.cleaned_data.get('descripcion')
        fecha_fin_inicio = self.cleaned_data.get('fecha_fin')
        fecha_fin_final = self.cleaned_data.get('fecha_fin')
        descuento = self.cleaned_data.get('descuento')
        usuario = self.cleaned_data.get('usuario')
        producto = self.cleaned_data.get('producto')

        if not nombre and not descripcion and not fecha_fin_inicio and not fecha_fin_final and not descuento and not usuario and not producto:
            self.add_error('nombre', 'Debe ingresar algún criterio de búsqueda.')
            self.add_error('descripcion', 'Debe ingresar algún criterio de búsqueda.')
            self.add_error('fecha_fin_inicio', 'Debe ingresar algún criterio de búsqueda.')
            self.add_error('fecha_fin_final', 'Debe ingresar algún criterio de búsqueda.')
            self.add_error('descuento', 'Debe ingresar algún criterio de búsqueda.')
            self.add_error('usuario', 'Debe ingresar algún criterio de búsqueda.')
            self.add_error('producto', 'Debe ingresar algún criterio de búsqueda.')


        # Validación de puntuación (verifica si no es None)
        if descuento is not None and descuento < 0:
            self.add_error('descuento', 'El descuento debe ser mayor que 0.')
        
        if descuento is not None and descuento > 10:
            self.add_error('descuento', 'El descuento debe ser menor que 10.')
                
        if fecha_fin_inicio:
            if fecha_fin_inicio > fecha_fin_final:
                self.add_error('fecha_fin_inicio', 'La fecha de fin de inicio debe ser menor que la de final')

        if fecha_fin_final:
            if fecha_fin_final < fecha_fin_inicio:
                self.add_error('fecha_fin_final', 'La fecha de fin debe ser mayor que la de inicio')

        return self.cleaned_data