from django.db import models
from django.contrib.sites.models import Site
from django.conf import settings
from content.validators import SizeValidator
from django.contrib.sites.managers import CurrentSiteManager
from providers.models import ProviderEntity
from inventory.models import Inventory
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from users.models import Functionary


# Create your models here.
class TagsProject(models.Model):
    name_tag_project = models.CharField(
        verbose_name="Nombre Tag",
        max_length=55,
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
        return self.name_tag_project

    class Meta:
        verbose_name = "Tag Proyecto"
        verbose_name_plural = "Tags Proyecto"


class CategoryProject(models.Model):
    name_category_project = models.CharField(
        verbose_name="Nombre Categoría",
        max_length=55,
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
        return self.name_category_project

    class Meta:
        verbose_name = "Categoría Proyecto"
        verbose_name_plural = "Categorías Proyecto"


class RelatedStatistical(models.Model):
    name = models.CharField(
        verbose_name="Nombre",
        max_length=255,
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
        return self.name

    class Meta:
        verbose_name = "Investigación estadística relacionada"
        verbose_name_plural = "Investigación estadística relacionada"


class ThemeProject(models.Model):
    name_theme_project = models.CharField(
        verbose_name="Temática Proyecto",
        max_length=55,
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
        return self.name_theme_project

    class Meta:
        verbose_name = "Temática Proyecto"
        verbose_name_plural = "Temáticas Proyecto"


class StateProject(models.Model):
    state_project = models.CharField(
        verbose_name="Estado del proyecto",
        help_text="Activo o Inactivo",
        max_length=55,
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
        return self.state_project

    def clean(self):
        self.is_cleaned = True
        if self.state_project == 'Activo' or self.state_project == 'Inactivo':
            super(StateProject, self).clean()
        else:
            raise ValidationError('Unicamente puede digitar Activo o Inactivo')

    def save(self, *args, **kwargs):
        if hasattr(self, 'is_cleaned'):
            if not self.is_cleaned:
                self.full_clean()
            super(StateProject, self).save(*args, **kwargs)
        else:
            super(StateProject, self).save(*args, **kwargs)
    class Meta:
        verbose_name = "Estado del Proyecto"
        verbose_name_plural = "Estado del Proyecto"


class Project(models.Model):
    name = models.CharField(
        verbose_name="Nombre",
        max_length=255,
        blank=True,
        null=False,
        default=''
    )
    objetive_project = models.CharField(
        verbose_name="Objetivo general del proyecto",
        max_length=300,
        blank=True,
        null=False,
        default=''
    )
    tag_project = models.ManyToManyField(
        TagsProject,
        verbose_name="Tags asociado",
        blank=False,
        null=False,
        default=''
    )
    provider_any_project = models.ManyToManyField(
        ProviderEntity,
        blank=True,
        null=True,
        verbose_name="Proveedor asociado",
        default=''
    )
    functionary_project = models.ForeignKey(
        Functionary,
        blank=True,
        null=True,
        verbose_name="Funcionario asociado",
        on_delete=models.CASCADE,
        default=''
    )
    category_project = models.ForeignKey(
        CategoryProject,
        verbose_name="Categoría Proyecto",
        blank=False,
        null=False,
        default='',
        on_delete=models.CASCADE,
    )
    area_in_charge = models.CharField(
        verbose_name="Área a cargo del proyecto",
        max_length=255,
        blank=True,
        null=False,
        default=''
    )
    related_statistical_research = models.CharField(
        verbose_name="Investigación estadística relacionada",
        max_length=255,
        blank=True,
        null=False,
        default=''
    )
    related_statistical = models.ForeignKey(
        RelatedStatistical,
        verbose_name="Investigación estadística relacionada",
        blank=True,
        null=True,
        default='',
        on_delete=models.CASCADE,
    )
    theme_project = models.ForeignKey(
        ThemeProject,
        blank=False,
        null=False,
        verbose_name="Temática Proyecto",
        on_delete=models.CASCADE,
        default=''
    )
    state_project = models.ForeignKey(
        StateProject,
        blank=False,
        null=False,
        verbose_name="Estado del Proyecto",
        on_delete=models.CASCADE,
        default=''
    )
    rraa_asociate = models.ManyToManyField(
        Inventory,
        verbose_name="Registros Administrativos Asociados",
        blank=True,
        null=True,
        default=''
    )
    sub_title = models.CharField(
        verbose_name="Subtítulo",
        max_length=55,
        blank=False,
        null=False,
        default=''
    )
    description_uno = RichTextField(
        verbose_name="Párrafo uno",
        help_text="Primer Párrafo ",
        blank=True,
        null=True,
        default=''
    )
    image_project_desk = models.ImageField(
        verbose_name="Imagen contenido Proyecto Desktop",
        upload_to='uploads/projects',
        blank=True,
        null=True,
        default='',
        validators=[SizeValidator(1170, 660)],
        help_text="Las imagen de avatar es de 1170x660 Pixeles"
    )
    image_project_mob = models.ImageField(
        verbose_name="Imagen contenido Proyecto Mobile",
        upload_to='uploads/projects',
        blank=True,
        null=True,
        default='',
        validators=[SizeValidator(370, 230)],
        help_text="Las imagen de avatar es de 370x230 Pixeles"
    )
    author_cita_imagen = models.CharField(
        verbose_name="Autor o Cita de la Imagen",
        max_length=100,
        blank=True,
        null=True,
        default=''
    )
    description_dos = RichTextField(
        verbose_name="Descripción Dos",
        blank=True,
        null=True,
        default='',
        max_length=1000,
    )
    cita_contenido = models.CharField(
        verbose_name="Cita del contenido",
        max_length=300,
        blank=True,
        null=True,
        default=''
    )
    author_cita_contenido = models.CharField(
        verbose_name="Autor Cita del contenido",
        max_length=100,
        blank=True,
        null=True,
        default=''
    )
    image_left_project_desk = models.ImageField(
        verbose_name="Imagen Lat Izquierda Proyecto Desk",
        upload_to='uploads/projects',
        blank=True,
        null=True,
        default='',
        validators=[SizeValidator(600, 350)],
        help_text="Las imagen de avatar es de 600x350 Pixeles"
    )
    image_left_project_mob = models.ImageField(
        verbose_name="Imagen Lat Izquierda Proyecto Mob",
        upload_to='uploads/projects',
        blank=True,
        null=True,
        default='',
        validators=[SizeValidator(370, 230)],
        help_text="Las imagen de avatar es de 370x230 Pixeles"
    )
    author_cita_imagen_left = models.CharField(
        verbose_name="Autor o Cita de la Imagen Izquierda",
        max_length=100,
        blank=True,
        null=True,
        default=''
    )
    image_right_project_desk = models.ImageField(
        verbose_name="Imagen Lat Derecha Proyecto Desk",
        upload_to='uploads/projects',
        blank=True,
        null=True,
        default='',
        validators=[SizeValidator(600, 350)],
        help_text="Las imagen de avatar es de 600x350 Pixeles"
    )
    image_right_project_mob = models.ImageField(
        verbose_name="Imagen Lat Derecha Proyecto Mob",
        upload_to='uploads/projects',
        blank=True,
        null=True,
        default='',
        validators=[SizeValidator(370, 230)],
        help_text="Las imagen de avatar es de 370x230 Pixeles"
    )
    author_cita_imagen_right = models.CharField(
        verbose_name="Autor o Cita de la Imagen Derecha",
        max_length=100,
        blank=True,
        null=True,
        default=''
    )
    description_tres = RichTextField(
        verbose_name="Descripción tres",
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
        return self.name

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
