from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('crear/', views.create_provider, name='create_provider'),
    path('ingresar/', views.login_user, name='login'),
    path('recuperar-clave/', views.password_reset_request, name="reset_password"),
    path('recuperar-clave-enviar/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/reset_password/password_reset_done.html'
         ),  name="password_reset_done"),
    path('recuperar-clave/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/reset_password/password_reset_confirm.html'
         ), name="password_reset_confirm"),
    path('recuperar-clave_completado/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/reset_password/password_reset_complete.html'
         ), name="password_reset_complete"),
    path('registro/', views.register, name='register'),
    path('perfil/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('notificaciones/', views.notifications, name='notifications'),
    path('<int:id>/eliminar-notificacion',
         views.delete_notification, name='delete_notification'),
    path('ocultar-notificacion/<int:id_notification>/',
         views.hidden_notification, name='hidden_notification'),
    path('inventario/', views.inventory, name='inventory'),
    path('seguir-inventario/<int:id_inventory>',
         views.inventory_follow, name='inventory_follow'),
    path('listado-usuarios/', views.list_user, name='list_user'),
    path('tablero/', views.activity_board, name='activity_board'),
    path('actualizar/<str:group>/<int:id_user>/',
         views.update_provider, name='update_provider'),
    path('tablero-actividades/', views.activity_boards,
         name='activity_board_functionary'),
    path('mis-actividades/', views.activities, name='activities'),
    path('gestion-actividades/', views.activity_management,
         name='activities_management'),
    path('inventario-funcionario/', views.inventories, name='inventories'),
    path('solicitudes-funcionario/', views.demands_functionary,
         name='demands_functionary'),
    path('notificaciones-funcionario/', views.notification, name='notification'),
    path('logout', views.custom_logout, name='logout'),
    path('editar-perfil', views.edit_profile, name='edit_profile'),
    path('editar-contrasena', views.edit_password, name='edit_password'),
    path('crear-usuario', views.create_any_user, name='create_any_user'),
    path('crear-usuario/<int:user_id>/',
         views.create_user_group, name='create_user_group'),
    path('exportar/', views.download_user, name='export_users'),
    path('activate-token/<str:token>/', views.activate, name='activate'),
    path('acceso-rraa/', views.acceso_rra, name='acceso_rra'),
    path('eliminar-acceso-rraa/<int:access_id>/',
         views.delete_acceso_rra, name='delete_acceso_rra'),
    path('crear-acceso-rraa/', views.create_acceso_rra, name='create_acceso_rra'),
    path('transferencias/', views.transfers_all, name='transfers_all'),
    path('notificar-contactar-proveedor/<int:id_inventory>',
         views.notify_to_provider, name='notify_to_provider'),
    path('envio-token/<int:id_user>/', views.send_token, name='send_token'),
    path('evaluaciones/', views.evaluations, name='evaluations'),
    path('acceso-registros/', views.access_rra, name='access_rra'),
]
