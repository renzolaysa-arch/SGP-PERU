from django.shortcuts import render
from random import normalvariate
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from .models import Inventory, FollowInventory, CommentInventory, QualityTest
from content.models import Divipola, TDivipola
from django.template import loader
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.urls import reverse
from users.decorators import check_user
from .filters import InventoryFilter
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import date, datetime, timedelta, timezone
from notifications.models import Notification
from notifications.services import create_notifications_and_send_emails_async
from inventory.forms import CreateInventoryForm, FilterOrderForm, CreateCommentForm, QualityTestForm
from users.models import Provider
from providers.models import ProviderEntity
from projects.models import Project
from content.models import Visitor
from users.models import Functionary, Unit_Central
import pandas
from django.conf import settings
# Create your views here.


class rraa_list_custom:
    def __init__(self, id, name_rraa, provider, date_request, status, checked, custody):
        self.id = id
        self.name_rraa = name_rraa
        self.provider = provider
        self.date_request = date_request
        self.status = status
        self.checked = checked
        self.custody = custody


def inventory_list(request):
    order_by = request.GET.get("order")
    user_id = request.user.id

    if order_by is not None and order_by != '':
        queryset = Inventory.on_site.filter().order_by(order_by)
    else:
        queryset = Inventory.on_site.filter().order_by('-created_date')

    filter_inventory = InventoryFilter(
        request.GET,
        queryset=queryset
    )

    form_order_by = FilterOrderForm()

    page_cant = 6
    paginated_filter_inventory = Paginator(filter_inventory.qs, page_cant)
    page_number = request.GET.get("page")
    if page_number is None:
        page_number = 1
    inventory_page_obj = paginated_filter_inventory.get_page(page_number)
    inventory_total = paginated_filter_inventory.count
    page = paginated_filter_inventory.page(page_number).object_list
    inventory_page = ((int(page_number)-1) * page_cant) + len(page)

    list_custom = []
    checked = True
    status = "Activo"
    for item in inventory_page_obj:
        if FollowInventory.on_site.filter(user=user_id, InventoryStatus=item.id):
            checked = True
        else:
            checked = False
        list_custom.append(rraa_list_custom(
            item.id, item.title, item.entity_provider, item.created_date, status, checked, item.custody))
        
    paginated_filter_inventory = Paginator(list_custom, page_cant)
    inventory_custom = paginated_filter_inventory.get_page(page_number)


    return render(
        request,
        'register/inventory_list.html',
        {
            'filter': filter_inventory,
            'list_custom': inventory_custom,
            'inventory_page_obj': inventory_page_obj,
            'inventory_total': inventory_total,
            'inventory_page': str(inventory_page),
            'form_order_by': form_order_by,
        }
    )


def detail_inventory(request, id_inventory):
    user = request.user
    group = user.groups.values_list('name', flat=True).first()

    inventory = get_object_or_404(Inventory, pk=id_inventory)
    if request.method == 'GET':
        list_inventory_tags = inventory.tag_sample_data_asociate.all()

        divipola = Divipola.objects.filter(inventory__id=inventory.id)
        count_projects = Project.on_site.filter(
            rraa_asociate=inventory).count()
        count_visitor = Visitor.on_site.filter(
            type_model_visited="Registros Administrativos", id_model_visited=id_inventory
        ).count()
        today = date.today()
        seven_day_before = today - timedelta(days=8)
        views_chart = Visitor.on_site.filter(
            type_model_visited="Registros Administrativos",
            id_model_visited=id_inventory,
            created_date__gte=seven_day_before,
        ).order_by('created_date__date')

        today_views = Visitor.on_site.filter(
            type_model_visited="Registros Administrativos",
            id_model_visited=id_inventory,
            created_date__date=today,
        ).count()

        tdivipolas = TDivipola.on_site.all().order_by('-id')

        data_chart = {}
        count = 1
        for view in views_chart:
            if view.created_date.strftime('%m %d') in data_chart:
                count += 1
            data_chart[view.created_date.strftime('%m %d')] = {
                'day': view.created_date.strftime('%d %b'),
                'quantity': count
            }
            count = 1

        list_for_inventory = []
        list_related_inventory = []

        for item in list_inventory_tags:
            inventory_related = Inventory.on_site.filter(
                tag_sample_data_asociate=item).distinct()
            list_for_inventory.append(inventory_related)
            for item in list_for_inventory:
                for it in item:
                    if it not in list_related_inventory:
                        list_related_inventory.append(it)

        if group == 'Funcionario':
            comments = CommentInventory.on_site.filter(inventory=inventory)
            commentForm = CreateCommentForm()
            dates_comments = CommentInventory.on_site.filter(
                inventory=inventory).distinct()
        else:
            comments = None
            commentForm = None
            dates_comments = None

        owner = False
        if group == 'Proveedor':
            owner = False
            user_id = request.user.id
            data_user = Provider.objects.filter(user=user_id).first()
            entity_provider = ProviderEntity.objects.get(
                pk=data_user.entity_provider.id)
            if inventory.entity_provider == entity_provider:
                owner = True
            else:
                owner = False

        return render(request, 'register/detail_inventory.html', {
            "inventory": inventory,
            "divipolas": divipola,
            'count_projects': count_projects,
            'count_visitor': count_visitor,
            'list_related_inventory': list_related_inventory,
            'data_chart': data_chart,
            'today_views': today_views,
            'tdivipolas': tdivipolas,
            'comments': comments,
            'commentForm': commentForm,
            'dates_comments': dates_comments,
            'owner': owner,
        })
    else:
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.inventory = inventory
            form_save.user_functionary_created = get_object_or_404(
                Functionary, user=request.user.id)
            form_save.save()
            try:
                rraa = Inventory.on_site.get(pk=id_inventory)
                owner_rraa = Provider.on_site.filter(
                    entity_provider=rraa.entity_provider.id)
                notifications = {form_save.user_functionary_created.user.id}

                for user_provider in owner_rraa:
                    notifications.add(user_provider.user.id)
                url = settings.SITE_URL
                name = "El funcionario " + form_save.user_functionary_created.user.first_name + " ha hecho un comentario al registro administrativo " + inventory.title + " <a target='_blank' href='" + \
                    url+"detalle-inventario/" + \
                    str(id_inventory) + "'>Consulta aquí</a>"

                message = 'Se ha realizado un nuevo comentario al registro administrativo: "' + \
                    inventory.title + '".'

                for notify in notifications:
                    Notification.on_site.create(
                        name=name,
                        sent_to=get_object_or_404(
                            User, pk=notify),
                        module_from='BI',
                        message=message,
                        name_link='Consultar comentario del registro administrativo',
                        link=url+"detalle-inventario/" + str(id_inventory)
                    )
            except:
                return redirect('inventory:detail_inventory', inventory.id)

        return redirect('inventory:detail_inventory', inventory.id)


def reply_comment(request, id_inventory, id_comment):
    inventory = get_object_or_404(Inventory, pk=id_inventory)
    if request.method == 'GET':
        commentForm = CreateCommentForm()
        form = CreateCommentForm()
        return render(request, 'register/reply_comment.html', {
            'commentForm': commentForm,
        })
    else:
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.inventory = inventory
            form_save.user_functionary_created = get_object_or_404(
                Functionary, user=request.user.id)
            form_save.comment = get_object_or_404(
                CommentInventory, pk=id_comment)
            form_save.save()
            try:
                rraa = Inventory.on_site.get(pk=id_inventory)
                owner_rraa = Provider.on_site.filter(
                    entity_provider=rraa.entity_provider.id)
                notifications = {form_save.user_functionary_created.user.id}

                for user_provider in owner_rraa:
                    notifications.add(user_provider.user.id)
                url = settings.SITE_URL
                name = "El funcionario " + form_save.user_functionary_created.user.first_name + " ha hecho un comentario al registro administrativo " + inventory.title + " <a target='_blank' href='" + \
                    url+"detalle-inventario/" + \
                    str(id_inventory) + "'>Consulta aquí</a>"

                message = 'Se ha realizado un nuevo comentario al registro administrativo: "' + \
                    inventory.title + '".'

                for notify in notifications:
                    Notification.on_site.create(
                        name=name,
                        sent_to=get_object_or_404(
                            User, pk=notify),
                        module_from='BI',
                        message=message,
                        name_link='Consultar comentario del registro administrativo',
                        link=url+"detalle-inventario/" + str(id_inventory)
                    )
            except:
                return redirect('inventory:detail_inventory', inventory.id)

        return redirect('inventory:detail_inventory', inventory.id)


def sample_data(request):
    return render(request, 'register/sample_data.html')


@check_user(['Proveedor'], 'login')
def inventory_create(request):
    if request.method == "GET":
        form_create_inventory = CreateInventoryForm()
        divipolas = Divipola.on_site.filter(parent=None)
        tdivipolas_count = TDivipola.on_site.all().count()
        return render(
            request,
            'register/inventory_create.html',
            {
                'form_create_inventory': form_create_inventory,
                'divipolas': divipolas,
                'tdivipolas_count': tdivipolas_count - 1,
            }
        )
    else:
        form_create_inventory = CreateInventoryForm(
            request.POST, request.FILES)
        if request.user.groups.filter(name='Proveedor').exists():
            user_id = request.user.id
            data_user = Provider.objects.get(user=user_id)
            entity_provider = ProviderEntity.objects.get(
                pk=data_user.entity_provider.id)
            if form_create_inventory.is_valid():
                new = form_create_inventory.save(commit=False)
                new.entity_provider = entity_provider
                new.save()
                try:
                    form_create_inventory.save_m2m()
                    id_form = form_create_inventory.instance.id
                    url = settings.SITE_URL
                    data_user_unit = Unit_Central.on_site.all()
                    data_user_func = Functionary.on_site.all()
                    notifications = {user_id}
                    for item in data_user_unit:
                        notifications.add(item.user.id)

                    for item in data_user_func:
                        notifications.add(item.user.id)

                    name = "Se agregó un nuevo registro administrativo, consultar <a target='_blank' href='" + \
                        url+"detalle-inventario/" + \
                        str(id_form) + "'>aquí</a>"
                    message = "Se agregó un nuevo registro administrativo" + \
                        request.POST['title']
                    link = url+"detalle-inventario/" + str(id_form)

                    recipients = User.objects.filter(pk__in=notifications)
                    create_notifications_and_send_emails_async([
                        Notification(
                            name=name,
                            sent_to=recipient,
                            module_from="IN",
                            message=message,
                            name_link='Consultar registro administrativo',
                            link=link,
                            site_id=get_current_site(request).id,
                        )
                        for recipient in recipients
                    ])
                except:
                    return redirect('inventory:inventory_list')
            else:
                form_create_inventory.errors
                return render(
                    request,
                    'register/inventory_create.html',
                    {
                        'form_create_inventory': form_create_inventory,
                    }
                )
    return redirect('inventory:inventory_list')


def get_child_divipola(request, id_divipola):
    node = get_object_or_404(Divipola, pk=id_divipola)
    note_children = Divipola.objects.filter(parent=node)
    data = {}
    for note in note_children:
        data[note.id] = {
            'id': note.id,
            'name': note.name,
            'type': note.tdivipola.name,
        }

    return JsonResponse(data)


@check_user(['Proveedor'], 'login')
def edit_inventory(request, id):
    inventory = get_object_or_404(
        Inventory, pk=id, site__id=get_current_site(request).id)
    if request.method == "GET":
        edit = True
        form_create_inventory = CreateInventoryForm(instance=inventory)

        return render(
            request,
            'register/inventory_create.html',
            {
                'form_create_inventory': form_create_inventory,
                'edit': edit,
                'id': id,
            }
        )
    else:
        form = CreateInventoryForm(
            request.POST, request.FILES, instance=inventory)
        user_id = request.user.id
        if form.is_valid():
            form.save()
            try:
                id_form = form.instance.id
                url = settings.SITE_URL
                data_user_unit = Unit_Central.on_site.all()
                data_user_func = Functionary.on_site.all()
                notifications = {user_id}
                for item in data_user_unit:
                    notifications.add(item.user.id)

                for item in data_user_func:
                    notifications.add(item.user.id)

                name = "Se ha editado el registro administrativo:" + request.POST['title']+", consultar <a target='_blank' href='" + \
                    url+"detalle-inventario/" + \
                    str(id_form) + "'>aquí</a>"
                message = "Se ha editado el registro administrativo" + \
                    request.POST['title']
                link = url+"detalle-inventario/" + str(id_form)

                recipients = User.objects.filter(pk__in=notifications)
                create_notifications_and_send_emails_async([
                    Notification(
                        name=name,
                        sent_to=recipient,
                        module_from="IN",
                        message=message,
                        name_link='Consultar registro administrativo',
                        link=link,
                        site_id=get_current_site(request).id,
                    )
                    for recipient in recipients
                ])
            except:
                return redirect('inventory:inventory_list')

    return redirect('inventory:inventory_list')


def filter_user_inventory(request, id_user):
    users = get_object_or_404(User, pk=id_user)
    users_list = Inventory.objects.filter(
        site__id=get_current_site(request).id, user_asociate=users).order_by('-created_date')

    template = loader.get_template('register/inventory_finder.html')
    context = {
        'users_list': users_list,
    }
    return HttpResponse(template.render(context, request))


def filter_status_inventory(request, id_status):
    status = get_object_or_404(Inventory, pk=id_status)
    status_list = Inventory.objects.filter(
        site__id=get_current_site(request).id, user_asociate=status).order_by('-created_date')

    template = loader.get_template('register/inventory_finder.html')
    context = {
        'status_list': status_list,
    }
    return HttpResponse(template.render(context, request))


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
                try:
                    q.save()
                    owner_rraa = Provider.on_site.filter(
                        entity_provider=inventory.entity_provider.id)
                    url = settings.SITE_URL
                    notifications = {request.user.id}
                    for item in owner_rraa:
                        notifications.add(item.user.id)

                    for notify in notifications:
                        name = "Se está siguiendo el registro administrativo:" + inventory.title + ", consultar <a target='_blank' href='" + \
                            url+"detalle-inventario/" + \
                            str(id_inventory) + "'>aquí</a>"
                        message = "Se está siguiendo el registro administrativo" + inventory.title

                        Notification.on_site.create(
                            name=name,
                            sent_to=get_object_or_404(
                                User, pk=notify),
                            module_from="IN",
                            message=message,
                            name_link='Se está siguiendo el registro administrativo',
                            link=url+"detalle-inventario/" + str(id_inventory)
                        )
                except:
                    return JsonResponse({'fail': 'True'})
            return JsonResponse({'success': 'True'})
        except:
            return JsonResponse({'fail': 'True'})


@check_user(['Funcionario', 'Proveedor'], 'login')
def get_inventory_follow(request, id_inventory):
    if request.user.is_authenticated:
        try:
            inventory = Inventory.objects.get(pk=id_inventory)
        except Inventory.DoesNotExist:
            inventory = None

        try:
            if inventory is not None:
                follow = FollowInventory.objects.get(
                    user=request.user, inventory=inventory
                )
            else:
                follow = None
        except FollowInventory.DoesNotExist:
            follow = None

        if follow is not None:
            return JsonResponse({'follow': 'True'})
        else:
            return JsonResponse({'follow': 'False'})


def view_sample_data(request, id_inventory):
    inventory = get_object_or_404(Inventory, pk=id_inventory)
    if inventory.type_format_data_asociate.type_format == '.csv':
        viewer = pandas.read_csv(inventory.file_example_sample_data.path)
    elif inventory.type_format_data_asociate.type_format == '.xlsx':
        viewer = pandas.read_excel(inventory.file_example_sample_data.path)

    mydict = {
        "df": viewer.to_html(table_id='sample-data', classes='table')
    }
    return render(request, 'register/view_sample_data.html', context=mydict)


def quality_test(request, id_inventory):
    if request.user.is_authenticated:
        data_user = ""
        if request.user.groups.filter(name='Proveedor').exists():
            user_id = request.user.id
            data_user = User.objects.get(pk=user_id)

            try:
                inventory = Inventory.objects.get(pk=id_inventory)
            except Inventory.DoesNotExist:
                inventory = None

            if inventory is not None:
                if request.method == "GET":
                    try:
                        test = QualityTest.on_site.get(inventory=inventory.id)
                    except QualityTest.DoesNotExist:
                        test = None

                    if test is None:
                        quality_test_form = QualityTestForm()
                        return render(
                            request,
                            'register/test_quality.html',
                            {
                                'form': quality_test_form,
                                'inventory': inventory
                            }
                        )
                    else:
                        total = int(test.quality_question_1)+int(test.quality_question_2)+int(
                            test.quality_question_3)+int(test.quality_question_4)+int(test.quality_question_5)
                        total = total/5
                        return render(
                            request,
                            'register/test_quality.html',
                            {
                                'total': total,
                                'inventory': inventory,
                                'test': test,
                            }
                        )
                else:
                    form = QualityTestForm(request.POST)
                    if form.is_valid():
                        form = form.save(commit=False)
                        form.user = data_user
                        form.inventory = inventory
                        form.save()
                        return redirect('profile')
            else:
                return redirect('profile')
        else:
            return redirect('profile')
    else:
        return redirect('profile')


def quality_test_delete(request, id_test):
    test = get_object_or_404(
        QualityTest, pk=id_test, site__id=get_current_site(request).id)
    test.delete()
    return redirect('profile')
