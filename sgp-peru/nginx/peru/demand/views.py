from django.shortcuts import redirect, render, get_object_or_404
from users.decorators import check_user
from users.models import Provider, Functionary, Unit_Central, User
from demand.models import (Demands, FollowDemand, Note, ProviderDemand, Reception,
                           Transfer, Negotiation, Transfers, Preparation, Preparations, DocumentDefinitionObjetives, Channels,
                           ParticipationDemand, Evaluation, Evaluations)
from providers.models import ProviderEntity
from inventory.models import Inventory
from django.contrib.sites.shortcuts import get_current_site
from demand.filters import DemandsFilter
from demand.forms import (FilterOrderForm, CreateDemandForm, NoteDemandForm,
                          ReceptionForm, DocumentForm, TransfersForm, NegotiationForm,
                          TransfersQuestionsForm, PreparationForm, PreparationRevisionForm, EvaluationsForm)
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import datetime, timezone
from notifications.models import Notification
from django.utils.dateparse import parse_datetime
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from .functions import calculate_process_board
import re


class demand_list_custom:
    def __init__(self, id, name_demand, provider, created_date, status, key_words, inventory, checked, type):
        self.id = id
        self.name_demand = name_demand
        self.provider = provider
        self.created_date = created_date
        self.status = status
        self.key_words = key_words
        self.inventory = inventory
        self.checked = checked
        self.type = type


@check_user(['Unidad Central', 'Funcionario'], 'login')
def demand_list(request):
    order_by = request.GET.get("order")
    user_id = request.user.id
    if order_by:
        queryset = Demands.on_site.filter().order_by(order_by)
    else:
        queryset = Demands.on_site.filter().order_by('-created_date')

    filter_demand = DemandsFilter(
        request.GET,
        queryset=queryset
    )
    form_order_by = FilterOrderForm()

    page_cant = 6
    paginated_filter_demand = Paginator(filter_demand.qs, page_cant)
    page_number = request.GET.get("page")
    if page_number is None:
        page_number = 1
    demand_page_obj = paginated_filter_demand.get_page(page_number)
    demand_total = paginated_filter_demand.count
    page = paginated_filter_demand.page(page_number).object_list
    demand_page = ((int(page_number)-1) * page_cant) + len(page)

    list_custom = []
    checked = True
    for item in demand_page_obj:
        if FollowDemand.on_site.filter(user=user_id, demand=item.id):
            checked = True
        else:
            checked = False
        list_custom.append(demand_list_custom(
            item.id, item.title, item.provider_entity, item.created_date, item.status, item.key_words, item.inventory, checked, item.type))
    paginated_filter_demand = Paginator(list_custom, page_cant)
    demand_custom = paginated_filter_demand.get_page(page_number)

    return render(
        request,
        'demand/demand_list.html',
        {
            'filter': filter_demand,
            'demand_custom': demand_custom,
            'demand_page_obj': demand_page_obj,
            'demand_total': demand_total,
            'demand_page': str(demand_page),
            'form_order_by': form_order_by,
        }
    )


@check_user(['Funcionario'], 'login')
def demand_create(request):
    if request.method == "GET":
        try:
            functionary = Functionary.on_site.get(user=request.user.id)
        except Functionary.DoesNotExist:
            functionary = None
        form_create_demands = CreateDemandForm(
            initial={'inventory': None, 'functionary': functionary})
        return render(
            request,
            'demand/demand_create.html',
            {
                'form_create_demand': form_create_demands,
            }
        )
    else:
        # capturar el id del usuario que esta logueado
        if request.user.groups.filter(name='Funcionario').exists():
            user_id = request.user.id
        form = CreateDemandForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                id_form = form.instance.id
                inventory_id = int(request.POST['inventory'])
                rraa = Inventory.on_site.get(pk=inventory_id)
                owner_rraa = Provider.on_site.filter(
                    entity_provider=rraa.entity_provider)
                demand = Demands.on_site.get(pk=id_form)
                functionary = Functionary.on_site.get(user=request.user.id)
                                
                if rraa.custody is False:
                    Reception.on_site.create(
                        demand=demand,
                        demand_process='ini'
                    )
                    ParticipationDemand.on_site.create(
                        user=functionary.user,
                        demand=demand
                    )
                    demand.type = 'ex'
                    demand.save()
                else:
                    demand.type = 'in'
                    demand.save()
                
                # Notificación
                url = settings.SITE_URL
                data_user_unit = Unit_Central.on_site.all()
                notifications = {user_id}
                for item in data_user_unit:
                    notifications.add(item.user.id)

                for item in owner_rraa:
                    notifications.add(item.user.id)
                try:
                    for notify in notifications:
                        name = "Se agregó una nueva Solicitud al registro "+rraa.title + ", consultar <a target='_blank' href='" + \
                            url+"solicitud/" + \
                            str(id_form) + "'>aquí</a>"
                        message = "Se agregó una nueva Solicitud: " + \
                            request.POST['title']

                        Notification.on_site.create(
                            name=name,
                            sent_to=get_object_or_404(
                                User, pk=notify),
                            module_from="SO",
                            message=message,
                            name_link='Consultar la solicitud',
                            link=url+"solicitud/" + str(id_form)
                        )
                except:
                    return render(request, 'demand/demand_create.html', {'form': form})
            except:
                return render(request, 'demand/demand_create.html', {'form': form})
           
        else:
            form = CreateDemandForm(request.POST)
            return render(request, 'demand/demand_create.html', {'form': form})
    return redirect('demand:demand_list')


@check_user(['Funcionario'], 'login')
def demand_create_inventory(request, id_inventory):
    if request.method == "GET":
        try:
            functionary = Functionary.on_site.get(user=request.user.id)
        except Functionary.DoesNotExist:
            functionary = None
        inventory = Inventory.on_site.get(pk=id_inventory)
        form_create_demands = CreateDemandForm(
            initial={'inventory': inventory, 'functionary': functionary})
        return render(
            request,
            'demand/demand_create.html',
            {
                'form_create_demand': form_create_demands,
            }
        )
    else:
        # capturar el id del usuario que esta logueado
        if request.user.groups.filter(name='Funcionario').exists():
            user_id = request.user.id
        form = CreateDemandForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                id_form = form.instance.id
                inventory_id = int(request.POST['inventory'])
                rraa = Inventory.on_site.get(pk=inventory_id)
                owner_rraa = Provider.on_site.filter(
                    entity_provider=rraa.entity_provider)
                demand = Demands.on_site.get(pk=id_form)
                functionary = Functionary.on_site.get(user=request.user.id)
                                
                if rraa.custody is False:
                    Reception.on_site.create(
                        demand=demand,
                        demand_process='ini'
                    )
                    ParticipationDemand.on_site.create(
                        user=functionary.user,
                        demand=demand
                    )
                    demand.type = 'ex'
                    demand.save()
                else:
                    demand.type = 'in'
                    demand.save()
                
                # Notificación
                url = settings.SITE_URL
                data_user_unit = Unit_Central.on_site.all()
                notifications = {user_id}
                for item in data_user_unit:
                    notifications.add(item.user.id)

                for item in owner_rraa:
                    notifications.add(item.user.id)
                try:
                    for notify in notifications:
                        name = "Se agregó una nueva Solicitud al registro "+rraa.title + ", consultar <a target='_blank' href='" + \
                            url+"solicitud/" + \
                            str(id_form) + "'>aquí</a>"
                        message = "Se agregó una nueva Solicitud: " + \
                            request.POST['title']

                        Notification.on_site.create(
                            name=name,
                            sent_to=get_object_or_404(
                                User, pk=notify),
                            module_from="SO",
                            message=message,
                            name_link='Consultar la solicitud',
                            link=url+"solicitud/" + str(id_form)
                        )
                except:
                    return render(request, 'demand/demand_create.html', {'form': form})
            except:
                return render(request, 'demand/demand_create.html', {'form': form})
        else:
            form = CreateDemandForm(request.POST)
            return render(request, 'demand/demand_create.html', {'form': form})
    return redirect('demand:demand_list')


class notes_demand:
    def __init__(self, id, first_name, last_name, created_date, commentary, owner_comment):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.created_date = created_date
        self.commentary = commentary
        self.owner_comment = owner_comment


@check_user(['Unidad Central', 'Proveedor', 'Funcionario'], 'login')
def demand_detail(request, id_demand):
    if request.method == 'GET':
        owner_comment = False
        list = []
        demands = get_object_or_404(Demands, pk=id_demand)
        notes = Note.objects.filter(demand__id=demands.id)
        form_note = NoteDemandForm()
        key_words = demands.key_words

        for note in notes:
            owner_comment = False
            if note.functionary.user.id == request.user.id:
                owner_comment = True

            list.append(notes_demand(note.id, note.functionary.user.first_name,
                        note.functionary.user.last_name, note.created_date, note.commentary, owner_comment))

        if demands.type == "ex":
            # Process
            board = calculate_process_board(id_demand)

            return render(request, 'demand/demand_detail.html', {
                "demand": demands,
                "key_words": key_words,
                "notes": list,
                "form_note": form_note,
                "process_board": board,
            })
        else:
            return render(request, 'demand/demand_detail.html', {
                "demand": demands,
                "key_words": key_words,
                "notes": list,
                "form_note": form_note,
                "process_board": None,
            })
    else:
        data_user = ""
        if request.user.groups.filter(name='Funcionario').exists():
            user_id = request.user.id
            data_user = Functionary.objects.get(user=user_id)
            Note.objects.create(
                demand=get_object_or_404(Demands, pk=id_demand),
                commentary=request.POST['commentary'],
                functionary=data_user
            )
        return redirect('/solicitud/' + str(id_demand))


@check_user(['Funcionario'], 'login')
def delete_note(request, id_demand, id_note):
    note = Note.on_site.filter(pk=id_note).first()
    if request.method == "POST":
        note.delete()
        # return HttpResponseRedirect("/")
        return redirect('/solicitud/' + str(id_demand))
    return redirect('/solicitud/' + str(id_demand))


@check_user(['Funcionario'], 'login')
def demand_follow(request, id_demand):
    if request.user.is_authenticated:
        try:
            demand = Demands.objects.get(pk=id_demand)
        except Demands.DoesNotExist:
            demand = None

        try:
            if demand is not None:
                follow = FollowDemand.objects.get(
                    user=request.user, demand=demand)
            else:
                follow = None
        except FollowDemand.DoesNotExist:
            follow = None
        try:
            if follow is not None:
                follow.delete()
            else:
                q = FollowDemand(
                    user=request.user,
                    demand=demand,
                )
                q.save()

                url = settings.SITE_URL
                notifications = {}
                if request.user.id == demand.functionary.user.id:
                    notifications = {request.user.id}
                else:
                    notifications = {request.user.id}
                    notifications.add(demand.functionary.user.id)
                try:
                    for notify in notifications:
                        name = "Se está siguiendo la solicitud :" + demand.title + ", de la cual es propietario, consultar <a target='_blank' href='" + \
                            url+"solicitud/" + \
                            str(id_demand) + "'>aquí</a>"
                        message = "Se está siguiendo la solicitud" + demand.title

                        Notification.on_site.create(
                            name=name,
                            sent_to=get_object_or_404(
                                User, pk=notify),
                            module_from="SO",
                            message=message,
                            name_link='Se está siguiendo la solicitud',
                            link=url+"solicitud/" + str(id_demand)
                        )
                except:
                    return JsonResponse({'fail': 'True'})
            return JsonResponse({'success': 'True'})
        except:
            return JsonResponse({'fail': 'True'})


@check_user(['Funcionario'], 'login')
def get_demand_follow(request, id_demand):
    if request.user.is_authenticated:
        try:
            demand = Demands.objects.get(pk=id_demand)
        except Demands.DoesNotExist:
            demand = None

        try:
            if demand is not None:
                follow = FollowDemand.objects.get(
                    user=request.user, demand=demand)
            else:
                follow = None
        except FollowDemand.DoesNotExist:
            follow = None

        if follow is not None:
            return JsonResponse({'follow': 'True'})
        else:
            return JsonResponse({'follow': 'False'})


# reception
@check_user(['Unidad Central'], 'login')
def process_reception(request, id_demand):
    demand = get_object_or_404(Demands, pk=id_demand)
    reception = Reception.on_site.get(demand=id_demand)
    process = reception.demand_process
    participations = ParticipationDemand.on_site.filter(demand=demand)
    rollback = True if 'regresar' in request.GET else False
    if request.method == "GET":
        if process == 'ini' or rollback == True:
            return render(request, 'demand/box_results_reception.html', {
                'demand': demand,
                'process': process,
                'participations': participations,
                'rollback': rollback,
            })
        elif process == 'pr':
            return redirect('demand:process_reception_process', id_demand)
        elif process == 're':
            return redirect('demand:process_reception_revision', id_demand)
        elif process == 'fi':
            return redirect('demand:process_reception_finalize', id_demand)

    else:
        if demand.process == 're' and process == 'ini':
            reception.demand_process = 'pr'
            reception.demand_subprocess = 'demand-validation'
            demand.process = 're'
            demand.save()
            reception.save()
        if rollback == True:
            return redirect('/solicitud/' + str(id_demand) + '/recepcion/proceso/?regresar=true')
        else:
            return redirect('demand:process_reception_process', id_demand)


@check_user(['Unidad Central'], 'login')
def process_reception_process(request, id_demand):
    demand = get_object_or_404(Demands, pk=id_demand)
    reception = Reception.on_site.get(demand=id_demand)
    process = reception.demand_process
    sub_process = reception.demand_subprocess
    rollback = True if 'regresar' in request.GET else False
    if process != 'pr' and rollback == False:
        return redirect('demand:process_reception', id_demand)
    documents_committee = reception.doc_verification_completeness.all()
    documents_presentation = reception.doc_committee_presentation.all()
    participations = ParticipationDemand.on_site.filter(demand=demand)

    form = ReceptionForm(initial={
        'status_demand_validation': reception.status_demand_validation,
        'demand_assessment': reception.demand_assessment,
        'status_demand_notification': reception.status_demand_notification,
        'date_tentative_presentation': reception.date_tentative_presentation,
        'comment': reception.comment,
    })

    if request.method == "GET":
        form_document = DocumentForm()
        return render(request, 'demand/box_results_reception.html', {
            'demand': demand,
            'reception': reception,
            'process': process,
            'sub_process': sub_process,
            'form': form,
            'form_document': form_document,
            'documents_committee': documents_committee if documents_committee else '',
            'documents_presentation': documents_presentation if documents_presentation else '',
            'participations': participations,
            'rollback': rollback,
        })
    else:
        if demand.process == 're' and process == 'pr':
            if sub_process == 'demand-validation':
                form = ReceptionForm(request.POST, instance=reception)
                if form.is_valid():
                    form.save()
                    status = form.cleaned_data.get('status_demand_validation')
                    if status == 'do':
                        reception.demand_subprocess = 'verification-completeness'
                        reception.date_demand_validation = datetime.today()
                        reception.save()

            elif sub_process == 'verification-completeness':
                new_request = request.POST.copy()
                new_request['status_demand_validation'] = reception.status_demand_validation
                form = ReceptionForm(new_request, instance=reception)
                form_document = DocumentForm(request.POST, request.FILES)
                if 'document' in request.POST:
                    if form_document.is_valid():
                        document = form_document.save()
                        reception.doc_verification_completeness.add(document)
                        reception.save()
                        if document:
                            users_list = []
                            users_list.append(
                                form_document.cleaned_data.get('assigned_to'))
                            all_copy_to = form_document.cleaned_data.get('copy_to')
                            s = [int(s) for s in re.findall(r'-?\d+\.?\d*', all_copy_to)]

                            for copy_to in s:
                                users_list.append(copy_to)
                            create_participation(users_list, demand)
                    else:
                        form_document.errors
                else:
                    if form.is_valid():
                        form.save()
                        reception.demand_subprocess = 'demand-notification'
                        reception.date_verification_completeness = datetime.today()
                        reception.save()

            elif sub_process == 'demand-notification':
                new_request = request.POST.copy()
                new_request['status_demand_validation'] = reception.status_demand_validation
                new_request['demand_assessment'] = reception.demand_assessment
                form = ReceptionForm(new_request, instance=reception)
                if form.is_valid():
                    form.save()
                    if form.cleaned_data.get('status_demand_notification'):
                        url = settings.SITE_URL
                        name = 'La recepción de la solicitud: "' + demand.title + '", fue aprobada, consultar <a target="_blank" href="' + \
                            url+'solicitud/' + \
                            str(demand.id) + '">aquí</a>'
                        message = 'La recepción de la solicitud: "' + demand.title + '", fue aprobada'
                        Notification.on_site.create(
                            name=name,
                            sent_to=demand.functionary.user,
                            module_from='SO',
                            message=message,
                            name_link='Consultar solicitud',
                            link=url+"solicitud/" + str(demand.id)
                        )
                    reception.demand_subprocess = 'technical-committee-presentation'
                    reception.date_demand_notification = datetime.today()
                    reception.save()

            elif sub_process == 'technical-committee-presentation':
                form_document = DocumentForm(request.POST, request.FILES)
                if 'document' in request.POST:
                    if form_document.is_valid():
                        document = form_document.save()
                        reception.doc_committee_presentation.add(document)
                        reception.save()
                        if document:
                            users_list = []
                            users_list.append(
                                form_document.cleaned_data.get('assigned_to'))
                            all_copy_to = form_document.cleaned_data.get('copy_to')
                            s = [int(s) for s in re.findall(r'-?\d+\.?\d*', all_copy_to)]

                            for copy_to in s:
                                users_list.append(copy_to)
                            create_participation(users_list, demand)
                else:
                    reception.demand_process = 're'
                    reception.save()
                    return redirect('demand:process_reception_revision', id_demand)

            return redirect('demand:process_reception_process', id_demand)
        elif rollback == True:
            return redirect('/solicitud/' + str(id_demand) + '/recepcion/revision/?regresar=true')


@check_user(['Unidad Central'], 'login')
def process_reception_revision(request, id_demand):
    demand = get_object_or_404(Demands, pk=id_demand)
    reception = Reception.on_site.get(demand=id_demand)
    process = reception.demand_process
    participations = ParticipationDemand.on_site.filter(demand=demand)
    form = ReceptionForm(initial={
        'status_demand_validation': reception.status_demand_validation,
        'comment_revision': reception.comment_revision,
    })
    rollback = True if 'regresar' in request.GET else False
    if process != 're' and rollback == False:
        return redirect('demand:process_reception', id_demand)

    if request.method == "GET":
        return render(request, 'demand/box_results_reception.html', {
            'demand': demand,
            'reception': reception,
            'process': process,
            'form': form,
            'participations': participations,
            'rollback': rollback,
        })
    else:
        if demand.process == 're' and process == 're':
            new_request = request.POST.copy()
            new_request['status_demand_validation'] = reception.status_demand_validation
            new_request['demand_assessment'] = reception.demand_assessment
            new_request['status_demand_notification'] = reception.status_demand_notification
            new_request['date_tentative_presentation'] = reception.date_tentative_presentation
            new_request['comment'] = reception.comment
            form = ReceptionForm(new_request, instance=reception)
            if form.is_valid():
                form.save()
                reception.date_demand_revision = datetime.now(timezone.utc)
                reception.date_demand_finalized = datetime.now(timezone.utc)
                end_time = reception.date_demand_finalized - reception.created_date
                #reception.time_demand_finalized = str(end_time)
                reception.demand_process = 'fi'
                reception.save()
        elif rollback == True:
            return redirect('/solicitud/' + str(id_demand) + '/recepcion/finalizado/?regresar=true')
        return redirect('demand:process_reception_revision', id_demand)


@check_user(['Unidad Central'], 'login')
def process_reception_finalize(request, id_demand):
    demand = get_object_or_404(Demands, pk=id_demand)
    reception = Reception.on_site.get(demand=id_demand)
    process = reception.demand_process
    participations = ParticipationDemand.on_site.filter(demand=demand)
    form = ReceptionForm(initial={
        'status_demand_validation': reception.status_demand_validation,
        'comment_finalized': reception.comment_finalized,
    })
    rollback = True if 'regresar' in request.GET else False
    if process != 'fi' and rollback == False:
        return redirect('demand:process_reception', id_demand)

    if request.method == "GET":
        return render(request, 'demand/box_results_reception.html', {
            'demand': demand,
            'reception': reception,
            'process': process,
            'form': form,
            'participations': participations,
            'rollback': rollback,
        })
    else:
        if demand.process == 're' and process == 'fi':
            new_request = request.POST.copy()
            new_request['status_demand_validation'] = reception.status_demand_validation
            new_request['demand_assessment'] = reception.demand_assessment
            new_request['status_demand_notification'] = reception.status_demand_notification
            new_request['date_tentative_presentation'] = reception.date_tentative_presentation
            new_request['comment'] = reception.comment
            new_request['comment_revision'] = reception.comment_revision
            form = ReceptionForm(new_request, instance=reception)
            if form.is_valid():
                form.save()
                demand.process = 'ne'
                demand.save()
                Negotiation.on_site.create(
                    demand=demand,
                )

        elif rollback == True:
            return redirect('/solicitud/' + str(id_demand) + '/relacionamiento/inicio/?regresar=true')

        return redirect('demand:process_negotiation', id_demand)
# end reception


# negotiation
@check_user(['Unidad Central'], 'login')
def process_negotiation(request, id_demand):
    demand = get_object_or_404(Demands, pk=id_demand)
    negotiation = Negotiation.on_site.get(demand=id_demand)
    process = negotiation.demand_process
    all_provider = ProviderEntity.on_site.all()
    selected_providers = ProviderDemand.on_site.filter(negotiation=negotiation)
    process_transfer = ""
    participations = ParticipationDemand.on_site.filter(demand=demand)
    rollback = True if 'regresar' in request.GET else False

    for selected_provider in selected_providers:
        process_transfer = process_transfer + \
            selected_provider.provider_entity.name + ','

    if request.method == "GET":
        if process == 'ini' or rollback == True:
            return render(request, 'demand/demand_relation.html', {
                'demand': demand,
                'process': process,
                'all_provider': all_provider,
                'selected_providers': process_transfer,
                'selected_providers_init': selected_providers,
                'participations': participations,
                'negotiation': negotiation,
                'rollback': rollback,
            })
        elif process == 'pr':
            return redirect('demand:process_negotiation_process', id_demand)
        elif process == 're':
            return redirect('demand:process_negotiation_revision', id_demand)
        else:
            return redirect('demand:process_negotiation_finalize', id_demand)

    else:
        if demand.process == 'ne' and process == 'ini':
            if not selected_providers:
                providers = request.POST["multilist"].split(',')
                for provider in providers:
                    provider_entity = ProviderEntity.on_site.get(name=provider)
                    ProviderDemand.objects.create(
                        negotiation=negotiation,
                        provider_entity=provider_entity,
                    ).save()
                    if provider_entity:
                        provider_participation = Provider.on_site.filter(
                            entity_provider=provider_entity)
                        users_list = []
                        for provider_item in provider_participation:
                            users_list.append(provider_item.user.id)
                        create_participation(users_list, demand)
            negotiation.demand_process = 'pr'
            negotiation.demand_subprocess = 'demand-validation'
            negotiation.save()
        elif rollback == True:
            return redirect('/solicitud/' + str(id_demand) + '/relacionamiento/proceso/?regresar=true')

        return redirect('demand:process_negotiation', id_demand)


@check_user(['Unidad Central'], 'login')
def process_negotiation_process(request, id_demand):
    demand = get_object_or_404(Demands, pk=id_demand)
    pre_provider = demand.provider_entity
    negotiation = Negotiation.on_site.get(demand=id_demand)
    process = negotiation.demand_process
    sub_process = negotiation.demand_subprocess
    all_provider = ProviderEntity.on_site.all()
    selected_providers = ProviderDemand.on_site.filter(
        negotiation=negotiation)
    form_document = DocumentForm()
    documents_validation = negotiation.doc_demand_validation.all()
    documents_definition = negotiation.doc_definition_objetives.all()
    documents_agreement = negotiation.doc_structuring_agreement.all()
    example_document = DocumentDefinitionObjetives.on_site.filter()
    if example_document:
        example_document = example_document.first()
    else:
        example_document = ''

    channels = Channels.objects.all()
    participations = ParticipationDemand.on_site.filter(demand=demand)

    rollback = True if 'regresar' in request.GET else False
    if process != 'pr' and rollback == False:
        return redirect('demand:process_negotiation', id_demand)

    if request.method == "GET":
        date_current = datetime.now()
        return render(request, 'demand/demand_relation.html', {
            'demand': demand,
            'process': process,
            'all_provider': all_provider,
            'negotiation': negotiation,
            'selected_providers': selected_providers,
            'form_document': form_document,
            'documents_validation': documents_validation,
            'sub_process': sub_process,
            'pre_provider': pre_provider,
            'documents_definition': documents_definition,
            'documents_agreement': documents_agreement,
            'example_document': example_document,
            'channels': channels,
            'participations': participations,
            'rollback': rollback,
            'date_curent': date_current,
        })

    else:
        if demand.process == 'ne' and process == 'pr':
            form_document = DocumentForm(request.POST, request.FILES)
            if sub_process == 'demand-validation':
                if 'document' in request.POST:
                    if form_document.is_valid():
                        document = form_document.save()
                        negotiation.doc_demand_validation.add(document)
                        negotiation.save()
                        if document:
                            users_list = []
                            users_list.append(
                                form_document.cleaned_data.get('assigned_to'))
                            all_copy_to = form_document.cleaned_data.get('copy_to')
                            s = [int(s) for s in re.findall(r'-?\d+\.?\d*', all_copy_to)]

                            for copy_to in s:
                                users_list.append(copy_to)
                            create_participation(users_list, demand)
                    else:
                        form_document.errors
                else:
                    for selected_provider in selected_providers:
                        state_demand = request.POST.get(
                            'state-demand-' + str(selected_provider.id))
                        status_record = request.POST.get(
                            'state-reception-' + str(selected_provider.id))
                        selected_provider.status_demand = state_demand
                        selected_provider.status_record = status_record
                        selected_provider.save()
                        negotiation.demand_subprocess = 'provider-confirmation'
                        negotiation.date_demand_validation = datetime.today()
                        negotiation.save()

            elif sub_process == "provider-confirmation":
                select_provider = request.POST.get('selected-agreement')
                entity_provider = ProviderEntity.on_site.get(
                    pk=int(select_provider))
                demand.provider_entity = entity_provider
                demand.save()
                new_sub_process = 'definition-objetives-and-scope'
                negotiation.demand_subprocess = new_sub_process
                negotiation.date_demand_confirmation = datetime.today()
                negotiation.save()

            elif sub_process == 'definition-objetives-and-scope':
                if 'document' in request.POST:
                    if form_document.is_valid():
                        document = form_document.save()
                        negotiation.doc_definition_objetives.add(document)
                        negotiation.save()
                        if document:
                            users_list = []
                            users_list.append(
                                form_document.cleaned_data.get('assigned_to'))
                            all_copy_to = form_document.cleaned_data.get('copy_to')
                            s = [int(s) for s in re.findall(r'-?\d+\.?\d*', all_copy_to)]

                            for copy_to in s:
                                users_list.append(copy_to)
                            create_participation(users_list, demand)
                    else:
                        form_document.errors
                else:
                    new_sub_process = 'scope-validation'
                    negotiation.demand_subprocess = new_sub_process
                    negotiation.date_definition_objetives = datetime.today()
                    negotiation.save()

            elif sub_process == 'scope-validation':
                status = request.POST['status_demand_negotiation']
                negotiation.status_demand_negotiation = status
                new_sub_process = 'structuring-of-the-agreement'
                negotiation.demand_subprocess = new_sub_process
                negotiation.date_scope_validate = datetime.today()
                negotiation.save()

                if status == 'do':
                    user_providers = Provider.on_site.filter(
                        entity_provider=demand.provider_entity)
                    url = settings.SITE_URL

                    for user_provider in user_providers:
                        name = 'La negociación de la solicitud: "' + demand.title + '", fue aprobada, consultar <a target="_blank" href="' + \
                            url+'solicitud/' + \
                            str(demand.id) + '">aquí</a>'
                        message = 'La negociación de la solicitud: "' + demand.title + '", fue aprobada'
                        Notification.on_site.create(
                            name=name,
                            sent_to=user_provider.user,
                            module_from='SO',
                            message=message,
                            name_link='Consultar solicitud',
                            link=url+"solicitud/" + str(demand.id)
                        )

            elif sub_process == 'structuring-of-the-agreement':
                if 'document' in request.POST:
                    if form_document.is_valid():
                        document = form_document.save()
                        negotiation.doc_structuring_agreement.add(document)
                        negotiation.save()
                        if document:
                            users_list = []
                            users_list.append(
                                form_document.cleaned_data.get('assigned_to'))
                            all_copy_to = form_document.cleaned_data.get('copy_to')
                            s = [int(s) for s in re.findall(r'-?\d+\.?\d*', all_copy_to)]

                            for copy_to in s:
                                users_list.append(copy_to)
                            create_participation(users_list, demand)
                    else:
                        form_document.errors
                else:
                    chanel = Channels.objects.filter(
                        pk=request.POST.get("channel", False))
                    if chanel:
                        negotiation.channel = chanel.first()
                    negotiation.demand_process = 're'
                    negotiation.date_structuring_agreement = datetime.today()
                    negotiation.date_agreed = request.POST["date_agreed"]
                    negotiation.time = request.POST["time"]
                    negotiation.type_time = 'days'
                    negotiation.date_agreement = request.POST["date_agreement"]
                    negotiation.consideration = request.POST["consideration"]
                    negotiation.save()
                    return redirect('demand:process_negotiation_revision', id_demand)
        elif rollback == True:
            return redirect('/solicitud/' + str(id_demand) + '/relacionamiento/revision/?regresar=true')
        return redirect('demand:process_negotiation', id_demand)


@check_user(['Unidad Central'], 'login')
def process_negotiation_revision(request, id_demand):
    demand = get_object_or_404(Demands, pk=id_demand)
    negotiation = Negotiation.on_site.get(demand=id_demand)
    process = negotiation.demand_process
    form_document = DocumentForm()
    doc_revision = negotiation.doc_revision.all()
    participations = ParticipationDemand.on_site.filter(demand=demand)
    form = NegotiationForm(initial={
        'meets_expectations': negotiation.meets_expectations,
        'required_documentation': negotiation.required_documentation,
        'ready_sign': negotiation.ready_sign,
    })

    rollback = True if 'regresar' in request.GET else False
    if process != 're' and rollback == False:
        return redirect('demand:process_negotiation', id_demand)

    if request.method == "GET":
        return render(request, 'demand/demand_relation.html', {
            'demand': demand,
            'negotiation': negotiation,
            'process': process,
            'form_document': form_document,
            'doc_revision': doc_revision,
            'form': form,
            'participations': participations,
            'rollback': rollback,
        })

    else:
        if demand.process == 'ne' and process == 're':
            form_document = DocumentForm(request.POST, request.FILES)
            if 'document' in request.POST:
                if form_document.is_valid():
                    document = form_document.save()
                    negotiation.doc_revision.add(document)
                    negotiation.save()
                    if document:
                        users_list = []
                        users_list.append(
                            form_document.cleaned_data.get('assigned_to'))
                        all_copy_to = form_document.cleaned_data.get('copy_to')
                        s = [int(s) for s in re.findall(r'-?\d+\.?\d*', all_copy_to)]

                        for copy_to in s:
                            users_list.append(copy_to)
                        create_participation(users_list, demand)
                else:
                    form_document.errors

            else:
                form = NegotiationForm(request.POST, instance=negotiation)
                if form.is_valid():
                    form.save()
                else:
                    form.errors
                negotiation.date_revision = datetime.now(timezone.utc)
                negotiation.date_finalize = datetime.now(timezone.utc)
                end_time = negotiation.date_finalize - negotiation.created_date
                negotiation.time_demand_finalized = end_time
                negotiation.demand_process = 'fi'
                negotiation.save()
        elif rollback == True:
            return redirect('/solicitud/' + str(id_demand) + '/relacionamiento/finalizado/?regresar=true')
        return redirect('demand:process_negotiation_revision', id_demand)


@check_user(['Unidad Central'], 'login')
def process_negotiation_finalize(request, id_demand):
    demand = get_object_or_404(Demands, pk=id_demand)
    negotiation = Negotiation.on_site.get(demand=id_demand)
    process = negotiation.demand_process
    participations = ParticipationDemand.on_site.filter(demand=demand)
    rollback = True if 'regresar' in request.GET else False
    if process != 'fi' and rollback == False:
        return redirect('demand:process_negotiation', id_demand)

    if request.method == "GET":
        return render(request, 'demand/demand_relation.html', {
            'demand': demand,
            'negotiation': negotiation,
            'process': process,
            'participations': participations,
            'rollback': rollback,
        })

    else:
        if demand.process == 'ne' and process == 'fi':
            negotiation.comment_finalized = request.POST["comment_finalized"]
            negotiation.save()
            demand.process = 'tr'
            demand.save()
            Transfer.on_site.create(
                demand=demand,
            )
            return redirect('demand:process_transfer', id_demand)
        elif rollback == True:
            return redirect('/solicitud/' + str(id_demand) + '/transferencia/inicio/?regresar=true')

        return redirect('demand:process_transfer', id_demand)
# end negotiation


# transfer
@check_user(['Unidad Central'], 'login')
def process_transfer(request, id_demand):
    demand = get_object_or_404(Demands, pk=id_demand)
    transfer = Transfer.on_site.get(demand=id_demand)
    transfers = Transfers.on_site.filter(transfer=transfer)
    negotiation = Negotiation.on_site.get(demand=id_demand)
    process = transfer.demand_process
    participations = ParticipationDemand.on_site.filter(demand=demand)
    list_frequency = calculate_frequency_delivery(
        id_demand, negotiation.date_agreed, negotiation.date_agreement, negotiation.time, negotiation.type_time)
    form = TransfersForm(initial={
        'transfer': transfer,
        'frequency_delivery': list_frequency
    })

    transfer.demand_process = 'ini'
    transfer.save()

    if request.method == "GET":
        return render(request, 'demand/demand_transfer.html', {
            'demand': demand,
            'process': process,
            'negotiation': negotiation,
            'form': form,
            'transfers': transfers,
            'participations': participations,
        })

    else:
        if "transfer" in request.POST and request.POST["comment"]:
            if int(request.POST["transfer"]) == transfer.id:
                transfer = Transfer.on_site.get(pk=request.POST['transfer'])
                channel = Channels.objects.get(pk=request.POST['channel'])
                status_transfer = request.POST['status_transfer']
                number_deliveries = request.POST['number_deliveries']
                date_delivery = request.POST['date_delivery']
                frequency = request.POST['frequency_delivery'].split("@")
                frequency_delivery = int(frequency[0])
                frequency_date_delivery = datetime.strptime(
                    frequency[1], '%Y-%m-%d').date()
                comment = request.POST['comment']
                q = Transfers(
                    transfer=transfer,
                    channel=channel,
                    status_transfer=status_transfer,
                    number_deliveries=number_deliveries,
                    date_delivery=date_delivery,
                    frequency_delivery=frequency_delivery,
                    frequency_date_delivery=frequency_date_delivery,
                    comment=comment,
                )
                q.save()
                demand.inventory.custody = True
                demand.inventory.save()
                return redirect('demand:process_transfer', id_demand)
        else:
            if demand.process == 'tr' and process == 'ini':
                transfer.demand_process = 'pr'
                transfer.save()

        return redirect('demand:process_transfer_process', id_demand)


@check_user(['Unidad Central'], 'login')
def process_transfer_process(request, id_demand):
    demand = get_object_or_404(Demands, pk=id_demand)
    transfer = Transfer.on_site.get(demand=id_demand)
    process = transfer.demand_process
    negotiation = Negotiation.on_site.get(demand=id_demand)
    transfers = Transfers.on_site.filter(transfer=transfer)
    filter = request.GET.get('month')
    participations = ParticipationDemand.on_site.filter(demand=demand)

    transfer.demand_process = 'pr'
    transfer.save()

    if filter is not None:
        transfers = Transfers.on_site.filter(
            transfer=transfer, date_delivery__month=filter)

    if request.method == "GET":
        return render(request, 'demand/demand_transfer.html', {
            'demand': demand,
            'process': process,
            'negotiation': negotiation,
            'transfers': transfers,
            'participations': participations,
        })
    else:
        if demand.process == 'tr' and process == 'pr':
            transfer.demand_process = 're'
            transfer.save()

        return redirect('demand:process_transfer_revision', id_demand)


@check_user(['Unidad Central'], 'login')
def process_transfer_revision(request, id_demand):
    demand = get_object_or_404(Demands, pk=id_demand)
    transfer = Transfer.on_site.get(demand=id_demand)
    process = transfer.demand_process
    negotiation = Negotiation.on_site.get(demand=id_demand)
    transfers = Transfers.on_site.filter(transfer=transfer)
    participations = ParticipationDemand.on_site.filter(demand=demand)

    filter = request.GET.get('month')
    form = TransfersQuestionsForm()

    transfer.demand_process = 're'
    transfer.save()

    if filter is not None:
        transfers = Transfers.on_site.filter(
            transfer=transfer, date_delivery__month=filter)

    if request.method == "GET":
        return render(request, 'demand/demand_transfer.html', {
            'demand': demand,
            'process': process,
            'negotiation': negotiation,
            'transfers': transfers,
            'form': form,
            'participations': participations,
        })
    else:
        if "review" in request.POST:
            transfers_object = get_object_or_404(
                Transfers, pk=request.POST['review'])
            form = TransfersQuestionsForm(
                request.POST, instance=transfers_object)
            if form.is_valid():
                form.save()
            else:
                form.errors

            date = request.POST["date_review"] + \
                ' ' + request.POST["hour_review"]
            date_review = parse_datetime(date)
            transfers_object.date_reviewed = date_review
            transfers_object.comment_review = request.POST["comment_review"]
            transfers_object.reviewed = True
            transfers_object.save()
            return redirect('demand:process_transfer_revision', id_demand)
        else:
            if demand.process == 'tr' and process == 're':
                transfer.demand_process = 'fi'
                transfer.save()

        return redirect('demand:process_transfer_finalize', id_demand)


@check_user(['Unidad Central'], 'login')
def process_transfer_finalize(request, id_demand):
    demand = get_object_or_404(Demands, pk=id_demand)
    transfer = Transfer.on_site.get(demand=id_demand)
    process = transfer.demand_process
    negotiation = Negotiation.on_site.get(demand=id_demand)
    transfers = Transfers.on_site.filter(transfer=transfer)
    participations = ParticipationDemand.on_site.filter(demand=demand)

    filter = request.GET.get('month')

    transfer.demand_process = 'fi'
    transfer.save()

    if filter is not None:
        transfers = Transfers.on_site.filter(
            transfer=transfer, date_delivery__month=filter)

    if request.method == "GET":
        return render(request, 'demand/demand_transfer.html', {
            'demand': demand,
            'process': process,
            'negotiation': negotiation,
            'transfers': transfers,
            'participations': participations,
        })
    else:
        if "finalize" in request.POST:
            transfers_object = get_object_or_404(
                Transfers, pk=request.POST.get('finalize'))
            date = request.POST["finalized-date-transfer"] + \
                ' ' + request.POST["finalized-hour-transfer"]
            date_review = parse_datetime(date)
            transfers_object.date_finalize = date_review
            transfers_object.comment_finalize = request.POST["finalize_comment"]
            transfers_object.finalize = True
            transfers_object.save()
            return redirect('demand:process_transfer_finalize', id_demand)
        else:
            if demand.process == 'tr' and process == 'fi':
                transfer.demand_process = 'fi'
                transfer.save()
                demand.process = 'pr'
                demand.save()
                return redirect('demand:process_preparation', id_demand)

        return redirect('demand:process_preparation', id_demand)
# end transfer


# preparation
@check_user(['Unidad Central'], 'login')
def process_preparation(request, id_demand):
    demand = get_object_or_404(Demands, pk=id_demand)
    transfer = Transfer.on_site.get(demand=id_demand)
    transfers = Transfers.on_site.filter(transfer=transfer)
    negotiation = Negotiation.on_site.get(demand=id_demand)
    participations = ParticipationDemand.on_site.filter(demand=demand)
    preparations = []

    try:
        preparation = Preparation.on_site.get(demand=id_demand)
    except Preparation.DoesNotExist:
        preparation = None

    if preparation is None:
        Preparation.on_site.create(
            demand=demand,
            demand_process='ini'
        )
        preparation = Preparation.on_site.get(demand=id_demand)
    else:
        try:
            preparations = Preparations.on_site.filter(preparation=preparation)
        except Preparations.DoesNotExist:
            preparations = None
            
    preparation.demand_process = 'ini'
    preparation.save()

    if request.method == "GET":
        return render(request, 'demand/demand_preparation.html', {
            'demand': demand,
            'negotiation': negotiation,
            'transfers': transfers,
            'participations': participations,
            'preparations': preparations,
        })
    else:
        selected_transfer = get_object_or_404(
            Transfers, pk=request.POST["transfer"])
        date = request.POST["date"] + \
            ' ' + request.POST["hour"]
        date_verification = parse_datetime(date)

        Preparations.on_site.create(
            preparation=preparation,
            transfer=selected_transfer,
            date_verification=date_verification,
            comment=request.POST["coments"],
        )

        selected_transfer.preparation = True
        selected_transfer.save()

        preparation.demand_process = 'pr'
        preparation.save()

        return redirect('demand:process_preparation', id_demand)


@check_user(['Unidad Central'], 'login')
def process_preparation_process(request, id_demand):
    demand = get_object_or_404(Demands, pk=id_demand)
    negotiation = Negotiation.on_site.get(demand=id_demand)
    transfer = Transfer.on_site.get(demand=id_demand)
    transfers = Transfers.on_site.filter(transfer=transfer)
    preparation = Preparation.on_site.get(demand=id_demand)
    preparations = Preparations.on_site.filter(preparation=preparation)
    participations = ParticipationDemand.on_site.filter(demand=demand)
    functionaries = Functionary.on_site.all()

    if preparations is None:
        return redirect('demand:process_preparation', id_demand)

    preparation.demand_process = 'pr'
    preparation.save()

    form = PreparationForm()
    preparation_id = request.GET.get("preparation")

    if preparation_id is not None and preparation_id != '':
        preparation_active = get_object_or_404(Preparations, pk=preparation_id)
        sub_process = preparation_active.demand_subprocess

    if request.method == "GET":
        form_document = DocumentForm()

        if preparation_id is not None and preparation_id != '':
            selected_transfer = preparation_active.transfer
            documents_consistency = preparation_active.doc_consistency.all()
            doc_standarization = preparation_active.doc_standarization.all()
            doc_detection = preparation_active.doc_detection.all()
            doc_anonymization = preparation_active.doc_anonymization.all()

            return render(request, 'demand/demand_preparation.html', {
                'preparation_id': preparation_id,
                'demand': demand,
                'negotiation': negotiation,
                'transfers': transfers,
                'preparation': preparation,
                'preparations': preparations,
                'preparation_active': preparation_active,
                'sub_process': sub_process,
                'selected_transfer': selected_transfer,
                'documents_consistency': documents_consistency,
                'doc_standarization': doc_standarization,
                'doc_detection': doc_detection,
                'doc_anonymization': doc_anonymization,
                'form_document': form_document,
                'participations': participations,
                'form': form,
                'functionaries': functionaries,
            })
        else:
            return render(request, 'demand/demand_preparation.html', {
                'preparation_id': preparation_id,
                'demand': demand,
                'negotiation': negotiation,
                'transfers': transfers,
                'preparation': preparation,
                'preparations': preparations,
                'form_document': form_document,
                'participations': participations,
                'form': form,
                'functionaries': functionaries,
            })

    else:
        form_document = DocumentForm(request.POST, request.FILES)
        if sub_process == 'consistency':
            if 'document' in request.POST:
                if form_document.is_valid():
                    document = form_document.save()
                    preparation_active.doc_consistency.add(document)
                    preparation_active.save()
            else:
                assigned_functionary = get_object_or_404(
                    Functionary, pk=request.POST["consistency_functionary"])
                preparation_active.consistency_functionary = assigned_functionary
                try:
                    url = settings.SITE_URL+"solicitud/" + \
                        str(id_demand)+"/" + str(preparation_active.id) + \
                        "/responder/consistencia"
                    name = "Se ha asignado para responder las preguntas del proceso de consistencia en la solicitud " + demand.title + " <a target='_blank' href='" + \
                        url+"'>Responder aquí</a>"

                    message = "Se ha asignado para responder las preguntas del proceso de consistencia en la solicitud " + demand.title

                    Notification.on_site.create(
                        name=name,
                        sent_to=get_object_or_404(
                            User, pk=assigned_functionary.user.id),
                        module_from='SO',
                        message=message,
                        name_link='Responder cuestionario',
                        link=url
                    )
                except:
                    name = None
                preparation_active.demand_subprocess = 'standardization-normalization'
                preparation_active.date_consistency = datetime.today()
                preparation_active.save()

        elif sub_process == 'standardization-normalization':
            if 'document' in request.POST:
                if form_document.is_valid():
                    document = form_document.save()
                    preparation_active.doc_standarization.add(document)
                    preparation_active.save()
            else:
                assigned_functionary = get_object_or_404(
                    Functionary, pk=request.POST["standardization_functionary"])
                preparation_active.standardization_functionary = assigned_functionary
                try:
                    url = settings.SITE_URL+"solicitud/" + \
                        str(id_demand)+"/" + str(preparation_active.id) + \
                        "/responder/estandarizacion"
                    name = "Se ha asignado para responder las preguntas del proceso de estandarización en la solicitud " + demand.title + " <a target='_blank' href='" + \
                        url+"'>Responder aquí</a>"

                    message = "Se ha asignado para responder las preguntas del proceso de estandarización en la solicitud " + demand.title

                    Notification.on_site.create(
                        name=name,
                        sent_to=get_object_or_404(
                            User, pk=assigned_functionary.user.id),
                        module_from='SO',
                        message=message,
                        name_link='Responder cuestionario',
                        link=url
                    )
                except:
                    name = None
                preparation_active.demand_subprocess = 'anomaly-detection'
                preparation_active.date_standarization = datetime.today()
                preparation_active.save()

        elif sub_process == 'anomaly-detection':
            if 'document' in request.POST:
                if form_document.is_valid():
                    document = form_document.save()
                    preparation_active.doc_detection.add(document)
                    preparation_active.save()
            else:
                assigned_functionary = get_object_or_404(
                    Functionary, pk=request.POST["anomaly_functionary"])
                preparation_active.anomaly_functionary = assigned_functionary
                try:
                    url = settings.SITE_URL+"solicitud/" + \
                        str(id_demand)+"/" + str(preparation_active.id) + \
                        "/responder/anomalias"
                    name = "Se ha asignado para responder las preguntas del proceso de anomalías en la solicitud " + demand.title + " <a target='_blank' href='" + \
                        url+"'>Responder aquí</a>"

                    message = "Se ha asignado para responder las preguntas del proceso de anomalías en la solicitud " + demand.title

                    Notification.on_site.create(
                        name=name,
                        sent_to=get_object_or_404(
                            User, pk=assigned_functionary.user.id),
                        module_from='SO',
                        message=message,
                        name_link='Responder cuestionario',
                        link=url
                    )
                except:
                    name = None
                preparation_active.demand_subprocess = 'anonymization-completeness'
                preparation_active.date_detection = datetime.today()
                preparation_active.save()

        elif sub_process == 'anonymization-completeness':
            if 'document' in request.POST:
                if form_document.is_valid():
                    document = form_document.save()
                    preparation_active.doc_anonymization.add(document)
                    preparation_active.save()
            else:
                if not preparation_active.anonymization_functionary:
                    assigned_functionary = get_object_or_404(
                        Functionary, pk=request.POST["anonymization_functionary"])
                    preparation_active.anonymization_functionary = assigned_functionary
                    try:
                        url = settings.SITE_URL+"solicitud/" + \
                            str(id_demand)+"/" + str(preparation_active.id) + \
                            "/responder/anonimizacion"
                        name = "Se ha asignado para responder las preguntas del proceso de anonimización en la solicitud " + demand.title + " <a target='_blank' href='" + \
                            url+"'>Responder aquí</a>"

                        message = "Se ha asignado para responder las preguntas del proceso de anonimización en la solicitud " + demand.title

                        Notification.on_site.create(
                            name=name,
                            sent_to=get_object_or_404(
                                User, pk=assigned_functionary.user.id),
                            module_from='SO',
                            message=message,
                            name_link='Responder cuestionario',
                            link=url
                        )
                    except:
                        name = None
                    preparation_active.date_anonymization = datetime.today()
                    preparation_active.save()

                    preparation.demand_process = 're'
                    preparation.save()
                return redirect('demand:process_preparation_revision', id_demand)

        return redirect('/solicitud/'+str(id_demand)+'/preparacion/proceso/?preparation='+str(preparation_id))


@check_user(['Funcionario'], 'login')
def answer_cuestions(request, id_demand, id_process, process):
    preparation = Preparations.on_site.get(pk=id_process)
    if preparation is None:
        return redirect('demand:process_preparation', id_demand)

    if request.method == 'GET':
        demand = get_object_or_404(Demands, pk=id_demand)

        user_answer = None
        answer_questions = None

        if process == "consistencia":
            user_answer = preparation.consistency_functionary.user
            answer_questions = preparation.consistency_answer
        elif process == "estandarizacion":
            user_answer = preparation.standardization_functionary.user
            answer_questions = preparation.standardization_answer
        elif process == "anomalias":
            user_answer = preparation.anomaly_functionary.user
            answer_questions = preparation.anomaly_answer
        elif process == "anonimizacion":
            user_answer = preparation.anonymization_functionary.user
            answer_questions = preparation.anonymization_answer

        #if request.user != user_answer or answer_questions is True:
        #    return redirect('profile')

        if answer_questions:
            form = PreparationForm(instance=preparation)
        else:
            form = PreparationForm()

        return render(request, 'demand/answer_questions.html', {
            'form': form,
            'process': process,
            'answer_questions': answer_questions,
        })

    else:
        if process == "consistencia":
            preparation.consistency_answer = True
            preparation.consistency_question_1 = request.POST['consistency_question_1']
            preparation.consistency_question_2 = request.POST['consistency_question_2']
            preparation.consistency_question_3 = request.POST['consistency_question_3']
        elif process == "estandarizacion":
            preparation.standardization_answer = True
            preparation.standarization_question_1 = request.POST['standarization_question_1']
            preparation.standarization_question_2 = request.POST['standarization_question_2']
            preparation.standarization_question_3 = request.POST['standarization_question_3']
        elif process == "anomalias":
            preparation.anomaly_answer = True
            preparation.detection_question_1 = request.POST['detection_question_1']
            preparation.detection_question_2 = request.POST['detection_question_2']
            preparation.detection_question_3 = request.POST['detection_question_3']
        elif process == "anonimizacion":
            preparation.anonymization_answer = True
            preparation.anonymization_question_1 = request.POST['anonymization_question_1']
            preparation.anonymization_question_2 = request.POST['anonymization_question_2']
            preparation.anonymization_question_3 = request.POST['anonymization_question_3']

        preparation.save()

    return redirect('profile')


@check_user(['Unidad Central'], 'login')
def process_preparation_revision(request, id_demand):
    demand = get_object_or_404(Demands, pk=id_demand)
    transfer = Transfer.on_site.get(demand=id_demand)
    transfers = Transfers.on_site.filter(transfer=transfer)
    preparation = Preparation.on_site.get(demand=id_demand)
    preparations = Preparations.on_site.filter(preparation=preparation)
    participations = ParticipationDemand.on_site.filter(demand=demand)

    if preparations is None:
        return redirect('demand:process_preparation', id_demand)

    preparation.demand_process = 're'
    preparation.save()

    preparation_id = request.GET.get("preparation")

    if preparation_id is not None and preparation_id != '':
        preparation_active = get_object_or_404(Preparations, pk=preparation_id)
        sub_process = preparation_active.demand_subprocess
        process = preparation.demand_process

    if request.method == "GET":
        if preparation_id is not None and preparation_id != '':
            revision_form = PreparationRevisionForm()
            metrics = {
                "consistency": round((preparation_active.consistency_question_1 + preparation_active.consistency_question_2 + preparation_active.consistency_question_3) / 3, 1) if preparation_active.consistency_question_1 else "Sin definir",
                "standardization": round((preparation_active.standarization_question_1 + preparation_active.standarization_question_2 + preparation_active.standarization_question_3) / 3, 1) if preparation_active.standarization_question_1 else "Sin definir",
                "anomaly": round((preparation_active.detection_question_1 + preparation_active.detection_question_2 + preparation_active.detection_question_3) / 3, 1) if preparation_active.detection_question_1 else "Sin definir",
                "anonymization": round((preparation_active.anonymization_question_1 + preparation_active.anonymization_question_2 + preparation_active.anonymization_question_3) / 3, 1) if preparation_active.anonymization_question_1 else "Sin definir",
            }

            return render(request, 'demand/demand_preparation.html', {
                'demand': demand,
                'transfers': transfers,
                'preparation': preparation,
                'preparations': preparations,
                'preparation_active': preparation_active,
                'sub_process': sub_process,
                'participations': participations,
                'metrics': metrics,
                'revision_form': revision_form,
            })
        else:
            return render(request, 'demand/demand_preparation.html', {
                'demand': demand,
                'transfers': transfers,
                'preparation': preparation,
                'preparations': preparations,
                'participations': participations,
            })

    else:
        if process == 're':
            if 'date' in request.POST and 'hour' in request.POST:
                date = request.POST["date"] + ' ' + request.POST["hour"]
                date_revision = parse_datetime(date)
                preparation_active.date_revision = date_revision
                preparation_active.comment_revision = request.POST["coments"]
                preparation_active.question_1 = request.POST["question_1"]
                preparation_active.question_2 = request.POST["question_2"]
                preparation_active.question_3 = request.POST["question_3"]
                preparation_active.save()

                preparation.demand_process = 'fi'
                preparation.save()
                return redirect('/solicitud/'+str(id_demand)+'/preparacion/revision/?preparation='+preparation_id)

        return redirect('demand:process_preparation_revision', id_demand)


@check_user(['Unidad Central'], 'login')
def process_preparation_finalize(request, id_demand):
    demand = get_object_or_404(Demands, pk=id_demand)
    transfer = Transfer.on_site.get(demand=id_demand)
    transfers = Transfers.on_site.filter(transfer=transfer)
    preparation = Preparation.on_site.get(demand=id_demand)
    preparations = Preparations.on_site.filter(preparation=preparation)
    participations = ParticipationDemand.on_site.filter(demand=demand)

    preparation.demand_process = 'fi'
    preparation.save()

    preparation_id = request.GET.get("preparation")

    if preparation_id is not None and preparation_id != '':
        preparation_active = get_object_or_404(Preparations, pk=preparation_id)
        sub_process = preparation_active.demand_subprocess

    if request.method == "GET":
        if preparation_id is not None and preparation_id != '':
            return render(request, 'demand/demand_preparation.html', {
                'demand': demand,
                'transfers': transfers,
                'preparation': preparation,
                'preparations': preparations,
                'sub_process': sub_process,
                'participations': participations,
                'preparation_active': preparation_active,
            })
        else:
            return render(request, 'demand/demand_preparation.html', {
                'demand': demand,
                'transfers': transfers,
                'preparation': preparation,
                'preparations': preparations,
                'participations': participations,
            })

    else:
        if 'date_finalize' in request.POST and 'hour_finalize' in request.POST:
            date = request.POST["date_finalize"] + \
                ' ' + request.POST["hour_finalize"]
            date_revision = parse_datetime(date)
            preparation_active.date_finalize = date_revision
            preparation_active.comment_finalize = request.POST["coments_finalize"]
            preparation_active.finalize = True
            preparation_active.transfer.validate_preparation = True
            preparation_active.transfer.save()
            preparation_active.save()
            
            try:
                evaluation = Evaluation.on_site.get(demand=id_demand)
            except:
                evaluation = None
                
            if evaluation is None:
                Evaluation.on_site.create(
                    demand=demand,
                )
                
            demand.process = 'ev'
            demand.save()
        return redirect('demand:process_evaluation', id_demand)

# end preparation

# evaluation


@check_user(['Unidad Central'], 'login')
def process_evaluation(request, id_demand):
    demand = get_object_or_404(Demands, pk=id_demand)
    try:
        evaluation = Evaluation.on_site.get(demand=id_demand)
    except:
        evaluation = None
        
    if evaluation is None:
        Evaluation.on_site.create(
            demand=demand,
        )
    evaluation = Evaluation.on_site.get(demand=id_demand)
    evaluations = Evaluations.on_site.filter(evaluation=evaluation)
    participations = ParticipationDemand.on_site.filter(demand=demand)
    negotiation = Negotiation.on_site.get(demand=id_demand)
    functionaries = Functionary.on_site.all()
    cant_evaluations = evaluations.count()
    evaluation_data = ""
    
    evaluation.demand_process = 'ini'
    evaluation.save()

    if cant_evaluations > 0:
        evaluation_data = evaluations[0]

    if request.method == "GET":
        return render(request, 'demand/demand_evaluation.html', {
            'cant': cant_evaluations,
            'demand': demand,
            'evaluation_data': evaluation_data,
            'evaluations': evaluations,
            'participations': participations,
            'functionaries': functionaries,
            'negotiation': negotiation,
        })

    else:
        if evaluations.count() == 0:
            functionary = request.POST["evaluation_functionary"]
            functionary = Functionary.on_site.get(pk=functionary)
            date_notification = datetime.strptime(
                request.POST["date_notification"], '%Y-%m-%d').date()
            finish_date = datetime.strptime(
                request.POST["finish_date"], '%Y-%m-%d').date()
            evaluation_frequency = request.POST["evaluation_frequency"]

            list_frequency = calculate_frequency_evaluation(
                date_notification, finish_date, evaluation_frequency)
            cont = 1

            for frecuency in list_frequency:
                Evaluations.on_site.create(
                    evaluation=evaluation,
                    functionary=functionary,
                    date_notification=date_notification,
                    frequency=evaluation_frequency,
                    finish_date=finish_date,
                    frequency_delivery=cont,
                    frequency_date_delivery=frecuency
                )
                cont = cont + 1

            url = settings.SITE_URL+"usuario/perfil/"
            name = "El funcionario " + functionary.user.first_name + \
                " ha sido asignado para responder las preguntas del proceso de evaluación en la solicitud " + demand.title

            message = "El funcionario " + functionary.user.first_name + \
                " ha sido asignado para responder las preguntas del proceso de evaluación en la solicitud " + demand.title
            Notification.on_site.create(
                name=name,
                sent_to=functionary.user,
                module_from='SO',
                message=message,
                name_link='Responder evaluación',
                link=url
            )
            participation = ParticipationDemand.on_site.filter(
                user=functionary.user, demand=demand)
            if not participation:
                user_functionary = User.objects.get(pk=functionary.user.id)
                ParticipationDemand.on_site.create(
                    user=user_functionary,
                    demand=demand
                )

        return redirect('demand:process_evaluation_process', id_demand)


@check_user(['Unidad Central'], 'login')
def process_evaluation_process(request, id_demand):
    if request.method == "GET":
        demand = get_object_or_404(Demands, pk=id_demand)
        evaluation = Evaluation.on_site.get(demand=id_demand)
        evaluations = Evaluations.on_site.filter(
            evaluation=evaluation).order_by('frequency_delivery')
        participations = ParticipationDemand.on_site.filter(demand=demand)
        negotiation = Negotiation.on_site.get(demand=id_demand)
        functionaries = Functionary.on_site.all()
        cant_evaluations = evaluations.count()
        evaluation_data = ""
        
        evaluation.demand_process = 'pr'
        evaluation.save()

        if cant_evaluations > 0:
            evaluation_data = evaluations[0]

        return render(request, 'demand/demand_evaluation.html', {
            'cant': cant_evaluations,
            'demand': demand,
            'evaluation_data': evaluation_data,
            'evaluations': evaluations,
            'participations': participations,
            'functionaries': functionaries,
            'negotiation': negotiation,
        })
    else:
        coments_interview = request.POST['coments_interview']
        id_evaluation = request.POST['id_evaluation']

        evaluation = Evaluations.on_site.get(pk=id_evaluation)
        evaluation.interview = coments_interview
        evaluation.save()

        return redirect('demand:process_evaluation_process', id_demand)


@check_user(['Unidad Central'], 'login')
def process_evaluation_revision(request, id_demand):
    demand = get_object_or_404(Demands, pk=id_demand)
    evaluation = Evaluation.on_site.get(demand=id_demand)
    
    evaluation.demand_process = 're'
    evaluation.save()

    if request.method == "GET":
        evaluations = Evaluations.on_site.filter(
            evaluation=evaluation).order_by('frequency_delivery')
        participations = ParticipationDemand.on_site.filter(demand=demand)
        functionaries = Functionary.on_site.all()
        cant_evaluations = evaluations.count()
        form_document = DocumentForm()
        documents = evaluation.doc_evaluation.all()
        evaluation_data = ""

        if cant_evaluations > 0:
            evaluation_data = evaluations[0]

        return render(request, 'demand/demand_evaluation.html', {
            'cant': cant_evaluations,
            'demand': demand,
            'evaluation_data': evaluation_data,
            'evaluations': evaluations,
            'evaluation': evaluation,
            'participations': participations,
            'functionaries': functionaries,
            'form_document': form_document,
            'documents': documents if documents else '',
        })
    else:
        form_document = DocumentForm(request.POST, request.FILES)
        if 'document' in request.POST:
            if form_document.is_valid():
                document = form_document.save()
                evaluation.doc_evaluation.add(document)
                evaluation.save()
                if document:
                    users_list = []
                    users_list.append(
                        form_document.cleaned_data.get('assigned_to'))
                    all_copy_to = form_document.cleaned_data.get('copy_to')
                    s = [int(s) for s in re.findall(r'-?\d+\.?\d*', all_copy_to)]

                    for copy_to in s:
                        users_list.append(copy_to)
                    create_participation(users_list, demand)
            else:
                form_document.errors

        return redirect('demand:process_evaluation_revision', id_demand)


@check_user(['Unidad Central'], 'login')
def process_evaluation_finalize(request, id_demand):
    demand = get_object_or_404(Demands, pk=id_demand)
    evaluation = Evaluation.on_site.get(demand=id_demand)
    
    evaluation.demand_process = 'fi'
    evaluation.save()

    if request.method == "GET":
        evaluations = Evaluations.on_site.filter(
            evaluation=evaluation).order_by('frequency_delivery')
        participations = ParticipationDemand.on_site.filter(demand=demand)
        functionaries = Functionary.on_site.all()
        cant_evaluations = evaluations.count()
        evaluation_data = ""

        if cant_evaluations > 0:
            evaluation_data = evaluations[0]

        return render(request, 'demand/demand_evaluation.html', {
            'cant': cant_evaluations,
            'demand': demand,
            'evaluation_data': evaluation_data,
            'evaluations': evaluations,
            'evaluation': evaluation,
            'participations': participations,
            'functionaries': functionaries,
        })
    else:
        coments_finalize = request.POST['coments_finalize']
        evaluation.comment_finalize = coments_finalize
        evaluation.date_finalize = timezone.now().date()
        evaluation.finalize = True

        evaluation.save()

        return redirect('demand:process_evaluation_finalize', id_demand)


def calculate_frequency_evaluation(date_notification, finish_date, evaluation_frequency):
    list_frequency = []
    day = 30 * int(evaluation_frequency)
    frequency = date_notification

    while frequency < finish_date:
        date_frequency = frequency + timedelta(days=int(day))
        if date_frequency < finish_date:
            list_frequency.append(date_frequency)
        frequency = date_frequency

    return list_frequency


@check_user(['Funcionario'], 'login')
def answer_cuestions_evaluations(request, id_demand, id_evaluation):
    evaluations = Evaluations.on_site.get(pk=id_evaluation)

    if evaluations is None:
        return redirect('profile', id_demand)

    if request.method == 'GET':
        user_answer = evaluations.functionary.user
        evaluation_answer = evaluations.evaluation_answer
        now = timezone.now().date()

        if request.user != user_answer:
            return redirect('profile')

        # if now != evaluations.frequency_date_delivery:
        #    return redirect('profile')

        if evaluation_answer:
            form = EvaluationsForm(instance=evaluations)
        else:
            form = EvaluationsForm()

        return render(request, 'demand/answer_questions_evaluations.html', {
            'form': form,
            'evaluation_answer': evaluation_answer,
        })

    else:
        evaluations.evaluation_answer = True
        evaluations.question_1 = request.POST['question_1']
        evaluations.question_2 = request.POST['question_2']
        evaluations.question_3 = request.POST['question_3']
        evaluations.question_4 = request.POST['question_4']
        evaluations.question_5 = request.POST['question_5']
        evaluations.question_6 = request.POST['question_6']
        evaluations.question_7 = request.POST['question_7']
        evaluations.question_8 = request.POST['question_8']
        evaluations.question_9 = request.POST['question_9']
        evaluations.question_10 = request.POST['question_10']
        evaluations.result = (int(request.POST['question_1'])+int(request.POST['question_2'])+int(request.POST['question_3'])+int(request.POST['question_4'])+int(request.POST['question_5'])+int(
            request.POST['question_6'])+int(request.POST['question_7'])+int(request.POST['question_8'])+int(request.POST['question_9'])+int(request.POST['question_10']))/10

        evaluations.save()

    return redirect('profile')


def create_participation(users, demand):
    for user in users:
        participation = ParticipationDemand.on_site.filter(user=user,demand=demand.id)
        if not participation:
            data_user = User.objects.get(pk=user)
            ParticipationDemand.on_site.create(
                user=data_user,
                demand=demand
            )


def calculate_frequency_delivery(id_demand, date_agreed, date_agreement, time, type_time):
    # id_demand = id de la solicitud
    # date_agreed = fecha acordada de entrega
    # date_agreement = fecha limite de duracion del convneio
    # time = frecuencia de actualizacion
    # type_time = tipo de frecuencia
    # ('days', 'Días'),
    # ('weeks', 'Semanas'),
    # ('months', 'Meses'),
    # ('years', 'Años'),

    list_frequency = []
    cont = 1
    day = 0
    frequency = date_agreed

    while frequency < date_agreement:
        date_frequency = date_agreed + timedelta(days=day)
        if date_frequency <= date_agreement:
            frequency = [
                str(cont) + "@" + str(date_frequency),
                "Entrega" + " " + str(cont) + " - " + date_frequency.strftime(
                    "%d") + " de " + date_frequency.strftime("%m") + " del " + date_frequency.strftime("%Y")
            ]
            list_frequency.append(frequency)
        day = day + time
        cont = cont + 1
        frequency = date_frequency

    return list_frequency
