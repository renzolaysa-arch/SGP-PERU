from django.shortcuts import get_object_or_404, render, redirect
from .forms import CreateProvider, loginUser, UpdateProvider, EditProfile, EditProfileFunctionary, EditProfileUnitCentral, EditProfileProvider, UniteCentralForm, ProviderForm, FunctionaryForm, AccessUserRRAForm
from .models import Provider, Unit_Central, Functionary, AccessUserRRA
from .filters import AccessUserRRAFilter
from projects.models import Project
from providers.models import ProviderEntity
from notifications.models import Notification
from inventory.models import Inventory, FollowInventory, InventoryThematic
from weblog.models import CommentThread, ThemeThread
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from .decorators import check_user
from notifications.functions import notify_email
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.decorators import login_required
import xlwt
from datetime import datetime
import secrets
import json
from django.conf import settings
from demand.models import Demands, Reception, Negotiation, Transfer, Preparation, Preparations, Transfers, FollowDemand, Evaluations
from django.utils import timezone
from django.core.mail import BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core import mail
from django.utils.html import strip_tags
from datetime import timedelta
from demand.functions import calculate_process_board
from django.core.paginator import Paginator
import csv
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.views.decorators.cache import never_cache
# Create your views here.


class rraa_list_custom:
    def __init__(self, id, name_rraa, coverage, provider, date_request, date_modified, status, checked):
        self.id = id
        self.name_rraa = name_rraa
        self.coverage = coverage
        self.provider = provider
        self.date_request = date_request
        self.date_modified = date_modified
        self.status = status
        self.checked = checked


class demand_list_custom:
    def __init__(self, id, name_demand, provider, created_date, status, checked):
        self.id = id
        self.name_demand = name_demand
        self.provider = provider
        self.created_date = created_date
        self.status = status
        self.checked = checked


class my__rraa_list_custom:
    def __init__(self, id, name_rraa, percentage, status_completed):
        self.id = id
        self.name_rraa = name_rraa
        self.percentage = percentage
        self.status_completed = status_completed


def get_user_all(limit=0):
    if limit > 0:
        number = int(limit)
        providers = Provider.on_site.select_related('user').all()[:number]
        unit_central = Unit_Central.on_site.select_related('user').all()[
            :number]
        functionary = Functionary.on_site.select_related('user').all()[:number]
        users = {
            'providers': providers,
            'unit_central': unit_central,
            'functionary': functionary
        }
    else:
        providers = Provider.on_site.select_related('user').all()
        unit_central = Unit_Central.on_site.select_related('user').all()
        functionary = Functionary.on_site.select_related('user').all()
        users = {
            'providers': providers,
            'unit_central': unit_central,
            'functionary': functionary
        }

    return users


def create_provider(request):
    if request.user.id:
        return redirect('profile')
    if request.method == 'GET':
        return render(request, 'users/create_provider.html', {
            "form": CreateProvider()
        })
    else:
        form = CreateProvider(request.POST, request.FILES)
        if form.is_valid():
            user_emil = request.POST['email']
            domain_user = user_emil.split('@')
            provider = ProviderEntity.objects.filter(
                site__id=get_current_site(request).id,
                domain=domain_user[1]
            )
            url = settings.SITE_URL
            if provider:
                try:
                    user_active = False
                    valid_data = True
                    token = secrets.token_hex(nbytes=16)
                    name_notify = "Nuevo posible proveedor registrado, recuerde dirigirse a la sección de Listado de usuarios, Solicitudes de accesos para activar el usuario creado."
                    message = "Para activar el nuevo proveedor puedes hacer clic para ir a Listado de usuarios, Solicitudes de accesos."
                    try:
                        head_unit = Unit_Central.on_site.all()

                        for notify in head_unit:
                            Notification.on_site.create(
                                name=name_notify,
                                sent_to=get_object_or_404(
                                    User, pk=notify.user.id),
                                module_from="PRV",
                                message=message,
                                name_link='Activa la cuenta del nuevo proveedor',
                                link=url + 'usuario/perfil/',
                            )
                        notify_email(
                            'Activa tu cuenta',
                            'Para activar su cuenta es necesario hacer clic',
                            user_emil,
                            'Activa tu cuenta',
                            url + 'usuario/activate-token/' + token,
                            settings.COUNTRY
                        )
                    except:
                        print("Error to get data Unit_Central")
                except:
                    response_data = {}
                    response_data['result'] = 'error'
                    response_data['message'] = 'Ha Ocurrido un Error con el envío de correo electrónico, es posible que deba corregirlo o contactar al administrador'
            else:
                # cuando el modele de unidad central este listo se debe migrar el correo
                # envio de notificaciones
                try:
                    head_unit = Unit_Central.on_site.all()
                    name_notify = "Nuevo posible proveedor registrado, recuerde dirigirse a la sección de Listado de usuarios, Solicitudes de accesos para activar el usuario creado."
                    message = "Para activar el nuevo proveedor puedes hacer clic para ir a Listado de usuarios, Solicitudes de accesos."
                    for notify in head_unit:
                        Notification.on_site.create(
                            name=name_notify,
                            sent_to=get_object_or_404(
                                User, pk=notify.user.id),
                            module_from="PRV",
                            message=message,
                            name_link='Activa la cuenta del nuevo proveedor',
                            link=url + 'usuario/perfil/',
                        )
                    notify_email(
                        'Nuevo proveedor',
                        'Se ha notificado a la Unidad Central una nueva solicitud de nuevo proveedor',
                        user_emil,
                        None,
                        None,
                        settings.COUNTRY
                    )
                    user_active = False
                    valid_data = False
                    token = ""
                except:
                    response_data = {}
                    response_data['result'] = 'error'
                    response_data['message'] = 'Ha Ocurrido un Error con el envío de correo electrónico, es posible que deba corregirlo o contactar al administrador'

            user = User.objects.create_user(
                first_name=request.POST['name'],
                last_name=request.POST['last_name'],
                username=user_emil,
                email=user_emil,
                password=request.POST['password'],
                is_active=user_active
            )
            group_provider = Group.objects.get(name='Proveedor')
            group_provider.user_set.add(user)
            Provider.objects.create(
                document_type=request.POST['document_type'],
                identification_number=request.POST['identification_number'],
                user=user,
                valid_data=valid_data,
                entity_provider=provider.first() if provider else None,
                hash=token
            )
            return redirect('/usuario/crear')

        else:
            form.errors
            return render(request, 'users/create_provider.html', {
                "form": form
            })


def send_token(request, id_user):
    try:
        provider = Provider.on_site.get(pk=id_user)
    except provider.DoesNotExist:
        provider = None

    if provider is not None:
        url = settings.SITE_URL
        notify_email(
            'Activa tu cuenta',
            'Para activar su cuenta de clic',
            provider.user.username,
            'Activa tu cuenta',
            url + 'usuario/activate-token/' + provider.hash,
            settings.COUNTRY
        )
    return redirect('/usuario/crear?unit='+str(id_user))


def activate(request, token):
    try:
        provider = Provider.on_site.get(hash=token)
    except provider.DoesNotExist:
        provider = None

    if provider is not None:
        try:
            user_provider = User.objects.get(id=provider.user_id)
        except user_provider.DoesNotExist:
            user_provider = None

        if user_provider is not None:
            provider.hash = ""
            provider.save()
            user_provider.is_active = True
            user_provider.save()
            return redirect('/usuario/ingresar')
        else:
            return redirect('/usuario/crear')

    else:
        return redirect('/usuario/crear')


def login_user(request):
    if request.user.id:
        return redirect('profile')
    if request.method == 'GET':
        return render(request,  'users/login.html', {
            "form": loginUser()
        })
    else:
        form = loginUser(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=request.POST['username'],
                password=request.POST['password'],
                site__id=get_current_site(request).id
            )
            if user is None:
                return render(request, 'users/login.html', {
                    "form": loginUser(),
                    "error": "Nombre de usuario o contraseña incorrectos"
                })
            else:
                try:
                    providers = Provider.on_site.get(user=user)
                except Provider.DoesNotExist:
                    providers = None

                try:
                    unit_central = Unit_Central.on_site.get(user=user)
                except Unit_Central.DoesNotExist:
                    unit_central = None

                try:
                    functionary = Functionary.on_site.get(user=user)
                except Functionary.DoesNotExist:
                    functionary = None

                if providers is None and unit_central is None and functionary is None:
                    return render(request, 'users/login.html', {
                        "form": loginUser(),
                        "error": "Nombre de usuario o contraseña incorrectos"
                    })
                else:
                    login(request, user)
                    if 'remember_me' not in request.POST:
                        request.session.set_expiry(0)
                    return redirect('profile')
        else:
            form.errors
            return render(request, 'users/login.html', {
                "form": form,
                "error": form.errors,
            })


def recovery(request):

    template = loader.get_template('users/recovery.html')
    context = {

    }
    return HttpResponse(template.render(context, request))


def register(request):

    template = loader.get_template('users/register.html')
    context = {

    }
    return HttpResponse(template.render(context, request))


@check_user(['Unidad Central'], 'login')
def list_user(request):
    limit = request.GET.get("limit")
    total_filter = 0
    if limit is not None:
        data_total = get_user_all(limit)
    else:
        data_total = get_user_all(0)

    total_users = len(data_total['providers']) + \
        len(data_total['unit_central']) + len(data_total['functionary'])
    total_active = 0
    total_inactive = 0

    for profile in data_total:
        for user in data_total[profile]:
            if user.user.is_active:
                total_active += 1
            else:
                total_inactive += 1

    groups = Group.objects.all()
    total_group = len(groups)

    number_usuers = {
        'total_users_filter': data_total,
        'total_users': total_users,
        'total_active': total_active,
        'total_inactive': total_inactive
    }

    provider = Provider.on_site.filter(
        user__groups__name='Proveedor',
        user__is_active=False,
        valid_data=1,
    ) | Provider.on_site.filter(
        user__groups__name='Proveedor',
        user__is_active=True,
        valid_data=0,
    ) | Provider.on_site.filter(
        user__groups__name='Proveedor',
        user__is_active=False,
        valid_data=0,
    )

    data = {
        'pending_provider': provider,
        'users_show_filter': data_total,
        'groups': groups,
        'total_group': total_group,
    }

    return render(request, 'users/head_unit/user_list.html', {
        'total_filter': total_filter,
        'data': data,
        'number_usuers': number_usuers,
    })


class notification_list:
    def __init__(self, id, name, hour, hidden):
        self.id = id
        self.name = name
        self.hour = hour
        self.hidden = hidden


@login_required(login_url='login')
@never_cache
def profile(request):
    if request.user.groups.filter(name='Unidad Central').exists():
        user_id = request.user.id
        try:
            user_provider = Unit_Central.on_site.get(user=user_id)
            data = {
                "image": user_provider.profile_image,
                "name": user_provider.user.first_name,
            }
            return render(request, 'users/head_unit/profile.html',
                          {
                              'data': data,
                          })
        except:
            return redirect('contents:home')
    elif request.user.groups.filter(name='Proveedor').exists():
        user_id = request.user.id
        user_provider = Provider.on_site.get(user=user_id)
        user_provider_entity = user_provider.entity_provider.id

        try:
            user_provider_entity_project = Project.on_site.filter(
                provider_any_project=user_provider_entity)
        except:
            user_provider_entity_project = None

        try:
            inventory_entity_provider = Inventory.on_site.filter(
                entity_provider=user_provider.entity_provider.id).order_by('-created_date')
            total_inventory = len(inventory_entity_provider)
        except:
            inventory_entity_provider = None
            total_inventory = 0

        custom_my_rraa = []
        status_completed = False
        for item in inventory_entity_provider:
            data_completed = int(
                item.cont_columns_count - item.empty_fields_count)

            percentage = round(
                ((data_completed*100)/item.cont_columns_count), None)

            if percentage >= 100:
                status_completed = True
            else:
                status_completed = False

            custom_my_rraa.append(my__rraa_list_custom(
                item.id, item.title, percentage, status_completed))

        user_notification = Notification.on_site.filter(
            sent_to=user_id).order_by('-created_date')
        date_format_str = '%d/%m/%Y %H:%M:%S.%f'
        date_2 = datetime.now()
        date_now = date_2.strftime(date_format_str)

        # creating list
        list = []
        cont = 0

        def calculate_hours(prov):
            date_create = prov.created_date.strftime(date_format_str)
            start = datetime.strptime(date_create, date_format_str)
            end = datetime.strptime(date_now, date_format_str)
            diff = end - start
            diff_in_hours = int(diff.total_seconds() / 3600)
            if diff_in_hours < 1:
                diff_in_hours = 0
                return "Hace menos de una hora"
            if diff_in_hours >= 24:
                day = diff_in_hours // 24
                hour = diff_in_hours - (day*24)
                return str(day) + " días, " + str(hour) + " horas"
            else:
                return str(diff_in_hours) + " horas"

        for prov in user_notification:
            hour = calculate_hours(prov)
            list.append(notification_list(
                prov.id, prov.name, hour, prov.hidden))
            cont = cont + 1

        data = {
            "image": user_provider.profile_image,
            "name": user_provider.entity_provider.name,
            "description": user_provider.entity_provider.description,
        }

        inventory_page_obj = Inventory.on_site.all()

        list_custom = []
        checked = True
        status = "Activo"
        for item in inventory_page_obj:
            if FollowInventory.on_site.filter(user=user_id, InventoryStatus=item.id):
                checked = True
                list_custom.append(rraa_list_custom(
                    item.id, item.title, item.geographic_coverages, item.entity_provider, item.created_date, item.modified_date, status, checked))

        # percentage profile:
        data_completed = int(
            user_provider.count_column_prov - user_provider.empty_fields_count_prov)
        percentage_profile_completed = round(
            ((data_completed * 100)/user_provider.count_column_prov), None)
        if percentage_profile_completed < 100:
            status_profile_completed = False
        else:
            status_profile_completed = True

        demands_provider = Demands.on_site.filter(
            provider_entity=user_provider_entity)

        multiple_averages = {}

        for demand in demands_provider:
            average = 0

            try:
                preparation = Preparation.on_site.get(demand=demand)
            except Preparation.DoesNotExist:
                preparation = None

            if preparation is not None:
                preparations = Preparations.on_site.filter(
                    preparation=preparation)

                if preparations:
                    for item_preparation in preparations:
                        if item_preparation.consistency_question_1:
                            average = (average + (item_preparation.consistency_question_1 +
                                                  item_preparation.consistency_question_2 + item_preparation.consistency_question_3))
                        if item_preparation.standarization_question_1:
                            average = (average + (item_preparation.standarization_question_1 +
                                                  item_preparation.standarization_question_2 + item_preparation.standarization_question_3))
                        if item_preparation.detection_question_1:
                            average = (average + (item_preparation.detection_question_1 +
                                                  item_preparation.detection_question_2 + item_preparation.detection_question_3))
                        if item_preparation.anonymization_question_1:
                            average = (average + (item_preparation.anonymization_question_1 +
                                                  item_preparation.anonymization_question_2 + item_preparation.anonymization_question_3))

                    average = average / (12 * len(preparations))
                    multiple_averages[demand] = round(average, 1)

        return render(request, 'users/profile.html', {
            'data': data,
            'notification_list': list,
            'cont': cont,
            'inventory_entity_provider': inventory_entity_provider,
            'total_inventory': total_inventory,
            'user_provider_entity': user_provider_entity,
            'project_list': user_provider_entity_project,
            'percentage_profile_completed': percentage_profile_completed,
            'status_profile_completed': status_profile_completed,
            'inventory_page_obj': list_custom,
            'custom_my_rraa': custom_my_rraa,
            'multiple_averages': multiple_averages,
        })
    elif request.user.groups.filter(name='Funcionario').exists():
        user_id = request.user.id
        user_provider = Functionary.objects.get(user=user_id)

        data = {
            "image": user_provider.profile_image,
            "name": user_provider.user.first_name,
        }
        return render(request, 'users/functionary/profile.html',
                      {
                          'data': data,
                      })
    else:
        return render(request, 'users/functionary/profile.html')


@check_user(['Unidad Central'], 'login')
def update_provider(request, group,  id_user):
    if request.method == 'GET':
        user_profile = False
        if group == 'Proveedor':
            user = get_object_or_404(Provider, pk=id_user)
            profile_form = UpdateProvider(initial={
                'profile_image': user.profile_image,
                'name': user.user.first_name,
                'last_name': user.user.last_name,
                'document_type': user.document_type,
                'identification_number': user.identification_number,
                'email': user.user.username,
                'entity_provider': user.entity_provider,
                'valid_data': user.valid_data,
                'is_active': user.user.is_active,
            })
        elif group == 'Unidad Central':
            user = get_object_or_404(Unit_Central, pk=id_user)
            user_profile = True
            profile_form = EditProfileUnitCentral(initial={
                'profile_image': user.profile_image,
                'name': user.user.first_name,
                'last_name': user.user.last_name,
                'email': user.user.username,
                'is_active': user.user.is_active,
            })
        elif group == 'Funcionario':
            user = get_object_or_404(Functionary, pk=id_user)
            user_profile = True
            profile_form = EditProfileFunctionary(initial={
                'profile_image': user.profile_image,
                'name': user.user.first_name,
                'last_name': user.user.last_name,
                'email': user.user.username,
                'is_active': user.user.is_active,
            })
        else:
            return redirect('profile')

        if user_profile:
            form = EditProfile(initial={
                'first_name': user.user.first_name,
                'last_name': user.user.last_name,
                'is_active': user.user.is_active
            })

        return render(request, 'users/update_user.html', {
            'form': form if 'form' in locals() else '',
            'profile_form': profile_form if 'profile_form' in locals() else '',
            'user_profile': user,
            'type': group,
        })
    else:
        user_id = request.user.id
        user_unit = Unit_Central.on_site.get(user=user_id)
        if group == 'Proveedor':
            provider = get_object_or_404(Provider, pk=id_user)
            provider.valid_data = 1 if 'valid_data' in request.POST else 0
            provider.document_type = request.POST['document_type']
            if 'profile_image' in request.FILES:
                provider.profile_image = request.FILES['profile_image']
            provider.identification_number = request.POST['identification_number']
            provider.entity_provider = get_object_or_404(
                ProviderEntity, pk=request.POST['entity_provider'])
            provider.save()
            email = request.POST['email']
            user = get_object_or_404(User, pk=provider.user.pk)

            if user.is_active == False and 'is_active' in request.POST:
                user.username = email
                user.first_name = request.POST['name']
                user.last_name = request.POST['last_name']
                user.is_active = 1 if 'is_active' in request.POST else 0
                # Si se activa enviar un email adicional
                user.email = email
                try:
                    user.save()
                    url = settings.SITE_URL + "/usuario/ingresar/"
                    name = "Su usuario ha sido activado por la Unidad Central: " + \
                        user_unit.user.first_name
                    message = "Su usuario ha sido activado por la Unidad Central: " + \
                        user_unit.user.first_name

                    Notification.on_site.create(
                        name=name,
                        sent_to=get_object_or_404(
                            User, pk=user.id),
                        module_from='CO',
                        message=message,
                        name_link='¡Su usuario ha sido aprobado!',
                        link=url
                    )
                except:
                    return redirect('update_provider')
                return redirect('profile')
            else:
                try:
                    user.username = email
                    user.first_name = request.POST['name']
                    user.last_name = request.POST['last_name']
                    user.is_active = 1 if 'is_active' in request.POST else 0
                    # Si se activa enviar un email adicional
                    user.email = email
                    user.save()
                    url = settings.SITE_URL
                    name = "Sus datos de perfil han sido actualizados por la Unidad Central: " + \
                        user_unit.user.first_name
                    message = "Sus datos de perfil han sido actualizados por la Unidad Central: " + \
                        user_unit.user.first_name

                    Notification.on_site.create(
                        name=name,
                        sent_to=get_object_or_404(
                            User, pk=user.id),
                        module_from='CO',
                        message=message,
                        name_link='Sus datos de perfil han sido actualizados',
                        link=url
                    )
                except:
                    return redirect('update_provider')
                return redirect('profile')
        elif group == 'Unidad Central':
            user = get_object_or_404(Unit_Central, pk=id_user)
            form = EditProfileFunctionary(request.POST, instance=user)
            if 'profile_image' in request.FILES:
                user.profile_image = request.FILES['profile_image']
            user.save()
            user_unit = get_object_or_404(User, pk=user.user.pk)
            user_unit.username = request.POST['email']
            user_unit.first_name = request.POST['name']
            user_unit.last_name = request.POST['last_name']
            user_unit.is_active = 1 if 'is_active' in request.POST else 0
            # Si se activa enviar un email adicional
            user_unit.email = request.POST['email']
            user_unit.save()
            try:
                url = settings.SITE_URL
                name = "Sus datos de perfil han sido actualizados por la Unidad Central: " + \
                    user_unit.first_name
                message = "Sus datos de perfil han sido actualizados por la Unidad Central: " + \
                    user_unit.first_name

                Notification.on_site.create(
                    name=name,
                    sent_to=get_object_or_404(
                        User, pk=user.user.id),
                    module_from='CO',
                    message=message,
                    name_link='Sus datos de perfil han sido actualizados',
                    link=url
                )
            except:
                return redirect('update_provider')

        elif group == 'Funcionario':
            user = get_object_or_404(Functionary, pk=id_user)
            form = EditProfileFunctionary(request.POST, instance=user)
            if 'profile_image' in request.FILES:
                user.profile_image = request.FILES['profile_image']
            user.save()

            user_functionary = get_object_or_404(User, pk=user.user.pk)
            user_functionary.username = request.POST['email']
            user_functionary.first_name = request.POST['name']
            user_functionary.last_name = request.POST['last_name']
            user_functionary.is_active = 1 if 'is_active' in request.POST else 0
            # Si se activa enviar un email adicional
            user_functionary.email = request.POST['email']
            user_functionary.save()
            try:
                url = settings.SITE_URL
                name = "Sus datos de perfil han sido actualizados por la Unidad Central: " + \
                    user_unit.user.first_name
                message = "Sus datos de perfil han sido actualizados por la Unidad Central: " + \
                    user_unit.user.first_name

                Notification.on_site.create(
                    name=name,
                    sent_to=get_object_or_404(
                        User, pk=user.user.id),
                    module_from='CO',
                    message=message,
                    name_link='Sus datos de perfil han sido actualizados',
                    link=url
                )
            except:
                return redirect('update_provider')

    return redirect('profile')


@check_user(['Unidad Central'], 'login')
def dashboard(request):
    user_id = request.user.id
    user_provider = Unit_Central.objects.get(user=user_id)
    user_notification = Notification.on_site.filter(
        sent_to=user_provider.user.id).order_by('-created_date')
    total_providers = ProviderEntity.on_site.all().count()
    total_projects_asociate = Project.on_site.all().count()
    total_inventory = Inventory.on_site.all().count()
    date_format_str = '%d/%m/%Y %H:%M:%S.%f'
    date_2 = datetime.now()
    date_now = date_2.strftime(date_format_str)
    # creating list
    list = []
    cont = 0

    def calculate_hours(prov):
        date_create = prov.created_date.strftime(date_format_str)
        start = datetime.strptime(date_create, date_format_str)
        end = datetime.strptime(date_now, date_format_str)
        diff = end - start
        diff_in_hours = int(diff.total_seconds() / 3600)
        if diff_in_hours < 1:
            diff_in_hours = 0
            return "Hace menos de una hora"
        if diff_in_hours >= 24:
            day = diff_in_hours // 24
            hour = diff_in_hours - (day*24)
            return str(day) + " días, " + str(hour) + " horas"
        else:
            return str(diff_in_hours) + " horas"

    for prov in user_notification:
        hour = calculate_hours(prov)
        list.append(notification_list(prov.id, prov.name, hour, prov.hidden))
        cont = cont + 1

    providers = ProviderEntity.objects.filter(
        site__id=get_current_site(request).id).order_by('-created_date')

    list_for_provider = {}
    sorted_best_providers = {}
    cont = 0

    for prov in providers:
        provider_inventory_cont = len(Inventory.on_site.filter(
            entity_provider_id=prov.id).order_by('-entity_provider'))
        list_for_provider[prov.name] = provider_inventory_cont
        sorted_best_providers = dict(
            sorted(list_for_provider.items(), key=lambda x: x[1], reverse=True))

    thematic = []
    inventory_thematic = InventoryThematic.on_site.all()

    for thematic_item in inventory_thematic:
        dic = {"nombre": thematic_item.name_thematic_inventory,
               "valor": count_thematic(thematic_item.id), "id": thematic_item.id}
        thematic.append(dic)

    provider = []
    inventory_provider = ProviderEntity.on_site.all()

    for provider_item in inventory_provider:
        dic = {"nombre": provider_item.name, "valor": count_inventory(
            provider_item.id), "id": provider_item.id}
        provider.append(dic)

    return render(request, 'users/head_unit/dashboard.html',
                  {
                      'notification_list': list,
                      'cont': cont,
                      'total_providers': total_providers,
                      'total_projects_asociate': total_projects_asociate,
                      'total_inventory': total_inventory,
                      'sorted_best_providers': sorted_best_providers,
                      'providers_inventory': list_for_provider,
                      'thematic': thematic,
                      'provider': provider,
                  })


@check_user(['Unidad Central'], 'login')
def notifications(request):
    user_id = request.user.id
    user_provider = Unit_Central.objects.get(user=user_id)
    user_notification = Notification.on_site.filter(
        sent_to=user_provider.user.id).order_by('-created_date')

    date_format_str = '%d/%m/%Y %H:%M:%S.%f'
    date_2 = datetime.now()
    date_now = date_2.strftime(date_format_str)
    # creating list
    list = []
    cont = 0

    def calculate_hours(prov):
        date_create = prov.created_date.strftime(date_format_str)
        start = datetime.strptime(date_create, date_format_str)
        end = datetime.strptime(date_now, date_format_str)
        diff = end - start
        diff_in_hours = int(diff.total_seconds() / 3600)
        if diff_in_hours < 1:
            diff_in_hours = 0
            return "Hace menos de una hora"
        if diff_in_hours >= 24:
            day = diff_in_hours // 24
            hour = diff_in_hours - (day*24)
            return str(day) + " días, " + str(hour) + " horas"
        else:
            return str(diff_in_hours) + " horas"

    for prov in user_notification:
        hour = calculate_hours(prov)
        list.append(notification_list(prov.id, prov.name, hour, prov.hidden))
        cont = cont + 1

    return render(request, 'users/head_unit/notifications.html',
                  {
                      'notification_list': list,
                      'cont': cont,
                  })


@check_user(['Unidad Central'], 'login')
def inventory(request):
    return render(request, 'users/head_unit/inventory.html')


@check_user(['Unidad Central'], 'login')
def activity_board(request):
    return render(request, 'users/head_unit/activity_board.html')


@check_user(['Unidad Central'], 'login')
def acceso_rra(request):
    queryset = AccessUserRRA.on_site.all()

    filter_rraa = AccessUserRRAFilter(
        request.GET,
        queryset=queryset
    )

    page_cant = 10
    paginated_filter_rraa = Paginator(filter_rraa.qs, page_cant)
    page_number = request.GET.get("page")
    if page_number is None:
        page_number = 1
    rraa_page_obj = paginated_filter_rraa.get_page(page_number)
    rraa_total = paginated_filter_rraa.count
    page = paginated_filter_rraa.page(page_number).object_list
    rraa_page = ((int(page_number)-1) * page_cant) + page.count()

    return render(
        request,
        'users/head_unit/access_rra.html',
        {
            'filter': filter_rraa,
            'rraa_page_obj': rraa_page_obj,
            'rraa_total': rraa_total,
            'rraa_page': str(rraa_page),
        }
    )


@check_user(['Funcionario'], 'login')
def access_rra(request):
    user_id = request.user.id
    user_provider = Functionary.objects.get(user=user_id)
    queryset = AccessUserRRA.on_site.filter(
        user=user_provider).order_by('date_limit')

    rraas = AccessUserRRA.on_site.filter(
        user=user_provider)

    list_rraa = []
    for rraa in rraas:
        list_rraa.append(rraa.inventory)

    filter_rraa = AccessUserRRAFilter(
        request.GET,
        queryset=queryset,
    )

    page_cant = 10
    paginated_filter_rraa = Paginator(filter_rraa.qs, page_cant)
    page_number = request.GET.get("page")
    if page_number is None:
        page_number = 1
    rraa_page_obj = paginated_filter_rraa.get_page(page_number)
    rraa_total = paginated_filter_rraa.count
    page = paginated_filter_rraa.page(page_number).object_list
    rraa_page = ((int(page_number)-1) * page_cant) + page.count()

    return render(
        request,
        'users/functionary/access_rra.html',
        {
            'filter': filter_rraa,
            'rraa_page_obj': rraa_page_obj,
            'rraa_total': rraa_total,
            'rraa_page': str(rraa_page),
            'list_rraa': list_rraa,
        }
    )


def create_acceso_rra(request):
    if request.method == "GET":
        acces_user_form = AccessUserRRAForm()
        return render(
            request,
            'users/head_unit/create_access_rra.html',
            {
                'acces_user_form': acces_user_form,
            }
        )
    else:
        form = AccessUserRRAForm(request.POST)
        if form.is_valid():
            form.save()
            try:
                form.save()
                data_rraa = Inventory.on_site.filter(
                    pk=request.POST['inventory']).first()
                url = settings.SITE_URL
                name = "Se la ha permitido el acceso al registro administrativo " + data_rraa.title + " <a target='_blank' href='" + \
                    url+"detalle-inventario/" + \
                    str(data_rraa.id) + "'>Consulta aquí</a>"

                message = 'Se la ha permitido el acceso al registro administrativo: "' + \
                    data_rraa.title + '".'
                functionary = Functionary.on_site.filter(
                    pk=int(request.POST['user']))
                for user_notify in functionary:
                    Notification.on_site.create(
                        name=name,
                        sent_to=get_object_or_404(
                            User, pk=user_notify.user.id),
                        module_from='CO',
                        message=message,
                        name_link='Se la ha permitido el acceso al registro administrativo',
                        link=url+"detalle-inventario/" + str(data_rraa.id)
                    )
            except:
                return redirect('profile')
    return redirect('profile')


def delete_acceso_rra(request, access_id):
    access = get_object_or_404(
        AccessUserRRA, pk=access_id, site__id=get_current_site(request).id)
    access.delete()
    return redirect('profile')


@check_user(['Funcionario'], 'login')
def activity_boards(request):
    user_id = request.user.id
    user_provider = Functionary.objects.get(user=user_id)
    count_comments = CommentThread.on_site.filter(
        functionary_commented=user_provider.id).count()
    functionary_threads = ThemeThread.on_site.filter(
        user_functionary_created=user_provider.id)
    data_functionary_commented = []
    for item in functionary_threads:
        query_users_commented = CommentThread.on_site.filter(
            threadt_to_comment=item.pk).values('functionary_commented').distinct()
        for val in query_users_commented:
            if val not in data_functionary_commented:
                data_functionary_commented.append(val)

    user_notification = Notification.on_site.filter(
        sent_to=user_provider.user.id).order_by('-created_date')
    total_providers = ProviderEntity.on_site.all().count()
    total_projects_asociate = Project.on_site.filter(
        functionary_project=user_provider.id).count()
    total_inventory = Inventory.on_site.all().count()
    date_format_str = '%d/%m/%Y %H:%M:%S.%f'
    date_2 = datetime.now()
    date_now = date_2.strftime(date_format_str)
    # creating list
    list = []
    cont = 0

    def calculate_hours(prov):
        date_create = prov.created_date.strftime(date_format_str)
        start = datetime.strptime(date_create, date_format_str)
        end = datetime.strptime(date_now, date_format_str)
        diff = end - start
        diff_in_hours = int(diff.total_seconds() / 3600)
        if diff_in_hours < 1:
            diff_in_hours = 0
            return "Hace menos de una hora"
        if diff_in_hours >= 24:
            day = diff_in_hours // 24
            hour = diff_in_hours - (day*24)
            return str(day) + " días, " + str(hour) + " horas"
        else:
            return str(diff_in_hours) + " horas"

    for prov in user_notification:
        hour = calculate_hours(prov)
        list.append(notification_list(prov.id, prov.name, hour, prov.hidden))
        cont = cont + 1

    providers = ProviderEntity.on_site.all().order_by('-created_date')

    list_for_provider = {}
    sorted_best_providers = {}

    for prov in providers:
        provider_inventory_cont = len(Inventory.on_site.filter(
            entity_provider_id=prov.id).order_by('-entity_provider'))
        list_for_provider[prov.name] = provider_inventory_cont
        sorted_best_providers = dict(
            sorted(list_for_provider.items(), key=lambda x: x[1], reverse=True))

    access_rraa = AccessUserRRA.on_site.filter(
        user=user_provider).order_by('date_limit')

    thematic = []
    inventory_thematic = InventoryThematic.on_site.all()

    for thematic_item in inventory_thematic:
        dic = {"nombre": thematic_item.name_thematic_inventory,
               "valor": count_thematic(thematic_item.id), "id": thematic_item.id}
        thematic.append(dic)

    provider = []
    inventory_provider = ProviderEntity.on_site.all()

    for provider_item in inventory_provider:
        dic = {"nombre": provider_item.name, "valor": count_inventory(
            provider_item.id), "id": provider_item.id}
        provider.append(dic)

    return render(request, 'users/functionary/activity_board.html',
                  {
                      'notification_list': list,
                      'cont': cont,
                      'total_providers': total_providers,
                      'total_projects_asociate': total_projects_asociate,
                      'total_inventory': total_inventory,
                      'count_comments': count_comments,
                      'comments_interactions': len(data_functionary_commented),
                      'sorted_best_providers': sorted_best_providers,
                      'access_rraa': access_rraa,
                      'thematic': thematic,
                      'provider': provider,
                  })


def count_thematic(id_thematic):
    return Inventory.on_site.filter(inventory_thematic_asociate=id_thematic, custody=True).count()


def count_inventory(id_provider):
    return Inventory.on_site.filter(entity_provider=id_provider, custody=True).count()


@check_user(['Funcionario'], 'login')
def activities(request):
    return render(request, 'users/functionary/activities.html')


class activity_management_list:
    def __init__(self, id, type, title, url_reception, porcent_reception, reception_demand_process, url_negotiation, porcent_negotiation, negotiation_demand_process, url_transfer, porcent_transfer, transfer_demand_process, url_preparation, porcent_preparation, preparation_demand_process, url_evaluation, porcent_evaluation, evaluation_demand_process):
        self.id = id
        self.type = type
        self.title = title
        self.url_reception = url_reception
        self.porcent_reception = porcent_reception
        self.reception_demand_process = reception_demand_process
        self.url_negotiation = url_negotiation
        self.porcent_negotiation = porcent_negotiation
        self.negotiation_demand_process = negotiation_demand_process
        self.url_transfer = url_transfer
        self.porcent_transfer = porcent_transfer
        self.transfer_demand_process = transfer_demand_process
        self.url_preparation = url_preparation
        self.porcent_preparation = porcent_preparation
        self.preparation_demand_process = preparation_demand_process
        self.url_evaluation = url_evaluation
        self.porcent_evaluation = porcent_evaluation
        self.evaluation_demand_process = evaluation_demand_process


@check_user(['Funcionario'], 'login')
def activity_management(request):
    user_id = request.user.id
    user_provider = Functionary.objects.get(user=user_id)

    demands = Demands.on_site.filter(
        functionary=user_provider.pk).order_by('-created_date')
    demands_list = []

    for item in demands:
        id_demand = item.id
        # Process
        if item.type == "ex":
            board = calculate_process_board(id_demand)

            demands_list.append(activity_management_list(
                item.id,
                item.type,
                item.title,
                board["url_reception"],
                board["porcent_reception"],
                board["status_reception"],
                board["url_negotiation"],
                board["porcent_negotiation"],
                board["status_negotiation"],
                board["url_transfer"],
                board["porcent_transfer"],
                board["status_transfer"],
                board["url_preparation"],
                board["porcent_preparation"],
                board["status_preparation"],
                board["url_evaluation"],
                board["porcent_evaluation"],
                board["status_evaluation"]))
        else:
            demands_list.append(activity_management_list(
                item.id, item.type, item.title, "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""))
    return render(request, 'users/functionary/activity_management.html',
                  {
                      'demands_list': demands_list,
                  })


@check_user(['Funcionario'], 'login')
def inventories(request):
    user_id = request.user.id
    inventory_page_obj = Inventory.on_site.all()

    list_custom = []
    checked = True
    status = "Activo"
    for item in inventory_page_obj:
        if FollowInventory.on_site.filter(user=user_id, InventoryStatus=item.id):
            checked = True
            list_custom.append(rraa_list_custom(
                item.id, item.title, item.geographic_coverages, item.entity_provider, item.created_date, item.modified_date, status, checked))

    return render(request, 'users/functionary/inventory.html',
                  {
                      'inventory_page_obj': list_custom,
                  })


@check_user(['Funcionario'], 'login')
def demands_functionary(request):
    user_id = request.user.id
    demand_page_obj = Demands.on_site.all()
    # modificar la query para que traiga los datos del innner join basados en el usuario
    list_custom = []
    checked = True
    status = "Activo"
    for item in demand_page_obj:
        if FollowDemand.on_site.filter(user=user_id, demand=item.id):
            checked = True
            list_custom.append(demand_list_custom(
                item.id, item.title, item.provider_entity, item.created_date, status, checked))

    return render(request, 'users/functionary/demands_functionary.html',
                  {
                      'demand_custom': list_custom,
                  })


@check_user(['Funcionario'], 'login')
def notification(request):
    user_id = request.user.id
    user_provider = Functionary.objects.get(user=user_id)
    user_notification = Notification.on_site.filter(
        sent_to=user_provider.user.id).order_by('-created_date')

    date_format_str = '%d/%m/%Y %H:%M:%S.%f'
    date_2 = datetime.now()
    date_now = date_2.strftime(date_format_str)
    # creating list
    list = []
    cont = 0

    def calculate_hours(prov):
        date_create = prov.created_date.strftime(date_format_str)
        start = datetime.strptime(date_create, date_format_str)
        end = datetime.strptime(date_now, date_format_str)
        diff = end - start
        diff_in_hours = int(diff.total_seconds() / 3600)
        if diff_in_hours < 1:
            diff_in_hours = 0
            return "Hace menos de una hora"
        if diff_in_hours >= 24:
            day = diff_in_hours // 24
            hour = diff_in_hours - (day*24)
            return str(day) + " días, " + str(hour) + " horas"
        else:
            return str(diff_in_hours) + " horas"

    for prov in user_notification:
        hour = calculate_hours(prov)
        list.append(notification_list(prov.id, prov.name, hour, prov.hidden))
        cont = cont + 1

    return render(request, 'users/functionary/notifications.html',
                  {
                      'notification_list': list,
                      'cont': cont,
                  })


def hidden_notification(request, id_notification):
    try:
        notify = Notification.on_site.filter(pk=id_notification).first()
        notify.hidden = True
        notify.save()
        return JsonResponse({'success': 'True'})
    except:
        return JsonResponse({'fail': 'True'})


@never_cache
def custom_logout(request):
    logout(request)
    return redirect("/")


@ login_required(login_url='login')
def edit_profile(request):
    if request.method == 'GET':
        user = request.user
        form = EditProfile(instance=user)
        group = user.groups.values_list('name', flat=True).first()
        if group == 'Unidad Central':
            user_object = Unit_Central.objects.filter(user=user).first()
            profile_form = EditProfileUnitCentral(instance=user_object)
        elif group == 'Proveedor':
            user_object = Provider.objects.filter(user=user).first()
            profile_form = EditProfileProvider(instance=user_object)
        elif group == 'Funcionario':
            user_object = Functionary.objects.filter(user=user).first()
            profile_form = EditProfileFunctionary(instance=user_object)

        return render(request, 'users/edit_profile.html', {
            "profile_form": profile_form if 'profile_form' in locals() else '',
            'form': form,
        })
    else:
        user = request.user
        form = EditProfile(request.POST, instance=user)
        group = user.groups.values_list('name', flat=True).first()
        if group == 'Unidad Central':
            user_object = Unit_Central.objects.filter(user=user).first()
            profile_form = EditProfileUnitCentral(
                request.POST, request.FILES, instance=user_object)
        elif group == 'Proveedor':
            user_object = Provider.objects.filter(user=user).first()
            profile_form = EditProfileProvider(
                request.POST, request.FILES, instance=user_object)
        elif group == 'Funcionario':
            user_object = Functionary.objects.filter(user=user).first()
            profile_form = EditProfileFunctionary(
                request.POST, request.FILES, instance=user_object)

        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            return redirect('profile')
        else:
            form.errors
            profile_form.errors
            return render(request, 'users/edit_profile.html', {
                "profile_form": profile_form if 'profile_form' in locals() else '',
                'form': form,
            })


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)               
            if associated_users.exists():
                print("Ingreso correo existe")              
                for user in associated_users:
                    subject = "Solicitud de cambio de contraseña"
                    email_template_name = "users/reset_password/password_reset_email.html"
                    domain = settings.SITE_URL[:-1]
                    token = default_token_generator.make_token(user),
                    token = token[0]
                    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                    reset_url = reverse('password_reset_confirm', args=[uidb64, token])
                    reset_url = domain + reset_url
                    c = {
                        "email": user.email,
                        'domain': domain,
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': token,
                        'protocol': 'https',
                        'country': settings.COUNTRY,
                        'url': settings.SITE_URL,
                        'reset_url': reset_url
                    }
                    email = render_to_string(email_template_name, c)
                    plain_message = strip_tags(email)
                    try:
                        mail.send_mail(
                            subject, plain_message, settings.EMAIL_HOST_USER, [user.email], html_message=email)
                    except:
                        send_error = {
                            'error_send': 'False'
                        }
                        return JsonResponse(send_error, status=503)
                    
                    successful_send = {  
                        'successful_send': 'True'
                    }
                    #return redirect("/usuario/ingresar?send=true")
                    return JsonResponse(successful_send, status=202)
            else:
                mensaje_error = {
                    'error': 'No se encontraron datos en la consulta.'
                }      
                # Devuelve la respuesta JSON con el mensaje de error
                return JsonResponse(mensaje_error, status=404)

    else:
        password_reset_form = PasswordResetForm()
        return render(request=request, template_name="users/reset_password/reset.html", context={"password_reset_form": password_reset_form})


@ login_required(login_url='login')
def edit_password(request):
    if request.method == 'GET':
        user = request.user
        change_password = PasswordChangeForm(user)
        return render(request, 'users/edit_profile.html', {
            'change_password': change_password
        })
    else:
        user = request.user
        change_password = PasswordChangeForm(user, request.POST)
        if change_password.is_valid():
            change_password.save()
            return redirect('profile')
        else:
            change_password.errors
            return render(request, 'users/edit_profile.html', {
                'change_password': change_password
            })


@ check_user(['Unidad Central'], 'login')
def create_any_user(request):
    if request.method == "GET":
        form = UserCreationForm()
        return render(request, 'users/head_unit/create_any_user.html', {
            'form': form
        })
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.first_name = request.POST['nombre']
            form_save.last_name = request.POST['apellido']
            form_save.email = request.POST['username']
            form_save.save()
            group_name = request.POST['group']
            group = Group.objects.get(name=group_name)
            form_save.groups.add(group)
            return redirect('create_user_group', form_save.id)
        else:
            form.errors
            return render(request, 'users/head_unit/create_any_user.html', {
                'form': form
            })


@ check_user(['Unidad Central'], 'login')
def create_user_group(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    group = user.groups.first()
    if request.method == 'GET':
        if group.name == 'Unidad Central':
            form_group = UniteCentralForm(instance=user)
        elif group.name == 'Proveedor':
            form_group = ProviderForm(instance=user)
        elif group.name == 'Funcionario':
            form_group = FunctionaryForm(instance=user)

        return render(request, 'users/head_unit/create_any_user.html', {
            'form_group': form_group if 'form_group' in locals() else '',
        })
    else:
        if group.name == 'Unidad Central':
            form_group = UniteCentralForm(request.POST, request.FILES)
        elif group.name == 'Proveedor':
            form_group = ProviderForm(request.POST, request.FILES)
        elif group.name == 'Funcionario':
            form_group = FunctionaryForm(request.POST, request.FILES)

        if form_group.is_valid():
            form_group.save()
            id_form = form_group.instance.id
            # Notificación a la unidad central
            url = settings.SITE_URL
            name = "Se ha registrado un nuevo usuario con el rol " + group.name + ",  <a target='_blank' href='" + \
                url+"usuario/actualizar/" + group.name + "/" + \
                str(id_form) + "'>Revisa los datos acá</a>"
            message = "Se ha registrado un nuevo usuario con el rol " + group.name
            try:
                Notification.on_site.create(
                    name=name,
                    sent_to=get_object_or_404(
                        User, pk=request.user.id),
                    module_from="CO",
                    message=message,
                    name_link='Se ha registrado un nuevo usuario con el rol ' + group.name,
                    link=url+"usuario/actualizar/" +
                    group.name + "/" + str(id_form)
                )
                name = "Se le ha registrado en la plataforma SGP como rol: " + group.name + ". Los datos de acceso son: email: " + \
                    form_group.instance.user.email + \
                    ". Debe ingresar por la opción de recuperar contraseña para asignar la clave de su preferencia."

                Notification.on_site.create(
                    name=name,
                    sent_to=get_object_or_404(
                        User, pk=user_id),
                    module_from="CO",
                    message=name,
                    name_link='Se le ha registrado en la plataforma SGP como rol' + group.name,
                    link=url+"usuario/ingresar/"
                )
            except:
                return redirect('profile')

            return redirect('profile')
        else:
            form_group.errors
            return render(request, 'users/head_unit/create_any_user.html', {
                'form_group': form_group if 'form_group' in locals() else '',
            })


@ check_user(['Unidad Central'], 'login')
def download_user(request):
    # content-type of response
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Users.xls"'

    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("users")

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True
    columns = ['Id', 'Usuario', 'Nombre', 'Apellido', 'Activo', 'Grupo',
               'Tipo documento', 'Docuemnto', 'Entidad proveedora', 'Data Verificada']

    # write column headers in sheet
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    data = get_user_all(0)
    for my_row in data:
        for row in data[my_row]:
            row_num = row_num + 1
            ws.write(row_num, 0, row.user.id, font_style)
            ws.write(row_num, 1, row.user.username, font_style)
            ws.write(row_num, 2, row.user.first_name, font_style)
            ws.write(row_num, 3, row.user.last_name, font_style)
            ws.write(
                row_num, 4, 'Activo' if row.user.is_active else 'Inactivo', font_style)
            ws.write(row_num, 5, row.user.groups.first().name, font_style)

        if my_row == 'providers':
            valid_data = row.valid_data
            ws.write(row_num, 6, row.document_type, font_style)
            ws.write(row_num, 7, row.identification_number, font_style)
            ws.write(row_num, 8, row.entity_provider.name, font_style)
            ws.write(row_num, 9, "Si" if valid_data else "No", font_style)
        else:
            ws.write(row_num, 6, 'n/a', font_style)
            ws.write(row_num, 7, 'n/a', font_style)
            ws.write(row_num, 8, 'n/a', font_style)
            ws.write(row_num, 9, 'n/a', font_style)

    wb.save(response)
    return response


@ login_required(login_url='login')
def delete_notification(request, id):
    try:
        notification = get_object_or_404(
            Notification, pk=id, site__id=get_current_site(request).id)
        if request.method == "POST":
            notification.delete()
            return JsonResponse({'success': 'True'})
    except:
        return JsonResponse({'fail': 'True'})


class transfers_list:
    def __init__(self,
                 id,
                 provider_id,
                 provider,
                 demand_id,
                 demand,
                 date_agreed,
                 channel,
                 status_transfer,
                 date_delivery,
                 frequency_delivery,
                 frequency_date_delivery
                 ):
        self.id = id
        self.provider_id = provider_id
        self.provider = provider
        self.demand_id = demand_id
        self.demand = demand
        self.date_agreed = date_agreed
        self.channel = channel
        self.status_transfer = status_transfer
        self.date_delivery = date_delivery
        self.frequency_delivery = frequency_delivery
        self.frequency_date_delivery = frequency_date_delivery


@ check_user(['Unidad Central'], 'login')
def transfers_all(request):
    demands = Demands.on_site.all().order_by('-created_date')
    transfer_list = []
    now = timezone.now().date()
    range = request.GET.get("day")

    if range is None:
        range = 0

    for demand in demands:
        cont = 1
        try:
            negotiation = Negotiation.on_site.get(demand_id=demand.id)
        except:
            negotiation = None

        if negotiation is not None:
            if negotiation.date_agreed is not None and negotiation.date_agreement is not None and negotiation.time is not None and negotiation.type_time:
                list_frequency = calculate_frequency_delivery(
                    demand.id, negotiation.date_agreed, negotiation.date_agreement, negotiation.time, negotiation.type_time, range)
                for frequency in list_frequency:
                    cont = cont + 1
                    try:
                        transfer_demand = Transfer.on_site.get(
                            demand=demand.id)
                    except:
                        transfer_demand = None

                    if transfer_demand is not None:
                        try:
                            transfers = Transfers.on_site.filter(
                                transfer=transfer_demand.id, frequency_date_delivery=frequency)
                        except:
                            transfers = None

                        if transfers is not None:
                            count = 0
                            status = ""
                            for transfer_item in transfers:
                                if transfer_item.status_transfer == "ac":
                                    status = "Aceptada"
                                elif transfer_item.status_transfer == "pe":
                                    status = "Pendiente"
                                elif transfer_item.status_transfer == "de":
                                    status = "Rechazado"

                                transfer_list.append(transfers_list(
                                    transfer_item.id,
                                    demand.provider_entity.id,
                                    demand.provider_entity.name,
                                    demand.id,
                                    demand.title,
                                    negotiation.date_agreed,
                                    transfer_item.channel,
                                    status,
                                    transfer_item.date_delivery,
                                    transfer_item.frequency_delivery,
                                    transfer_item.frequency_date_delivery
                                ))
                                count += 1

                            if count == 0:
                                transfer_list.append(transfers_list(
                                    "-",
                                    demand.provider_entity.id,
                                    demand.provider_entity.name,
                                    demand.id,
                                    demand.title,
                                    negotiation.date_agreed,
                                    "-",
                                    "Sin entregar",
                                    "-",
                                    cont + int(range),
                                    now + timedelta(days=int(range))
                                ))

                        else:
                            transfer_list.append(transfers_list(
                                "-",
                                demand.provider_entity.id,
                                demand.provider_entity.name,
                                demand.id,
                                demand.title,
                                negotiation.date_agreed,
                                "-",
                                "Sin entregar",
                                "-",
                                cont + int(range),
                                now + timedelta(days=int(range))
                            ))
                    else:
                        transfer_list.append(transfers_list(
                            "-",
                            demand.provider_entity.id,
                            demand.provider_entity.name,
                            demand.id,
                            demand.title,
                            negotiation.date_agreed,
                            "-",
                            "Sin entregar",
                            "-",
                            cont + int(range),
                            now + timedelta(days=int(range))
                        ))

    return render(request, 'users/head_unit/transfers.html', {
        'transfer_list': transfer_list,
        'date': now + timedelta(days=int(range))
    })


def calculate_frequency_delivery(id_demand, date_agreed, date_agreement, time, type_time, range):
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
    day = 0
    frequency = date_agreed
    now = timezone.now().date() + timedelta(days=int(range))

    while frequency <= now and now <= date_agreement:
        date_frequency = date_agreed + timedelta(days=day)
        if date_frequency == now:
            list_frequency.append(date_frequency)
        day = day + time
        frequency = date_frequency

    return list_frequency


@check_user(['Funcionario', 'Proveedor'], 'login')
def inventory_follow(request, id_inventory):
    if request.user.is_authenticated:
        try:
            inventory = Inventory.objects.get(pk=id_inventory)
        except Inventory.DoesNotExist:
            inventory = None

        try:
            if inventory is not None:
                follow = FollowInventory.objects.get(
                    user=request.user, InventoryStatus=inventory)
            else:
                follow = None
        except FollowInventory.DoesNotExist:
            follow = None

        try:
            if follow is not None:
                follow.delete()
            else:
                q = FollowInventory(
                    user=request.user,
                    InventoryStatus=inventory,
                )
                q.save()
            return JsonResponse({'success': 'True'})
        except:
            return JsonResponse({'fail': 'True'})


@check_user(['Proveedor'], 'login')
def notify_to_provider(request, id_inventory):
    if request.user.is_authenticated:
        user_id = request.user.id
        try:
            # Notificación
            url = settings.SITE_URL

            provider_current = Provider.on_site.get(user=user_id)
            rraa = Inventory.on_site.get(pk=id_inventory)
            owner_rraa = Provider.on_site.filter(
                entity_provider=rraa.entity_provider.id)
            notifications = {user_id}

            for item in owner_rraa:
                notifications.add(item.user.id)

            for notify in notifications:
                name = "El Proveedor " + provider_current.entity_provider.name + ", Desea ponerse en contacto respecto al registro administrativo " + rraa.title + " <a target='_blank' href='" + \
                    url+"detalle-inventario/" + \
                    str(id_inventory) + "'>aquí</a>"
                message = "Solicitud de contacto: " + provider_current.entity_provider.name

                Notification.on_site.create(
                    name=name,
                    sent_to=get_object_or_404(
                        User, pk=notify),
                    module_from="IN",
                    message=message,
                    name_link='Consultar el registro administrativo del cual desea ponerse en contacto',
                    link=url+"detalle-inventario/" + str(id_inventory)
                )
            return JsonResponse({'success': 'True'})
        except:
            return JsonResponse({'fail': 'True'})


@check_user(['Funcionario'], 'login')
def evaluations(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        functionary = Functionary.on_site.get(user=user_id)
        evaluations = Evaluations.on_site.filter(
            functionary=functionary).order_by('frequency_date_delivery')
        now = timezone.now().date()

        return render(request, 'users/functionary/evaluations.html', {
            'evaluations': evaluations,
            'now': now
        })
