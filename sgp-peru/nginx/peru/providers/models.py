from django.core.validators import RegexValidator
from django.db import models
from django.contrib.sites.models import Site
from django.conf import settings
from django.contrib.sites.managers import CurrentSiteManager
from .validators import SizeValidator
from content.models import Divipola

# Create your models here.


class ProviderStatus(models.Model):
    name = models.CharField(
        verbose_name="Nombre",
        max_length=255,
        blank=False,
        null=False,
        default=''
    )
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
        verbose_name = "Estado (T)"
        verbose_name_plural = "Estados (T)"


class ProviderCategory(models.Model):
    name = models.CharField(
        verbose_name="Nombre",
        max_length=255,
        blank=False,
        null=False,
        default=''
    )
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
        verbose_name = "Categoria (T)"
        verbose_name_plural = "Categorias (T)"


class ProviderTopic(models.Model):
    name = models.CharField(
        verbose_name="Nombre",
        max_length=255,
        blank=False,
        null=False,
        default=''
    )
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
        verbose_name = "Tematica (T)"
        verbose_name_plural = "Tematicas (T)"


class ProviderType(models.Model):
    name = models.CharField(
        verbose_name="Nombre",
        max_length=255,
        blank=False,
        null=False,
        default=''
    )
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
        verbose_name = "Tipo (T)"
        verbose_name_plural = "Tipos (T)"


class ProviderSector(models.Model):
    name = models.CharField(
        verbose_name="Nombre",
        max_length=255,
        blank=False,
        null=False,
        default=''
    )
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
        verbose_name = "Sector (T)"
        verbose_name_plural = "Sector (T)"


class ProviderEntity(models.Model):
    name = models.CharField(
        verbose_name="Nombre",
        max_length=255,
        blank=False,
        null=False,
        default=''
    )
    identification_number = models.CharField(
        verbose_name="Número de Identificación Tributaria",
        max_length=255,
        blank=True,
        null=True,
        default=''
    )
    description = models.TextField(
        verbose_name="Descripción",
        blank=False,
        null=False,
        default=''
    )
    sector = models.ForeignKey(
        ProviderSector,
        blank=True,
        null=True,
        verbose_name="Sector",
        on_delete=models.CASCADE,
        default='',
    )
    type = models.ForeignKey(
        ProviderType,
        blank=True,
        null=True,
        verbose_name="Tipo",
        on_delete=models.CASCADE,
        default='',
    )
    mision = models.TextField(
        verbose_name="Misión",
        blank=True,
        null=True,
        default=''
    )
    sicode = models.CharField(
        verbose_name="Código SICODE",
        max_length=255,
        blank=True,
        null=True,
        default=''
    )
    territorial_level = models.CharField(
        verbose_name="Nivel territorial",
        max_length=255,
        blank=True,
        null=True,
        default=''
    )
    web = models.URLField(
        verbose_name="Página web",
        max_length=255,
        blank=True,
        null=True,
        default=''
    )
    mail = models.EmailField(
        verbose_name="Correo electrónico",
        max_length=255,
        blank=True,
        null=True,
        default=''
    )
    telephone = models.CharField(
        verbose_name="Telefonos",
        max_length=255,
        blank=True,
        null=True,
        default=''
    )
    location = models.ForeignKey(
        Divipola,
        blank=True,
        null=True,
        verbose_name="Ubicación",
        on_delete=models.CASCADE,
    )
    agent_mame = models.CharField(
        verbose_name="Nombre del principal representante",
        max_length=255,
        blank=True,
        null=True,
        default=''
    )
    agent_position = models.CharField(
        verbose_name="Cargo del principal representante",
        max_length=255,
        blank=True,
        null=True,
        default=''
    )
    official_name = models.CharField(
        verbose_name="Nombre del funcionario enlace",
        max_length=255,
        blank=True,
        null=True,
        default=''
    )
    official_position = models.CharField(
        verbose_name="Cargo del funcionario enlace",
        max_length=255,
        blank=True,
        null=True,
        default=''
    )
    official_mail = models.EmailField(
        verbose_name="Correo electrónico del funcionario enlace",
        max_length=255,
        blank=True,
        null=True,
        default=''
    )
    official_telephone = models.CharField(
        verbose_name="Telefono del funcionario enlace",
        max_length=255,
        blank=True,
        null=True,
        default=''
    )
    image = models.ImageField(
        verbose_name="Imagen",
        upload_to='uploads/providers/entity',
        blank=False,
        null=False,
        default='',
        validators=[SizeValidator(80, 80)],
        help_text="Las imágenes debe ser exactamente de 80x80 píxeles"
    )
    domain = models.CharField(
        verbose_name="Dominio",
        max_length=255,
        blank=False,
        null=False,
        default='',
        # Se compara con el dominio del correo de quien se registra para enviarle el enlace de activacion
        validators=[RegexValidator(
            regex=r'^(?!www\.)[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+$',
            message="Escriba solo el dominio del correo institucional, por ejemplo minedu.gob.pe (sin http, www, @ ni barras).",
        )],
        help_text="Dominio del correo institucional, por ejemplo minedu.gob.pe. No es la página web."
    )
    status = models.ForeignKey(
        ProviderStatus,
        blank=True,
        null=True,
        verbose_name="Estado",
        on_delete=models.CASCADE,
        default='',
    )
    category = models.ManyToManyField(
        ProviderCategory,
        blank=True,
        null=True,
        verbose_name="Categorias",
        default='',
    )
    topic = models.ManyToManyField(
        ProviderTopic,
        blank=True,
        null=True,
        verbose_name="Temáticas",
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
        verbose_name = "Entidad Proveedora"
        verbose_name_plural = "Entidades Proveedoras"


class Stage(models.Model):
    name_stage = models.CharField(
        max_length=50,
        verbose_name="Etapa del Documento",
        blank=False,
        null=False,
        default=''
    )
    modified_date = models.DateTimeField(
        verbose_name="Actualización",
        auto_now=True
    )

    def __str__(self):
        return self.name_stage

    class Meta:
        verbose_name = "Etapa del Documento (T)"
        verbose_name_plural = "Etapas del Documento (T)"

class ProviderDocuments(models.Model):
    stage_document = models.ForeignKey(
        Stage,
        blank=True,
        null=True,
        verbose_name="Etapa del documento",
        on_delete=models.CASCADE,
        default=''
    )
    provider = models.ForeignKey(
        ProviderEntity,
        on_delete=models.CASCADE,
        verbose_name="Entidad Proveedora",
    )
    name = models.CharField(
        verbose_name="Nombre",
        max_length=255,
        blank=False,
        null=False,
        default=''
    )
    documents = models.FileField(
        upload_to='uploads/providers/documents',
        verbose_name="Documento",
        blank=False,
        null=False,
    )
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
        verbose_name = "Documento (T)"
        verbose_name_plural = "Documentos (T)"
