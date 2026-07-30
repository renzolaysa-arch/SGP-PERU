from django.urls import path
from . import views

app_name = 'demand'
urlpatterns = [
    path('crear-solicitud/', views.demand_create, name='demand_create'),
    path('lista-solicitudes/', views.demand_list, name='demand_list'),
    path('solicitud/<int:id_demand>', views.demand_detail,
         name='demand_detail'),
    path('eliminar-nota/<int:id_demand>/<int:id_note>', views.delete_note,
         name='delete_note'),
    path('seguir-solicitud/<int:id_demand>',
         views.demand_follow, name='demand_follow'),
    path('obtener-seguir-solicitud/<int:id_demand>',
         views.get_demand_follow, name='get_demand_follow'),
    path('crear-solicitud/<int:id_inventory>/',
         views.demand_create_inventory, name='demand_create_inventory'),

    # reception
    path('solicitud/<int:id_demand>/recepcion/inicio/',
         views.process_reception, name='process_reception'),
    path('solicitud/<int:id_demand>/recepcion/proceso/',
         views.process_reception_process, name='process_reception_process'),
    path('solicitud/<int:id_demand>/recepcion/revision/',
         views.process_reception_revision, name='process_reception_revision'),
    path('solicitud/<int:id_demand>/recepcion/finalizado/',
         views.process_reception_finalize, name='process_reception_finalize'),

    # negotiation
    path('solicitud/<int:id_demand>/relacionamiento/inicio/',
         views.process_negotiation, name='process_negotiation'),
    path('solicitud/<int:id_demand>/relacionamiento/proceso/',
         views.process_negotiation_process,
         name='process_negotiation_process'),
    path('solicitud/<int:id_demand>/relacionamiento/revision/',
         views.process_negotiation_revision,
         name='process_negotiation_revision'),
    path('solicitud/<int:id_demand>/relacionamiento/finalizado/',
         views.process_negotiation_finalize,
         name='process_negotiation_finalize'),

    # transfer
    path('solicitud/<int:id_demand>/transferencia/inicio/',
         views.process_transfer, name='process_transfer'),
    path('solicitud/<int:id_demand>/transferencia/proceso/',
         views.process_transfer_process, name='process_transfer_process'),
    path('solicitud/<int:id_demand>/transferencia/revision/',
         views.process_transfer_revision, name='process_transfer_revision'),
    path('solicitud/<int:id_demand>/transferencia/finalizado/',
         views.process_transfer_finalize, name='process_transfer_finalize'),

    # preparation
    path('solicitud/<int:id_demand>/preparacion/inicio/',
         views.process_preparation, name='process_preparation'),
    path('solicitud/<int:id_demand>/preparacion/proceso/',
         views.process_preparation_process, name='process_preparation_process'),
    path('solicitud/<int:id_demand>/preparacion/revision/',
         views.process_preparation_revision, name='process_preparation_revision'),
    path('solicitud/<int:id_demand>/preparacion/finalizado/',
         views.process_preparation_finalize, name='process_preparation_finalize'),
    path('solicitud/<int:id_demand>/<int:id_process>/responder/<str:process>/',
         views.answer_cuestions, name='process_preparation_finalize'),

    # evaluation
    path('solicitud/<int:id_demand>/evaluacion/inicio/',
         views.process_evaluation, name='process_evaluation'),
    path('solicitud/<int:id_demand>/evaluacion/proceso/',
         views.process_evaluation_process, name='process_evaluation_process'),
    path('solicitud/<int:id_demand>/evaluacion/revision/',
         views.process_evaluation_revision, name='process_evaluation_revision'),
    path('solicitud/<int:id_demand>/evaluacion/finalizado/',
         views.process_evaluation_finalize, name='process_evaluation_finalize'),
    path('solicitud/<int:id_demand>/evaluacion/<int:id_evaluation>/responder/',
         views.answer_cuestions_evaluations, name='answer_cuestions_evaluations'),
]
