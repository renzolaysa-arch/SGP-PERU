from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.conf import settings
from providers.models import ProviderEntity
from content.models import Divipola
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, FieldError
# Create your models here.


class InventoryTheme (models.Model):
    name_theme_inventory = models.CharField(
        verbose_name="Nombre Tema",
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
        return self.name_theme_inventory

    class Meta:
        verbose_name = "Tema del Inventario"
        verbose_name_plural = "Temas de los Inventarios"


class InventoryThematic (models.Model):
    name_thematic_inventory = models.CharField(
        verbose_name="Nombre Tema",
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
        return self.name_thematic_inventory

    class Meta:
        verbose_name = "Temática del Inventario"
        verbose_name_plural = "Temáticas de los Inventarios"


class InventoryStatus (models.Model):
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
        verbose_name = "Estado inventario"
        verbose_name_plural = "Estados de inventarios"


class TypeFormatSampleData(models.Model):
    type_format = models.CharField(
        verbose_name="Tipo de formato",
        max_length=15,
        blank=False,
        null=False,
        default='',
        help_text="Ejemplo: .xls, .xlsx, .csv, .sql, .json, .spss, .accdb"
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
        return self.type_format.lower()

    def clean(self):
        self.is_cleaned = True

        if self.type_format is not None and self.type_format.startswith('.'):
            super(TypeFormatSampleData, self).clean()
        else:
            raise ValidationError('No se reconoce formatos de extensión')

    def save(self, *args, **kwargs):
        if hasattr(self, 'is_cleaned'):
            if not self.is_cleaned:
                self.full_clean()
            super(TypeFormatSampleData, self).save(*args, **kwargs)
        else:
            super(TypeFormatSampleData, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Tipo Formato"
        verbose_name_plural = "Tipos de Formatos"


class TransferMediumSampleData(models.Model):
    transfer_medium = models.CharField(
        verbose_name="Medio de Transferencia",
        max_length=15,
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
        return self.transfer_medium

    class Meta:
        verbose_name = "Medio de Transferencia Base de Datos"
        verbose_name_plural = "Medios de Transferencia Base de Datos"


class TagsSampleData(models.Model):
    tags_sample_data = models.CharField(
        verbose_name="Tags Ejemplo Base de Datos",
        max_length=15,
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
        return self.tags_sample_data

    class Meta:
        verbose_name = "Tag Ejemplo Base de Datos"
        verbose_name_plural = "Tags Ejemplo Base de Datos"


class VariablesSampleData(models.Model):
    variables_sample_data = models.CharField(
        verbose_name="Variables Base de Datos",
        max_length=15,
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
        return self.variables_sample_data

    class Meta:
        verbose_name = "Variables Base de Datos"
        verbose_name_plural = "Variables Base de Datos"


class Inventory(models.Model):
    # TAB1
    title = models.CharField(
        verbose_name="Nombre registro administrativo",
        max_length=255,
        blank=False,
        null=False,
        default='',
    )
    administrative_record = [
        ('S', 'Si'),
        ('N', 'No'),
    ]
    record_choice = models.CharField(
        verbose_name="Registro administrativo activo",
        max_length=25,
        choices=administrative_record,
        blank=True,
        null=True,
        default='Si'
    )
    objective = models.TextField(
        verbose_name="Objetivo del registro administrativo",
        blank=True,
        null=True,
        default='',
        max_length=800,
    )
    target_population = models.TextField(
        verbose_name="¿Cuál es la población objetivo del registro administrativo?",
        blank=True,
        null=True,
        default='',
        max_length=800,
    )
    inventory_thematic_asociate = models.ForeignKey(
        InventoryThematic,
        verbose_name="Temática del área",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default='',
    )
    inventory_theme_asociate = models.ForeignKey(
        InventoryTheme,
        verbose_name="Tema",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default='',
    )
    # TAB2
    laws_decrees = [
        ('C.P', 'Constitución política'),
        ('L', 'Ley'),
        ('D.N', 'Decreto Nacional'),
        ('D.D', 'Decreto departamental'),
        ('D.M', 'Decreto Municipal'),
        ('O', 'Resolución, Ordenanza, Acuerdo'),
        ('N', 'Ninguna'),
        ('O.T', 'Otras'),
    ]
    use_laws_decrees = models.CharField(
        verbose_name="¿Cuál es la base legal o normativa que sustenta la creación del registro administrativo?",
        max_length=40,
        choices=laws_decrees,
        blank=True,
        null=True,
        default='Si'
    )
    political_constitution = models.CharField(
        verbose_name="Constitución política:",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    law = models.CharField(
        verbose_name="Ley:",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    decree = models.CharField(
        verbose_name="Decreto(Nacional, departamental, municipal):",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    choice_laws_decrees = models.CharField(
        verbose_name="Resolución, ordenanza:",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    decree_other = models.CharField(
        verbose_name="Otras:",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    year_creation = models.CharField(
        verbose_name="¿Cuál es el año de creación del registro administrativo? ",
        max_length=4,
        blank=True,
        null=True,
        default='',
    )
    provided_government_item = [
        ('Si', 'Si'),
        ('No', 'No'),
        ('No sabe', 'No sabe'),
    ]
    provided_government = models.CharField(
        verbose_name="¿El registro administrativo es proporcionado a otra(s) institución(es) del Estado?",
        max_length=25,
        choices=provided_government_item,
        blank=True,
        null=True,
        default='Si'
    )
    provided_government_which = models.CharField(
        verbose_name="¿Cuál? ",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    restriction_item = [
        ('Si', 'Si'),
        ('No', 'No'),
        ('No sabe', 'No sabe'),
    ]
    restriction = models.CharField(
        verbose_name="¿Existe alguna restricción  para la entrega de información al INE?",
        max_length=25,
        choices=restriction_item,
        blank=True,
        null=True,
        default='Si'
    )
    restriction_which_item = [
        ('Mandato legal', 'Mandato legal'),
        ('Acuerdos con los informantes', 'Acuerdos con los informantes'),
        ('Políticas de la entidad', 'Políticas de la entidad'),
    ]
    restriction_which = models.CharField(
        verbose_name="¿Cuál?",
        max_length=255,
        choices=restriction_which_item,
        blank=True,
        null=True,
        default='Mandato legal'
    )
    date_start_collection = models.DateField(
        verbose_name="Fecha de inicio de recolección de información:",
        blank=True,
        null=True,
    )
    date_finish_collection = models.DateField(
        verbose_name="Fecha de última de recolección de información:",
        blank=True,
        null=True,
    )
    year_creation_bd = models.CharField(
        verbose_name="¿Desde qué año se dispone del registro administrativo en base de datos?",
        max_length=4,
        blank=True,
        null=True,
        default='',
    )
    method_documentes_choice = [
        ('S', 'Si'),
        ('N', 'No'),
    ]
    method_document = models.CharField(
        verbose_name="¿El RA cuenta con alguno de los siguientes  documentos metodológicos o funcionales?",
        max_length=25,
        choices=method_documentes_choice,
        default='Si',
        blank=True,
        null=True,
    )
    methodologycal_documents = [
        ('M.D', 'Manual de diligenciamiento'),
        ('D.D', 'Diccionario de datos'),
        ('D.S', 'Ficha técnica'),
        ('O', 'Otros'),
    ]
    document_choice = models.CharField(
        verbose_name="Tipo de documento metodológico",
        max_length=40,
        choices=methodologycal_documents,
        blank=True,
        null=True,
        default='Manual de diligenciamiento'
    )
    other_methodologycal_document = models.CharField(
        verbose_name="Cuál tipo de documento metodológico",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    nomenclature_classifications = [
        ('S', 'Si'),
        ('N', 'No'),
    ]
    nomenclature_choice = models.CharField(
        verbose_name="¿Utiliza nomenclaturas o clasificaciones?",
        max_length=25,
        choices=nomenclature_classifications,
        blank=True,
        null=True,
        default='Si'
    )
    yes_nomenclature = models.CharField(
        verbose_name="Si, ¿cuáles?:",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    not_nomenclature = models.CharField(
        verbose_name="No, ¿por qué?:",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    method_collections = [
        ('Registro de datos por parte del funcionario (entrevistas)', 'Registro de datos por parte del funcionario (entrevistas)'),
        ('Usuarios responden formuarios', 'Usuarios responden formuarios'),
        ('Usuarios responden via web', 'Usuarios responden via web'),
        ('Mixto funcionario y usuario', 'Mixto funcionario y usuario'),
        ('Otros', 'Otros'),
    ]
    method_collections_choice = models.CharField(
        verbose_name="¿Qué método utiliza para la recolección de datos?",
        max_length=255,
        choices=method_collections,
        blank=True,
        null=True,
        default=''
    )
    other_methods_collections = models.CharField(
        verbose_name="Otros, ¿cuáles?",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    defined_form_item = [
        ('S', 'Si'),
        ('N', 'No'),
    ]
    defined_form = models.CharField(
        verbose_name="¿Cuenta el registro administrativo con un formulario definido, que contenga las variables necesarias para su captura?",
        max_length=25,
        choices=defined_form_item,
        blank=True,
        null=True,
        default='Si'
    )
    collection_frequency = [
        ('A', 'Anual'),
        ('S', 'Semestral'),
        ('B', 'Bimensual'),
        ('T', 'Trimestral'),
        ('M', 'Mensual'),
        ('D', 'Diaria'),
        ('P.E', 'Por evento'),
        ('O', 'Otros'),
    ]
    frequency_choice = models.CharField(
        verbose_name="¿Con qué frecuencia se realiza la recolección de datos?",
        max_length=255,
        choices=collection_frequency,
        blank=True,
        null=True,
        default='Anual'
    )
    other_frequency_collections = models.CharField(
        verbose_name="Otros, ¿cuáles?:",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    processing_tools = [
        ('E', 'Excel'),
        ('A', 'Access'),
        ('R', 'R'),
        ('S', 'SAS'),
        ('S.P', 'SPSS'),
        ('O.R', 'Oracle'),
        ('S.T', 'Stata'),
        ('O', 'Otros'),
    ]
    processing_choice = models.CharField(
        verbose_name="Indique cuáles de las herramientas utiliza para el procesamiento de datos:",
        max_length=255,
        choices=processing_tools,
        blank=True,
        null=True,
        default=''
    )
    other_proccesing_tools = models.CharField(
        verbose_name="Otros, ¿cuáles?:",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    geographic_coverages_type_item = [
        ('Nacional', 'Nacional'),
        ('Regional', 'Regional'),
        ('Departamental', 'Departamental'),
        ('Provincial', 'Provincial'),
        ('Comuna', 'Comuna'),
        ('Distrital', 'Distrital'),
        ('Municipal', 'Municipal'),
        ('Otro', 'Otro'),
    ]
    geographic_coverages_type = models.CharField(
        verbose_name="Cuál es la cobertura geográfica del RRAA?",
        max_length=255,
        choices=geographic_coverages_type_item,
        blank=True,
        null=True,
        default='Excel'
    )
    other_geographic_coverages_type = models.CharField(
        verbose_name="Cual?",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    geographic_coverages = models.ForeignKey(
        Divipola,
        verbose_name="Seleccione la cobertura geografica del RRAA",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default='',
    )
    #TAB3
    dependence_name = models.CharField(
        verbose_name="Nombre dependencia:",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    director_name = models.CharField(
        verbose_name="Nombre director:",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    position = models.CharField(
        verbose_name="Posición del director:",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    director_email = models.CharField(
        verbose_name="Correo electrónico del director",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    director_phone = models.CharField(
        verbose_name="Teléfono del director",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    responsible_custody = models.CharField(
        verbose_name="¿Cuál es área de su institución, responsable de gestionar o custodiar los datos del registro administrativo a nivel nacional?",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    responsible_report = models.CharField(
        verbose_name="¿Cuál es la unidad responsable de reportar los registros administrativos?",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    responsible_name = models.CharField(
        verbose_name="Nombre del responsable",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    responsible_position = models.CharField(
        verbose_name="Posición del responsable",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    responsible_email = models.CharField(
        verbose_name="Correo eléctronico responsable:",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    responsible_phone = models.CharField(
        verbose_name="Teléfono responsable temático:",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    #TAB4

    international_organization_choices = [
        ('Sí', 'Sí'),
        ('No', 'No')
    ]

    international_organization = models.CharField(
        verbose_name="¿El registro administrativo pertenece a algun organismo internacional?",
        max_length=255,
        choices=international_organization_choices,
        blank=True,
        null=True,
    )
    organism_documents = [
        ('S', 'Si'),
        ('N', 'No'),
        ('O', 'Otros'),
    ]
    organism_document_choice = models.CharField(
        verbose_name="¿El organismo posee leyes o documentos de creación propia?",
        max_length=25,
        choices=organism_documents,
        default='Si',
        blank=True,
        null=True,
    )
    documents_organization = models.CharField(
        verbose_name="¿Cuáles documentos usa?",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    national_organization = models.CharField(
        verbose_name="¿A qué organismo nacional pertenece?",
        max_length=255,
        choices=international_organization_choices,
        blank=True,
        null=True,
    )

    laws_decrets = models.CharField(
        verbose_name="Leyes, decretos ¿Cuál?:",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    own_creation = models.CharField(
        verbose_name="¿El organismo posee leyes o documentos de creación propia?",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    others_standars = models.CharField(
        verbose_name="Otros, ¿Cuáles?:",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    security_information = [
        ('B', 'Backups'),
        ('A.S', 'Aislamiento del servidor'),
        ('U.P', 'Utilización de perfiles'),
        ('O', 'Otros'),
    ]
    security_choice = models.CharField(
        verbose_name="¿Con cuál herramienta cuenta para garantizar la seguridad de la información?",
        max_length=255,
        choices=security_information,
        blank=True,
        null=True,
        default='Backups'
    )
    other_security_imformation = models.CharField(
        verbose_name="Otros, ¿cuáles?:",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    information_stored = [
        ('S', 'Si'),
        ('N', 'No'),
    ]
    information_stored_choice = models.CharField(
        verbose_name="¿La información es guardada en una base de datos?",
        max_length=255,
        choices=information_stored,
        blank=True,
        null=True,
        default='Si'
    )
    information_collected = [
        ('A', 'Anual'),
        ('S', 'Semestral'),
        ('B', 'Bimensual'),
        ('T', 'Trimestral'),
        ('M', 'Mensual'),
        ('D', 'Diaria'),
        ('O', 'Otra'),
    ]
    information_choice = models.CharField(
        verbose_name="¿Con qué frecuencia guarda información en la base de datos?",
        max_length=255,
        choices=information_collected,
        blank=True,
        null=True,
        default='Anual'
    )
    other_security_imformations = models.CharField(
        verbose_name="Otras, ¿cuáles?:",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    centralized_item = [
        ('Centralizada', 'Centralizada'),
        ('Descentralizada', 'Descentralizada'),
    ]
    centralized = models.CharField(
        verbose_name="¿Las bases de datos del registro administrativo se encuentran centralizadas o descentralizadas?",
        max_length=255,
        choices=centralized_item,
        blank=True,
        null=True,
        default='Si'
    )
    object_rra = models.CharField(
        verbose_name="¿Cuál es la unidad de observación (objeto) del registro administrativo?",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    consistency_review_item = [
        ('Si', 'Si'),
        ('No', 'No'),
    ]
    consistency_review = models.CharField(
        verbose_name="¿Se efectúa algún análisis de consistencia o de revisión a la base de datos del registro administrativo?",
        max_length=255,
        choices=consistency_review_item,
        blank=True,
        null=True,
        default='Si'
    )
    generate_information = models.CharField(
        verbose_name="¿La entidad hace uso de los datos del RA para generar información estadística (Agregados, indicadores, Resultados estadísticos, etc)?",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    aceess_user = [
        ('S', 'Si'),
        ('N', 'No'),
    ]
    external_user = models.CharField(
        verbose_name="¿Los usuarios externos, tienen acceso a los datos del RRAA?",
        max_length=255,
        choices=aceess_user,
        default='Si',
        blank=True,
        null=True,
    )
    statistics_user = models.CharField(
        verbose_name="¿Las estadísticas generadas están disponibles para usuarios públicos y/o privados?",
        max_length=255,
        choices=aceess_user,
        default='Si',
        blank=True,
        null=True,
    )
    main_reason_not_permissed = [
        ('P.E', 'Políticas de la entidad'),
        ('D.N', 'Disposición normativa'),
        ('A.I', 'Acuerdos con el informante'),
        ('C.C', 'Caracter confidencial'),
        ('O', 'Otra'),
    ]
    main_choice = models.CharField(
        verbose_name="¿Cuál es la razón principal por la cual no se permite el acceso a los datos del RA?",
        max_length=255,
        choices=main_reason_not_permissed,
        blank=True,
        null=True,
        default='Politicas de la entidad'
    )
    other_main_not_permissed = models.CharField(
        verbose_name="Otras, ¿cuáles?:",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    observations = models.TextField(
        verbose_name="Observaciones",
        max_length=800,
        blank=True,
        null=True,
        default='',
    )
    requierements = [
        ('S', 'Si'),
        ('N', 'No'),
    ]
    requierements_choice = models.CharField(
        verbose_name="Requerimientos ODS",
        max_length=25,
        choices=requierements,
        blank=True,
        null=True,
        default='Si'
    )
    ods_indicator = models.CharField(
        verbose_name="Indicador ODS:",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    #TAB4
    type_format_data_asociate = models.ForeignKey(
        TypeFormatSampleData,
        verbose_name="Tipo de Formato",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default='',
    )
    separared_options = [
        ('S.C', 'Separado por Comas'),
        ('S.P', 'Separado por Puntos'),
        ('S.G', 'Separado por Guion'),
        ('S.E', 'Separado por Espacios'),
    ]
    seperated_columns_file = models.CharField(
        verbose_name="¿Los valores están separados por:? ",
        max_length=30,
        choices=separared_options,
        blank=True,
        null=True,
        default=''
    )
    transfer_medium_data_asociate = models.ForeignKey(
        TransferMediumSampleData,
        verbose_name="Medio de Transferencia",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default='',
    )
    size_sample_data = models.IntegerField(
        verbose_name="Tamaño Aproximado de la Base de Datos",
        blank=True,
        null=True,
    )
    count_sample_data = models.IntegerField(
        verbose_name="Cantidad de archivos",
        blank=True,
        null=True,
    )
    file_example_sample_data = models.FileField(
        verbose_name="Archivo ejemplo Base de Datos",
        upload_to='uploads/sample-data',
        blank=True,
        null=True,
        default='',
    )
    name_file = models.CharField(
        verbose_name="Nombre del archivo",
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    date_load_field = models.DateField(
        verbose_name="Fecha Archivo Sample data",
        blank=True,
        null=True,
    )
    tag_sample_data_asociate = models.ManyToManyField(
        TagsSampleData,
        verbose_name="Tags Sample Data Asociado",
        blank=True,
        null=True,
        default=''
    )
    variables_sample_data_asociate = models.ManyToManyField(
        VariablesSampleData,
        verbose_name="Variables Sample Data Asociado",
        blank=True,
        null=True,
        default=''
    )
    entity_provider = models.ForeignKey(
        ProviderEntity,
        verbose_name="Proveedor",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default='',
    )
    custody = models.BooleanField(
        verbose_name='En custodia del INE',
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
        return self.title

    def clean(self):
        self.is_cleaned = True
        if self.file_example_sample_data:
            if self.file_example_sample_data is not None and self.file_example_sample_data.name.endswith(str(self.type_format_data_asociate)):
                super(Inventory, self).clean()
            else:
                raise ValidationError(
                    'La extensión del archivo no coincide con el Tipo de Formato' + str(self.type_format_data_asociate))

    def save(self, *args, **kwargs):
        if hasattr(self, 'is_cleaned'):
            if not self.is_cleaned:
                self.full_clean()
            super(Inventory, self).save(*args, **kwargs)
        else:
          super(Inventory, self).save(*args, **kwargs)  

    @property
    def empty_fields_count(self):
        fields = ["title", "objective", "inventory_theme_asociate", "inventory_thematic_asociate",  "use_laws_decrees",
                  "date_start_collection", "date_finish_collection", "method_document", "nomenclature_choice", "method_collections_choice",
                  "frequency_choice", "processing_choice", "geographic_coverages", "record_choice", "dependence_name",
                  "director_name", "position", "director_email", "director_phone", "responsible_name", "responsible_position", "responsible_email",
                  "responsible_phone", "international_organization", "organism_document_choice", "national_organization", "security_choice",
                  "information_stored_choice", "generate_information", "external_user", "observations", "requierements_choice", "type_format_data_asociate",
                  "transfer_medium_data_asociate", "size_sample_data", "count_sample_data",
                  "file_example_sample_data", "name_file", "date_load_field", "tag_sample_data_asociate", "variables_sample_data_asociate"]
        empty_values = {"", None}
        empty_values_count = 0
        for field in fields:
            field_value = getattr(self, field)
            if field_value in empty_values:
                empty_values_count += 1
        return empty_values_count

    @property
    def cont_columns_count(self):
        fields = ["title", "objective", "inventory_theme_asociate", "inventory_thematic_asociate", "use_laws_decrees",
                  "date_start_collection", "date_finish_collection", "method_document", "nomenclature_choice", "method_collections_choice",
                  "frequency_choice", "processing_choice", "geographic_coverages", "record_choice", "dependence_name",
                  "director_name", "position", "director_email", "director_phone", "responsible_name", "responsible_position", "responsible_email",
                  "responsible_phone", "international_organization", "organism_document_choice", "national_organization", "security_choice",
                  "information_stored_choice", "generate_information", "external_user", "observations", "requierements_choice", "type_format_data_asociate",
                  "transfer_medium_data_asociate", "size_sample_data", "count_sample_data",
                  "file_example_sample_data", "name_file", "date_load_field", "tag_sample_data_asociate", "variables_sample_data_asociate"]
        return len(fields)

    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"


class FollowInventory (models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Usuario",
        on_delete=models.CASCADE,
    )
    InventoryStatus = models.ForeignKey(
        Inventory,
        verbose_name="Inventario",
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
        return str(self.InventoryStatus)

    class Meta:
        verbose_name = "Inventario seguido"
        verbose_name_plural = "Inventarios seguidos"


class CommentInventory (models.Model):
    comment_text = models.TextField(
        verbose_name="Comentario",
        blank=False,
        null=False,
        default=''
    )
    inventory = models.ForeignKey(
        Inventory,
        verbose_name="Inventario",
        on_delete=models.CASCADE,
    )
    comment = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        verbose_name="Respuesta",
        on_delete=models.CASCADE,
        default='',
    )
    site = models.ForeignKey(
        Site,
        verbose_name="Sitio",
        on_delete=models.CASCADE,
        default=settings.SITE_ID
    )
    user_functionary_created = models.ForeignKey(
        'users.Functionary',
        verbose_name="Funcionario que comenta",
        on_delete=models.CASCADE,
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
        return self.comment_text

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"


ASSESSMENT = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
]


class QualityTest (models.Model):
    inventory = models.ForeignKey(
        Inventory,
        verbose_name="Inventario",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        User,
        verbose_name="Usuario",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    quality_question_1 = models.IntegerField(
        verbose_name="En una escala del 1 al 5, donde 1 indica la ausencia total de una definición clara y precisa y 5 indica una definición excepcionalmente clara, precisa y totalmente integrada, ¿Cómo evaluaría la claridad y regulación de la definición de las unidades o casos de interés de sus registros, en los documentos formales de su organización? Escala Likert: 1= No Implementado. 2= Parcialmente Implementado. 3= Moderadamente Implementado. 4= Ampliamente Implementado. 5= Completamente Implementado y Efectivo.",
        max_length=2,
        choices=ASSESSMENT,
        blank=True,
        null=True,
    )
    quality_question_2 = models.IntegerField(
        verbose_name="¿El registro administrativo incorpora identificadores únicos como Documento de Identidad, RUC, Número de Ficha Registral, Número de Seguro Social, etc., para rastrear y gestionar de manera efectiva las unidades o casos de interés?",
        max_length=2,
        choices=ASSESSMENT,
        blank=True,
        null=True,
    )
    quality_question_3 = models.IntegerField(
        verbose_name="En relación con el registro administrativo ingresado al SGP, ¿Dispone de un diccionario de variables que defina claramente el significado, la pertinencia y la exactitud de cada variable? Escala Likert: 1= No Disponible. 2= Parcialmente Completo. 3= Básicamente Adecuado. 4= Muy Bueno. 5= Excelente y Completamente Integrado.",
        max_length=2,
        choices=ASSESSMENT,
        blank=True,
        null=True,
    )
    quality_question_4 = models.IntegerField(
        verbose_name="En la base de datos del SGP, ¿Se verifica eficazmente que los datos registrados correspondan exclusivamente a la unidad de estudio especificada? Por ejemplo, en un registro de pacientes diabéticos, ¿se asegura que no se incluyan datos de pacientes no diabéticos? Escala Likert: 1= Totalmente Inadecuada. 2= Mayormente Inadecuada. 3= Moderadamente Adecuada. 4= Muy Adecuada. 5= Excelente y Completamente Confiable.",
        max_length=2,
        choices=ASSESSMENT,
        blank=True,
        null=True,
    )
    quality_question_5 = models.IntegerField(
        verbose_name="¿Con qué frecuencia se utilizan códigos y clasificadores internacionales estándar, como, por ejemplo: el CIE-10 para enfermedades o el CIU para actividades económicas, en su registro administrativo? Califique del 1 al 5, donde 1 indica que nunca se utilizan y 5 que se utilizan en todas las instancias pertinentes. Escala Likert: 1= Nunca. 2= Raramente. 3= Ocasionalmente. 4= Frecuentemente. 5= Siempre.",
        max_length=2,
        choices=ASSESSMENT,
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
        return self.inventory.title

    class Meta:
        verbose_name = "Test de Calidad"
        verbose_name_plural = "Test de Calidad"
