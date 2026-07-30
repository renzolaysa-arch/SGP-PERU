from django.urls import path
from . import views

app_name = 'contents'
urlpatterns = [
    path('', views.home, name='home'),
    path('glosario/', views.glosary, name='glosary'),
    path('glosario/<str:letter>', views.glosary_filter, name='glosary_filter'),
    path('preguntas-frecuentes/', views.frequent_questions,
         name='frequent_questions'),
    path('documento/<int:id_document>', views.document, name='document'),
    path('documento/crear-documento', views.newDocument, name='new_document'),
    path('eliminar-documento/<int:id_document>',
         views.deleteDocument, name='delete_document'),
    path('noticias/', views.new, name='news'),
    path('noticias/<int:id_new>', views.detail_new, name='new'),
    path('lista-noticias/', views.filter_search_new, name='new_filter'),
    path('contenido-academico/', views.academy_content, name='academy_content'),
    path('contenido-academico/<int:id_new>', views.detail_academy_content, name='academy_content_detail'),
    path('lista-contenido-academico/', views.filter_search_academy_content, name='academy_content_filter'),
    path('testimonios/', views.testimony, name='testimony'),
    path('testimonios/crear-testimonios', views.create_testimony, name='create_testimony'),
    path('404/', views.page_not_found, name='404'),
    path('menu-filtro-inventario/', views.return_filter_inventory, name='filter_menu_inventory'),
    path('menu-filtro-proveedor/', views.return_filter_provider, name='filter_menu_provider'),
]

#handler404 = 'page_not_found'
