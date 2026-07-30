from pyexpat import model
from tabnanny import verbose
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.db import models
from django.conf import settings
from .validators import SizeValidator, FileType
from django.contrib.auth.models import User, Group
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError, FieldError
from notifications.models import Notification
from django.shortcuts import get_object_or_404


class Banner(models.Model):
    title = models.CharField(
        verbose_name="Titulo",
        max_length=40,
        blank=False,
        null=False,
        default=''
    )
    sub_title = models.CharField(
        verbose_name="Sub Titulo",
        max_length=25,
        blank=False,
        null=False,
        default=''
    )
    description = models.TextField(
        verbose_name="Descripción",
        blank=False,
        null=False,
        default='',
        max_length=300,
    )
    url_name = models.CharField(
        verbose_name="Nombre del botón",
        max_length=255,
        blank=False,
        null=False,
        default=''
    )
    url_link = models.URLField(
        verbose_name="Enlace del botón",
        max_length=200,
        blank=False,
        null=False,
        default=''
    )
    background = models.ImageField(
        verbose_name="Imagen de fondo",
        upload_to='uploads/banner_home/background',
        blank=False,
        null=False,
        default='',
        validators=[SizeValidator(1920, 900)],
        help_text="Las imágenes debe ser exactamente de 1920x900 píxeles"
    )
    image = models.ImageField(
        verbose_name="Imagen previa del video",
        upload_to='uploads/banner_home/images',
        blank=False,
        null=False,
        default='',
        validators=[SizeValidator(760, 730)],
        help_text="Las imágenes debe ser exactamente de 760x730 píxeles"
    )
    youtube = models.CharField(
        verbose_name="Código del video de Youtube",
        max_length=255,
        blank=False,
        null=False,
        default='',
        help_text="Ejemplo Md57cPGB1"
    )
    site = models.ForeignKey(
        Site,
        verbose_name="Sitio",
        on_delete=models.CASCADE,
        default=settings.SITE_ID
    )
    objects = models.Manager()
    on_site = CurrentSiteManager()
    created_date = models.DateTimeField(
        verbose_name="Publicación",
        auto_now_add=True
    )
    modified_date = models.DateTimeField(
        verbose_name="Actualización",
        auto_now=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"


class Benefit(models.Model):
    title = models.CharField(
        verbose_name="Titulo",
        max_length=60,
        blank=False,
        null=False,
        default='',
    )
    description = models.TextField(
        verbose_name="Descripción",
        blank=False,
        null=False,
        default='',
        max_length=200,
    )
    icon = models.ImageField(
        verbose_name="Imagen de icono",
        upload_to='uploads/benefits_home/icon/',
        blank=False,
        null=False,
        default='',
        validators=[SizeValidator(60, 60)],
        help_text="Las imágenes debe ser exactamente de 60x60 píxeles"
    )
    site = models.ForeignKey(
        Site,
        verbose_name="Sitio",
        on_delete=models.CASCADE,
        default=settings.SITE_ID
    )
    objects = models.Manager()
    on_site = CurrentSiteManager()
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Publicación",
    )
    modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name="Actualización",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Beneficio"
        verbose_name_plural = "Beneficios"


class TDivipola(models.Model):
    name = models.CharField(
        verbose_name="Nombre",
        max_length=255,
        blank=False,
        null=False,
        default='',
    )
    sigla = models.CharField(
        verbose_name="Sigle",
        blank=False,
        null=False,
        default='',
        max_length=4,
    )
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        verbose_name="Padre",
        on_delete=models.CASCADE,
        default='',
    )
    site = models.ForeignKey(
        Site,
        verbose_name="Sitio",
        on_delete=models.CASCADE,
        default=settings.SITE_ID
    )
    objects = models.Manager()
    on_site = CurrentSiteManager()
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Publicación",
    )
    modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name="Actualización",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "TDivipola"
        verbose_name_plural = "TDivipolas"


class Divipola(models.Model):
    name = models.CharField(
        verbose_name="Nombre",
        max_length=255,
        blank=False,
        null=False,
        default='',
    )
    sigla = models.CharField(
        verbose_name="Sigle",
        blank=False,
        null=False,
        default='',
        max_length=4,
    )
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        verbose_name="Padre",
        on_delete=models.CASCADE,
        default='',
    )
    tdivipola = models.ForeignKey(
        TDivipola,
        verbose_name="Tipo",
        on_delete=models.CASCADE,
        default='',
    )
    site = models.ForeignKey(
        Site,
        verbose_name="Sitio",
        on_delete=models.CASCADE,
        default=settings.SITE_ID
    )
    objects = models.Manager()
    on_site = CurrentSiteManager()
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Publicación",
    )
    modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name="Actualización",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Divipola"
        verbose_name_plural = "Divipolas"


class menuList(models.Model):
    titleMenu = models.CharField(
        verbose_name="Título menú",
        max_length=255,
        blank=False,
        null=False,
        default=''
    )
    Menu_Type_Choices = [
        ('B.S', 'Busquedas Sugeridas'),
        ('M.H', 'Menu Hamburguesa'),
        ('N.A', 'Necesitas ayuda'),
        ('L.I', 'Links de interes'),
        ('R.S', 'Redes sociales'),
        ('S.F', 'Segundo Footer'),
    ]
    Menu_Choice = models.CharField(
        verbose_name="Tipo de menú",
        max_length=25,
        choices=Menu_Type_Choices,
        default='Busquedas Sugeridas'
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        default=settings.SITE_ID
    )

    def __str__(self):
        return self.titleMenu

    def ordered_menuitem_set(self):
        return self.menuitem_set.all().order_by('order')

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"


class MenuItem(models.Model):
    menuList = models.ForeignKey(
        menuList,
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    is_cleaned = False
    title = models.CharField(
        verbose_name="Titulo",
        max_length=255,
        blank=False,
        null=False,
        default=''
    )
    iconMenu = models.ImageField(
        verbose_name="Imagen de icono",
        upload_to='uploads/menu_site/icon/',
        blank=True,
        null=True,
        default='',
        validators=[SizeValidator(40, 40)],
        help_text="Las imágenes debe ser exactamente de 40x40 píxeles"
    )
    link_Menu = models.CharField(
        verbose_name="Enlace del menú",
        max_length=200,
        blank=False,
        null=False,
        default=''
    )
    url_type_choice = [
        ('U.I', 'URL Interna'),
        ('U.E', 'URL Externa'),
    ]
    url_choice = models.CharField(
        verbose_name="Tipo de URL",
        max_length=25,
        choices=url_type_choice,
        default='URL Interna'
    )
    assigned_to = models.ManyToManyField(
        Group,
        blank=True,
        null=True,
        verbose_name="Asignada a:",
        default='',
    )
    order = models.IntegerField(
        verbose_name="Posición del ítem",
        blank=False,
        null=False,
        default=1
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )
    modified_date = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title

    def clean(self):
        self.is_cleaned = True
        if self.url_choice == 'U.I':
            if self.link_Menu.startswith('http://') or self.link_Menu.startswith('https://') or self.link_Menu.startswith('www'):
                raise ValidationError(
                    'Haz seleccionado url Interna, pero el formato de url no es correcto')
            elif self.link_Menu.startswith('/'):
                super(MenuItem, self).clean()
        elif self.url_choice == 'U.E':
            if self.link_Menu.startswith('http://') or self.link_Menu.startswith('https://') or self.link_Menu.startswith('www'):
                super(MenuItem, self).clean()
            elif self.link_Menu.startswith('/'):
                raise ValidationError(
                    'Haz seleccionado url Externa, pero el formato de url no es correcto')
        else:
            raise ValidationError('Valida el formato de la Url')

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.full_clean()
        super(MenuItem, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"


class Documents(models.Model):
    title = models.CharField(
        max_length=90,
        verbose_name="Titulo del documento",
        blank=False,
        null=False,
        default=''
    )
    document = models.FileField(
        verbose_name="Documento",
        validators=[FileType('pdf')],
        upload_to='uploads/documents',
        blank=False,
        null=False,
        default='',
    )
    assigned_to = models.ForeignKey(
        User,
        verbose_name="Documento asignado a",
        related_name="document_assigned_to",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    copy_to = models.ManyToManyField(
        User,
        blank=True,
        null=True,
        verbose_name="Docuemnto con copia a",
        related_name="document_copy_to",
        default='',
    )
    requires_approval = models.BooleanField(
        verbose_name='Requiere aprobación',
        help_text='Si se selecciona se le mostrará al usuario asignado un campo para aprobar el documento',
        default=False,
    )
    approved = models.BooleanField(
        verbose_name='Aprobado',
        help_text='Aprobación del documento',
        default=False,
    )
    comment = RichTextField(
        verbose_name="Comentario",
        help_text="Comntario sobre la aprobación del documento",
        blank=True,
        null=True,
        default=''
    )
    site = models.ForeignKey(
        Site,
        verbose_name="Sitio",
        on_delete=models.CASCADE,
        default=settings.SITE_ID
    )
    objects = models.Manager()
    on_site = CurrentSiteManager()
    created_date = models.DateTimeField(
        verbose_name="Publicación",
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        super(Documents, self).save(*args, **kwargs)

        id_doc = self.id
        if id_doc is not None:
            document = Documents.on_site.get(pk=id_doc)
            assigned_to = document.assigned_to
            all_copy_to = document.copy_to.all()
            requires_approval = document.requires_approval
            url = settings.SITE_URL

            if requires_approval == True:
                name = "Se agregó un nuevo documento y requiere su aprobación, consultar <a target='_blank' href='" + \
                    url+"documento/" + \
                    str(id_doc) + "'>aquí</a>"
                message = "Se agregó un nuevo documento y requiere su aprobación."
            else:
                name = "Se agregó un nuevo documento informativo, consultar <a target='_blank' href='" + \
                    url+"documento/" + \
                    str(id_doc) + "'>aquí</a>"
                message = "Se agregó un nuevo documento informativo"

            Notification.on_site.create(
                name=name,
                sent_to=get_object_or_404(
                    User, pk=assigned_to.id),
                module_from="CO",
                message=message,
                name_link='Consultar documento',
                link=url+"documento/" + str(id_doc)
            )

            for notify in all_copy_to:
                name = "Se agregó un nuevo documento informativo, consultar <a target='_blank' href='" + \
                    url+"documento/" + \
                    str(id_doc) + "'>aquí</a>"
                message = "Se agregó un nuevo documento informativo"

                Notification.on_site.create(
                    name=name,
                    sent_to=get_object_or_404(
                        User, pk=notify.id),
                    module_from="CO",
                    message=message,
                    name_link='Consultar documento',
                    link=url+"documento/" + str(id_doc)
                )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Docuemento"
        verbose_name_plural = "Documentos"


class Tags(models.Model):
    name_tag = models.CharField(
        verbose_name="Nombre Tag",
        max_length=20,
        blank=False,
        null=False,
        default=''
    )
    type_choice_opt = [
        ('red', 'Rojo'),
        ('blue', 'Azul'),
        ('orange', 'Naranja'),
        ('gray', 'Gris'),
        ('purple', 'Violeta'),
        ('yellow', 'Amarillo'),
        ('green', 'Verde'),
    ]
    type_color_choice = models.CharField(
        verbose_name="Color de la Etiqueta",
        max_length=25,
        choices=type_choice_opt,
        blank=False,
        null=False,
        default='',
        help_text='Seleccione el color de la etiqueta'
    )
    site = models.ForeignKey(
        Site,
        verbose_name="Sitio",
        on_delete=models.CASCADE,
        default=settings.SITE_ID
    )
    objects = models.Manager()
    on_site = CurrentSiteManager()
    created_date = models.DateTimeField(
        verbose_name="Publicación",
        auto_now_add=True
    )
    modified_date = models.DateTimeField(
        verbose_name="Actualización",
        auto_now=True
    )

    def __str__(self):
        return self.name_tag

    class Meta:
        verbose_name = "Tag Noticia"
        verbose_name_plural = "Tags Noticias"


class News(models.Model):
    tag_asociate = models.ManyToManyField(
        Tags,
        verbose_name="Tags asociado",
        blank=False,
        null=False,
        default=''
    )
    type_choice_opt = [
        ('New', 'Noticias'),
        ('C.E', 'Contenido Educativo'),
    ]
    type_choice = models.CharField(
        verbose_name="Tipo de Artículo",
        max_length=25,
        choices=type_choice_opt,
        blank=False,
        null=False,
        default='Noticias',
        help_text='Tipo de Artículo (Noticias, Contenido Educativo)'
    )
    title = models.CharField(
        verbose_name="Titulo",
        max_length=40,
        blank=False,
        null=False,
        default=''
    )
    previous_description = RichTextField(
        verbose_name="Descripción Previa",
        blank=False,
        null=False,
        default='',
        max_length=300,
    )
    author = models.CharField(
        verbose_name="Autor",
        max_length=25,
        blank=False,
        null=False,
        default=''
    )
    photo_author = models.ImageField(
        verbose_name="Avatar del autor",
        upload_to='uploads/news',
        blank=True,
        null=True,
        default='',
        validators=[SizeValidator(60, 60)],
        help_text="Las imagen de avatar es de 60x60 Pixeles"
    )
    sub_title = models.CharField(
        verbose_name="Sub Titulo",
        max_length=25,
        blank=True,
        null=True,
        default=''
    )
    description_uno = RichTextField(
        verbose_name="Descripción Uno",
        blank=True,
        null=True,
        default='',
        max_length=1000,
    )
    youtube = models.CharField(
        verbose_name="Código del video de Youtube",
        max_length=255,
        blank=True,
        null=True,
        default='',
        help_text="Ejemplo Md57cPGB1"
    )
    cita_youtube = models.CharField(
        verbose_name="Información o Cita para el video",
        max_length=55,
        blank=True,
        null=True,
        default='',
        help_text="Información del Video"
    )
    description_dos = RichTextField(
        verbose_name="Descripción Dos",
        blank=True,
        null=True,
        default='',
        max_length=1000,
    )
    cita_noticia = RichTextField(
        verbose_name="Cita Noticia",
        blank=True,
        null=True,
        default='',
        max_length=200,
    )
    main_image_new_desk = models.ImageField(
        verbose_name="Imagen principal Desktop",
        upload_to='uploads/news',
        blank=False,
        null=False,
        default='',
        validators=[SizeValidator(800, 500)],
        help_text="Las imágenes debe ser exactamente de 800x500  píxeles"
    )
    main_image_new_mob = models.ImageField(
        verbose_name="Imagen principal Mobile",
        upload_to='uploads/news',
        blank=False,
        null=False,
        default='',
        validators=[SizeValidator(360, 360)],
        help_text="Las imágenes debe ser exactamente de 360x360  píxeles"
    )
    site = models.ForeignKey(
        Site,
        verbose_name="Sitio",
        on_delete=models.CASCADE,
        default=settings.SITE_ID
    )
    objects = models.Manager()
    on_site = CurrentSiteManager()
    created_date = models.DateTimeField(
        verbose_name="Publicación",
        auto_now_add=True
    )
    modified_date = models.DateTimeField(
        verbose_name="Actualización",
        auto_now=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"


class Gallery(models.Model):
    galleryList = models.ForeignKey(
        News,
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    title = models.CharField(
        verbose_name="Title Imagen",
        max_length=40,
        blank=False,
        null=False,
        default=''
    )
    alt = models.CharField(
        verbose_name="Alt Imagen",
        max_length=40,
        blank=False,
        null=False,
        default=''
    )
    img_desk_gallery = models.ImageField(
        verbose_name="Imagen Galeria Desktop",
        upload_to='uploads/Gallery',
        blank=False,
        null=False,
        default='',
        validators=[SizeValidator(600, 600)],
        help_text="Las imágenes debe ser exactamente de 600x600  píxeles"
    )
    img_mob_gallery = models.ImageField(
        verbose_name="Imagen Galeria Mobile",
        upload_to='uploads/Gallery',
        blank=False,
        null=False,
        default='',
        validators=[SizeValidator(360, 360)],
        help_text="Las imágenes debe ser exactamente de 360x360  píxeles"
    )
    created_date = models.DateTimeField(
        verbose_name="Publicación",
        auto_now_add=True
    )
    modified_date = models.DateTimeField(
        verbose_name="Actualización",
        auto_now=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Galeria"
        verbose_name_plural = "Imágenes"


class Letter(models.Model):
    name_letter = models.CharField(
        verbose_name="Letra Vocabulario",
        max_length=5,
        blank=False,
        null=False,
        default=''
    )
    site = models.ForeignKey(
        Site,
        verbose_name="Sitio",
        on_delete=models.CASCADE,
        default=settings.SITE_ID
    )
    objects = models.Manager()
    on_site = CurrentSiteManager()
    created_date = models.DateTimeField(
        verbose_name="Publicación",
        auto_now_add=True
    )
    created_date = models.DateTimeField(
        verbose_name="Publicación",
        auto_now_add=True
    )
    modified_date = models.DateTimeField(
        verbose_name="Actualización",
        auto_now=True
    )

    def __str__(self):
        return self.name_letter

    class Meta:
        verbose_name = "Letra Glosario"
        verbose_name_plural = "Letras Glosario"


class Vocabulary(models.Model):
    letter = models.ForeignKey(
        Letter,
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    word = models.CharField(
        verbose_name="Palabra",
        max_length=20,
        blank=False,
        null=False,
        default=''
    )
    meaning = RichTextField(
        verbose_name="Significado",
        max_length=1000,
        blank=False,
        null=False,
        default=''
    )
    site = models.ForeignKey(
        Site,
        verbose_name="Sitio",
        on_delete=models.CASCADE,
        default=settings.SITE_ID
    )
    objects = models.Manager()
    on_site = CurrentSiteManager()
    created_date = models.DateTimeField(
        verbose_name="Publicación",
        auto_now_add=True
    )
    created_date = models.DateTimeField(
        verbose_name="Publicación",
        auto_now_add=True
    )
    modified_date = models.DateTimeField(
        verbose_name="Actualización",
        auto_now=True
    )

    def __str__(self):
        return self.word

    class Meta:
        verbose_name = "Vocabulario"
        verbose_name_plural = "Vocabularios"


class FAQs(models.Model):
    name_question_faqs = models.CharField(
        verbose_name="Pregunta",
        max_length=100,
        blank=False,
        null=False,
        default=''
    )
    response_faqs = RichTextField(
        verbose_name="Respuesta",
        max_length=1000,
        blank=False,
        null=False,
        default=''
    )
    site = models.ForeignKey(
        Site,
        verbose_name="Sitio",
        on_delete=models.CASCADE,
        default=settings.SITE_ID
    )
    objects = models.Manager()
    on_site = CurrentSiteManager()
    created_date = models.DateTimeField(
        verbose_name="Publicación",
        auto_now_add=True
    )
    modified_date = models.DateTimeField(
        verbose_name="Actualización",
        auto_now=True
    )

    def __str__(self):
        return self.name_question_faqs

    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"


class Visitor(models.Model):
    ip_user = models.TextField(
        verbose_name="Ip Visitante",
        max_length=20,
        blank=False,
        null=False,
        default=None
    )
    rol_visited = models.TextField(
        verbose_name="Rol Visitante",
        max_length=30,
        blank=False,
        null=False,
        default=''
    )
    url_visited = models.TextField(
        verbose_name="Url Visitada",
        max_length=100,
        blank=False,
        null=False,
        default=''
    )
    type_model_visited = models.TextField(
        verbose_name="Tipo de Modelo",
        max_length=50,
        blank=True,
        null=True,
        default=''
    )
    id_model_visited = models.TextField(
        verbose_name="Id Modelo Visitado",
        max_length=10,
        blank=True,
        null=True,
        default=''
    )
    site = models.ForeignKey(
        Site,
        verbose_name="Sitio",
        on_delete=models.CASCADE,
        default=settings.SITE_ID
    )
    objects = models.Manager()
    on_site = CurrentSiteManager()
    created_date = models.DateTimeField(
        verbose_name="Fecha Registro",
        auto_now_add=True
    )

    def __str__(self):
        return self.ip_user

    class Meta:
        verbose_name = "Visitante"
        verbose_name_plural = "Visitante"


class Testimony (models.Model):
    user_testimony = models.ForeignKey(
        User,
        blank=True,
        null=True,
        verbose_name="Proveedor",
        on_delete=models.CASCADE,
        default='',
    )
    logo = models.ImageField(
        verbose_name="Logo",
        upload_to='uploads/testimony/logo',
        blank=False,
        null=False,
        default='',
        validators=[SizeValidator(155, 31)],
        help_text="Las imágenes debe ser exactamente de 155x31  píxeles"
    )
    title = models.CharField(
        verbose_name="Nombre",
        max_length=40,
        blank=False,
        null=False,
        default=''
    )
    video_image = models.ImageField(
        verbose_name="Imagen del video",
        upload_to='uploads/testimony/video',
        blank=False,
        null=False,
        default='',
        validators=[SizeValidator(930, 510)],
        help_text="Las imágenes debe ser exactamente de 930x510  píxeles"
    )
    video_testimony = models.CharField(
        verbose_name="Código video de Youtube",
        max_length=255,
        blank=False,
        null=False,
        default='',
        help_text="Ejemplo Md57cPGB1"
    )
    description_testimony = models.TextField(
        verbose_name="Descripción",
        blank=False,
        null=False,
        default='',
        max_length=160
    )
    site = models.ForeignKey(
        Site,
        verbose_name="Sitio",
        on_delete=models.CASCADE,
        default=settings.SITE_ID
    )
    objects = models.Manager()
    on_site = CurrentSiteManager()
    created_date = models.DateTimeField(
        verbose_name="Fecha Registro",
        auto_now_add=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Testimonio"
        verbose_name_plural = "Testimonios"
