from django.shortcuts import redirect, render, get_object_or_404
from users.models import Functionary
from .models import ThemeThread, CommentThread
from users.models import User
from notifications.models import Notification
from .forms import CreateCommentThreadForm, CreateThemeThreadForm
from datetime import datetime
from django.conf import settings

# Create your views here.


def binacle(request):
    # asociar el id del funcionario para que se guarde al crearlo
    user_id = request.user.id
    user_functionary = Functionary.objects.get(user=user_id)
    list_tread = ThemeThread.on_site.all().order_by('-created_date')

    return render(request, 'users/functionary/binacle.html',
    {
        'list_tread': list_tread,
    })


class comments_list:
    def __init__(self, id, commentary, functionary_commented, hour, owner_comment):
        self.id = id
        self.commentary = commentary
        self.functionary_commented = functionary_commented
        self.hour = hour
        self.owner_comment = owner_comment


def thread_comments(request, id):
    user_id = request.user.id
    user_functionary = Functionary.objects.filter(user=user_id).first()
    if user_functionary:
        item_thread = ThemeThread.objects.get(pk=id)
        form_create_comments = CreateCommentThreadForm()

        comments_tread = CommentThread.on_site.filter(
            threadt_to_comment=id).order_by('-created_date')
        date_format_str = '%d/%m/%Y %H:%M:%S.%f'
        date_2 = datetime.now()
        date_now = date_2.strftime(date_format_str)
        # creating list
        list = []
        owner_thread = False
        if item_thread.user_functionary_created.id == user_functionary.id:
            owner_thread = True



        def calculate_hours(prov):
            date_create = prov.created_date.strftime(date_format_str)
            start = datetime.strptime(date_create, date_format_str)
            end = datetime.strptime(date_now, date_format_str)
            diff = end - start
            diff_in_hours = int(diff.total_seconds() / 3600)
            if diff_in_hours < 1:
                diff_in_hours = 0
            return diff_in_hours
        
        owner_comment = False
        for item in comments_tread:
            owner_comment = False
            if item.functionary_commented.id == user_functionary.id:
                owner_comment = True
            hour = calculate_hours(item)
            list.append(comments_list(item.id, item.commentary, item.functionary_commented, hour, owner_comment))
    return render(request, 'users/functionary/content-binacle.html',
    {
        'comments_for_tread': list,
        'form_create_comments': form_create_comments,
        'id_thread':id,
        'id_functionary': user_functionary.id,
        'item_thread':item_thread,
        'owner_thread':owner_thread,
        'owner_comment':owner_comment,
    })


def create_comments(request, id_thread, id_functionary):
    user_id = request.user.id
    user_functionary = Functionary.objects.filter(user=user_id).first()
    if user_functionary:
        thread = ThemeThread.objects.get(id=id_thread)
        #user_propietary_thread =
        form = CreateCommentThreadForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.threadt_to_comment = thread
            form.functionary_commented = user_functionary
            form.save()
            name = "El funcionario "+ user_functionary.user.first_name +" ha hecho un comentario, ve a mi perfil y responde respecto! "
            url = settings.SITE_URL
            message='Se ha realizado un nuevo comentario al hilo: "' + thread.name_thread + '".'
            Notification.on_site.create(
                name=name,
                sent_to= get_object_or_404(
                    User, pk=thread.user_functionary_created.user.id),
                module_from='BI',
                message=message,
                name_link='Consultar comentario en la sala de bitácora',
                link=url+"usuario/perfil/"
            )
        else:
            form = CreateCommentThreadForm(request.POST)
            return render(request, 'users/functionary/content-binacle.html', {'form': form})
    return redirect('profile')
    

def create_thread(request):
    user_id = request.user.id
    user_functionary = Functionary.objects.get(user=user_id)
    form_create_thread = CreateThemeThreadForm()
    form = CreateThemeThreadForm(request.POST)
    if form.is_valid():
        form = form.save(commit=False)
        form.user_functionary_created = user_functionary
        form.save()
        url = settings.SITE_URL
        user_functionary_list = Functionary.on_site.all()
        message="El funcionario "+ user_functionary.user.first_name +" ha creado un nuevo hilo en la sala de bitácora: " + request.POST['name_thread']

        name = "El funcionario "+ user_functionary.user.first_name +" ha creado un nuevo hilo en la sala de bitácora, ve a mi perfil y comenta al respecto! "
        for item in user_functionary_list:
            Notification.on_site.create(
                name=name,
                sent_to=get_object_or_404(
                    User, pk=item.user.id),
                module_from='BI',
                message=message,                
                name_link='Consultar hilo en la sala de bitácora',
                link=url+"usuario/perfil/"
            )
    else:
        form = CreateThemeThreadForm(request.POST)
        return render(request, 'users/functionary/binacle-create-thread.html',
        {
            'form': form,
            'form_create_thread':form_create_thread,
        })
    return redirect('profile')

def delete_thread(request, id_thread):
    thread = ThemeThread.on_site.filter(pk=id_thread).first()
    if request.method == "POST":
        thread.delete()
        # return HttpResponseRedirect("/")
        return redirect('/usuario/perfil/')
    return render(request, '/usuario/perfil/')


def delete_comment(request, id_comment):
    comment = CommentThread.on_site.filter(pk=id_comment).first()
    if request.method == "POST":
        comment.delete()
        # return HttpResponseRedirect("/")
        return redirect('/usuario/perfil/')
    return render(request, '/usuario/perfil/')

