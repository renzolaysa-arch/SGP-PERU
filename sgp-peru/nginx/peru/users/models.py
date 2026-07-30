from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.sites.managers import CurrentSiteManager
from django.forms import BooleanField
from providers.models import ProviderEntity
from content.validators import SizeValidator
from inventory.models import Inventory

# Create your models here.


class UserManage(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name="Usuario",
        on_delete=models.CASCADE,
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        default=settings.SITE_ID
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )
    modified_date = models.DateTimeField(
        auto_now=True
    )
    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        abstract = True


class Provider(UserManage):
    DOCUMENT_TYPE_CHOICES = [
        ('no', 'Seleccionar'),
        ('CC', 'C.C'),
        ('CE', 'C.E'),
    ]
    profile_image = models.ImageField(
        verbose_name="Imagen de perfil",
        upload_to='uploads/profile/',
        blank=True,
        null=True,
        default='',
        validators=[SizeValidator(150, 150)],
        help_text="Las imágenes debe ser exactamente de 150x150 píxeles"
    )
    document_type = models.CharField(
        verbose_name="Tipo de Documento",
        max_length=2,
        choices=DOCUMENT_TYPE_CHOICES,
        default='CC',
    )
    identification_number = models.CharField(
        verbose_name="Documento",
        max_length=255,
        blank=False,
        null=False,
        default=''
    )
    user = models.OneToOneField(
        User,
        verbose_name="Usuario",
        on_delete=models.CASCADE,
    )
    entity_provider = models.ForeignKey(
        ProviderEntity,
        verbose_name="Entidad proveedora",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    valid_data = models.BooleanField(
        verbose_name='Data verificada',
        default=True
    )
    hash = models.CharField(
        verbose_name="Hash",
        max_length=255,
        blank=True,
        null=True,
        default=''
    )

    def __str__(self):
        return self.user.username

    @property
    def empty_fields_count_prov(self):
        fields = ["profile_image", "document_type", "identification_number", "user", "entity_provider", "valid_data"]
        empty_values = {"", None, "no"}
        empty_values_count = 0
        for field in fields:
            field_value = getattr(self, field)
            if field_value in empty_values:
                empty_values_count += 1
        return empty_values_count

    @property
    def count_column_prov(self):
        fields = ["profile_image", "document_type", "identification_number", "user", "entity_provider", "valid_data"]
        return len(fields)
     
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"


class Unit_Central (UserManage):
    profile_image = models.ImageField(
        verbose_name="Imagen de perfil",
        upload_to='uploads/profile/',
        blank=True,
        null=True,
        default='',
        validators=[SizeValidator(150, 150)],
        help_text="Las imágenes debe ser exactamente de 150x150 píxeles"
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Unidad Central"
        verbose_name_plural = "Unidades Centrales"


class Functionary (UserManage):
    profile_image = models.ImageField(
        verbose_name="Imagen de perfil",
        upload_to='uploads/profile/',
        blank=True,
        null=True,
        default='',
        validators=[SizeValidator(150, 150)],
        help_text="Las imágenes debe ser exactamente de 150x150 píxeles"
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Funcionario"
        verbose_name_plural = "Funcionarios"


class AccessUserRRA (models.Model):
    inventory = models.ForeignKey(
        Inventory,
        verbose_name="Registro administrativo",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        default='',
    )
    user = models.ForeignKey(
        Functionary,
        verbose_name="Funcionario",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        default='',
    )
    date_access = models.DateField(
        verbose_name="Fecha de acceso",
        blank=True,
        null=True,
    )
    date_limit = models.DateField(
        verbose_name="Fecha limite de acceso",
        blank=True,
        null=True,
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
        return str(self.inventory) + " - " + str(self.user)

    class Meta:
        verbose_name = "Acceso a RRAA"
        verbose_name_plural = "Accesos a RRAA"
