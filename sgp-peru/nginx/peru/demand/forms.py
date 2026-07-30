from django import forms
from .models import KeyWords, ProviderEntity, DemandsCategories, Reception, Negotiation, ProviderDemand, Transfers, Demands, Inventory, Project, Preparation, Preparations, DemandsStatus, DemandsTheme, Topic, Evaluations
from users.models import Functionary, Provider, Unit_Central
from content.models import Documents
from django.contrib.auth.models import User
from .widgets import DatePickerInput
from datetime import datetime
from django.apps import apps
from django.db import connections


def data_users_related():
    options_users = []
    modelo = apps.get_model('users', 'Provider')

    with connections['default'].cursor() as cursor:
        table_names = connections['default'].introspection.table_names()
        if modelo._meta.db_table in table_names:
            providers = Provider.on_site.filter(user__is_active=True)
            unit_central = Unit_Central.on_site.filter(user__is_active=True)
            functionary = Functionary.on_site.filter(user__is_active=True)
            users = [
                providers,
                unit_central,
                functionary
            ]

            for provider in users:
                for item in provider:
                    options_users.append((item.user.id, item.user.username))

    return options_users



ORDER_CHOICES = (
    ('', 'Ordenar por:'),
    ('name', 'Nombre'),
    ('created_date', 'Fecha'),
)


class FilterOrderForm(forms.Form):
    order = forms.CharField(
        label="",
        required=False,
        widget=forms.Select(
            choices=ORDER_CHOICES
        ),
    )


class CreateDemandForm(forms.ModelForm):
    inventory = forms.ModelChoiceField(
        queryset=Inventory.on_site.all(),
        required=False,
    )
    project = forms.ModelChoiceField(
        queryset=Project.on_site.all(),
        required=False,
    )
    category = forms.ModelChoiceField(
        queryset=DemandsCategories.on_site.all(),
        required=False,
    )
    status = forms.ModelChoiceField(
        queryset=DemandsStatus.on_site.all(),
        required=False,
    )
    theme = forms.ModelChoiceField(
        queryset=DemandsTheme.on_site.all(),
        required=False,
    )
    topic = forms.ModelChoiceField(
        queryset=Topic.on_site.all(),
        required=False,
    )
    key_words = forms.ModelMultipleChoiceField(
        queryset=KeyWords.on_site.all(),
        required=False,
    )

    class Meta:
        model = Demands
        fields = ["title", "inventory", "project", "description", "use", "use_other", "time", "product",
                  "category", "status", "theme", "topic", "key_words", "file_demand", "functionary"]
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Deje aquí los comentarios de la solicitud', 'required': True}),
            'functionary': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(CreateDemandForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            inventory = kwargs['initial']['inventory']
            functionary = kwargs['initial']['functionary']


class NoteDemandForm(forms.Form):
    commentary = forms.CharField(
        widget=forms.Textarea(attrs={
            "rows": 8,
            "cols": 100,
            "placeholder": 'Agregar una nota',
        }),
    )


class ReceptionForm(forms.ModelForm):
    class Meta:
        model = Reception
        fields = [
            "status_demand_validation",
            "demand_assessment",
            "status_demand_notification",
            "date_tentative_presentation",
            "comment",
            "comment_revision",
            "comment_finalized",
            "punctual_need",
            "full_justification",
            "approval_instance",
        ]
        widgets = {
            'status_demand_validation': forms.Select(attrs={'class': 'input-normal', 'required': True}),
            'demand_assessment': forms.RadioSelect(attrs={'class': 'radioinput', 'required': True}),
            'status_demand_notification': forms.Select(attrs={'class': 'input-normal', 'required': True}),
            'date_tentative_presentation': DatePickerInput(attrs={'class': 'input-normal', 'required': True, 'min': datetime.now().strftime("%Y-%m-%d")}),
            'comment': forms.Textarea(attrs={'placeholder': 'Inserte comentarios del proceso', 'required': True}),
            'comment_revision': forms.Textarea(attrs={'placeholder': 'Inserte comentarios del proceso', 'required': True}),
            'comment_finalized': forms.Textarea(attrs={'placeholder': 'Inserte comentarios del proceso'}),
            'punctual_need': forms.Select(attrs={'class': 'input-normal', 'required': True}),
            'full_justification': forms.Select(attrs={'class': 'input-normal', 'required': True}),
            'approval_instance': forms.Select(attrs={'class': 'input-normal', 'required': True}),
        }

    def __init__(self, *args, **kwargs):
        super(ReceptionForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            status = kwargs['initial']['status_demand_validation']
            if status and status == 'do':
                self.fields['status_demand_validation'].widget.attrs.update(
                    {'disabled': 'disabled'})


class PreparationForm(forms.ModelForm):
    class Meta:
        model = Preparations
        fields = [
            "consistency_question_1",
            "consistency_question_2",
            "consistency_question_3",
            "standarization_question_1",
            "standarization_question_2",
            "standarization_question_3",
            "detection_question_1",
            "detection_question_2",
            "detection_question_3",
            "anonymization_question_1",
            "anonymization_question_2",
            "anonymization_question_3",
        ]

        widgets = {
            'consistency_question_1': forms.RadioSelect(attrs={'class': 'radioinput', 'required': True}),
            'consistency_question_2': forms.RadioSelect(attrs={'class': 'radioinput', 'required': True}),
            'consistency_question_3': forms.RadioSelect(attrs={'class': 'radioinput', 'required': True}),
            'standarization_question_1': forms.RadioSelect(attrs={'class': 'radioinput', 'required': True}),
            'standarization_question_2': forms.RadioSelect(attrs={'class': 'radioinput', 'required': True}),
            'standarization_question_3': forms.RadioSelect(attrs={'class': 'radioinput', 'required': True}),
            'detection_question_1': forms.RadioSelect(attrs={'class': 'radioinput', 'required': True}),
            'detection_question_2': forms.RadioSelect(attrs={'class': 'radioinput', 'required': True}),
            'detection_question_3': forms.RadioSelect(attrs={'class': 'radioinput', 'required': True}),
            'anonymization_question_1': forms.RadioSelect(attrs={'class': 'radioinput', 'required': True}),
            'anonymization_question_2': forms.RadioSelect(attrs={'class': 'radioinput', 'required': True}),
            'anonymization_question_3': forms.RadioSelect(attrs={'class': 'radioinput', 'required': True}),
        }


class NegotiationForm(forms.ModelForm):
    class Meta:
        model = Negotiation
        fields = [
            "meets_expectations",
            "required_documentation",
            "ready_sign",
        ]
        widgets = {
            'meets_expectations': forms.Select(attrs={'class': 'input-normal', 'required': True}),
            'required_documentation': forms.Select(attrs={'class': 'input-normal', 'required': True}),
            'ready_sign': forms.Select(attrs={'class': 'input-normal', 'required': True}),
        }


class DocumentForm(forms.ModelForm):
    document = forms.FileField()

    assigned_to = forms.CharField(
        label="Asignado A:",
        required=True,
        widget=forms.Select(choices=data_users_related()),
    )

    copy_to = forms.CharField(
        label="Copia A:",
        required=True,
        widget=forms.SelectMultiple(choices=data_users_related()),
    )

    class Meta:
        model = Documents
        fields = [
            "title",
            "document",
            "requires_approval"
        ]

    def save(self, *args, **kwargs):
        m = super(DocumentForm, self).save(commit=False, *args, **kwargs)
        data = self.cleaned_data
        assigned_to = User.objects.get(id=data['assigned_to'])
        m.assigned_to = assigned_to
        m.save()
        return m



class ProviderDemandForm(forms.ModelForm):
    class Meta:
        model = ProviderDemand
        fields = [
            "status_demand",
            "status_record",
        ]
        widgets = {
            'status_demand': forms.CheckboxInput(attrs={
                'class': 'checkboxinput'
            }),
            'status_record': forms.Select(attrs={'class': 'input-normal'}),
        }


class TransfersForm(forms.ModelForm):
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'input-normal input-textarea',
                              'placeholder': 'Inserte comentarios del proceso'}),
    )
    number_deliveries = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input-normal'}),
    )
    frequency_delivery = forms.ChoiceField(
        required=True,
    )

    class Meta:
        model = Transfers

        fields = [
            "transfer",
            "status_transfer",
            "frequency_delivery",
            "number_deliveries",
            "date_delivery",
            "comment",
            "channel",
        ]

        widgets = {
            'transfer': forms.HiddenInput(),
            'status_transfer': forms.Select(attrs={'class': 'input-normal'}),
            'date_delivery': forms.DateInput(attrs={'class': 'input-normal', 'type': 'date', 'min': datetime.now().strftime("%Y-%m-%d")}),
            'channel': forms.Select(attrs={'class': 'input-normal'}),
        }

    def __init__(self, *args, **kwargs):
        super(TransfersForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            self.fields['frequency_delivery'].choices = kwargs['initial']['frequency_delivery']


class TransfersQuestionsForm(forms.ModelForm):

    class Meta:
        model = Transfers

        fields = [
            "open_base",
            "expected_size",
            "meets_terms",
            "approve_reception_bd",
        ]

        widgets = {
            'open_base': forms.Select(attrs={'class': 'input-normal', 'required': True}),
            'expected_size': forms.Select(attrs={'class': 'input-normal', 'required': True}),
            'meets_terms': forms.Select(attrs={'class': 'input-normal', 'required': True}),
            'approve_reception_bd': forms.Select(attrs={'class': 'input-normal', 'required': True}),
        }


class EvaluationsForm(forms.ModelForm):

    class Meta:
        model = Evaluations

        fields = [
            "question_1",
            "question_2",
            "question_3",
            "question_4",
            "question_5",
            "question_6",
            "question_7",
            "question_8",
            "question_9",
            "question_10",
        ]

        widgets = {
            'question_1': forms.RadioSelect(attrs={'required': True}),
            'question_2': forms.RadioSelect(attrs={'required': True}),
            'question_3': forms.RadioSelect(attrs={'required': True}),
            'question_4': forms.RadioSelect(attrs={'required': True}),
            'question_5': forms.RadioSelect(attrs={'required': True}),
            'question_6': forms.RadioSelect(attrs={'class': 'radioinput', 'required': True}),
            'question_7': forms.RadioSelect(attrs={'class': 'radioinput', 'required': True}),
            'question_8': forms.RadioSelect(attrs={'class': 'radioinput', 'required': True}),
            'question_9': forms.RadioSelect(attrs={'class': 'radioinput', 'required': True}),
            'question_10': forms.RadioSelect(attrs={'class': 'radioinput', 'required': True}),
        }


class PreparationRevisionForm(forms.ModelForm):
    class Meta:
        model = Preparations
        fields = [
            "question_1",
            "question_2",
            "question_3",
        ]