from django import forms
from .models import ProviderEntity, ProviderDocuments, ProviderType, ProviderStatus, Stage, Divipola

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


class FilterDocumentsProvider(forms.Form):

    stage_document = forms.ModelChoiceField(
        label="Estado Documento",
        queryset=Stage.objects.all(),
        required=False,
    )


class FilterProviderForm(forms.Form):
    name = forms.CharField(
        label="Buscador",
        required=False,
    )
    type = forms.ModelChoiceField(
        label="Tipo de empresa",
        queryset=ProviderType.objects.all(),
        required=False,
    )
    status = forms.ModelChoiceField(
        label="Estado",
        queryset=ProviderStatus.objects.all(),
        required=False,
    )


class CreateProviderForm(forms.ModelForm):

    class DiviProvider(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            verbose_name='Aprobar',
            return obj.__str__

    location = DiviProvider(Divipola.on_site.all())
    class Meta:
        model = ProviderEntity
        fields = '__all__'
        exclude = [
            "site",
            "created_date",
            "modified_date"
        ]
        labels = {
        "Ubicación": "location"
        }


class CreateDocumetsForm(forms.ModelForm):
    class Meta:
        model = ProviderDocuments
        widgets = {'provider': forms.HiddenInput()}
        fields = '__all__'
        exclude = [
            "created_date",
            "modified_date"
        ]
