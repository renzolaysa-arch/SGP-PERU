from .models import ProviderEntity, ProviderStatus, ProviderType, Stage
from django import forms
import django_filters


class ProviderEntityFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        label="",
        lookup_expr='icontains'
    )
    type = django_filters.ModelMultipleChoiceFilter(
        queryset=ProviderType.objects.all().distinct(),
        field_name="type",
        widget=forms.CheckboxSelectMultiple(),
        label="Tipo de empresa",
    )
    status = django_filters.ModelMultipleChoiceFilter(
        queryset=ProviderStatus.objects.all().distinct(),
        field_name="status",
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = ProviderEntity
        fields = ['name', 'type', 'status', 'sector']


class DocumentsEntityFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        label="Buscador",
        lookup_expr='icontains'
    )
    created_date = django_filters.DateFilter(
        field_name='created_date',
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}),
        lookup_expr='contains',
        label='Fecha'
    )
    stage_document = django_filters.AllValuesFilter(
        label="Estado Documento",
        # queryset=Stage.objects.all(),
        required=True,

    )

    class Meta:
        model = ProviderEntity
        fields = ['name', 'created_date']
