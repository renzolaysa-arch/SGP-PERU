from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'inventory'
urlpatterns = [
    path('historial-archivos/<int:id_inventory>/', views.file_history, name='file_history'),
    path('historial-archivos/<int:id_inventory>/<int:id_version>/descargar/', views.file_version_download, name='file_version_download'),
    path('lista-registros/', views.inventory_list, name='inventory_list'),
    path('detalle-inventario/<int:id_inventory>', views.detail_inventory, name='detail_inventory'),
    path('view-sample-data/<int:id_inventory>', views.view_sample_data, name='view_sample_data'),
    path('sample-data/', views.sample_data, name = 'sample_data'),
    path('crear-registro-administrativo/', views.inventory_create, name= 'inventory_create'),
    path('seguir-inventario/<int:id_inventory>', views.inventory_follow, name='inventory_follow'),
    path('obtener-seguir-inventario/<int:id_inventory>', views.get_inventory_follow, name='get_demand_follow'),
    path('editar-inventario/<int:id>', views.edit_inventory, name='edit_inventory'),
    path('reply-comment/<int:id_inventory>/<int:id_comment>', views.reply_comment, name='reply_comment'),
    path('hijo-divipola/<int:id_divipola>', views.get_child_divipola, name='get_child_divipola'),
    path('test-calidad/<int:id_inventory>', views.quality_test, name='quality_test'),
    path('test-calidad/eliminar/<int:id_test>', views.quality_test_delete, name='quality_test_delete'),
]
