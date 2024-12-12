from django.db import models

# Create your models here.
class Usuario(models.Model):    
    nombre = models.CharField(max_length = 100)
    edad = models.IntegerField()

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length = 100)
    puede_tener_promociones = models.BooleanField()

    def __str__(self):
        return self.nombre
    
class Promocion(models.Model):
    nombre = models.CharField(max_length = 100)
    descripcion = models.TextField()
    producto = models.ForeignKey(Producto, on_delete = models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    descuento = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    
    def __str__(self):
        return self.nombre
