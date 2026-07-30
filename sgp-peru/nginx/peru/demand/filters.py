from .models import Demands, DemandsCategories, DemandsStatus, ProviderEntity
from django import forms
import django_filters
from django.forms.widgets import NumberInput


class DemandsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        label="",
    )
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=DemandsCategories.on_site.all().distinct(),
        field_name="category",
        widget=forms.CheckboxSelectMultiple(),
        label="Categoría",
    )
    status = django_filters.ModelMultipleChoiceFilter(
        queryset=DemandsStatus.on_site.all().distinct(),
        field_name="status",
        widget=forms.CheckboxSelectMultiple(),
        label="Estado",
    )
    provider_entity = django_filters.ModelChoiceFilter(
        queryset=ProviderEntity.on_site.all().distinct(),
    )

    created_date = django_filters.DateFilter(
        field_name='created_date',
        widget=forms.DateInput(
            attrs={'type': 'date'}),
        lookup_expr='contains',
        label='Fecha')
    created_date__gt = django_filters.NumberFilter(
        field_name='created_date', lookup_expr='year__gte', label='', widget=NumberInput(attrs={'placeholder': 'Desde', 'min': '0'}))
    created_date__lt = django_filters.NumberFilter(
        field_name='created_date', lookup_expr='year__lte', label='', widget=NumberInput(attrs={'placeholder': 'Hasta', 'min': '1'}))

    class Meta:
        model = Demands
        fields = ['title', 'category', 'provider_entity', 'created_date',
                  'created_date__gt', 'created_date__lt','type']
