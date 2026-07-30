from django.urls import path
from . import views

app_name = 'providers'
urlpatterns = [
    path('lista-proveedores/', views.provider_list, name='provider_list'),
    path('proveedores/', views.provider_main, name='provider_main'),
    path('crear-proveedor/', views.provider_create, name='provider_create'),
    path("proveedor/<int:provider_entity_id>/",
         views.provider_detail, name="provider_detail"),
    path('guardar-documento/<int:provider_entity_id>/',
         views.provider_document_create, name='provider_document_create'),
    path('guardar-proveedor/<int:provider_entity_id>/',
         views.provider_save, name='provider_save'),
]
