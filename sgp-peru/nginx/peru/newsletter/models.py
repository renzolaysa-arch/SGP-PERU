from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.db import models
from django.conf import settings

# Create your models here.

class NewsLetter(models.Model):
    mail = models.EmailField(
        verbose_name = "Correo electrónico",
        max_length = 255,
        blank = False,
        null = False,
        default = ""
    )
    terms = models.BooleanField(
        verbose_name = "Al inscribirte reconoces y aceptas nuestras Políticas de privacidad",
        default = False,
        blank = False,
        null = False,
    )
    site = models.ForeignKey(
        Site,
        on_delete = models.CASCADE,
        default = settings.SITE_ID
    )
    objects = models.Manager()
    on_site = CurrentSiteManager()
    created_date = models.DateTimeField(
        auto_now_add = True
    )
    modified_date = models.DateTimeField(
        auto_now = True
    )
    
    def __str__(self):
        return self.mail
    
    class Meta:
        verbose_name = "Boletin"
        verbose_name_plural = "Boletines"
        