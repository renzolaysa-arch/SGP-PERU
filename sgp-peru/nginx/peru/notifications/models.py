from django.db import models
from django.contrib.sites.models import Site
from django.conf import settings
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from notifications.functions import notify_email

# Create your models here.


class Notification(models.Model):
    is_cleaned = False
    MODULES = [
        ('', 'Seleccionar'),
        ('CO', 'Contenido'),
        ('SO', 'Solicitudes'),
        ('IN', 'Inventario'),
        ('PRV', 'Proveedores'),
        ('PRO', 'Proyectos'),
        ('BI', 'Bitácora'),
    ]
    name = models.CharField(
        verbose_name="Nombre",
        max_length=255,
        blank=False,
        null=False,
        default='',
    )
    sent_to = models.ForeignKey(
        User,
        verbose_name="Notificar a",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    module_from = models.CharField(
        verbose_name="Modulo origen",
        max_length=3,
        choices=MODULES,
        default='',
    )
    message = RichTextField(
        verbose_name="Mensaje",
        blank=True,
        null=True,
        default=''
    )
    name_link = models.CharField(
       verbose_name="Nombre del enlace",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    link = models.CharField(
       verbose_name="Enlace",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    hidden = models.BooleanField(
        verbose_name="Oculto",
        default=False,
    )
    site = models.ForeignKey(
        Site,
        verbose_name="Sitio",
        on_delete=models.CASCADE,
        default=settings.SITE_ID,
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

    def clean(self):
        self.is_cleaned = True
        if self.hidden == False:
            notify_email(
                'Alertas y Notificaciones',
                self.message,
                self.sent_to.email,
                self.name_link,
                self.link,
                settings.COUNTRY
            )

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.full_clean()
        super(Notification, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Notificacion"
        verbose_name_plural = "Notificaciones"
