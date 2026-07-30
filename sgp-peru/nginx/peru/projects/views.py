from django.shortcuts import render
from users.decorators import check_user
from .models import Project, TagsProject
from users.models import Provider, User
from notifications.models import Notification
from .filters import ProjectFilter
from .forms import FilterOrderForm, FilterProjectForm, CreateProjectForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings

# Create your views here.


@check_user(['Unidad Central', 'Proveedor', 'Funcionario'], 'login')
def list_projects(request):
    order_by = request.GET.get("order")

    if order_by is not None and order_by != '':
        queryset = Project.objects.filter(
            site__id=get_current_site(request).id).order_by(order_by)
    else:
        queryset = Project.objects.filter(
            site__id=get_current_site(request).id).order_by('-created_date')

    filter_project = ProjectFilter(
        request.GET,
        queryset=queryset
    )
    form_order_by = FilterOrderForm()
    form_filter_project = FilterProjectForm()
    page_cant = 6
    paginated_filter_project = Paginator(filter_project.qs, page_cant)
    page_number = request.GET.get("page")
    if page_number is None:
        page_number = 1
    project_page_obj = paginated_filter_project.get_page(page_number)
    project_total = paginated_filter_project.count
    page = paginated_filter_project.page(page_number).object_list
    project_page = ((int(page_number)-1) * page_cant) + page.count()

    return render(
        request,
        'projects/list_projects.html',
        {
            'filter': filter_project,
            'form_filter_project': form_filter_project,
            'project_page_obj': project_page_obj,
            'project_total': project_total,
            'project_page': str(project_page),
            'form_order_by': form_order_by,
        }
    )


@check_user(['Unidad Central', 'Proveedor', 'Funcionario'], 'login')
def projects(request, id):
    project = get_object_or_404(Project, pk=id)

    list_projects_tags = project.tag_project.all()

    list_for_projects = []
    list_related_projects = []
    for item in list_projects_tags:
        project_related = Project.on_site.filter(tag_project=item).distinct()
        list_for_projects.append(project_related)
        for item in list_for_projects:
            for it in item:
                if it not in list_related_projects:
                    list_related_projects.append(it)

    return render(
        request,
        'projects/projects.html',
        {
            'project_item': project,
            'project_related': list_related_projects,
        }
    )


def handle_uploaded_file(f):
    with open('media/uploads/projects/'+str(f), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@check_user(['Unidad Central'], 'login')
def create_project(request):
    if request.method == "GET":
        form_create_project = CreateProjectForm()
        return render(
            request,
            'projects/project_create.html',
            {
                'form_create_project': form_create_project,
            }
        )
    else:
        form = CreateProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            try:
                id_form = form.instance.id
                owner_provider = Provider.on_site.filter(
                    entity_provider=int(request.POST['provider_any_project']))
                url = settings.SITE_URL
                name = "Se ha creado un nuevo proyecto y se le ha sido asignado como entidad proveedora, <a target='_blank' href='" + \
                    url+"proyecto/" + \
                    str(id_form) + "'>Consultalo aquí</a>"
                for item in owner_provider:
                    message = 'Se ha creado un nuevo proyecto "' + \
                        request.POST['name'] + \
                        '" y le han asignado como entidad proveedora, Haz clic en "Ver más" para ver el detalle'
                    Notification.on_site.create(
                        name=name,
                        sent_to=get_object_or_404(
                            User, pk=item.user.id),
                        module_from='BI',
                        message=message,
                        name_link='Consultar nuevo proyecto creado y asignado',
                        link=url+"proyecto/" + str(id_form)
                    )
                return redirect('projects:list_projects')
            except:
                return redirect('projects:list_projects')
        return redirect('projects:create_project')


@check_user(['Unidad Central', 'Funcionario'], 'login')
def edit_project(request, id):
    project = get_object_or_404(
        Project, pk=id, site__id=get_current_site(request).id)
    if request.method == "GET":
        edit = True
        form_create_project = CreateProjectForm(instance=project)

        return render(
            request,
            'projects/project_create.html',
            {
                'form_create_project': form_create_project,
                'edit': edit,
                'id': id,
            }
        )
    else:
        form = CreateProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()

    return redirect('projects:list_projects')


def delete_project(request, id):
    project = get_object_or_404(
        Project, pk=id, site__id=get_current_site(request).id)
    if request.method == "POST":

        project.delete()
        # return HttpResponseRedirect("/")
        return redirect('projects:list_projects')
    return render(request, 'projects/list_projects.html')
