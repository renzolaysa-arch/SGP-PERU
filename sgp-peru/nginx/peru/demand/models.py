from django.db import models
from django.contrib.sites.models import Site
from django.conf import settings
from django.contrib.sites.managers import CurrentSiteManager
from providers.models import ProviderEntity
from content.models import Documents
from django.contrib.auth.models import User
from users.models import Functionary
from notifications.models import Notification
from users.models import Unit_Central, Provider
from projects.models import Project
from datetime import date
from inventory.models import Inventory
from content.validators import FileType

# Create your models here.


class DemandsCategories(models.Model):
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
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"


class DemandsStatus (models.Model):
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
        verbose_name = "Estado solicitud"
        verbose_name_plural = "Estados de solicitudes"


class DemandsTheme (models.Model):
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
        verbose_name = "Tema solicitud"
        verbose_name_plural = "Tema de solicitudes"


class KeyWords(models.Model):
    name = models.CharField(
        verbose_name="Nombre",
        max_length=40,
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
        verbose_name = "Palabra clave"
        verbose_name_plural = "Palabras claves"


class Topic (models.Model):
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
        verbose_name = "Temática"
        verbose_name_plural = "Temáticas"


class Demands(models.Model):
    PROCESS = [
        ('re', 'Recepción'),
        ('ne', 'Negociación'),
        ('tr', 'Transferencia'),
        ('pr', 'Preparación'),
        ('ev', 'Evaluación'),
    ]
    USE = [
        ('eo', 'Generar directamente estadística oficial'),
        ('va', 'Realizar validación'),
        ('rb', 'Conformar un registro base'),
        ('ex', 'Estadística experimental'),
        ('ca', 'Evaluar su calidad'),
        ('ot', 'Otro'),
    ]
    TIME = [
        ('1', '1 mes'),
        ('2', '2 meses'),
        ('3', '3 meses'),
        ('4', '4 meses'),
        ('5', '5 meses'),
        ('6', '6 meses'),
        ('7', '7 meses'),
        ('8', '8 meses'),
        ('9', '9 meses'),
        ('10', '10 meses'),
        ('11', '11 meses'),
        ('12', '1 año'),
    ]
    TYPE = [
        ('in', 'Interno'),
        ('ex', 'Externo'),
    ]
    functionary = models.ForeignKey(
        Functionary,
        verbose_name="Funcionario",
        on_delete=models.CASCADE,
        default='',
    )
    inventory = models.ForeignKey(
        Inventory,
        verbose_name="Inventario",
        on_delete=models.CASCADE,
        default='',
    )
    project = models.ForeignKey(
        Project,
        verbose_name="Proyecto",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=7
    )
    title = models.CharField(
        verbose_name="Titulo",
        max_length=40,
        blank=False,
        null=False,
        default=''
    )
    description = models.TextField(
        verbose_name="Descripción",
        blank=True,
        null=True,
        default='',
        max_length=300,
    )
    use = models.CharField(
        verbose_name="¿Cual va hacer su uso?",
        max_length=2,
        choices=USE,
        blank=True,
        null=True,
        default='',
    )
    use_other = models.CharField(
        verbose_name="Otro",
        max_length=40,
        blank=True,
        null=True,
        default=''
    )
    time = models.CharField(
        verbose_name="Tiempo de uso requerido",
        max_length=2,
        choices=TIME,
        blank=True,
        null=True,
        default='',
    )
    product = models.TextField(
        verbose_name="Producto final esperado",
        blank=True,
        null=True,
        default='',
        max_length=300,
    )
    status = models.ForeignKey(
        DemandsStatus,
        blank=True,
        null=True,
        verbose_name="Estado",
        on_delete=models.CASCADE,
        default='',
    )
    category = models.ForeignKey(
        DemandsCategories,
        blank=True,
        null=True,
        verbose_name="Categoría",
        on_delete=models.CASCADE,
        default='',
    )
    theme = models.ForeignKey(
        DemandsTheme,
        blank=True,
        null=True,
        verbose_name="Tema",
        on_delete=models.CASCADE,
        default='',
    )
    provider_entity = models.ForeignKey(
        ProviderEntity,
        blank=True,
        null=True,
        verbose_name="Proveedor",
        on_delete=models.CASCADE,
        default='',
    )
    topic = models.ForeignKey(
        Topic,
        blank=True,
        null=True,
        verbose_name="Temática",
        on_delete=models.CASCADE,
        default='',
    )
    key_words = models.ManyToManyField(
        KeyWords,
        blank=True,
        null=True,
        verbose_name="Palabras claves",
        default='',
    )
    finish_date = models.DateField(
        verbose_name="Fecha finalización",
        blank=True,
        null=True,
    )
    file_demand = models.FileField(
        verbose_name="Archivo",
        upload_to='uploads/solicitudes',
        blank=True,
        null=True,
        default='',
    )
    process = models.CharField(
        verbose_name="Proceso",
        max_length=2,
        choices=PROCESS,
        default='re',
    )
    type = models.CharField(
        verbose_name="Tipo",
        max_length=2,
        choices=TYPE,
        blank=False,
        null=False,
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
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"


class Note(models.Model):
    demand = models.ForeignKey(
        Demands,
        verbose_name="Solicitud",
        on_delete=models.CASCADE,
        default='',
    )
    commentary = models.TextField(
        verbose_name="Nota",
        blank=False,
        null=False,
        default='',
        max_length=300,
    )
    functionary = models.ForeignKey(
        Functionary,
        verbose_name="Funcionario",
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
        verbose_name = "Nota"
        verbose_name_plural = "Notas"


class GeographicCoverage (models.Model):
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
        verbose_name = "Cobertura geográfica"
        verbose_name_plural = "Coberturas geográficas"


class FollowDemand (models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Usuario",
        on_delete=models.CASCADE,
    )
    demand = models.ForeignKey(
        Demands,
        verbose_name="Solicitud",
        on_delete=models.CASCADE,
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
        return str(self.user) + " - " + str(self.demand)

    class Meta:
        verbose_name = "Solicitud seguida"
        verbose_name_plural = "Solicitudes seguidas"


# All models processes

class ProcessesManager(models.Model):
    PROCESS = [
        ('ini', 'Inicio'),
        ('pr', 'En proceso'),
        ('re', 'En revision'),
        ('fi', 'Finzalizado'),
    ]
    demand = models.OneToOneField(
        Demands,
        verbose_name="Solicitud",
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
    demand_process = models.CharField(
        verbose_name="Proceso",
        max_length=3,
        choices=PROCESS,
        default='ini'
    )
    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        abstract = True


class Reception(ProcessesManager):
    ANSWERS = [
        ('Y', 'Si'),
        ('N', 'No'),
    ]
    STATUS = [
        ('do', 'Aprobado'),
        ('de', 'Rechazado'),
    ]
    SUB_PROCESS = [
        ('demand-validation', 'Validación Solicitud'),
        ('verification-completeness', 'Verificación y Completitud'),
        ('demand-notification', 'Notificación Solicitud'),
        ('technical-committee-presentation', 'Presentación Comité Técnico'),
    ]
    ASSESSMENT = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]
    # in process
    date_demand_validation = models.DateTimeField(
        verbose_name="Fecha Validación Solicitud",
        blank=True,
        null=True,
    )
    date_verification_completeness = models.DateTimeField(
        verbose_name="Fecha Verificación y Completitud",
        blank=True,
        null=True,
    )
    date_demand_notification = models.DateTimeField(
        verbose_name="Fecha Notificación solicitud",
        blank=True,
        null=True,
    )
    date_tentative_presentation = models.DateTimeField(
        verbose_name="Fecha Tentativa presentación",
        blank=True,
        null=True,
    )
    date_demand_presentation = models.DateTimeField(
        verbose_name="Fecha Presentación Comité Técnico",
        blank=True,
        null=True,
    )
    status_demand_validation = models.CharField(
        verbose_name="Estado",
        max_length=2,
        choices=STATUS,
        blank=True,
        null=True,
    )
    status_demand_notification = models.CharField(
        verbose_name="Estado notificación",
        max_length=2,
        choices=STATUS,
        blank=True,
        null=True,
    )
    comment = models.TextField(
        verbose_name="Comentario",
        blank=True,
        null=True,
        default='',
    )
    demand_subprocess = models.CharField(
        verbose_name="Sub proceso",
        max_length=35,
        choices=SUB_PROCESS,
        blank=True,
        null=True,
    )
    demand_assessment = models.CharField(
        verbose_name="Valoración",
        max_length=2,
        choices=ASSESSMENT,
        blank=True,
        null=True,
    )
    doc_verification_completeness = models.ManyToManyField(
        Documents,
        blank=True,
        null=True,
        verbose_name="Docuemnto verificación y completitud",
        default='',
    )
    doc_committee_presentation = models.ManyToManyField(
        Documents,
        blank=True,
        null=True,
        verbose_name="Docuemnto presentación Comité Técnico",
        related_name="document_presentation",
        default='',
    )

    # revision
    date_demand_revision = models.DateTimeField(
        verbose_name="Fecha Revisión Solicitud",
        blank=True,
        null=True,
    )
    comment_revision = models.TextField(
        verbose_name="Comentario revisión",
        blank=True,
        null=True,
        default='',
    )
    punctual_need = models.CharField(
        verbose_name="¿La solicitud responde a una necesidad puntual de la entidad?",
        max_length=2,
        choices=ANSWERS,
        default='',
        blank=True,
        null=True,
    )
    full_justification = models.CharField(
        verbose_name="¿La Justificación es completa?",
        max_length=2,
        choices=ANSWERS,
        default='',
        blank=True,
        null=True,
    )
    approval_instance = models.CharField(
        verbose_name="¿Cumplió con las diferentes instancias de aprobación previas, Valida la solicitud?",
        max_length=2,
        choices=ANSWERS,
        default='',
        blank=True,
        null=True,
    )

    # finalized
    date_demand_finalized = models.DateTimeField(
        verbose_name="Fecha Finalizacion",
        blank=True,
        null=True,
    )
    time_demand_finalized = models.TimeField(
        verbose_name="Druación proceso",
        blank=True,
        null=True,
    )
    comment_finalized = models.TextField(
        verbose_name="Comentario finalizacion",
        blank=True,
        null=True,
        default='',
    )

    def __str__(self):
        return self.demand.title

    class Meta:
        verbose_name = "Recepción"
        verbose_name_plural = "Recepciones"


class Channels(models.Model):
    title = models.CharField(
        verbose_name="Titulo",
        max_length=40,
        blank=False,
        null=False,
        default=''
    )
    objects = models.Manager()
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
        verbose_name = "Canal (T)"
        verbose_name_plural = "Canales (T)"


class Negotiation(ProcessesManager):
    ANSWERS = [
        ('Y', 'Si'),
        ('N', 'No'),
    ]
    SUB_PROCESS = [
        ('demand-validation', 'Validación Solicitud'),
        ('provider-confirmation', 'Confirmación de Proveedor'),
        ('definition-objetives-and-scope', 'Definición Objetivos & Alcance'),
        ('scope-validation', 'Validación de alcance'),
        ('structuring-of-the-agreement', 'Estructuración del Convenio'),
    ]
    STATUS = [
        ('do', 'Aprobado'),
        ('de', 'Rechazado'),
    ]
    TYPE_TIME = [
        ('days', 'Días'),
    ]
    demand_subprocess = models.CharField(
        verbose_name="Sub proceso",
        max_length=35,
        choices=SUB_PROCESS,
        blank=True,
        null=True,
    )

    # in process
    date_demand_validation = models.DateTimeField(
        verbose_name="Fecha Validación Solicitud",
        blank=True,
        null=True,
    )
    doc_demand_validation = models.ManyToManyField(
        Documents,
        blank=True,
        null=True,
        verbose_name="Docuemnto Validación Solicitud",
        default='',
    )
    date_demand_confirmation = models.DateTimeField(
        verbose_name="Fecha Confirmación Proveedor",
        blank=True,
        null=True,
    )
    date_definition_objetives = models.DateTimeField(
        verbose_name="Fecha Definición Objetivos y Alcance",
        blank=True,
        null=True,
    )
    doc_definition_objetives = models.ManyToManyField(
        Documents,
        blank=True,
        null=True,
        verbose_name="Docuemnto Definición Objetivos y Alcance",
        related_name="document_definition_objetives",
        default='',
    )
    date_scope_validate = models.DateTimeField(
        verbose_name="Fecha Validación de alcance",
        blank=True,
        null=True,
    )
    status_demand_negotiation = models.CharField(
        verbose_name="Estado negociación",
        max_length=2,
        choices=STATUS,
        blank=True,
        null=True,
    )
    doc_structuring_agreement = models.ManyToManyField(
        Documents,
        blank=True,
        null=True,
        verbose_name="Docuemnto Estructuración del Convenio",
        related_name="document_structuring_agreement",
        default='',
    )
    date_structuring_agreement = models.DateTimeField(
        verbose_name="Fecha Estructuración del Convenio",
        blank=True,
        null=True,
    )
    date_agreed = models.DateField(
        verbose_name="Fecha Acordada Entrega",
        blank=True,
        null=True,
    )
    time = models.IntegerField(
        verbose_name="Frecuencia actualización",
        blank=True,
        null=True,
    )
    type_time = models.CharField(
        verbose_name="Tipo",
        max_length=6,
        choices=TYPE_TIME,
        blank=True,
        null=True,
    )
    channel = models.ForeignKey(
        Channels,
        verbose_name="Canal Habilitado",
        default='',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    date_agreement = models.DateField(
        verbose_name="Duración del convenio",
        blank=True,
        null=True,
    )
    consideration = models.CharField(
        verbose_name="Servicios de contraprestacion al provedor ",
        max_length=35,
        blank=True,
        null=True,
        default='',
    )

    # revision
    date_revision = models.DateTimeField(
        verbose_name="Fecha Revision",
        blank=True,
        null=True,
    )
    doc_revision = models.ManyToManyField(
        Documents,
        blank=True,
        null=True,
        verbose_name="Docuemntos Revision",
        related_name="document_revision",
        default='',
    )
    meets_expectations = models.CharField(
        verbose_name="¿Cumple el alcance y expectativa previsto entre ambas partes?",
        max_length=2,
        choices=ANSWERS,
        default='',
        blank=True,
        null=True,
    )
    required_documentation = models.CharField(
        verbose_name="¿El convenio hasta esta instancia cumple con la documentación requerida?",
        max_length=2,
        choices=ANSWERS,
        default='',
        blank=True,
        null=True,
    )
    ready_sign = models.CharField(
        verbose_name="¿Está listo para la firma de ambas partes?",
        max_length=2,
        choices=ANSWERS,
        default='',
        blank=True,
        null=True,
    )

    # finalize
    date_finalize = models.DateTimeField(
        verbose_name="Fecha Finalización",
        blank=True,
        null=True,
    )
    time_demand_finalized = models.DurationField(
        verbose_name="Druación proceso",
        blank=True,
        null=True,
    )
    comment_finalized = models.TextField(
        verbose_name="Comentario finalizacion",
        blank=True,
        null=True,
        default='',
    )

    def __str__(self):
        return self.demand.title

    class Meta:
        verbose_name = "Negociación"
        verbose_name_plural = "Negociaciones"


class ProviderDemand(models.Model):
    STATUS_DEMAND = [
        ('do', 'Aceptada'),
        ('pe', 'Pendiente'),
        ('de', 'Rechazado'),
    ]
    STATUS_RECORD = [
        ('do', 'Disponible'),
        ('pe', 'Pendiente'),
    ]
    negotiation = models.ForeignKey(
        Negotiation,
        blank=True,
        null=True,
        verbose_name="Negociación",
        default='',
        on_delete=models.CASCADE
    )
    provider_entity = models.ForeignKey(
        ProviderEntity,
        blank=True,
        null=True,
        verbose_name="Entidad Proveedora",
        default='',
        on_delete=models.CASCADE
    )
    status_demand = models.CharField(
        verbose_name="Estado solicitud",
        max_length=35,
        choices=STATUS_DEMAND,
        blank=True,
        null=True,
    )
    status_record = models.CharField(
        verbose_name="Estado soliciud",
        max_length=35,
        choices=STATUS_RECORD,
        blank=True,
        null=True,
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        default=settings.SITE_ID
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
    )
    modified_date = models.DateTimeField(
        auto_now=True,
    )
    objects = models.Manager()
    on_site = CurrentSiteManager()


class Transfer(ProcessesManager):

    def __str__(self):
        return self.demand.title

    class Meta:
        verbose_name = "Proceso Transferencia"
        verbose_name_plural = "Proceso Transferencia"


class Transfers(models.Model):
    ANSWERS = [
        ('Y', 'Si'),
        ('N', 'No'),
    ]
    STATUS_DEMAND = [
        ('ac', 'Aceptada'),
        ('pe', 'Pendiente'),
        ('de', 'Rechazado'),
    ]
    transfer = models.ForeignKey(
        Transfer,
        verbose_name="Transferencia",
        default='',
        on_delete=models.CASCADE
    )
    channel = models.ForeignKey(
        Channels,
        verbose_name="Canal Habilitado",
        default='',
        on_delete=models.CASCADE
    )
    status_transfer = models.CharField(
        verbose_name="Estado transferencia",
        max_length=35,
        choices=STATUS_DEMAND,
        default='ac',
    )
    number_deliveries = models.CharField(
        verbose_name="Nombre de entrega",
        max_length=35,
        default=''
    )
    date_delivery = models.DateField(
        verbose_name="Fecha de Entrega",
        default=date.today
    )
    frequency_delivery = models.IntegerField(
        verbose_name="Frecuencia de entrega",
        default=0
    )
    frequency_date_delivery = models.DateField(
        verbose_name="Fecha de Entrega",
        default=date.today
    )
    comment = models.TextField(
        verbose_name="Comentario",
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
        verbose_name="Publicación",
        auto_now_add=True
    )
    modified_date = models.DateTimeField(
        verbose_name="Actualización",
        auto_now=True
    )
    reviewed = models.BooleanField(
        verbose_name='Revisado',
        default=False,
    )
    date_reviewed = models.DateTimeField(
        verbose_name="Fecha Revisión",
        blank=True,
        null=True,
    )
    comment_review = models.TextField(
        verbose_name="Comentario Revisión",
        blank=True,
        null=True,
        default='',
    )
    date_finalize = models.DateTimeField(
        verbose_name="Fecha Finalización",
        blank=True,
        null=True,
    )
    comment_finalize = models.TextField(
        verbose_name="Comentario finalización",
        blank=True,
        null=True,
        default='',
    )
    finalize = models.BooleanField(
        verbose_name='Finalizado',
        default=False,
    )
    validate_preparation = models.BooleanField(
        verbose_name='Preparación',
        default=False,
    )

    # questions
    open_base = models.CharField(
        verbose_name="¿Se puede abrir la base?",
        max_length=2,
        choices=ANSWERS,
        default='Y',
        blank=True,
        null=True,
    )
    expected_size = models.CharField(
        verbose_name="¿El tamaño corresponde al esperado?",
        max_length=2,
        choices=ANSWERS,
        default='Y',
        blank=True,
        null=True,
    )
    meets_terms = models.CharField(
        verbose_name="¿Cumple con los términos pactados en convenió?",
        max_length=2,
        choices=ANSWERS,
        default='Y',
        blank=True,
        null=True,
    )
    approve_reception_bd = models.CharField(
        verbose_name="¿Aprueba la recepcion de esta base de acuerdo a las espectativas que tiene la entidad?",
        max_length=2,
        choices=ANSWERS,
        default='Y',
        blank=True,
        null=True,
    )
    preparation = models.BooleanField(
        verbose_name='¿Tiene preparación?',
        default=False,
    )

    def __str__(self):
        return self.transfer.demand.title

    class Meta:
        verbose_name = "Transferencia"
        verbose_name_plural = "Transferencias"


class Preparation(ProcessesManager):

    def __str__(self):
        return self.demand.title

    class Meta:
        verbose_name = "Proceso Preparación"
        verbose_name_plural = "Proceso Preparación"


class Preparations(models.Model):
    SUB_PROCESS = [
        ('consistency', 'Consistencia'),
        ('standardization-normalization', 'Estandarización y Normalizaciónr'),
        ('anomaly-detection', 'Detección de anomalías'),
        ('anonymization-completeness', 'Anonimización y completitud'),
    ]
    ASSESSMENT = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    ASSESSMENT_1 = [
        ('Respuesta 1', 'Siempre puntual'),
        ('Respuesta 2', 'Generalmente puntual'),
        ('Respuesta 3', 'A veces puntual, a veces no'),
        ('Respuesta 4', 'Generalmente impuntual'),
        ('Respuesta 5', 'Siempre impuntual'),
    ]
    ASSESSMENT_2 = [
        ('Respuesta 1', 'Ningún impacto'),
        ('Respuesta 2', 'Impacto menor, no afectó plazos'),
        ('Respuesta 3', 'Impacto moderado, se ajustaron algunos procesos'),
        ('Respuesta 4', 'Impacto alto, se retrasaron tareas críticas'),
        ('Respuesta 5', 'No se pudo realizar el análisis a tiempo'),
    ]
    ASSESSMENT_3 = [
        ('Respuesta 1', 'Totalmente adecuada'),
        ('Respuesta 2', 'Adecuada en la mayoría de los casos'),
        ('Respuesta 3', 'Medianamente adecuada'),
        ('Respuesta 4', 'Frecuencia insuficiente'),
        ('Respuesta 5', 'Totalmente inadecuada'),
    ]
    preparation = models.ForeignKey(
        Preparation,
        verbose_name="Preparación",
        default='',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    transfer = models.ForeignKey(
        Transfers,
        verbose_name="Transferencia",
        default='',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    demand_subprocess = models.CharField(
        verbose_name="Sub proceso",
        max_length=50,
        choices=SUB_PROCESS,
        blank=True,
        null=True,
        default='consistency'
    )
    date_verification = models.DateTimeField(
        verbose_name="Fecha Verificación",
        blank=True,
        null=True,
    )
    comment = models.TextField(
        verbose_name="Comentario",
        blank=True,
        null=True,
        default='',
    )
    # in process
    date_consistency = models.DateTimeField(
        verbose_name="Fecha Consistencia",
        blank=True,
        null=True,
    )
    doc_consistency = models.ManyToManyField(
        Documents,
        blank=True,
        null=True,
        verbose_name="Docuemnto Consistencia",
        related_name="document_consistency",
        default='',
    )
    consistency_functionary = models.ForeignKey(
        Functionary,
        verbose_name="Funcionario consistencia",
        help_text='Fucionar asignado para responder las preguntas de cosistencia',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default='',
    )
    consistency_answer = models.BooleanField(
        verbose_name='Preguntas Respondidas',
        default=False,
    )
    consistency_question_1 = models.IntegerField(
        verbose_name="¿Las relaciones entre variables mantienen consistencia lógica y estadística dentro del registro (por ejemplo, edad vs. fecha de nacimiento, nivel educativo vs. edad)? Escala Likert: 1 = Nunca, 2 = Rara vez, 3 = Algunas veces, 4 = Frecuentemente, 5 = Siempre",
        max_length=2,
        choices=ASSESSMENT,
        blank=True,
        null=True,
    )
    consistency_question_2 = models.IntegerField(
        verbose_name="¿Se emplean de manera homogénea los códigos, formatos y clasificaciones (geográficas, institucionales, categóricas, etc.) en todas las unidades de registro y períodos de referencia? Escala Likert: 1 = Totalmente en desacuerdo, 2 = En desacuerdo, 3 = Ni de acuerdo ni en desacuerdo, 4 = De acuerdo, 5 = Totalmente de acuerdo",
        max_length=2,
        choices=ASSESSMENT,
        blank=True,
        null=True,
    )
    consistency_question_3 = models.IntegerField(
        verbose_name="¿Los campos obligatorios están completos en todos los registros? Escala Likert: 1 = Totalmente en desacuerdo, 2 = En desacuerdo, 3 = Ni de acuerdo ni en desacuerdo, 4 = De acuerdo, 5 = Totalmente de acuerdo",
        max_length=2,
        choices=ASSESSMENT,
        blank=True,
        null=True,
    )
    date_standarization = models.DateTimeField(
        verbose_name="Fecha Estandarización",
        blank=True,
        null=True,
    )
    doc_standarization = models.ManyToManyField(
        Documents,
        blank=True,
        null=True,
        verbose_name="Docuemnto Estandarización",
        related_name="document_standarization",
        default='',
    )
    standardization_functionary = models.ForeignKey(
        Functionary,
        verbose_name="Estandarización consistencia",
        related_name="standardization_functionary",
        help_text='Fucionar asignado para responder las preguntas de cosistencia',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default='',
    )
    standardization_answer = models.BooleanField(
        verbose_name='Preguntas Respondidas',
        default=False,
    )
    standarization_question_1 = models.IntegerField(
        verbose_name="Las bases de datos estandarizadas son aquellas que contienen estructuras o formatos de datos consistentes; como, por ejemplo; El Registro de personas: cada registro representa a una persona, y cada columna en la base de datos representa un atributo de cada persona de manera individual. En ese sentido; ¿Qué tan estandarizada se encuentra la base de datos que usted utiliza? (Califique de 1 a 5) Escala Likert: 1 = Poco estandarizada, 2= Algo estandarizada, 3= Medianamente estandarizada, 4=Bastante estandarizada, 5= Muy estandarizada",
        max_length=2,
        choices=ASSESSMENT,
        blank=True,
        null=True,
    )
    standarization_question_2 = models.IntegerField(
        verbose_name="Las bases de datos normalizadas son aquellas que contienen datos organizados con tablas relacionadas, con el fin de evitar redundancias. Ej. La tabla de datos referida a personas que esté relacionada con otra tabla mediante una variable común (DNI), como por ejemplo la solicitud de clientes de compras de producto con despacho a domicilio, tiene como atributo el DNI del cliente solicitante. En este caso, la variable común es el DNI. En ese sentido; ¿Qué tan normalizada se encuentra la base de datos? (Califique de 1 a 5) Escala Likert: 1 = Poco estandarizada, 2= Algo estandarizada, 3= Medianamente estandarizada, 4=Bastante estandarizada, 5= Muy estandarizada",
        max_length=2,
        choices=ASSESSMENT,
        blank=True,
        null=True,
    )
    standarization_question_3 = models.IntegerField(
        verbose_name="¿Qué tan coherente y eficiente encuentra el manejo de la estructura y organización de la base de datos en términos de estandarización y normalización? Escala Likert: 1= Muy ineficiente, 2=Ineficiente, 3=Moderadamente Eficiente, 4=Eficiente, 5=Muy Eficiente ",
        max_length=2,
        choices=ASSESSMENT,
        blank=True,
        null=True,
    )
    date_detection = models.DateTimeField(
        verbose_name="Fecha Detección de anomalías",
        blank=True,
        null=True,
    )
    doc_detection = models.ManyToManyField(
        Documents,
        blank=True,
        null=True,
        verbose_name="Documento detección Anomalías",
        related_name="document_detection",
        default='',
    )
    anomaly_functionary = models.ForeignKey(
        Functionary,
        verbose_name="Detección de anomalías",
        help_text='Fucionar asignado para responder las preguntas de detección de anomalías',
        related_name="anomaly_functionary",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default='',
    )
    anomaly_answer = models.BooleanField(
        verbose_name='Preguntas Respondidas',
        default=False,
    )
    detection_question_1 = models.IntegerField(
        verbose_name="¿Con qué frecuencia su institución realiza en forma sistémica auditorías internas donde se vinculada a la calidad, gestión y/o informáticas? (Califique de 1 a 5) Escala Likert: 1 = Nunca, 2 = Raramente, 3 = Ocasionalmente, 4 = Frecuentemente, 5 = Muy frecuentemente",
        max_length=2,
        choices=ASSESSMENT,
        blank=True,
        null=True,
    )
    detection_question_2 = models.IntegerField(
        verbose_name="¿Qué tan útil son los datos del registro administrativo para generar estadísticas? (Califique de 1 a 5) Escala Likert: 1 = Poco útiles, 2= Algo útiles, 3= Medianamente útiles, 4= Bastante útiles, 5= Muy útiles",
        max_length=2,
        choices=ASSESSMENT,
        blank=True,
        null=True,
    )
    detection_question_3 = models.IntegerField(
        verbose_name="¿El instrumento de recolección de datos garantiza la fiabilidad de los datos? (Califique de 1 ó 5) Escala Likert: 1 = No garantiza, 5= Sí garantiza",
        max_length=2,
        choices=ASSESSMENT,
        blank=True,
        null=True,
    )
    date_anonymization = models.DateTimeField(
        verbose_name="Fecha Anonimización y completitud",
        blank=True,
        null=True,
    )
    doc_anonymization = models.ManyToManyField(
        Documents,
        blank=True,
        null=True,
        verbose_name="Docuemnto Anonimización y completitud",
        related_name="document_anonymization",
        default='',
    )
    anonymization_functionary = models.ForeignKey(
        Functionary,
        verbose_name="Anonimización y completitud",
        help_text='Fucionar asignado para responder las preguntas de Anonimización y completitud',
        related_name="anonymization_functionary",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default='',
    )
    anonymization_answer = models.BooleanField(
        verbose_name='Preguntas Respondidas',
        default=False,
    )
    anonymization_question_1 = models.IntegerField(
        verbose_name="¿Qué tanto es el nivel de riesgo de poder identificar a una persona con la base de datos? (Califique de 1 a 5) Escala Likert: 1 = Poco probable, 2= Algo probable, 3= Medianamente probable, 4= Bastante probable, 5=Altamente probable",
        max_length=2,
        choices=ASSESSMENT,
        blank=True,
        null=True,
    )
    anonymization_question_2 = models.IntegerField(
        verbose_name="¿Qué tanto es el nivel de sensibilidad de los datos presentada en el registro? (Califique de 1 a 5) Escala Likert: 1 = Poco sensible, 2= Algo sensible, 3= Medianamente sensible, 4= Bastante sensible, 5=Altamente sensible",
        max_length=2,
        choices=ASSESSMENT,
        blank=True,
        null=True,
    )
    anonymization_question_3 = models.IntegerField(
        verbose_name="¿Qué tan difícil resulta anonimizar los datos del registro? (Califique de 1 a 5) Escala Likert: 1 = Poco difícil, 2= Algo difícil, 3= Medianamente difícil, 4= Bastante difícil, 5=Altamente difícil",
        max_length=2,
        choices=ASSESSMENT,
        blank=True,
        null=True,
    )
    # revision
    date_revision = models.DateTimeField(
        verbose_name="Fecha Revisión",
        blank=True,
        null=True,
    )
    comment_revision = models.TextField(
        verbose_name="Comentario Revisión",
        blank=True,
        null=True,
        default='',
    )
    question_1 = models.CharField(
        verbose_name="¿La base de datos fue entregada dentro del plazo acordado?",
        max_length=255,
        choices=ASSESSMENT_1,
        blank=True,
        null=True,
        default=''
    )
    question_2 = models.CharField(
        verbose_name="¿La base de datos fue entregada dentro del plazo acordado?",
        max_length=255,
        choices=ASSESSMENT_2,
        blank=True,
        null=True,
        default=''
    )
    question_3 = models.CharField(
        verbose_name="¿La frecuencia de entrega la base de datos es adecuada?",
        max_length=255,
        choices=ASSESSMENT_3,
        blank=True,
        null=True,
        default=''
    )
    # finalize
    date_finalize = models.DateTimeField(
        verbose_name="Fecha Finalización",
        blank=True,
        null=True,
    )
    comment_finalize = models.TextField(
        verbose_name="Comentario Finalización",
        blank=True,
        null=True,
        default='',
    )
    finalize = models.BooleanField(
        verbose_name='Finalizado',
        default=False,
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
        return self.transfer.number_deliveries

    class Meta:
        verbose_name = "Preparación"
        verbose_name_plural = "Preparaciones"


class Evaluation (ProcessesManager):
    doc_evaluation = models.ManyToManyField(
        Documents,
        blank=True,
        null=True,
        verbose_name="Plan de mejora",
        default='',
    )
    date_finalize = models.DateTimeField(
        verbose_name="Fecha Finalización",
        blank=True,
        null=True,
    )
    comment_finalize = models.TextField(
        verbose_name="Comentario Finalización",
        blank=True,
        null=True,
        default='',
    )
    finalize = models.BooleanField(
        verbose_name='Finalizado',
        default=False,
    )

    def __str__(self):
        return self.demand.title

    class Meta:
        verbose_name = "Proceso Evaluación"
        verbose_name_plural = "Proceso Evaluación"


class Evaluations (models.Model):
    FREQUENCY = [
        ('2', '2 Meses'),
        ('4', '4 Meses'),
        ('6', '6 Meses'),
    ]

    ASSESSMENT = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        
    ]

    ASSESSMENT_1 = [
        (1, 'Nunca'),
        (2, 'Rara vez'),
        (3, 'A veces'),
        (4, 'Frecuentemente'),
        (5, 'Siempre'),
    ]

    ASSESSMENT_2 = [
        (1, 'Nada comparables / nada consistentes'),
        (2, 'Poco comparables / poco consistentes'),
        (3, 'Medianamente comparables / consistentes'),
        (4, 'Bastante comparables / consistentes'),
        (5, 'Totalmente comparables / consistentes'),
    ]

    ASSESSMENT_3 = [
        (1, 'Nada comparables / nada consistentes'),
        (2, 'Poco comparables / poco consistentes'),
        (3, 'Medianamente comparables / consistentes'),
        (4, 'Bastante comparables / consistentes'),
        (5, 'Totalmente comparables / consistentes'),
    ]

    ASSESSMENT_4 = [
        (1, 'Nada comparables / nada consistentes'),
        (2, 'Poco comparables / poco consistentes'),
        (3, 'Medianamente comparables / consistentes'),
        (4, 'Bastante comparables / consistentes'),
        (5, 'Totalmente comparables / consistentes'),
    ]

    ASSESSMENT_5 = [
        (1, 'Nunca'),
        (2, 'Rara vez'),
        (3, 'A veces'),
        (4, 'Frecuentemente'),
        (5, 'Siempre'),
    ]

    ASSESSMENT_6 = [
        (1, 'Muy deficiente'),
        (2, 'Deficiente'),
        (3, 'Aceptable'),
        (4, 'Buena'),
        (5, 'Excelente'),
    ]

    ASSESSMENT_7 = [
        (1, 'Nada comparables / nada consistentes'),
        (2, 'Poco comparables / poco consistentes'),
        (3, 'Medianamente comparables / consistentes'),
        (4, 'Bastante comparables / consistentes'),
        (5, 'Totalmente comparables / consistentes'),
    ]

    ASSESSMENT_8 = [
        (1, 'Muy deficiente'),
        (2, 'Deficiente'),
        (3, 'Aceptable'),
        (4, 'Buena'),
        (5, 'Excelente'),
    ]

    ASSESSMENT_9 = [
        (1, 'Nunca'),
        (2, 'Rara vez'),
        (3, 'A veces'),
        (4, 'Frecuentemente'),
        (5, 'Siempre'),
    ]

    ASSESSMENT_10 = [
        (1, 'Nunca'),
        (2, 'Rara vez'),
        (3, 'A veces'),
        (4, 'Frecuentemente'),
        (5, 'Siempre'),
    ]

    evaluation = models.ForeignKey(
        Evaluation,
        verbose_name="Evaluación",
        default='',
        on_delete=models.CASCADE
    )
    functionary = models.ForeignKey(
        Functionary,
        verbose_name="Funcionario",
        help_text='Fucionar asignado para responder la evaluación',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default='',
    )
    date_notification = models.DateTimeField(
        verbose_name="Fecha de notificación",
        blank=True,
        null=True,
    )
    frequency = models.CharField(
        verbose_name="Frecuencia de evaluación",
        max_length=50,
        choices=FREQUENCY,
        blank=True,
        null=True,
        default='2'
    )
    frequency_delivery = models.IntegerField(
        verbose_name="Numero de frecuencia de evaluación",
        blank=True,
        null=True,
        default=0
    )
    frequency_date_delivery = models.DateField(
        verbose_name="Fecha de evaluación",
        blank=True,
        null=True,
        default=date.today
    )
    finish_date = models.DateTimeField(
        verbose_name="Fecha de finalización",
        blank=True,
        null=True,
    )
    interview = models.TextField(
        verbose_name="Comentario de entrevista",
        blank=True,
        null=True,
        default='',
    )
    question_1 = models.CharField(
        verbose_name="1.¿Se han establecido puntos de contacto o canales de comunicación para personas que necesiten ayuda adicional para acceder a la información sobre los indicadores?",
        max_length=255,
        choices=ASSESSMENT_1,
        blank=True,
        null=True,
        default=''
    )
    question_2 = models.CharField(
        verbose_name="2.¿Los indicadores son comparables a lo largo del tiempo y entre programas similares?",
        max_length=255,
        choices=ASSESSMENT_2,
        blank=True,
        null=True,
        default=''
    )
    question_3 = models.CharField(
        verbose_name="3.¿Los indicadores son comparables entre programas similares o entre diferentes jurisdicciones?",
        max_length=255,
        choices=ASSESSMENT_3,
        blank=True,
        null=True,
        default=''
    )
    question_4 = models.CharField(
        verbose_name="4.¿Se ha asegurado la consistencia en la recopilación y presentación de datos para garantizar la continuidad de los indicadores?",
        max_length=255,
        choices=ASSESSMENT_4,
        blank=True,
        null=True,
        default=''
    )
    question_5 = models.CharField(
        verbose_name="5.¿Se han establecido estándares de calidad para la medición y presentación de los indicadores?",
        max_length=255,
        choices=ASSESSMENT_5,
        blank=True,
        null=True,
        default=''
    )
    question_6 = models.IntegerField(
        verbose_name="6.¿Se han identificado y abordado posibles fuentes de error en la medición de los indicadores?",
        max_length=2,
        choices=ASSESSMENT_6,
        blank=True,
        null=True,
    )
    question_7 = models.IntegerField(
        verbose_name="7.¿Se utiliza algún tipo de codificación o estandarización para facilitar la comparación entre diferentes indicadores?",
        max_length=2,
        choices=ASSESSMENT_7,
        blank=True,
        null=True,
    )
    question_8 = models.IntegerField(
        verbose_name="8.¿Los datos utilizados para calcular los indicadores se recopilan y actualizan regularmente?",
        max_length=2,
        choices=ASSESSMENT_8,
        blank=True,
        null=True,
    )
    question_9 = models.IntegerField(
        verbose_name="9.¿Se realizan auditorías o revisiones periódicas de los indicadores?",
        max_length=2,
        choices=ASSESSMENT_9,
        blank=True,
        null=True,
    )
    question_10 = models.IntegerField(
        verbose_name="10.¿Se establecen plazos claros para la recopilación y presentación de datos relacionados con los indicadores?",
        max_length=2,
        choices=ASSESSMENT_10,
        blank=True,
        null=True,
    )
    result = models.FloatField(
        verbose_name="Pregunta 10",
        blank=True,
        null=True,
    )
    evaluation_answer = models.BooleanField(
        verbose_name='Preguntas Respondidas',
        default=False,
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
        return self.evaluation.demand.title

    class Meta:
        verbose_name = "Evaluaciónes"
        verbose_name_plural = "Evaluaciónes"


class DocumentDefinitionObjetives (models.Model):
    name = models.CharField(
        verbose_name="Nombre del archivo",
        max_length=35,
        default=''
    )
    document = models.FileField(
        verbose_name="Documento ejemplo",
        validators=[FileType('docx')],
        upload_to='uploads/documents',
        blank=False,
        null=False,
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
        verbose_name="Publicación",
        auto_now_add=True
    )
    modified_date = models.DateTimeField(
        verbose_name="Actualización",
        auto_now=True
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Ejemplo Definición y objetivos"
        verbose_name_plural = "Ejemplo Definición y objetivos"


class ParticipationDemand (models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Usuario",
        on_delete=models.CASCADE,
    )
    demand = models.ForeignKey(
        Demands,
        verbose_name="Solicitud",
        on_delete=models.CASCADE,
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
        return self.user.username

    class Meta:
        verbose_name = "Participante"
        verbose_name_plural = "Participantes"
