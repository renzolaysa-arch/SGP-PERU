from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'projects'
urlpatterns = [

    #path('lista-proyectos/tags/<int:id_tag>', views.project_tags, name='project_tag'),
    
    path('proyecto/<int:id>', views.projects, name='project'),
    path('lista-proyectos/', views.list_projects, name='list_projects'),
    path('crear-proyecto/', views.create_project, name='create_project'),
    path('editar-proyecto/<int:id>', views.edit_project, name='edit_project'),
    path('<int:id>/eliminar-proyecto', views.delete_project, name='delete_project'),
    
]