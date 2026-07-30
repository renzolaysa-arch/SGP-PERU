from django.db import models
from django.contrib.sites.models import Site
from users.models import Functionary
from django.conf import settings
from django.contrib.sites.managers import CurrentSiteManager

# Create your models here.
class ThemeThread(models.Model):
    name_thread = models.CharField(
        verbose_name="Título del Hilo",
        max_length=70,
        blank=False,
        null=False,
        default=''
    )
    content_thread = models.TextField(
        verbose_name="Contenido del Hilo",
        max_length=300,
        blank=False,
        null=False,
        default=''
    )
    user_functionary_created = models.ForeignKey(
        Functionary,
        verbose_name="Funcionario que crea nuevo Hilo",
        on_delete=models.CASCADE,
        blank=True,
        null=True
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
        return self.name_thread

    class Meta:
        verbose_name = "Bitácora"
        verbose_name_plural = "Bitácoras"

class CommentThread(models.Model):
    threadt_to_comment = models.ForeignKey(
        ThemeThread,
        verbose_name="Hilo a comentar",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    commentary = models.TextField(
        verbose_name="Comentario",
        blank=False,
        null=False,
        default='',
        max_length=300,
    )
    functionary_commented = models.ForeignKey(
        Functionary,
        verbose_name="Funcionario que comenta el Hilo",
        on_delete=models.CASCADE,
        blank=True,
        null=True
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
        return self.commentary

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"