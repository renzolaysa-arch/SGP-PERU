from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import ProviderEntity, Stage
from users.models import Unit_Central, User
from notifications.models import Notification
from .filters import ProviderEntityFilter, DocumentsEntityFilter
from .forms import FilterOrderForm, CreateProviderForm, FilterProviderForm, CreateDocumetsForm, FilterDocumentsProvider
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from users.decorators import check_user
from .models import ProviderEntity, ProviderSector
from inventory.models import Inventory
from projects.models import Project
from demand.models import Demands, Reception, Negotiation, Transfer, Preparation
from django.conf import settings
from demand.functions import calculate_process_board


@check_user(['Unidad Central', 'Funcionario'], 'login')
def provider_main(request):
    form_filter_provider = FilterProviderForm()
    total = ProviderEntity.objects.filter(
        site__id=get_current_site(request).id).count()
    total_day = ProviderEntity.objects.filter(site__id=get_current_site(
        request).id, created_date__date=timezone.now()).count()

    providers = ProviderEntity.objects.filter(
        site__id=get_current_site(request).id).order_by('-created_date')[:10]

    project_total = Project.objects.filter(
        site__id=get_current_site(request).id).count()

    rraa_total = Inventory.objects.filter(
        site__id=get_current_site(request).id).count()

    list_for_provider = {}
    sorted_best_providers = {}

    for prov in providers:
        provider_inventory_cont = len(Inventory.on_site.filter(
            entity_provider_id=prov.id).order_by('-entity_provider'))
        list_for_provider[prov.name] = provider_inventory_cont
        sorted_best_providers = dict(
            sorted(list_for_provider.items(), key=lambda x: x[1], reverse=True))

    sector = []

    provider_sector = ProviderSector.objects.all()

    for sector_item in provider_sector:
        dic = {"nombre": sector_item.name, "valor": count_sector(sector_item.id), "id": sector_item.id}
        sector.append(dic)

    return render(
        request,
        'providers/provider_main.html',
        {
            'total': total,
            'total_day': total_day,
            'form_filter_provider': form_filter_provider,
            'providers': providers,
            'providers_inventory': list_for_provider,
            'project_total': project_total,
            'rraa_total': rraa_total,
            'sorted_best_providers': sorted_best_providers,
            'sector': sector,
        }
    )


def count_sector(id_sector):
    return ProviderEntity.on_site.filter(sector=id_sector).count()


@check_user(['Unidad Central', 'Funcionario'], 'login')
def provider_list(request):
    order_by = request.GET.get("order")
    queryset = ProviderEntity.objects.filter(
        site__id=get_current_site(request).id).order_by('-created_date')

    list_for_provider = {}
    for prov in queryset:
        provider_inventory_cont = len(Inventory.on_site.filter(
            entity_provider_id=prov.id).order_by('-entity_provider'))
        list_for_provider[prov.name] = provider_inventory_cont
    if order_by is not None and order_by != '':
        queryset = ProviderEntity.objects.filter(
            site__id=get_current_site(request).id).order_by(order_by)

    filter_provider = ProviderEntityFilter(
        request.GET,
        queryset=queryset
    )

    form_order_by = FilterOrderForm()

    page_cant = 6
    paginated_filter_provider = Paginator(filter_provider.qs, page_cant)
    page_number = request.GET.get("page")
    if page_number is None:
        page_number = 1
    provider_page_obj = paginated_filter_provider.get_page(page_number)
    provider_total = paginated_filter_provider.count
    page = paginated_filter_provider.page(page_number).object_list
    provider_page = ((int(page_number)-1) * page_cant) + page.count()

    return render(
        request,
        'providers/provider_list.html',
        {
            'filter': filter_provider,
            'provider_page_obj': provider_page_obj,
            'provider_total': provider_total,
            'provider_page': str(provider_page),
            'form_order_by': form_order_by,
        }
    )


@check_user(['Unidad Central'], 'login')
def provider_create(request):
    if request.method == "GET":
        form_create_provider = CreateProviderForm()
        return render(
            request,
            'providers/provider_create.html',
            {
                'form_create_provider': form_create_provider,
            }
        )
    else:
        user_id = request.user.id
        user_unit = Unit_Central.on_site.get(user=user_id)
        form = CreateProviderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            try:
                url = settings.SITE_URL
                name = "La Unidad Central: " + user_unit.user.first_name + " ha creado una nueva entidad proveedora " + request.POST['name'] + " <a target='_blank' href='" + \
                    url+"proveedor/" + \
                    str(form.id) + "'>Consula aquí</a>"
                message = "La Unidad Central: " + user_unit.user.first_name + \
                    " ha creado una nueva entidad proveedora" + \
                    request.POST['name']

                Notification.on_site.create(
                    name=name,
                    sent_to=get_object_or_404(
                        User, pk=user_id),
                    module_from='PRV',
                    message=message,
                    name_link='Se ha creado una nueva entidad proveedora',
                    link=url
                )
            except:
                return redirect('providers:provider_create')
        else:
            return redirect('providers:provider_create')

    return redirect('providers:provider_list')


class activity_management_list:
    def __init__(self, id, title, url_reception, porcent_reception, reception_demand_process, url_negotiation, porcent_negotiation, negotiation_demand_process, url_transfer, porcent_transfer, transfer_demand_process, url_preparation, porcent_preparation, preparation_demand_process, url_evaluation, porcent_evaluation, evaluation_demand_process):
        self.id = id
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


@check_user(['Unidad Central', 'Funcionario'], 'login')
def provider_detail(request, provider_entity_id):
    form_filter_provider = FilterDocumentsProvider()
    provider = get_object_or_404(
        ProviderEntity, pk=provider_entity_id, site__id=get_current_site(request).id)
    documents_queryset = provider.providerdocuments_set.all()

    provider_form = CreateProviderForm(instance=provider)
    documents_form = CreateDocumetsForm(
        initial={'provider': provider_entity_id})

    filter_documents = DocumentsEntityFilter(
        request.GET,
        queryset=documents_queryset
    )

    page_cant = 6
    paginated_filter_documents = Paginator(filter_documents.qs, page_cant)
    page_number = request.GET.get("page")
    if page_number is None:
        page_number = 1
    documents_page_obj = paginated_filter_documents.get_page(page_number)

    documents_total = paginated_filter_documents.count
    page = paginated_filter_documents.page(page_number).object_list
    documents_page = ((int(page_number)-1) * page_cant) + page.count()

    demands = Demands.on_site.filter(provider_entity=provider_entity_id)
    demands_list = []

    for item in demands:
        id_demand = item.id
        # Process
        board = calculate_process_board(id_demand)

        demands_list.append(activity_management_list(
            item.id,
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

    inventory = Inventory.on_site.filter(entity_provider=provider_entity_id)

    page_cant = 6
    paginated_inventory = Paginator(inventory, page_cant)
    page_number = request.GET.get("page")
    if page_number is None:
        page_number = 1
    inventory_page_obj = paginated_inventory.get_page(page_number)

    inventory_total = paginated_inventory.count
    page = paginated_inventory.page(page_number).object_list
    inventory_page = ((int(page_number)-1) * page_cant) + page.count()

    return render(
        request,
        'providers/provider_detail.html',
        {
            "provider": provider,
            "documets_form": documents_form,
            "provider_form": provider_form,
            'form_filter_provider': form_filter_provider,
            'filter': filter_documents,
            'documents_page_obj': documents_page_obj,
            'documents_total': documents_total,
            'documents_page': documents_page,
            'demands_list': demands_list,
            'inventory_page_obj': inventory_page_obj,
            'inventory_total': inventory_total,
            'inventory_page': inventory_page
        }
    )


def handle_uploaded_file(f):
    with open('media/uploads/providers/documents/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def provider_document_create(request, provider_entity_id):
    if request.POST:
        f = CreateDocumetsForm(request.POST, request.FILES)
        if f.is_valid:
            handle_uploaded_file(request.FILES["documents"])
            f.save()
            return HttpResponseRedirect(reverse('providers:provider_detail', args=(provider_entity_id,)))


def provider_save(request, provider_entity_id):
    if request.POST:
        p = ProviderEntity.objects.get(pk=provider_entity_id)
        p = CreateProviderForm(request.POST, request.FILES, instance=p)
        p.save()
        return HttpResponseRedirect(reverse('providers:provider_detail', args=(provider_entity_id,)))
