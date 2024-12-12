from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('enlaces/', views.pagina_de_enlaces, name='pagina_de_enlaces'),
    path('buscar/', views.busqueda_avanzada, name='buscar'),
    #CEAR
    path('formulario/promocionFormulario', views.promocion_Form, name = 'promocionFormulario'),
    path('formulario/filtros-avanzados-promociones/', views.filtros_avanzados_promociones, name='filtros_avanzados_promociones'),
    path('formulario/promocion-modificar/<int:promocion_id>', views.promocion_modificar,name="promocion_modificar"),
    path('formulario/promocion-eliminar/<int:promocion_id>',views.eliminar_promocion,name='eliminar_promocion'),
]