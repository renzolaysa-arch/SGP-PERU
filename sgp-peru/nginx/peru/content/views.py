from random import normalvariate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from .models import Banner, Benefit, Gallery, Tags, Documents, News, Letter, Vocabulary, FAQs, Visitor, Testimony
from projects.models import Project
from notifications.models import Notification
from .forms import CommentDocumentForm, NewDocumentForm, CreateTestimonyForm
from django.template import loader
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from newsletter.forms import NewsLetterForm
from django.contrib.auth.models import User
from django.urls import reverse
from users.decorators import check_user
from .filters import NewFilter
from inventory.filters import InventoryFilter
from providers.filters import ProviderEntityFilter
from django.core.paginator import Paginator
from django.db.models import Q
from providers.models import ProviderEntity
from inventory.models import Inventory
from django.utils import timezone
from django.conf import settings
from django.template import RequestContext
from django.db.models.functions import Lower
import re


# Create your views here.


def home(request):
    banner_list = Banner.objects.filter(
        site__id=get_current_site(request).id).order_by('-created_date')[:5]
    benefit_list = Benefit.objects.filter(
        site__id=get_current_site(request).id).order_by('-created_date')[:10]

    new_list = News.objects.filter(
        site__id=get_current_site(request).id, type_choice='New').order_by('-created_date')[:6]

    content_academy_list = News.objects.filter(
        site__id=get_current_site(request).id, type_choice='C.E').order_by('-created_date')[:6]

    project_list = Project.objects.filter(
        site__id=get_current_site(request).id).order_by('-created_date')[:6]

    providers_count = ProviderEntity.objects.filter(
        site__id=get_current_site(request).id).count()

    rraa_count = Inventory.on_site.filter(
        modified_date__date=timezone.now()).count()
    testimony = Testimony.on_site.all().order_by('-created_date')[:4]
    rraa_list = Inventory.on_site.filter(
    ).order_by('-created_date')[:4]

    template = loader.get_template('content/home.html')
    context = {
        'project_list': project_list,
        'providers_count': providers_count,
        'rraa_count': rraa_count,
        'rraa_list': rraa_list,
        'new_list': new_list,
        'content_academy_list': content_academy_list,
        'banner_list': banner_list,
        'benefit_list': benefit_list,
        'testimony': testimony,
    }
    return HttpResponse(template.render(context, request))


def glosary(request, letter='a'):
    active = "active"
    
    letter_list = Letter.on_site.annotate(
        lower_name=Lower('name_letter')
    ).order_by(
        'lower_name', 'name_letter'
    ).values()
    
    try:
        letter_item = Letter.on_site.filter(name_letter=letter.upper()).first()
    except Letter.DoesNotExist:
        letter_item = None
    vocabularies = None
    vocabulary_total = 0
    vocabulary_page = 0
    vocabularies_page_obj = 0
    try:   
        if letter_item is not None:
            vocabularies = Vocabulary.on_site.filter(letter=letter_item.id).order_by('word').values() 
    except Vocabulary.DoesNotExist:
        vocabularies = None

    if vocabularies is not None:
        page_cant = 8
        paginated_filter_vocabularies = Paginator(vocabularies, page_cant)
        page_number = request.GET.get("page")
        if page_number is None:
            page_number = 1
        vocabularies_page_obj = paginated_filter_vocabularies.get_page(page_number)
        vocabulary_total = paginated_filter_vocabularies.count
        page = paginated_filter_vocabularies.page(page_number).object_list
        vocabulary_page = ((int(page_number)-1) * page_cant) + page.count()

    template = loader.get_template('content/glosary/glosary.html')
    context = {
        'letter_list': letter_list,
        'letter_item': letter_item,
        'active': active,
        'letter': letter.upper(),
        'vocabularies': vocabularies_page_obj,
        'vocabulary_total': vocabulary_total,
        'vocabulary_page': str(vocabulary_page),
    }
    return HttpResponse(template.render(context, request))


def glosary_filter(request, letter):
    active = "active"
    letter_list = Letter.on_site.filter().order_by('name_letter').values()
    try:
        letter_item = Letter.on_site.filter(name_letter=letter.upper()).first()
    except Letter.DoesNotExist:
        letter_item = None
    vocabularies = None
    vocabulary_total = 0
    vocabulary_page = 0
    vocabularies_page_obj = 0    
    try:   
        if letter_item is not None:
            vocabularies = Vocabulary.on_site.filter(letter=letter_item.id).order_by('word').values() 
    except Vocabulary.DoesNotExist:
        vocabularies = None

    if vocabularies is not None:
        page_cant = 8
        paginated_filter_vocabularies = Paginator(vocabularies, page_cant)
        page_number = request.GET.get("page")
        if page_number is None:
            page_number = 1
        vocabularies_page_obj = paginated_filter_vocabularies.get_page(page_number)
        vocabulary_total = paginated_filter_vocabularies.count
        page = paginated_filter_vocabularies.page(page_number).object_list
        vocabulary_page = ((int(page_number)-1) * page_cant) + page.count()

    template = loader.get_template('content/glosary/glosary_filter.html')
    context = {
        'letter_list': letter_list,
        'letter_item': letter_item,
        'active': active,
        'letter': letter.upper(),
        'vocabularies': vocabularies_page_obj,
        'vocabulary_total': vocabulary_total,
        'vocabulary_page': str(vocabulary_page),
    }
    return HttpResponse(template.render(context, request))


def frequent_questions(request):
    faqs_list = FAQs.on_site.all()

    template = loader.get_template(
        'content/frequent_questions/frequent_questions.html')

    page_cant = 8
    paginated_filter_faqs = Paginator(faqs_list, page_cant)
    page_number = request.GET.get("page")
    if page_number is None:
        page_number = 1
    vocabularies_page_obj = paginated_filter_faqs.get_page(page_number)
    faqs_total = paginated_filter_faqs.count
    page = paginated_filter_faqs.page(page_number).object_list
    faqs_page = ((int(page_number)-1) * page_cant) + page.count()

    context = {
        'faqs_list': vocabularies_page_obj,
        'faqs_total': faqs_total,
        'faqs_page': str(faqs_page),
    }
    return HttpResponse(template.render(context, request))


@check_user(['Unidad Central', 'Proveedor', 'Funcionario'], 'login')
def document(request, id_document):
    document = get_object_or_404(Documents, pk=id_document)
    if request.method == "GET":
        user = request.user
        edit = False
        if document.assigned_to == user or document.copy_to.filter(username=user).exists():
            if document.assigned_to == user and document.approved != True:
                edit = True
            return render(request, 'content/document.html', {
                'document': document,
                'form': CommentDocumentForm(instance=document),
                'edit': edit,
            })
        else:
            return redirect('contents:home')
    else:
        form = CommentDocumentForm(request.POST, instance=document)
        if form.is_valid():
            form.save()
            return redirect('contents:document', id_document=id_document)
        else:
            form.errors
            return render(request, 'content/document.html', {
                'document': document,
                'form': CommentDocumentForm(instance=document),
                'edit': True,
            })


@check_user(['Unidad Central', 'Funcionario'], 'login')
def newDocument(request):
    if request.method == 'GET':
        return render(request, 'content/new_document.html', {
            'form': NewDocumentForm(),
        })
    else:
        form = NewDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            id_doc = form.instance.id
            assigned_to = int(request.POST['assigned_to'])
            all_copy_to = form.cleaned_data.get('copy_to')
            s = [int(s) for s in re.findall(r'-?\d+\.?\d*', all_copy_to)]
            notifications = {assigned_to}
            url = settings.SITE_URL

            for copy_to in s:
                notifications.add(copy_to)

            for notify in notifications:
                if notify == assigned_to and 'requires_approval' in request.POST:
                    name = "Se agregó un nuevo documento y <b>requiere su aprobación</b>, consultar <a target='_blank' href='" + \
                        url+"documento/" + \
                        str(id_doc) + "'>aquí</a>"
                    message = "Se agregó un nuevo documento y <b>requiere su aprobación.</b>"
                elif 'requires_approval' in request.POST:
                    name = "Se agregó un nuevo documento y <b>requiere aprobación</b>, consultar <a target='_blank' href='" + \
                        url+"documento/" + \
                        str(id_doc) + "'>aquí</a>"
                    message = "Se agregó un nuevo documento y <b>requiere aprobación.</b>"
                else:
                    name = "Se agregó un nuevo documento informativo, consultar <a target='_blank' href='" + \
                        url+"documento/" + \
                        str(id_doc) + "'>aquí</a>"
                    message = "Se agregó un nuevo documento informativo"

                Notification.on_site.create(
                    name=name,
                    sent_to=get_object_or_404(
                        User, pk=notify),
                    module_from="CO",
                    message=message,
                    name_link='Consultar documento',
                    link=url+"documento/" + str(id_doc)
                )
            return redirect('contents:home')
        else:
            return render(request, 'content/new_document.html', {
                'form': form,
            })


@check_user(['Unidad Central', 'Funcionario'], 'login')
def deleteDocument(request, id_document):
    document = get_object_or_404(Documents, pk=id_document)
    document.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def new(request):
    new_list = News.objects.filter(
        site__id=get_current_site(request).id, type_choice='New').order_by('-created_date')[2:]
    new_1 = News.objects.filter(
        site__id=get_current_site(request).id, type_choice='New').order_by('-created_date')[0:1]
    new_2 = News.objects.filter(
        site__id=get_current_site(request).id, type_choice='New').order_by('-created_date')[1:2]

    filter_new = NewFilter(
        request.GET,
        queryset=new_list
    )
    page_cant = 8
    paginated_filter_news = Paginator(filter_new.qs, page_cant)
    page_number = request.GET.get("page")
    if page_number is None:
        page_number = 1
    new_page_obj = paginated_filter_news.get_page(page_number)
    new_total = paginated_filter_news.count
    page = paginated_filter_news.page(page_number).object_list
    new_page = ((int(page_number)-1) * page_cant) + page.count()
    template = loader.get_template('content/news.html')
    context = {
        'new_1': new_1,
        'new_2': new_2,
        'new_list': new_page_obj,
        'filter': filter_new,
        'new_total': new_total,
        'new_page': str(new_page),
    }
    return HttpResponse(template.render(context, request))


def detail_new(request, id_new):
    new = get_object_or_404(News, pk=id_new)
    list_new_tags = new.tag_asociate.all()

    list_for_news = []
    list_related_news = []

    for item in list_new_tags:
        project_related = News.on_site.filter(tag_asociate=item, type_choice="New").distinct()
        list_for_news.append(project_related)
        for item in list_for_news:
            for it in item:
                if it not in list_related_news:
                    list_related_news.append(it)

    galleries = Gallery.objects.filter(
        galleryList=new.id

    )
    count_visitor = Visitor.on_site.filter(
        type_model_visited="Noticias", id_model_visited=id_new
    ).count()
    return render(
        request,
        'content/detail_news.html',
        {
            'new_item': new,
            'galleries': galleries,
            'news_related': list_related_news,
            'count_visitor': count_visitor
        }
    )


def filter_search_new(request):
    queryset = News.objects.filter(
        site__id=get_current_site(request).id, type_choice="New").order_by('-created_date')
    new_1 = News.objects.filter(
        site__id=get_current_site(request).id, type_choice="New").order_by('-created_date')[0:1]
    new_2 = News.objects.filter(
        site__id=get_current_site(request).id, type_choice="New").order_by('-created_date')[1:2]

    filter_new = NewFilter(
        request.GET,
        queryset=queryset
    )
    page_cant = 8
    paginated_filter_news = Paginator(filter_new.qs, page_cant)
    page_number = request.GET.get("page")
    if page_number is None:
        page_number = 1
    new_page_obj = paginated_filter_news.get_page(page_number)
    new_total = paginated_filter_news.count
    page = paginated_filter_news.page(page_number).object_list
    new_page = ((int(page_number)-1) * page_cant) + page.count()
    template = loader.get_template('content/news.html')
    context = {
        'new_1': new_1,
        'new_2': new_2,
        'new_list': new_page_obj,
        'filter': filter_new,
        'new_total': new_total,
        'new_page': str(new_page),
    }
    return HttpResponse(template.render(context, request))


def letter_list(request):
    letter_list = News.objects.filter(
        site__id=get_current_site(request).id).order_by('-created_date')[2:]
    template = loader.get_template('content/news.html')
    context = {
        'letter_list': letter_list,
    }
    return HttpResponse(template.render(context, request))


def academy_content(request):
    new_list = News.objects.filter(
        site__id=get_current_site(request).id, type_choice='C.E').order_by('-created_date')[2:]
    new_1 = News.objects.filter(
        site__id=get_current_site(request).id, type_choice='C.E').order_by('-created_date')[0:1]
    new_2 = News.objects.filter(
        site__id=get_current_site(request).id, type_choice='C.E').order_by('-created_date')[1:2]

    filter_new = NewFilter(
        request.GET,
        queryset=new_list
    )
    page_cant = 8
    paginated_filter_news = Paginator(filter_new.qs, page_cant)
    page_number = request.GET.get("page")
    if page_number is None:
        page_number = 1
    new_page_obj = paginated_filter_news.get_page(page_number)
    new_total = paginated_filter_news.count
    page = paginated_filter_news.page(page_number).object_list
    new_page = ((int(page_number)-1) * page_cant) + page.count()
    template = loader.get_template('content/main_academy_content.html')
    context = {
        'new_1': new_1,
        'new_2': new_2,
        'new_list': new_page_obj,
        'filter': filter_new,
        'new_total': new_total,
        'new_page': str(new_page),
    }
    return HttpResponse(template.render(context, request))


def detail_academy_content(request, id_new):
    new = get_object_or_404(News, pk=id_new)
    list_new_tags = new.tag_asociate.all()

    list_for_news = []
    list_related_news = []

    for item in list_new_tags:
        project_related = News.on_site.filter(tag_asociate=item, type_choice="C.E").distinct()
        list_for_news.append(project_related)
        for item in list_for_news:
            for it in item:
                if it not in list_related_news:
                    list_related_news.append(it)

    galleries = Gallery.objects.filter(
        galleryList=new.id
    )
    count_visitor = Visitor.on_site.filter(
        type_model_visited="Contenido Educativo", id_model_visited=id_new
    ).count()
    return render(
        request,
        'content/detail_academy_content.html',
        {
            'new_item': new,
            'galleries': galleries,
            'news_related': list_related_news,
            'count_visitor': count_visitor
        }
    )


def filter_search_academy_content(request):
    queryset = News.objects.filter(
        site__id=get_current_site(request).id, type_choice='C.E').order_by('-created_date')
    new_1 = News.objects.filter(
        site__id=get_current_site(request).id, type_choice='C.E').order_by('-created_date')[0:1]
    new_2 = News.objects.filter(
        site__id=get_current_site(request).id, type_choice='C.E').order_by('-created_date')[1:2]

    filter_new = NewFilter(
        request.GET,
        queryset=queryset
    )
    page_cant = 8
    paginated_filter_news = Paginator(filter_new.qs, page_cant)
    page_number = request.GET.get("page")
    if page_number is None:
        page_number = 1
    new_page_obj = paginated_filter_news.get_page(page_number)
    new_total = paginated_filter_news.count
    page = paginated_filter_news.page(page_number).object_list
    new_page = ((int(page_number)-1) * page_cant) + page.count()
    template = loader.get_template('content/main_academy_content.html')
    context = {
        'new_1': new_1,
        'new_2': new_2,
        'new_list': new_page_obj,
        'filter': filter_new,
        'new_total': new_total,
        'new_page': str(new_page),
    }
    return HttpResponse(template.render(context, request))


def testimony(request):
    # se asigna el id para saber a qué usuario creó el testimonio
    user_id = request.user.id
    user_testimony = User.objects.get(user=user_id)
    list_testimony = Testimony.on_site.all().order_by('-created_date')

    return render(request, 'content/templates/home.html',
                  {
                      'list_testimony': list_testimony,
                  })


def create_testimony(request):
    user_id = request.user.id
    user_testimony = User.objects.get(user=user_id)
    form_create_testimony = CreateTestimonyForm()
    form = CreateTestimonyForm(request.POST)
    if form.is_valid():
        form = form.save(commit=False)
        form.user_functionary_created = user_testimony
        form.save()
    else:
        form = CreateTestimonyForm(request.POST)
        return render(request, 'content/templates/create-testimony.html',
                      {
                          'form': form,
                          'form_create_testimony': form_create_testimony,
                      })
    return redirect('home')

def page_not_found(request):
     return render (request, 'content/404.html')
    



def return_filter_inventory(request):
    queryset = Inventory.on_site.all()
    
    filter_inventory = InventoryFilter(
        request.GET,
        queryset=queryset
    )

    return render(request, 'content/menu_filter/menu_filter_inventory.html',
    {
        'filter_inventory': filter_inventory,
    })

def return_filter_provider(request):
    queryset = ProviderEntity.on_site.all()
    
    filter_provider = ProviderEntityFilter(
        request.GET,
        queryset=queryset
    )
    return render(request, 'content/menu_filter/menu_filter_provider.html',
    {
        'filter_provider': filter_provider
    })