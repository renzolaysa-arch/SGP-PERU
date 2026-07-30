from django.urls import path
from . import views
app_name = 'thread'
urlpatterns = [
    path('bitacora/', views.binacle, name='binacle'),
    path('bitacora/<int:id>', views.thread_comments, name='thread_comments'),
    path('bitacora/crear-comentario/<int:id_thread>/<int:id_functionary>', views.create_comments, name='create_comments'),
    path('bitacora/eliminar-comentario/<int:id_comment>/', views.delete_comment, name='delete_comment'),
    path('bitacora/crear-tema', views.create_thread, name='create_thread'),
    path('bitacora/eliminar-tema/<int:id_thread>/', views.delete_thread, name='delete_thread'),
]
